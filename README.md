
# splatoon3 Read Aloud the weapon killed

ひろゆきがスプラトゥーンのキルデス報告をしてくれるアプリです

AIひろゆき音声利用しています。
Voiced by https://CoeFont.cloud

## 

[【画像認識】AIひろゆきがスプラトゥーン3のキルデス報告してくれるアプリ作った話](https://qiita.com/Kazuma_Kikuya/items/71644455015a30a01571)

スプラトゥーン3のバトル画面を解析し、様々な情報を読み上げるアプリです。
https://CoeFont.cloudにて事前に生成した音声データを読み上げています。

読み上げる内容は

- 味方・敵の何のブキがデスしたか
- 味方・敵の何のスペシャルウエポンを抱え落ちしたか
- 味方が何のスペシャルウエポン使用したか
- 敵が何のスペシャルウエポン貯まったか
- マップから「イカ忍」「ステジャン」「対物」持ちの敵のブキを読み上げ
- 敵の何のブキが復帰したか

他、各プレイヤーの「デス回数」「生存秒数」「デスから復帰までの秒数」をゲージで表示し可視化します。

※ブキの分類にテンプレートマッチングを利用していますが、ゲーム画面からから抽出テンプレート画像を配布することは権利上問題ありそうなので各自で用意してassetsディレクトリに置いてください。

# Demo
https://www.youtube.com/watch?v=zgMndF3gcMI

## Usage

キャプチャボードが必要です。
nintendo switch <---> キャプチャボード <---> PC　と接続してください。 

assetsディレクトリにブキテンプレートを用意します。

python main.py

バトル開始時するとゲージ表示のGUIが表示され。読み上げが開始されます。

## Requirement
- Python 3.8.5
- opencv
- numpy
- pydub

## Reference

## Author
Kazuma Kikuya
[FB](https://www.facebook.com/profile.php?id=100030409253259)
[qiita](https://qiita.com/Kazuma_Kikuya)

## Licence
MIT



