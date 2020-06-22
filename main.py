from myjagular4 import MyJagular4
import sys

if __name__ == "__main__":
    args = sys.argv
    mj4 = MyJagular4(int(args[1]))  # 引数1 の 設定値を用いてインスタンス化
    mj4.simulate(int(args[2]))  # 引数2 の シミュレートゲーム数を用いてシミュレート
    mj4.to_csv(args[3])  # 引数3 の ファイル名にcsvを吐き出す
