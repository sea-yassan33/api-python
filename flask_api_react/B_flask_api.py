from flask import Flask, jsonify
import pandas as pd
import os
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
    '三重県': 'mie', '京都府': 'kyoto', '佐賀県': 'saga', '兵庫県': 'hyogo', '北海道': 'hokkaido',
    '千葉県': 'chiba', '和歌山県': 'wakayama', '埼玉県': 'saitama', '大分県': 'oita', '大阪府': 'osaka',
    '奈良県': 'nara', '宮城県': 'miyagi', '宮崎県': 'miyazaki', '富山県': 'toyama', '山口県': 'yamaguchi',
    '山形県': 'yamagata', '山梨県': 'yamanashi', '岐阜県': 'gifu', '岡山県': 'okayama', '岩手県': 'iwate',
    '島根県': 'shimane', '広島県': 'hiroshima', '徳島県': 'tokushima', '愛媛県': 'ehime', '愛知県': 'aichi',
    '新潟県': 'niigata', '東京都': 'tokyo', '栃木県': 'tochigi', '沖縄県': 'okinawa', '滋賀県': 'shiga',
    '熊本県': 'kumamoto', '石川県': 'ishikawa', '神奈川県': 'kanagawa', '福井県': 'fukui', '福岡県': 'fukuoka',
    '福島県': 'fukushima', '秋田県': 'akita', '群馬県': 'gunma', '茨城県': 'ibaraki', '長崎県': 'nagasaki',
    '長野県': 'nagano', '青森県': 'aomori', '静岡県': 'shizuoka', '香川県': 'kagawa', '高知県': 'kochi',
    '鳥取県': 'tottori', '鹿児島県': 'kagoshima'
}

# e-StatのAPI_KEY
api = os.environ.get("API_KEY")
# データの取得と整形
df = web.DataReader("0003411884", "estat", api_key=api, retry_count=3)
map_df = df[(df['時間軸(年次)'] == '2022年') & (df['性別'] == '総数') & (df['都道府県（特別区－指定都市再掲）'] != '全国')]
map_df = map_df.reset_index().drop(['index', '時間軸(年次)', '性別'], axis=1)
map_df.rename(columns={'都道府県（特別区－指定都市再掲）': 'name', '人口': 'population_jp'}, inplace=True)
map_df['name'] = map_df['name'].replace(prefecture_map)
# データフレームを辞書に変換
map_dict = map_df.set_index('name')['population_jp'].to_dict()

@app.route('/api/ice_data/', methods=['GET'])
def get_ice_data():
    # 辞書型をJSON型にして返す
    return jsonify(ice_df.to_dict(orient='records'))

@app.route('/api/map_data/', methods=['GET'])
def get_map_data():
    # 辞書型をJSON型にして返す
    return jsonify(map_dict)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)