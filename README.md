# python-myjagular4-simulator

マイジャグラー 4 の Python シミュレータ

# requirements

- Python 3.X
- Numpy
- Pandas

## 使い方

### myjagular4.py

- MyJagular4 クラス
  - コンストラクタ \_\_init\_\_(int: config_num) ・・・ 設定値(int: 0~6，0 でランダム設定)
  - メソッド
    - play() ・・・ 1 ゲームプレイ
    - simulate(int: simu_num) ・・・ 指定回数分シミュレートする
    - to_csv(str: filename) ・・・ 指定ファイルに現在までのメダル数の遷移を csv 形式で出力

### main.py

- コマンドライン引数
  - 引数 1 ・・・ 設定値(int: 0~6，0 でランダム設定)
  - 引数 2 ・・・ シミュレート回数(int)
  - 引数 3 ・・・ csv 出力ファイル名(str)
  - 例 ```$ python main.py 6 10000 test.csv```
