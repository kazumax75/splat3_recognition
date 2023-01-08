from collections import defaultdict
import os
import re
import cv2
from typing import Tuple
import dataclasses
@dataclasses.dataclass
class Wapon:
    filename: str
    name: str
    short_name: str
    sp: str
    temp_img = None
    
icons_dict = defaultdict(list)
template_wapons = defaultdict(dict)    
wapons = {}
arr = []

# 全武器のテンプレートファイル名や名前、SP名の定数定義
arr.append( Wapon("wakaba","わかばシューター","わかば","barrier"))
arr.append( Wapon("bo-rudo","ボールドマーカー","ボールド","ultrahanco"))
arr.append( Wapon("sya-pu","シャープマーカー","シャーカー","kanitank"))
arr.append( Wapon("susi","スプラシューター","スシ","ultrashot"))
arr.append( Wapon("hiro","ヒーローシューター レプリカ","ヒロシュ","ultrashot"))
arr.append( Wapon("prime","プライムシューター","プライム","kanitank"))
arr.append( Wapon("52g",".52ガロン","ゴーニー","megaphone"))
arr.append( Wapon("96g",".96ガロン","クロ","kyu-inki"))
arr.append( Wapon("jet","ジェットスイーパー","ジェット","kyu-inki"))
arr.append( Wapon("zap","N-ZAP85","黒ザップ","energystand"))
arr.append( Wapon("ginmode","プロモデラーMG","銀モデ","sameride"))
arr.append( Wapon("l3","L3リールガン","L3","kanitank"))
arr.append( Wapon("h3","H3リールガン","H3","energystand"))
arr.append( Wapon("hot","ホットブラスター","ホッブラ","barrier"))
arr.append( Wapon("long","ロングブラスター","ロンブラ","hopsonar"))
arr.append( Wapon("rapi","ラピッドブラスター","ラピ","tripletornado"))
arr.append( Wapon("rapieri","Rブラスターエリート","ラピエリ","kyu-inki"))
arr.append( Wapon("nova","ノヴァブラスター","ノヴァ","syokuwonder"))
arr.append( Wapon("clash","クラッシュブラスター","クラブラ","ultrashot"))
arr.append( Wapon("botol","ボトルガイザー","ボトル","ultrashot"))
arr.append( Wapon("ro-ra-","スプラローラー","ローラー","barrier"))
arr.append( Wapon("ka-bon","カーボンローラー","カーボン","syokuwonder"))
arr.append( Wapon("valia","ヴァリアブルローラー","ヴァリアブル","multimissile"))
arr.append( Wapon("dainamo","ダイナモローラー","ダイナモ","energystand"))
arr.append( Wapon("paburo","パブロ","パブロ","megaphone"))
arr.append( Wapon("hokusai","ホクサイ","ホクサイ","syokuwonder"))
arr.append( Wapon("tya-","スプラチャージャー","チャー","kyu-inki"))
arr.append( Wapon("4k","リッター4K","リッター","hopsonar"))
arr.append( Wapon("sukuiku","スクイックリンα、β、γ","スクイク","barrier"))
arr.append( Wapon("take","14式竹筒銃・甲","竹","megaphone"))
arr.append( Wapon("soi","ソイチューバー","ソイチュ","multimissile"))
arr.append( Wapon("manyu","スプラマニューバー","マニュ","kanitank"))
arr.append( Wapon("kerubin","ケルビン525","ケルビン","nicedama"))
arr.append( Wapon("dual","デュアルスイーパー","デュアル","hopsonar"))
arr.append( Wapon("supa","スパッタリー","赤スパ","energystand"))
arr.append( Wapon("quad","クアッドホッパーブラック","クアッド","sameride"))
arr.append( Wapon("bake","バケットスロッシャー","バケツ","tripletornado"))
arr.append( Wapon("hissen","ヒッセン","ヒッセン","jetpack"))
arr.append( Wapon("sukusuro","スクリュースロッシャー","スクスロ","nicedama"))
arr.append( Wapon("exp","エクスプロッシャー","エクス","amehurashi"))
arr.append( Wapon("furo","オーバーフロッシャー","お風呂","amehurashi"))
arr.append( Wapon("bareru","バレルスピナー","バレル","hopsonar"))
arr.append( Wapon("supusupi","スプラスピナー","スプスピ","ultrahanco"))
arr.append( Wapon("haidora","ハイドラント","ハイドラ","nicedama"))
arr.append( Wapon("kuge","クーゲルシュライバー","クーゲル","jetpack"))
arr.append( Wapon("no-ti","ノーチラス47","ノーチラス","amehurashi"))
arr.append( Wapon("kasa","パラシェルター","傘","tripletornado"))
arr.append( Wapon("camp","キャンピングシェルター","キャンプ","kyu-inki"))
arr.append( Wapon("supaiga","スパイガジェット","スパイガ","sameride"))
arr.append( Wapon("try","トライストリンガー","弓","megaphone"))
arr.append( Wapon("lact","LACT-450","ラクト","multimissile"))
arr.append( Wapon("drive","ドライブワイパー","ワイパー","ultrahanco"))
arr.append( Wapon("gym","ジムワイパー","ジムワイパー","syokuwonder"))
# Chill Season 追加ブキ
arr.append( Wapon("momiji","もみじシューター","もみじ","hopsonar"))
arr.append( Wapon("susikora","スプラシューターコラボ","スシコラ","tripletornado"))
arr.append( Wapon("purakora","プライムシューターコラボ","プラコラ","nicedama"))
arr.append( Wapon("kinmode","プロモデラーRG","金モデ","nicedama"))
arr.append( Wapon("supesyu","スペースシューター","スペシュ","megaphone"))
arr.append( Wapon("novaneo","ノヴァブラスターネオ","ノヴァネオ","ultrahanco"))
arr.append( Wapon("ka-deco","カーボンローラーデコ","カーデコ","ultrashot"))
arr.append( Wapon("wide","ワイドローラー","ワイロラ","kyu-inki"))
arr.append( Wapon("pabuhyu","パブロ・ヒュー","パヒュー","ultrahanco"))
arr.append( Wapon("rpen","R-PEN/5H","アルペン","energystand"))
arr.append( Wapon("supahyu","スパッタリー・ヒュー","スパヒュー","sameride"))
arr.append( Wapon("bakedeco","バケットスロッシャーデコ","バケデコ","syokuwonder"))
arr.append( Wapon("supikora","スプラスピナーコラボ","スピコラ","barrier"))

# 配列を辞書に入れ替える
for wapon in arr:
    wapons[wapon.filename] = wapon
    
# マッチング用テンプレート画像を置いてるディレクトリを指定
path = r"./assets/icons_asset/nuki"

files = os.listdir(path)
files = [f for f in files if os.path.isfile(os.path.join(path, f))]
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
    wapons[head].temp_img = _im.copy()


def ブキアイコン画像から分類(img):
    results = []
    # テンプレートを総当りでマッチングする
    for key, val in template_wapons.items():
        res = cv2.matchTemplate(img, val["img"], cv2.TM_CCORR_NORMED, mask=val["mask"])
        _, max_val, _, _ = cv2.minMaxLoc(res)
        results.append([key, max_val])
    
    results.sort(key=lambda x: x[1], reverse=True)

    # 一致率が一番高い要素がしきい値以上なら、そのテンプレート画像のブキと判定する
    if results[0][1] > 0.92: #threshold
        return wapons[ results[0][0] ]
    
    return None