from config import CONFIG  # 設定別確率のインポート
import random
import pandas as pd
import numpy as np


class MyJagular4:
    # 設定1~6の数字を引数にとるコンストラクタ
    def __init__(self, config_num):
        # もし0ならランダムに設定を決める
        self.__config_num = config_num if config_num != 0 else random.randint(
            1, 6)

        # 設定の値に応じて対応する確率設定をプロパティにセット
        self.__config = CONFIG["CONFIG{}".format(config_num)]

        # 現在のゲーム数とメダル数のカウンタ
        self.__game = 0
        self.__medal = 0

        # 役のカウンタ
        self.__grape = 0
        self.__cherry = 0
        self.__big = 0
        self.__reg = 0
        self.__clown = 0
        self.__bell = 0
        self.__replay = 0

        # シミュレータ用 何ゲームシミュレートするか
        self.__simu_num = 0

        # メダル数の遷移を保存するリスト
        self.__medal_list = []

    def __str__(self):
        return "マイジャグラー4の設定{}シミュレータ".format(self.__config_num)

    # 役のフラグを確率に沿ってランダム選択
    def flag_selecter(self):
        flag = np.random.choice(
            a=[
                "GRAPE",
                "CORNER_CHERRY",
                "NORMAL_BIG",
                "BIG_WITH_CORNER_CHERRY",
                "BIG_WITH_CENTER_CHERRY",
                "NORMAL_REG",
                "REG_WITH_CORNER_CHERRY",
                "CLOWN",
                "BELL",
                "REPLAY",
                "NOTHING"
            ],
            p=[
                self.__config["GRAPE"],
                self.__config["CORNER_CHERRY"]
                - self.__config["BIG_WITH_CORNER_CHERRY"]
                - self.__config["REG_WITH_CORNER_CHERRY"],
                self.__config["NORMAL_BIG"],
                self.__config["BIG_WITH_CORNER_CHERRY"],
                self.__config["BIG_WITH_CENTER_CHERRY"],
                self.__config["NORMAL_REG"],
                self.__config["REG_WITH_CORNER_CHERRY"],
                self.__config["CLOWN"],
                self.__config["BELL"],
                self.__config["REPLAY"],
                1
                - self.__config["GRAPE"]
                - (self.__config["CORNER_CHERRY"]
                   - self.__config["BIG_WITH_CORNER_CHERRY"]
                   - self.__config["REG_WITH_CORNER_CHERRY"])
                - self.__config["NORMAL_BIG"]
                - self.__config["BIG_WITH_CORNER_CHERRY"]
                - self.__config["BIG_WITH_CENTER_CHERRY"]
                - self.__config["NORMAL_REG"]
                - self.__config["REG_WITH_CORNER_CHERRY"]
                - self.__config["CLOWN"]
                - self.__config["BELL"]
                - self.__config["REPLAY"]
            ]
        )
        return flag

    # 選択した役の実行
    def flag_executor(self):
        flag = self.flag_selecter()  # 役の選択

        if flag == "GRAPE":  # ぶどう
            self.__medal += 7  # 7枚払い出し
            self.__medal_list.append(self.__medal)
            self.__grape += 1  # ぶどうカウンタ

        elif flag == "CORNER_CHERRY":  # 角チェリー
            self.__medal += 2  # 2枚払い出し
            self.__medal_list.append(self.__medal)
            self.__cherry += 1  # チェリーカウンタ

        elif flag == "NORMAL_BIG":  # 通常BIG
            self.__medal -= 1  # 目押しに1枚使う
            self.__medal += 312  # 312枚払い出し
            self.__medal_list.append(self.__medal)
            self.__big += 1  # BIGカウンタ

        elif flag == "BIG_WITH_CORNER_CHERRY":  # 角チェリー + BIG
            self.__medal -= 1  # 目押しに1枚使う
            self.__medal += 314  # 角チェリー2枚 + BIG312枚払い出し
            self.__medal_list.append(self.__medal)
            self.__big += 1  # BIGカウンタ
            self.__cherry += 1  # チェリーカウンタ

        elif flag == "BIG_WITH_CENTER_CHERRY":  # 中段チェリー + BIG
            self.__medal -= 1  # 目押しに1枚使う
            self.__medal += 314  # 中段チェリー2枚 + BIG312枚払い出し
            self.__medal_list.append(self.__medal)
            self.__big += 1  # BIGカウンタ
            self.__cherry += 1  # チェリーカウンタ

        elif flag == "NORMAL_REG":  # 通常REG
            self.__medal -= 1  # 目押しに1枚使う
            self.__medal += 104  # 104枚払い出し
            self.__medal_list.append(self.__medal)
            self.__reg += 1  # REGカウンタ

        elif flag == "REG_WITH_CORNER_CHERRY":  # 角チェリー + REG
            self.__medal -= 1  # 目押しに1枚使う
            self.__medal += 106  # 角チェリー2枚 + REG104枚払い出し
            self.__medal_list.append(self.__medal)
            self.__reg += 1  # REGカウンタ
            self.__cherry += 1  # チェリーカウンタ

        elif flag == "CLOWN":  # ピエロ
            self.__medal += 15  # 15枚払い出し
            self.__medal_list.append(self.__medal)
            self.__clown += 1  # ピエロカウンタ

        elif flag == "BELL":  # ベル
            self.__medal += 15  # 15枚払い出し
            self.__medal_list.append(self.__medal)
            self.__bell += 1  # ベルカウンタ

        elif flag == "REPLAY":  # リプレイ
            self.__medal_list.append(self.__medal)
            self.__replay += 1  # リプレイカウンタ
            if(self.__simu_num > self.__game):  # シミュレート回数を超えていなければリプレイ実行
                self.__game += 1  # ゲーム数 + 1
                self.flag_executor()  # 役の選択と実行

        elif flag == "NOTHING":  # 役なし
            self.__medal_list.append(self.__medal)

        '''
        共通処理であるself.__medal_list.append()をここで実行しないのは、
        リプレイが入るとメダル数を記録する前に次のゲームを回してしまうため
        '''

    # 1ゲームプレイ
    def play(self):
        self.__medal -= 3  # 1ゲーム3枚BET
        self.__game += 1  # ゲーム数 + 1
        self.flag_executor()  # 役の選択と実行

    # シミュレート用
    def simulate(self, simu_num):
        # 引数にシミュレートするゲーム数を取る
        self.__simu_num = simu_num

        print("シミュレート開始：マイジャグラー4，設定{}，{}ゲーム".format(
            self.__config_num, simu_num))

        while(self.__game < int(simu_num)):
            self.play()
            print("\r", "ゲーム数:", self.__game, "メダル数:", self.__medal, end="")

        print("\nシミュレート終了")

        print("シミュレート結果:")

        print("\tGRAPE : {}, 期待値 : {}".format(
            str(self.__grape/int(simu_num)), str(self.__config["GRAPE"])))

        print("\tCHERRY : {}, 期待値 : {}".format(str(self.__cherry/int(simu_num)),
                                               str(self.__config["CORNER_CHERRY"]+self.__config["BIG_WITH_CENTER_CHERRY"])))

        print("\tREPLAY : {}, 期待値 : {}".format(
            str(self.__replay/int(simu_num)), str(self.__config["REPLAY"])))

        print("\tCLOWN : {}, 期待値 : {}".format(
            str(self.__clown/int(simu_num)), str(self.__config["CLOWN"])))

        print("\tBELL : {}, 期待値 : {}".format(
            str(self.__bell/int(simu_num)), str(self.__config["BELL"])))

        print("\tREG : {}, 期待値 : {}".format(
            str(self.__reg/int(simu_num)), str(self.__config["REG"])))

        print("\tBIG : {}, 期待値 : {}".format(
            str(self.__big/int(simu_num)), str(self.__config["BIG"])))

        print("\t合算 : {}, 期待値 : {}".format(
            str((self.__big+self.__reg)/int(simu_num)), str(self.__config["BONUS_SUM"])))

    # ゲーム数のメダル遷移をcsvに吐き出し
    def to_csv(self, filepath):
        game_list = [i + 1 for i in range(len(self.__medal_list))]
        df = pd.DataFrame({'G': game_list, 'medal': self.__medal_list})
        df.to_csv(filepath, index=False)
