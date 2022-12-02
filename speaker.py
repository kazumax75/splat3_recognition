import os
from pydub import AudioSegment
from pydub.playback import play
import threading
from pydub.silence import split_on_silence

class Speaker:
    def __init__(self) -> None:
        self.buki = self.loadToDict(r"./assets\hiroyuki\buki")
        
        # print(self.buki)
        
        self.yari = self.loadToDict(r"./assets\hiroyuki\yari")
        self.kakaeoti = self.loadToDict(r"./assets\hiroyuki\kakaeoti")
        self.yarareta = self.loadToDict(r"./assets\hiroyuki\yarareta")
        self.haita = self.loadToDict(r"./assets\hiroyuki\haita")
        self.kimasuyo = self.loadToDict(r"./assets\hiroyuki\kimasuyo")

        self.maisuu = {
            1: AudioSegment.from_wav(r"./assets\hiroyuki\\1mai.wav"),
            2: AudioSegment.from_wav(r"./assets\hiroyuki\\2mai.wav"),
            3: AudioSegment.from_wav(r"./assets\hiroyuki\\3mai.wav"),
            4: AudioSegment.from_wav(r"./assets\hiroyuki\\4mai.wav"),
        }
        
        self.aite_bomu    = AudioSegment.from_wav(r"./assets\hiroyuki\\aite_bomu.wav")
        self.kotti_bomu   = AudioSegment.from_wav(r"./assets\hiroyuki\\kotti_bom.wav")
        self.hokomoti = AudioSegment.from_wav(r"./assets\hiroyuki\\hokomoti.wav")
        self._2oti   = AudioSegment.from_wav(r"./assets\hiroyuki\\2oti.wav")
        self._3oti   = AudioSegment.from_wav(r"./assets\hiroyuki\\3oti.wav")
        self.ikanin  = AudioSegment.from_wav(r"./assets\hiroyuki\\ikanin.wav")
        self.sutejan = AudioSegment.from_wav(r"./assets\hiroyuki\\sutejan.wav")
        self.taibutu = AudioSegment.from_wav(r"./assets\hiroyuki\\taibutu.wav")
        
        self.gias = {
            "ikanin": AudioSegment.from_wav(r"./assets\hiroyuki\\ikanin.wav"),
            "sutejan": AudioSegment.from_wav(r"./assets\hiroyuki\\sutejan.wav"),
            "taibutu": AudioSegment.from_wav(r"./assets\hiroyuki\\taibutu.wav"),
        }
        
        return
    
    def loadToDict(self, path):
        files = os.listdir(path)
        files_file = [f for f in files if os.path.isfile(os.path.join(path, f))]
        dic = {}
        for filename in files_file:
            
            fn, exp = os.path.splitext(filename)

            _audio = AudioSegment.from_wav(
                os.path.join(path, filename)
            )
            dic[fn] = _audio
            
        return dic
    
    def play(self):
        
        return 
    def マップ情報読み(self, gia_data):
        _au = AudioSegment.silent(duration=0)
        
        for k, gia in gia_data.items():
            _au += self.gias[k]
            
            for wapon_file_name in gia:
                
                _au += self.buki[wapon_file_name]
                
        if _au.duration_seconds == 0: return
        _audio = AudioSegment.silent(duration=0)
        chunks = split_on_silence(_au, min_silence_len=300, silence_thresh=-35, keep_silence=120)
        for i, chunk in enumerate( chunks ):
            _audio += chunk
            
        threading.Thread(target=play, args=(_audio,)).start()
        
        return 
    
    def ボム枚数(self, enemy_bom_num, ally_bom_num):
        # 足し合わせ
        silent = AudioSegment.silent(duration=180)
        
        if 0 < enemy_bom_num <= 4:
            _enemy = self.aite_bomu + self.maisuu[enemy_bom_num]
        
        if 0 < ally_bom_num <= 4:
            _ally = self.kotti_bomu + self.maisuu[ally_bom_num]
        
        _au = _enemy + silent + _ally

        threading.Thread(target=play, args=(_au,)).start()
        
        return 
        
    def ブキやり(self, wapon_file_name):
        t = threading.Thread(target=play, args=(self.yari[wapon_file_name],))
        t.start()
        return
        
    def ブキ抱え落ち(self, wapon_file_name):
        t = threading.Thread(target=play, args=(self.kakaeoti[wapon_file_name],))
        t.start()
        
        return
    def ホコ持ち(self, wapon_file_name):
        t = threading.Thread(target=play, args=(self.hokomoti[wapon_file_name],))
        t.start()
        
        return
        
    def ブキやられ(self, wapon_file_name):
        t = threading.Thread(target=play, args=(self.yarareta[wapon_file_name],))
        t.start()
        
        return
    
    def SP来る(self, sp_file_name):
        t = threading.Thread(target=play, args=(self.kimasuyo[ sp_file_name ],))
        t.start()
        
        return 
    
    def SP吐いた(self, sp_file_name):
        t = threading.Thread(target=play, args=(self.haita[ sp_file_name ],))
        t.start()
        
        return 