
import pprint
import math
import time
import cv2
import numpy as np
from collections import defaultdict
import os
import datetime
import re
from collections import deque
import statistics
from statistics import StatisticsError
import speaker
import status as s
import ika_icon

    
playerData = [None]*8

is_ready_queue = deque([], 100)
is_map_queue =   deque([], 5)
is_opened_map = False
ready_start = 0

for i in range(is_ready_queue.maxlen):
    is_ready_queue.append(False)
for i in range(is_map_queue.maxlen):
    is_map_queue.append(False)

is_playing_queue =   deque([], 4)
for i in range(is_playing_queue.maxlen):
    is_playing_queue.append(False)
    
template_ready = cv2.imread(r"./assets/ready_mask_x.bmp", cv2.IMREAD_GRAYSCALE)
template_point = cv2.imread(r"./assets/icons_asset/gia/point.bmp")
template_map_batu = cv2.imread(r"./assets/icons_asset/gia/map_batu.bmp")
template_left_button =  cv2.imread(r"./assets/icons_asset/gia/map_left_button.bmp")
template_right_button = cv2.imread(r"./assets/icons_asset/gia/map_right_button.bmp")
template_ikanin = cv2.imread(r"./assets/icons_asset/gia/ikanin.bmp")
template_taibutu = cv2.imread(r"./assets/icons_asset/gia/taibutu.bmp")
template_sutejan = cv2.imread(r"./assets/icons_asset/gia/sutejan.bmp")


death_count_img  = cv2.imread(r"./assets/icons_asset/gia/death_count.bmp")
death_count_mask = cv2.bitwise_not( cv2.inRange(death_count_img, (255,255,255), (255,255,255)) )

template_death = [
    cv2.imread(r"./assets/death_x1.bmp", cv2.IMREAD_GRAYSCALE),
    cv2.imread(r"./assets/death_x2.bmp", cv2.IMREAD_GRAYSCALE),
]

mask_point = cv2.bitwise_not( cv2.inRange(template_point, (0,0,255), (0,0,255)) )
mask_map_batu = cv2.bitwise_not( cv2.inRange(template_map_batu, (0,0,255), (0,0,255)) )
mask_left_button = cv2.bitwise_not( cv2.inRange(template_left_button, (0,0,255), (0,0,255)) )
mask_right_button = cv2.bitwise_not( cv2.inRange(template_right_button, (0,0,255), (0,0,255)) )
mask_ikanin = cv2.bitwise_not( cv2.inRange(template_ikanin, (0,0,255), (0,0,255)) )
mask_taibutu = cv2.bitwise_not( cv2.inRange(template_taibutu, (0,0,255), (0,0,255)) )
mask_sutejan = cv2.bitwise_not( cv2.inRange(template_sutejan, (0,0,255), (0,0,255)) )

path = r"./assets/icons_asset/nuki"

files = os.listdir(path)
files = [f for f in files if os.path.isfile(os.path.join(path, f))]

icons_dict = defaultdict(list)
template_wapons = defaultdict(dict)

for fn in files:
    head = re.split('[ \(.]', fn)[0]
    icons_dict[head].append(fn)
    _im = cv2.imread(path+"/"+fn)
    
    # 周囲1pxをカット
    _im = _im[2:-2, 2:-2]
    
    template_wapons[head]["img"] = _im
    template_wapons[head]["mask"] = cv2.bitwise_not(
        cv2.inRange(template_wapons[head]["img"], (255,255,255), (255,255,255))
    )

if __name__ == '__main__':
    pass

