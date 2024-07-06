from flask import Flask, jsonify
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import japanize_matplotlib
from dotenv import load_dotenv
import jpy_datareader.data as web
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
# UTF-8に変換（日本語をJSONで返す場合は必要）
app.config["JSON_AS_ASCII"] = False
# アプリ全体に対してCORSを有効化にする
CORS(app)

# アイスクリームのデータフレームに格納
ice_data = [
    {"年度": "2014年", "金額(円)": 8006},
    {"年度": "2015年", "金額(円)": 8708},
    {"年度": "2016年", "金額(円)": 8908},
    {"年度": "2017年", "金額(円)": 9047},
    {"年度": "2018年", "金額(円)": 9670},
    {"年度": "2019年", "金額(円)": 9701},
    {"年度": "2020年", "金額(円)": 10113},
    {"年度": "2021年", "金額(円)": 10148},
    {"年度": "2022年", "金額(円)": 10847},
    {"年度": "2023年", "金額(円)": 11580}
]
ice_df = pd.DataFrame(ice_data)

# 都道府県の対応辞書を作成
prefecture_map = {
    '三重県': '三重', '京都府': '京都', '佐賀県': '佐賀', '兵庫県': '兵庫', '北海道': '北海道',
    '千葉県': '千葉', '和歌山県': '和歌山', '埼玉県': '埼玉', '大分県': '大分', '大阪府': '大阪',
    '奈良県': '奈良', '宮城県': '宮城', '宮崎県': '宮崎', '富山県': '富山', '山口県': '山口',
    '山形県': '山形', '山梨県': '山梨', '岐阜県': '岐阜', '岡山県': '岡山', '岩手県': '岩手',
    '島根県': '島根', '広島県': '広島', '徳島県': '徳島', '愛媛県': '愛媛', '愛知県': '愛知',
    '新潟県': '新潟', '東京都': '東京', '栃木県': '栃木', '沖縄県': '沖縄', '滋賀県': '滋賀',
    '熊本県': '熊本', '石川県': '石川', '神奈川県': '神奈川', '福井県': '福井', '福岡県': '福岡',
    '福島県': '福島', '秋田県': '秋田', '群馬県': '群馬', '茨城県': '茨城', '長崎県': '長崎',
    '長野県': '長野', '青森県': '青森', '静岡県': '静岡', '香川県': '香川', '高知県': '高知',
    '鳥取県': '鳥取', '鹿児島県': '鹿児島'
}
# 都道府県コードの辞書
prefecture_codes = {
    "北海道": 1, "青森": 2, "岩手": 3, "宮城": 4, "秋田": 5, "山形": 6, "福島": 7, "茨城": 8, "栃木": 9, "群馬": 10,
    "埼玉": 11, "千葉": 12, "東京": 13, "神奈川": 14, "新潟": 15, "富山": 16, "石川": 17, "福井": 18, "山梨": 19, 
    "長野": 20, "岐阜": 21, "静岡": 22, "愛知": 23, "三重": 24, "滋賀": 25, "京都": 26, "大阪": 27, "兵庫": 28, "奈良": 29, 
    "和歌山": 30, "鳥取": 31, "島根": 32, "岡山": 33, "広島": 34, "山口": 35, "徳島": 36, "香川": 37, "愛媛": 38, "高知": 39, 
    "福岡": 40, "佐賀": 41, "長崎": 42, "熊本": 43, "大分": 44, "宮崎": 45, "鹿児島": 46, "沖縄": 47
}

# e-StatのAPI_KEY
api = os.environ.get("API_KEY")
# データの取得と整形
df = web.DataReader("0003411884", "estat", api_key=api,retry_count=3)
map_df = df[(df['時間軸(年次)'] == '2022年') & (df['性別'] == '総数') & (df['都道府県（特別区－指定都市再掲）'] != '全国')]
map_df = map_df.reset_index().drop(['index', '時間軸(年次)', '性別'], axis=1)
map_df.rename(columns={'都道府県（特別区－指定都市再掲）': 'name', '人口': 'population_jp'}, inplace=True)
map_df['name'] = map_df['name'].replace(prefecture_map)
# カラーマップでmatplotlibのcmapのjetを設定
cmap = plt.get_cmap('jet')
# 人口の最小値と最大値を取得
min_val = map_df['population_jp'].min()
max_val = map_df['population_jp'].max()
# カラーマップの最小値と最大値を設定
norm = plt.Normalize(vmin=min_val,vmax=max_val)
# データをSeries化する際に可視化対象のデータをカラーマップに従ってカラーコードに変換する関数を作成
fcol = lambda x: '#' + bytes(cmap(norm(x), bytes=True)[:3]).hex()
map_df['color'] =map_df['population_jp'].apply(fcol)
map_df['prefecture_code'] = map_df['name']
map_df['prefecture_code'] = map_df['prefecture_code'].map(prefecture_codes)
map_df = map_df.sort_values('prefecture_code')
map_df = map_df.set_index('prefecture_code')

# JSON用のリストを作成
json_list = []

for index, row in map_df.iterrows():
    json_item = {
        "code": index,
        "name": row["name"],
        "color": row["color"],
        "number": row["population_jp"]
    }
    json_list.append(json_item)

json_output = json.dumps(json_list, ensure_ascii=False, indent=4)

@app.route('/api/ice_data/', methods=['GET'])
def get_ice_data():
    # 辞書型をJSON型にして返す
    return jsonify(ice_df.to_dict(orient='records'))

@app.route('/api/map_data/', methods=['GET'])
def get_map_data():
    return json_output

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)