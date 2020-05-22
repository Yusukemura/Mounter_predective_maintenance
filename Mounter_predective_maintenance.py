# Mounter_predictive_maintenance.py - 流量センサデータの昨日分を加工、分析し、エアー漏れが起きていないか確認する

from datetime import datetime, timedelta
import glob
import csv
import os
import pandas as pd


# "昨日"の文字列を定義
today = datetime.today()
yesterday = today - timedelta(days=1)
yesterday_str = datetime.strftime(yesterday, '%y%m%d')

# フォルダ中のパスを取得
# DATA_PATH = "./SampleCode_20200325/DIOデータ分析/csv/" - 本番の値
DATA_PATH = "" # 仮の値
Yesterday_Datas = glob.glob('{}*{}*.csv'.format(DATA_PATH,yesterday_str))
print(Yesterday_Datas)

# "昨日"のcsvデータを1つに結合
list = []

for data in Yesterday_Datas:
    list.append(pd.read_csv(data))

df = pd.concat(list, sort=False)
df = df.query('SensorId == 1')
df = df.sort_values('TIME')
print(df)

# 結合したcsvを出力
df.to_csv('{}.csv'.format(yesterday_str), encoding='utf_8')

# csvの上から1行目から順にValueを読み取り、
# TODO: 値が0以外の時のTIMEを始業時刻と定義する
df = df.set_index('TIME')
# reader = csv.reader('{}.csv'.format(yesterday_str))
for x in df['Value']:
    if x == 0:
        continue
    else:
        print(x)
        first_value = x
        print(df.query('Value==12.5').index)
        break

# TODO: 終業時刻も同様に定義


# TODO: 始業時刻、終業時刻から操業時間を読み取り(for, if)、
# TODO: 操業時間中に値が0(zero_count)の時がいくつあるか数える(count)


# 値が0の回数が1回以上あれば異常なし。0回であればエアー漏れの恐れあり。
if zero_count >= 1:
    print("{}は異常ありません。".format(yesterday_str))
else:
    print("エアー漏れの恐れがあります。")