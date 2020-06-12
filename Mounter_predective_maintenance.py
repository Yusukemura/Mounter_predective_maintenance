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

# Valueが0より大きい値（列）を抽出
value_not_zero = df[df[‘Value’] > 0]

# 抽出されたdfの最初の時間(始業時間)と最後の時間(終業時間)を抽出
start_record = value_not_zero[0:1]
end_record = value_not_zero[-2:-1]

start_time = start_record['TIME']
end_time = end_record['TIME']

# TODO: ②後のdfから操業時間の間のdfを抽出(df[‘始業’:’終業’])またはindexで指定。

# TODO: 操業時間中に値が0(zero_count)の時がいくつあるか数える(count)


# 値が0の回数が1回以上あれば異常なし。0回であればエアー漏れの恐れあり。
if zero_count >= 1:
    print("{}は異常ありません。".format(yesterday_str))
else:
    print("エアー漏れの恐れがあります。")