def 濃いグレーのバツアイコン取得(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = (
        0,
        0 * 2.55,
        35 * 2.55,
    )
    upper = (
        255,
        20 * 2.55,
        42 * 2.55,
    )
    mask = cv2.inRange(hsv, np.clip(lower, 0, 255), np.clip(upper, 0, 255))
    kernel = np.array([
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,1,1,1,0,0],
        [1,1,1,1,1,1,1],
        [0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
    ], np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    filterdContours = []
    for contour in contours:
        _x, _y, _w, _h = cv2.boundingRect(contour)
        
        if 55 <= _w  and _y == 0 and _y+_h == img.shape[0]: #threshold
            filterdContours.append(contour)
    
    # マスクからノイズ輪郭を消す
    mask = np.zeros_like(mask)
    cv2.drawContours(mask, filterdContours, -1, color=(255, 255, 255), thickness=-1)
    
    return mask

def 黒かグレーのバツアイコン取得(img, drawedImg=None):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = (
        0,
        0 * 2.55,
        66 * 2.55,
    )
    upper = (
        255,
        28 * 2.55,
        79 * 2.55,
    )
    mask = cv2.inRange(hsv, np.clip(lower, 0, 255), np.clip(upper, 0, 255))
    
    # 真っ黒
    mask2 = cv2.inRange(img, (0,0,0), (5,5,5))
    mask3 = cv2.inRange(hsv, 
        (0,   214, 0),
        (255, 255, 80)
    )
    
    mask = cv2.bitwise_or(mask, mask2)
    mask = cv2.bitwise_or(mask, mask3)
    
    kernel = np.array([
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
        [0,0,1,1,1,0,0],
        [1,1,1,1,1,1,1],
        [0,0,1,1,1,0,0],
        [0,0,0,1,0,0,0],
        [0,0,0,1,0,0,0],
    ], np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("death morphologyEx", mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    filterdContours = []
    matching_target = np.zeros_like(mask)
    for contour in contours:
        _x, _y, _w, _h = cv2.boundingRect(contour)
        # テンプレマッチベース
        if _y == 0 and _y+_h == img.shape[0]:
            matching_target.fill(0)
            cv2.drawContours(matching_target, [contour], -1, color=(255, 255, 255), thickness=-1)
            
            for j, temp in enumerate(template_death):
                res = cv2.matchTemplate(matching_target, temp, cv2.TM_CCORR_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val >= 0.9: #threshold
                    filterdContours.append(contour)
                    break
    mask.fill(0)
    cv2.drawContours(mask, filterdContours, -1, color=(255, 255, 255), thickness=-1)
    
    return mask


def 非アイコン領域取得(_img):
    img = _img[75:101, 517:1406]
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask_list = [
        cv2.inRange(hsv, 
        (
            0,
            0,
            138,
        ), (
            255,
            21,
            157,
        )),
        cv2.inRange(hsv, 
        (
            0,
            33,
            4,
        ), (
            255,
            255,
            59,
        )),
        濃いグレーのバツアイコン取得(img),
        黒かグレーのバツアイコン取得(_img[75:101, 517-30:1406+30])[:, 30:-30]
    ]
    
    # モルフォロジー変換でノイズ除去
    kernel = np.ones((2,2),np.uint8)
    mask_list[0] = cv2.morphologyEx(mask_list[0], cv2.MORPH_OPEN, kernel)
    kernel = np.ones((3,1),np.uint8)
    mask_list[0] = cv2.dilate(mask_list[0], kernel, iterations=1)
    
    ## マスク重ねる
    newMask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for ma in mask_list:
        newMask = cv2.bitwise_or(newMask, ma)

    contours, _ = cv2.findContours(newMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    filterdContours = []
    for contour in contours:
        _x, _y, _w, _h = cv2.boundingRect(contour)
        if _w >= 55-3 and _y == 0 and _y+_h == img.shape[0]:
            filterdContours.append(contour)
    
    # マスクからノイズ輪郭を消す
    newMask = np.zeros_like(newMask)
    cv2.drawContours(newMask, filterdContours, -1, color=(255, 255, 255), thickness=-1)
    return newMask

def バーの領域取得(frame):
    img = frame[75:101, 517:1406].copy()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #  黄色が色移りしたバーの色領域のマスク取得 ※キャプボによって色の出方は変わると思うのでHSV値は適宜変更してください
    mask = cv2.inRange(hsv,
        (22, 119, 51),
        (43, 243, 99)
    )
    # 青色が色移りしたバーの色領域のマスク取得 ※キャプボによって色の出方は変わると思うのでHSV値は適宜変更してください
    mask2 = cv2.inRange(hsv, 
        (119, 121,  53),
        (130, 194, 93)
    )
    
    # マスク足し合わせ、モルフォロジーオープニングでノイズ除去
    mask = cv2.bitwise_or(mask, mask2)
    kernel = np.ones((3,2),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 連結成分分析でバー領域のみを抽出する。
    _, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    mask.fill(0)
    for i, stat in enumerate(stats[1:], 1):
        _bottom = stat[cv2.CC_STAT_TOP] + stat[cv2.CC_STAT_HEIGHT]
        
        if stat[cv2.CC_STAT_LEFT] < 847 :
            # 凹みの無いバーの領域の時
            if (
              5 <= stat[cv2.CC_STAT_WIDTH] <= 29+2 and 
              stat[cv2.CC_STAT_AREA] >= 4*4 and 
              stat[cv2.CC_STAT_TOP] <= 15 and
              np.count_nonzero((labels[-1:] == i) == True) >= 5
            ):
                mask[labels==i] = 255
        else:
            # 右端のバーに凹みがある領域の時
            if (
              5 <= stat[cv2.CC_STAT_WIDTH] <= 29+2 and 
              stat[cv2.CC_STAT_AREA] >= 3*3 and
              stat[cv2.CC_STAT_TOP] <= 15 and
              _bottom >= 26 - 6
            ):
                mask[labels==i] = 255
    
    # バーの中心部分（残り時間の周辺）をfloodFillの塗りつぶしによってマスクを取得する
    fill_mask = np.zeros((img.shape[0] + 2, img.shape[1] + 2), dtype=np.uint8)
    _, _, _, _ = cv2.floodFill(
        img,
        mask=fill_mask,
        seedPoint=(433, 25), # バーの中心座標を塗りつぶしの起点とする。残り時間のちょっと下のあたり
        newVal=(0, 0, 255),
        loDiff=(7,7,7),
        upDiff=(7,7,7),
        flags = 4 | 255 << 8,
    )
    
    # 周囲1pxカット
    fill_mask = fill_mask[1:-1,1:-1]
    
    # フィルタリングしたマスクと塗りつぶしたマスクを足し合わせる
    mask = cv2.bitwise_or(mask, fill_mask)
    
    # cv2.imshow("bar filtered", mask)
    return mask


def アイコン情報からrectを算出(icon_between_mask, icon_data):
    # icon_dataは参照渡し
    _ws = []
    for ic in icon_data:
        if ic['is_death']: continue
        
        # 左端アイコンがバーをはみ出していた時の補正処理
        if ic['l'] == 0:
            # x = ic['l']
            # ic['l'] = -0.35*x + 275.78
            
            ic['l'] = ic['r'] - 69 #todo 定数で対応
        # 右端アイコンがバーをはみ出していた時の補正処理
        if ic['r'] == icon_between_mask.shape[0] - 1:
            # x = ic['l']
            # ic['r'] = 0.35*x + -410.6
            ic['r'] = ic['l'] + 69 #todo 定数で対応
            
        _w = ic['r'] - ic['l']
        _ws.append(_w)
    
    # オールデスの時、top,bottomは定数で返す
    if len(_ws) == 0: return [0, 88]
    
    x = statistics.mode(_ws)
    if x >= 62:
        t =  -x + 87
        b =  0.5*x+82
    else:
        t = -0.25 * x + 40.5
        b = 0.66*x + 71.66
    
    return int(t), int(b)
    
def マスクからアイコンの位置を分析(icon_between_mask, frame, team, frame2):
    
    if team == s.TEAM.ALLY:
        icon_between_mask = icon_between_mask[:,:893-517].copy()
        img = frame[71:89, 517-30:893+30].copy()
        
    elif team == s.TEAM.ENEMY:
        icon_between_mask = icon_between_mask[:,1020-517:].copy()
        img = frame[71:89, 1020-30:1406+30].copy()
    
    
    icon_between_box = np.zeros((icon_between_mask.shape[0], icon_between_mask.shape[1], 3), dtype=np.uint8)

    _, _, stats, _ = cv2.connectedComponentsWithStats(icon_between_mask)
    for i, stat in enumerate(stats[1:], 1):
        cv2.rectangle(icon_between_box, (stat[0], 0), (stat[0]+stat[2], icon_between_box.shape[0]), (255, 255, 255), -1)
    
    # cv2.imshow(str(team)+"icon_between_box", icon_between_box)
    # cv2.imshow(str(team)+"icon_box", cv2.bitwise_not(icon_between_box) )
    
    icon_data = []
    batu_x_pos, _ = デスアイコン領域取得ConvexHull(img, int(team)*1000 )
    
    for pos in batu_x_pos:
        icon_data += [{
            'is_death': True, 
            'l': pos - 30, 
            'r': pos + 30
        }]
    
    _, _, stats, _ = cv2.connectedComponentsWithStats(cv2.bitwise_not(icon_between_mask))
    for i, stat in enumerate(stats[1:], 1):
        #todo 55px以上69以下とかに絞って良いかも
        icon_data += [{
            'is_death': False, 
            'l': stat[0], 
            'r': stat[0]+stat[2]
        }]
        
    if len(icon_data) < 4: return # ICONクラスのフレーム更新をしない

    order = True if team == s.TEAM.ALLY else False
    icon_data.sort(key=lambda x: x['l'], reverse=order)
    
    t,b = アイコン情報からrectを算出(icon_between_mask, icon_data)
    
    # デスのときアイコンに表示する真っ黒な画像作成
    dummy_img = np.zeros((b-t, 69, 3), dtype=np.uint8)
    
    imgs = []
    for i in range(4):
        ic = icon_data[i]
        _idx = 3-i if team == s.TEAM.ALLY else i+4
        _offset_x = (
            517 
            if team == s.TEAM.ALLY else 
            1020
        )
        
        if ic['is_death'] == False:
            im = frame[ t:b, ic['l']+_offset_x:ic['r']+_offset_x ].copy()
            col = (0,0,255)
        else:
            im = dummy_img.copy()
            col = (0,255,0)
        
        imgs.append(im)
        playerData[_idx].フレーム更新(im, ic['is_death'])
        
        # アイコンに矩形枠線と武器名、状態等　表示
        cv2.rectangle(frame2, (ic['l']+_offset_x, t), (ic['r']+_offset_x, b), col, 1)
        stat = playerData[_idx].status_queue[0]
        if s.Status.NONE == stat:
            state_str = "NONE"
        elif s.Status.ALIVE == stat:
            state_str = "ALIVE"
        elif s.Status.DEATH == stat:
            state_str = "DEATH"
        elif s.Status.SP == stat:
            state_str = "SP"
        elif s.Status.HAS_HOKO == stat:
            state_str = "HOKO"
            
        cv2.putText(frame2,
            text=playerData[_idx].wapon.filename,
            org=(ic['l']+_offset_x, b+22),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=col,
            thickness=2,
            lineType=cv2.LINE_4)
        cv2.putText(frame2,
            text=state_str,
            org=(ic['l']+_offset_x, b+22*2),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=col,
            thickness=2,
            lineType=cv2.LINE_4)
        cv2.putText(frame2,
            text="de: "+ str(playerData[_idx].deathCount) ,
            org=(ic['l']+_offset_x, b+22*3),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=col,
            thickness=2,
            lineType=cv2.LINE_4)
        cv2.putText(frame2,
            text="sp: "+ str(playerData[_idx].spCount) ,
            org=(ic['l']+_offset_x, b+22*4),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=col,
            thickness=2,
            lineType=cv2.LINE_4)
        
    # プレイヤーアイコンを並べて画像表示(imgs, team)
      
def プレイヤーアイコンを並べて画像表示(imgs, team):
    if team == s.TEAM.ALLY:
        tmp_imgs = []
        for im in imgs: tmp_imgs.insert(0, im)
        imgs = tmp_imgs
    
    hcon = cv2.hconcat(imgs)
    x_pos = 0
    for i, im in enumerate(imgs):
        _idx = i if team == s.TEAM.ALLY else i+4
        stat = playerData[_idx].status_queue[0]
        if s.Status.NONE == stat:
            state_str = "NONE"
        elif s.Status.ALIVE == stat:
            state_str = "ALIVE"
        elif s.Status.DEATH == stat:
            state_str = "DEATH"
        elif s.Status.SP == stat:
            state_str = "SP"
        elif s.Status.HAS_HOKO == stat:
            state_str = "HOKO"
            
        cv2.putText(hcon,
            text=state_str,
            org=(x_pos, im.shape[0] - 5),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 0, 255),
            thickness=2,
            lineType=cv2.LINE_4)
            
        cv2.putText(hcon,
            text=str(playerData[_idx].deathCount),
            org=(x_pos, 20),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(0, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)
            
        cv2.putText(hcon,
            text=str(playerData[_idx].spCount),
            org=(x_pos, 40),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(255, 255, 0),
            thickness=2,
            lineType=cv2.LINE_4)
            
        x_pos += im.shape[1]
        
    cv2.imshow(
        str(team)+"_hconcat", 
        cv2.resize(hcon, None, fx=2, fy=2, interpolation=cv2.INTER_NEAREST)
    )
    cv2.imshow(
        str(team)+"_big",
        cv2.resize(hcon, None, fx=3.5, fy=3.5, interpolation=cv2.INTER_NEAREST)
    )
    return 
    
def アイコンの位置検出と取得(frame, frame2):
    bar_mask = バーの領域取得(frame)
    death_mask = 非アイコン領域取得(frame)
    
    icon_between_mask = cv2.bitwise_or(bar_mask, death_mask)
    
    # 残り時間の周辺塗りつぶす
    cv2.rectangle(icon_between_mask, (395-40, 0), (520+12, icon_between_mask.shape[0]), (255, 255, 255), -1)
    
    # クロージングでマスク間の隙間埋める。拡張幅はアイコン細足幅 55~69pxくらいが本来適切？
    kernel = np.ones((1,30),np.uint8)
    icon_between_mask = cv2.morphologyEx(icon_between_mask, cv2.MORPH_CLOSE, kernel)
    
    # 隙間埋めた後、矩形をマスクをし反転する
    new_mask = np.zeros_like(icon_between_mask)
    contours, _ = cv2.findContours(icon_between_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i, contour in enumerate(contours):
        _x, _y, _w, _h = cv2.boundingRect(contour)
        cv2.rectangle(new_mask, (_x, 0), (_x+_w, new_mask.shape[0]), (255, 255, 255), -1)
    not_mask = new_mask.copy()
    
    # 矩形マスクから、味方・敵それぞれアイコンの位置算出・SP等の状態検出を行う
    マスクからアイコンの位置を分析(not_mask, frame, s.TEAM.ALLY, frame2)
    マスクからアイコンの位置を分析(not_mask, frame, s.TEAM.ENEMY, frame2)
    
    return

def ゲーム開始画面がチェックしイカアイコンを保存(frame, path):
    isStart = バトル開始画面の状態検出(frame)
    is_ready_queue.appendleft(isStart)
    
    if (is_ready_queue[1] == False and 
        is_ready_queue[0] == True):
        fn =  datetime.datetime.now().strftime('%Y%m%d_%H%M')# 保存するファイル名は時刻ベースの乱数
        print(fn)
        
        ally_imgs, enemy_imgs = バトル開始画面からブキアイコンを切り出す(frame)
        
        for i, im in enumerate(ally_imgs):
            cv2.imwrite(path+fn+str(i)+".bmp", im)
        for i, im in enumerate(enemy_imgs):
            cv2.imwrite(path+fn+str(i+4)+".bmp", im)
        
    
def バトル開始画面からブキアイコンを切り出す(frame):
    ally_imgs =  [0]*4
    enemy_imgs = [0]*4
    
    ally_imgs[0] = frame[24:109, 524:524 +88]
    ally_imgs[1] = frame[24:109, 613:613 +88]
    ally_imgs[2] = frame[24:109, 702:702 +88]
    ally_imgs[3] = frame[24:109, 791:791 +88]
    
    enemy_imgs[0] = frame[24:109, 1042: 1042+88]
    enemy_imgs[1] = frame[24:109, 1130: 1130+88]
    enemy_imgs[2] = frame[24:109, 1219: 1219+88]
    enemy_imgs[3] = frame[24:109, 1307: 1307+88]
    
    return ally_imgs, enemy_imgs
    
def アイコン位置認識可能状態かどうか(frame):
    global ready_start
    
    if ready_start != 0 and 2500 < (int(time.time() * 1000) - ready_start):
        # isPlaing = イカアイコンが存在するか検出(frame)
        
        # 4F中1こでもtrueならOK
        # is_playing_queue.appendleft( イカアイコンが存在するか検出(frame) )
        is_playing_queue.appendleft( イカアイコンが存在するか検出＿右上サブウエポンアイコンベース(frame) )
        
        isPlaing = any( is_playing_queue )
        return isPlaing
    return False
    
def ゲーム開始画面かチェックしブキを分類(frame):
    isStart = バトル開始画面の状態検出(frame)
    is_ready_queue.appendleft(isStart)
    
    global ready_start
    if (is_ready_queue[1] == False and 
        is_ready_queue[0] == True):
        
        ready_start = int(time.time() * 1000)
        print("バトル開始！")
        
        global is_opened_map
        is_opened_map = False
        
        ally_imgs, enemy_imgs = バトル開始画面からブキアイコンを切り出す(frame)

        for i, _img in enumerate(ally_imgs):
            playerData[i] = ika_icon.ICON(_img, i, s.TEAM.ALLY)
            
            
        for i, _img in enumerate(enemy_imgs):
            playerData[i+4] = ika_icon.ICON(_img, i+4, s.TEAM.ENEMY)
            
        imgs = []
        for ic in playerData:
            imgs.append(ic.wapon.temp_img)
            
        
        #debug
        # cv2.imshow("Buki", cv2.hconcat(imgs))
    
def バトル開始画面の状態検出(frame):
    img = frame[471:633, 721:1192]

    # 白ピクセル抽出、一定の面積あればテンプレマッチング
    mask = cv2.inRange(img, 
    (
        249-1,
        252-1,
        250-1,
    ), (
        249+1,
        252+1,
        250+1,
    ))
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 一定以上の面積があればテンプレマッチングを行う
    if 15000 > np.count_nonzero(mask == 255):
        return False
        
    # テンプレートマッチング実行
    res = cv2.matchTemplate(mask, template_ready, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    if max_val >= 0.8:
        return True
    else :
        return False
    
def マップ画面の状態検出(frame):
    img = frame[0:225, 0:179]
    
    # マップ画面の左上のバツボタンのテンプレートマッチング
    res = cv2.matchTemplate(img, template_map_batu, cv2.TM_CCORR_NORMED, mask=mask_map_batu)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    
    if max_val < 0.95:
        return False
    
    img2 = frame[495:581, 34:116]   # マップに表示される十字左ボタン
    img3 = frame[495:581, 1386:1468]# マップに表示される十字左ボタン
    
    res = cv2.matchTemplate(img2, template_left_button, cv2.TM_CCORR_NORMED, mask=mask_left_button)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    if max_val < 0.95:
        return False
    
    res = cv2.matchTemplate(img3, template_right_button, cv2.TM_CCORR_NORMED, mask=mask_right_button)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    if max_val < 0.95:
        return False
        
    return True

def イカアイコンが存在するか検出(frame):
    # 塗りポイントの領域
    img = frame[60:123, 1503:1675]
    # フォントの白ピクセル抽出
    mask = cv2.inRange(img, 
    (
        249-1,
        252-1,
        250-1,
    ), (
        249+1,
        252+1,
        250+1,
    ))
    kernel = np.ones((4, 3),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 塗りpのフォントを、矩形領域をしきい値として判別
    _, _, stats, _ = cv2.connectedComponentsWithStats(mask)

    x_pos = []
    for i, stat in enumerate(stats[1:], 1):
        if i == 0: continue
        x_pos.append(stat[cv2.CC_STAT_LEFT])
        x_pos.append(stat[cv2.CC_STAT_LEFT] + stat[cv2.CC_STAT_WIDTH])
    
    if not len(x_pos) > 0:
        return False
        
    width = max(x_pos) - min(x_pos)
    
    if width < 134:
        return False
        
    # 右上の「P」画像テンプレートマッチング
    img2 = frame[84:123, 1654:1675]
    res = cv2.matchTemplate(img2, template_point, cv2.TM_CCORR_NORMED, mask=mask_point)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    
    if not max_val > 0.99:
        return False
    return True

def イカアイコンが存在するか検出＿右上サブウエポンアイコンベース(frame):
    img = frame[28-12:87+12, 1682-12:1741+12]
    
    # 右上のサブウエポンの黄色丸アイコン探す　存在する時
    mask = cv2.inRange(img, 
    (
        51-10,
        252-10,
        231-10,
    ), (
        51+10,
        252+10,
        231+10,
    ))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10, 10) )
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    filterdContours = []
    for contour in contours:
        filterdContours.append(contour)
    cv2.drawContours(mask, contours, -1, color=(255, 255, 255), thickness=-1)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    for contour in contours:
        _x, _y, _w, _h = cv2.boundingRect(contour)
        if 50 <= _w <= 60 and 50 <= _h <= 60:
            return True

    return False

def マップ開いてるかチェックしギア読み上げ(frame):
    isMap = マップ画面の状態検出(frame)
    global is_opened_map
    if isMap and is_opened_map==False:
    # if isMap:
        is_opened_map = True
        マップからギアとサブスペ取得(frame)
    
    
def マップからギアとサブスペ取得(frame):
    sab_icon = []
    sp_img = []
    gias = []

    gias.append(    frame[58:107, 1706:1851])
    sab_icon.append(frame[63:102, 1604:1642])
    sp_img.append(  frame[63:102, 1646:1684])
    gias.append(    frame[124:173, 1706:1851])
    sab_icon.append(frame[129:168, 1604:1642])
    sp_img.append(  frame[129:168, 1646:1684])
    gias.append(    frame[188:237, 1706:1851])
    sab_icon.append(frame[193:232, 1604:1642])
    sp_img.append(  frame[193:232, 1646:1684])
    gias.append(    frame[254:303, 1706:1851])
    sab_icon.append(frame[259:298, 1604:1642])
    sp_img.append(  frame[259:298, 1646:1684])
    
    gia_data = defaultdict(list)
    
    for i, gia in enumerate(gias):
        # イカ忍者アイコン　テンプレートマッチング実行
        res = cv2.matchTemplate(gia, template_ikanin, cv2.TM_CCORR_NORMED, mask=mask_ikanin)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > 0.94:
            gia_data["ikanin"].append(playerData[i+4].wapon.filename)
        
        # ステジャンアイコン　テンプレートマッチング実行
        res = cv2.matchTemplate(gia, template_sutejan, cv2.TM_CCORR_NORMED, mask=mask_sutejan)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > 0.96:
            gia_data["sutejan"].append(playerData[i+4].wapon.filename)
            
        # 対物アイコン　テンプレートマッチング実行
        res = cv2.matchTemplate(gia, template_taibutu, cv2.TM_CCORR_NORMED, mask=mask_taibutu)
        _, max_val, _, _ = cv2.minMaxLoc(res)
        if max_val > 0.96:
            gia_data["taibutu"].append(playerData[i+4].wapon.filename)
    
    spe = speaker.Speaker()
    spe.マップ情報読み(gia_data)
    return 

def プレイヤー状況を画面に表示する():
    gui = np.zeros((1180, 2560, 3), dtype=np.uint8)
    gui += 255
    
    width  = 1280
    height = 295
    
    idx = 0
    for i in range(4):
        player = playerData[i]
        if player is None: return -1
        
        im = player_state(
            icon_img=player.wapon.temp_img,
            width=  width,
            height= height,
            is_death=player.is_death, 
            is_sp=False, # debug 
            alive_start=player.alive_start, 
            death_start=player.death_start, 
            death_count=player.deathCount, 
            max_sec=60
        )
        
        gui[idx:idx+height,:width] = im
        idx += height
        
    idx = 0
    
    for i in range(4):
        player = playerData[i+4]
        if player is None: return -1
        
        im = player_state(
            icon_img=player.wapon.temp_img,
            width=  width,
            height= height,
            is_death=player.is_death, 
            is_sp=False, # debug 
            alive_start=player.alive_start, 
            death_start=player.death_start, 
            death_count=player.deathCount, 
            max_sec=60
        )
        gui[idx:idx+height,width:] = im
        idx += height
        
    # 中央の縦線アイコン仕切り
    cv2.line(gui, (1280, 0), (1280, gui.shape[0]), (0, 0, 0), thickness=8)
    cv2.imshow("gui", gui)

# 1つのアイコンのUI画像を生成
def player_state(icon_img, width, height, is_death, is_sp, alive_start, death_start, death_count, max_sec):
    # guiの横幅の中で何pxをゲージの幅にするか
    gauge_width = 1280-290
    
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    if is_sp and is_death == False:
        img[:,:] = (172,234,255)
    else:
        img[:,:] = (255,255,255)
    
    img_w = width - gauge_width
    re_img = cv2.resize(icon_img, (img_w, img_w), interpolation=cv2.INTER_NEAREST)
    
    img[:, 0:img_w] = (255,255,255)
    img[0:img_w, 0:img_w] = re_img
    
    rate = gauge_width / (max_sec * 1000)
    
    gauge_color = (23, 115, 255)
    if is_death:
        gauge_color = (46, 82, 137)
        death_ms_time = int(time.time() * 1000) - death_start
        # デス状態の時、生存時間のゲージを止めるため。。。
        alive_ms_time = death_start - alive_start
        
    else:
        alive_ms_time = int(time.time() * 1000) - alive_start
    
    #最大60秒とする 60fps
    gauge =  int(alive_ms_time * rate)
    gauge_index = width - gauge_width

    
    cv2.rectangle(img,  
        (gauge_index, 0), 
        (gauge_index+gauge, height),
        gauge_color, -1
    )
    
    if is_death:
        gauge = int(death_ms_time * rate)
        gauge_index = width - gauge_width
        cv2.rectangle(img, 
            (gauge_index, 0), 
            (gauge_index+gauge, height),
            (127, 127, 127), -1
        )
        
        # リスポン復帰 8.5秒
        cv2.line(img, (img.shape[1]-gauge_width + int(8500 * rate), 0), (img.shape[1]-gauge_width + int(8500 * rate), img.shape[0]), (0, 0, 255), thickness=2)
        # # スパジャン復帰 7.5 + 3.633
        # cv2.line(img, (img.shape[1]-gauge_width + int((7500+3633) * rate), 0), (img.shape[1]-gauge_width + int((7500+3633) * rate), img.shape[0]), (0, 0, 255), thickness=2)
    
    cv2.putText(img,
        text=str(death_count),
        org=(gauge_index+130, 250),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=4.0,
        color=(0, 0, 0),
        thickness=7,
        lineType=cv2.LINE_4)
    

    # bottomボーダー
    cv2.line(img, (0, img.shape[0]), (img.shape[1], img.shape[0]), (0, 0, 0), thickness=15)
    # 縦線アイコン仕切り
    cv2.line(img, (img.shape[1]-gauge_width, 0), (img.shape[1]-gauge_width, img.shape[0]), (0, 0, 0), thickness=8)
    
    
    # デス数カウント画像を貼り付ける
    dx = 325
    dy = 0
    h, w = death_count_img.shape[:2]
    img[dy:dy+h, dx:dx+w][death_count_mask>0] = death_count_img[death_count_mask>0]
    
    return img
    
def 線分の情報(a, b):
    # ２点間の傾き、距離を返す
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    
    if dx != 0:
        slope = dy / dx
    else:
        slope = None
    distance = np.sqrt( dx**2 + dy**2 )
    return slope, distance

def バツアイコンの検出(img, *args):
    mask_list = []
    
    for arg in args:
        # inRange()のrgb,hsvの切り替えの条件分岐
        try:
            arg[2]
            _mask = cv2.inRange(img, arg[0], arg[1])
        except IndexError:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            _mask = cv2.inRange(hsv, arg[0], arg[1])
        
        kernel = np.array([
            [0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0],
            [0,0,1,1,1,0,0],
            [1,1,1,1,1,1,1],
            [0,0,1,1,1,0,0],
            [0,0,0,1,0,0,0],
            [0,0,0,1,0,0,0],
        ], np.uint8)
        _mask = cv2.morphologyEx(_mask, cv2.MORPH_OPEN, kernel)
        
        mask_list.append(_mask)
    
    newMask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for ma in mask_list:
        newMask = cv2.bitwise_or(newMask, ma)
    
    _, labels, stats, _ = cv2.connectedComponentsWithStats(newMask)

    batu_x_pos = []
    newMask.fill(0)
    for i, stat in enumerate(stats[1:], 1):
        top    = {'left':0, 'right':0, 'length':0}
        bottom = {'left':0, 'right':0, 'length':0}
        
        idxs =  np.where(labels[0] == i)[0].tolist()
        idxs2 = np.where(labels[newMask.shape[0]-1] == i)[0].tolist()
        
        if not idxs or not idxs2: continue
        
        top['left'] = min(idxs)
        top['right'] = max(idxs)
        top['length'] = top['right'] - top['left']
        
        bottom['left'] = min(idxs2)
        bottom['right'] = max(idxs2)
        bottom['length'] = bottom['right'] - bottom['left']
        
        # print("bottom", bottom)

        line_info = [
            線分の情報((top['left'],  0) ,(bottom['left'],  newMask.shape[0]-1)),
            線分の情報((top['right'], 0), (bottom['right'], newMask.shape[0]-1)),
        ]
        
        # 傾き無し（90度）の直線ならその時点で無視
        if line_info[0][0] is None or line_info[1][0] is None: continue
        
        # 斜線のとき
        if (-1.4 <= line_info[0][0] <= -0.7 and
            -1.4 <= line_info[1][0] <= -0.7 and 
            top['length']   >= 9 and
            bottom['length']>= 9
        ):
            newMask[labels==i] = 255
            # x軸の中心座標をリストに格納
            batu_x_pos.append(top['left'] + top['length'] // 2 )
        
        # バツマークのとき
        if (-1.4 <= line_info[0][0] <= -0.7 and
             0.7 <= line_info[1][0] <= 1.4 and
             top['length']   >= 9 and
             bottom['length']>= 9
        ):
            newMask[labels==i] = 255
            # x軸の中心座標をリストに格納
            batu_x_pos.append(top['left'] + top['length'] // 2 )
            
    return batu_x_pos, newMask

def 消灯アイコン検出(img, idx=0):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_list = [
        cv2.inRange(hsv, 
        (
            0,
            0,
            138,
        ), (
            255,
            21,
            157,
        )),
        cv2.inRange(hsv, 
        (
            0,
            33,
            4,
        ), (
            255,
            255,
            59,
        ))
    ]
    
    kernel = np.ones((3,3),np.uint8) #threshold
    mask_list[0] = cv2.dilate(mask_list[0], kernel, iterations=1)
    
    ## マスク足し合わせ
    newMask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for ma in mask_list:
        newMask = cv2.bitwise_or(newMask, ma)
        
    _, labels, stats, _ = cv2.connectedComponentsWithStats(newMask)

    death_x_pos = []
    newMask.fill(0)
    
    for i, stat in enumerate(stats[1:], 1):
        idxs =  np.where(labels[img.shape[0]-1] == i)[0].tolist()
        if not idxs: continue
        
        bottom_left = min(idxs)
        bottom_right = max(idxs)
        bottom_sum = np.count_nonzero( (labels[:,bottom_left:bottom_right] == i) == True)
        
        top_cnt = np.count_nonzero( (labels[0] == i) == True)
        
        if (45 <= top_cnt    <= 105 and
            50 <= bottom_right-bottom_left <= 90 and
            # top幅、bottom幅の矩形面積と、全体面積を比較する形。
            0.95 <= (bottom_right-bottom_left)*img.shape[0] / bottom_sum <= 1.15
        ):
            newMask[labels==i] = 255    
            xx = bottom_left + (bottom_right - bottom_left) // 2
            death_x_pos.append(xx)
    
    return death_x_pos, newMask

            


def デスアイコン領域取得ConvexHull(img, idx=1000):
    death_info = [
        消灯アイコン検出(img, idx),
        バツアイコンの検出(img, 
            ((
                0,
                0 * 2.55,
                66 * 2.55,
            ),(
                255,
                28 * 2.55,
                79 * 2.55,
            ))
        ),
        バツアイコンの検出(img,
            ((0,0,0), (7,7,7), "rgb"),
            ((0, 214, 0),(255, 255, 80)),
        ),
        バツアイコンの検出(img, 
            ((
                0,
                0 * 2.55,
                35 * 2.55,
            ), (
                255,
                20 * 2.55,
                42 * 2.55,
            ))
        )
    ]
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    death_icon_x_pos = []
    for item in death_info:
        # death_icon_x_pos += item[0] - 30 # bar_imgと切り取り座標異なるので調整
        death_icon_x_pos += item[0] # bar_imgと切り取り座標異なるので調整
        mask = cv2.bitwise_or(mask, item[1])
    
    # _, _, stats, _ = cv2.connectedComponentsWithStats(mask)
    # mask.fill(0)
    
    # for i, stat in enumerate(stats[1:], 1):
    #     cv2.rectangle(mask, (stat[cv2.CC_STAT_LEFT], 0), (stat[cv2.CC_STAT_LEFT]+stat[cv2.CC_STAT_WIDTH], img.shape[0]), (255, 255, 255), -1)
            
    # cv2.imshow("maskmask", mask)
    return death_icon_x_pos, mask

def 色移りなし(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, 
        (0  , 9,  17),
        (255, 128, 60)
    )
    kernel = np.ones((3,2),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 連結成分分析でバー領域のみを抽出する。
    _, labels, stats, _ = cv2.connectedComponentsWithStats(mask)
    mask.fill(0)
    mask2 = np.zeros_like(mask)
    for i, stat in enumerate(stats[1:], 1):
        _bottom = stat[cv2.CC_STAT_TOP] + stat[cv2.CC_STAT_HEIGHT]
        
        if stat[cv2.CC_STAT_LEFT] < 847 :
            # 凹みの無いバーの領域の時
            if (
            #   5 <= stat[cv2.CC_STAT_WIDTH] <= 29+2 and 
            #   stat[cv2.CC_STAT_AREA] >= 4*4 and 
              stat[cv2.CC_STAT_TOP] <= 1 and
              np.count_nonzero((labels[-4:] == i) == True) >= 5
            ):
                mask2[labels==i] = 255
                cv2.rectangle(mask, (stat[cv2.CC_STAT_LEFT], 0), (stat[cv2.CC_STAT_LEFT]+stat[cv2.CC_STAT_WIDTH], img.shape[0]), (255, 255, 255), -1)

        else:
            # 右端のバーに凹みがある領域の時
            if (
            #   5 <= stat[cv2.CC_STAT_WIDTH] <= 29+2 and 
            #   stat[cv2.CC_STAT_AREA] >= 3*3 and
              stat[cv2.CC_STAT_TOP] <= 1 and
              _bottom >= 26 - 6
            ):
                mask2[labels==i] = 255
                cv2.rectangle(mask, (stat[cv2.CC_STAT_LEFT], 0), (stat[cv2.CC_STAT_LEFT]+stat[cv2.CC_STAT_WIDTH], img.shape[0]), (255, 255, 255), -1)

    # cv2.imshow("gtay", mask2)
    return mask

    
    
    
    