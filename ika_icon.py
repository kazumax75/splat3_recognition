import time
import cv2
from collections import deque
import wapon as wa
import status as s
import speaker

# １つのアイコンの情報保持し、状態の変化の検知を行うクラス
class ICON:
    histSize = [50, 50]
    ranges = [0, 256] + [0, 256]
    channels = [1, 2]
    
    ally_death_num  = 0 # 現在味方の落ちてる数
    enemy_death_num = 0 # 現在敵の落ちてる数
    
    def __init__(self, img, index, team):
        self.index = index
        self.initImg = self.img = img # 分類結果にかかわらず一旦imgに入れる。
        
        self.team: s.TEAM = team
        self.deathCount = 0 # デス数
        self.spCount = 0    # SP使用数
        self.is_death = False # デスしてるかのフラグ
        self.alive_start = int(time.time() * 1000) # 初期化時・復帰時の時刻　unixtime(ミリ秒)
        self.death_start = 0 # デス開始時の時刻
        
        self.speaker = speaker.Speaker()
        
        # deque
        self.status_queue = deque([], 15) # 状態を保持する両端キュー
        for i in range(self.status_queue.maxlen):
            self.status_queue.append(s.Status.NONE) # 初期化
            
        # DEBUG
        self.compare_hist_queue = deque([], 30)
        for i in range(self.compare_hist_queue.maxlen):
            self.compare_hist_queue.append(999) # 初期化

        # 開始時アイコンのヒストグラム算出
        if img is None:
            self.wapon = None
            self.initHist = None
        else:
            self.wapon = wa.ブキアイコン画像から分類(self.initImg)
            hsv = cv2.cvtColor(self.initImg[:, 14:-12], cv2.COLOR_BGR2HSV)
            self.initHist = cv2.calcHist([hsv], ICON.channels, None, ICON.histSize, ICON.ranges)
                
    def 現フレームの状態検出(self, death_flag):
        # デス状態ならならstateデックに追加
        if death_flag:
            self.status_queue.appendleft(s.Status.DEATH)
            return 
        
        # デス状態でなく、ヒストグラムに差があるとき「SP貯まってる」or「ホコ持ちアイコン」
        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], ICON.channels, None, ICON.histSize, ICON.ranges)
        res = cv2.compareHist(self.initHist, hist, 0)
        
        self.compare_hist_queue.appendleft(res)
        
        self.current_hist = res
        if abs(res) <= 0.92:
            self.status_queue.appendleft(s.Status.SP)
            # todo
            # isHoko = ホコアイコンかどうか判定する(self.img)
            # if isHoko:
            #     # ホコアイコンならホコ持ち状態
            #     self.status_queue.appendleft(s.Status.HAS_HOKO)
            # else:
            #     # そうでなければSP状態
            #     self.status_queue.appendleft(s.Status.SP)
            
            return
        
        #どれでもなければ、通常アイコン
        self.status_queue.appendleft(s.Status.ALIVE)
    
    def 状態変化の検出ー通知(self):
        #debug 　ヒストグラム比較結果一覧
        # if (
        #     self.status_queue[14] == s.Status.SP
        # ):
            
        #     print("idx", self.index, "que:", list(self.compare_hist_queue) )
            
        #     pass
        
        # if self.index == 0:
        #     print("idx", self.index, "que:", list(self.compare_hist_queue) )
        
        
        # アイコンが 通常＞デス に変化した時の処理
        if (self.status_queue[3] == s.Status.ALIVE and
            self.status_queue[2] == s.Status.DEATH and 
            self.status_queue[1] == s.Status.DEATH and 
            self.status_queue[0] == s.Status.DEATH ):
            
            self.deathCount += 1;self.is_death = True; self.death_start = int(time.time() * 1000)
            
            if self.team == s.TEAM.ALLY:
                ICON.ally_death_num += 1
                self.speaker.ブキやられ(self.wapon.filename, ICON.ally_death_num)
            elif self.team == s.TEAM.ENEMY:
                self.speaker.ブキやり(self.wapon.filename)
                ICON.enemy_death_num += 1
        
        # アイコンが デス＞通常 に変化した時の処理
        elif (
            self.status_queue[3] == s.Status.DEATH and 
            self.status_queue[2] == s.Status.DEATH and 
            self.status_queue[1] == s.Status.DEATH and 
            self.status_queue[0] == s.Status.ALIVE ):
            
            self.is_death = False; self.alive_start = int(time.time() * 1000)
            
            if self.team == s.TEAM.ALLY:
                ICON.ally_death_num -= 1
            elif self.team == s.TEAM.ENEMY:
                ICON.enemy_death_num -= 1
        
        # アイコンが 通常＞SP に変化した時の処理
        elif (self.status_queue[2] == s.Status.ALIVE and 
              self.status_queue[1] == s.Status.ALIVE and 
              self.status_queue[0] == s.Status.SP ):
              
            if self.team == s.TEAM.ENEMY:
                self.speaker.SP来る(self.wapon.sp)
            
        # アイコンが SP＞通常 に変化した時の処理
        elif (self.status_queue[2] == s.Status.SP and 
              self.status_queue[1] == s.Status.SP and 
              self.status_queue[0] == s.Status.ALIVE ):
              
            self.spCount += 1
            
            if self.team == s.TEAM.ALLY:
                self.speaker.SP吐いた(self.wapon.sp)
            elif self.team == s.TEAM.ENEMY:
                pass
        
        # アイコンが SP＞デス に変化した時の処理
        elif (
            self.status_queue[3] == s.Status.SP and
            self.status_queue[2] == s.Status.DEATH and 
            self.status_queue[1] == s.Status.DEATH and 
            self.status_queue[0] == s.Status.DEATH ):
            
            self.deathCount += 1;self.is_death = True; self.death_start = int(time.time() * 1000)
            
            # SP抱え落ち
            if self.team == s.TEAM.ALLY:
                ICON.ally_death_num += 1
                self.speaker.ブキやられ(self.wapon.filename, ICON.ally_death_num)
            elif self.team == s.TEAM.ENEMY:
                self.speaker.ブキ抱え落ち(self.wapon.filename)
                ICON.enemy_death_num += 1
            
        return 
            
    def フレーム更新(self, img, death_flag):
        # 現フレームのアイコンをセット
        self.img = img
        self.現フレームの状態検出(death_flag)
        self.状態変化の検出ー通知()
