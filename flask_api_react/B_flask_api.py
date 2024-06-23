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

# e-StatのAPI_KEY
api = os.environ.get("API_KEY")
# データの取得と整形
df = web.DataReader("0003411884", "estat", api_key=api, retry_count=3)
map_df = df[(df['時間軸(年次)'] == '2022年') & (df['性別'] == '総数') & (df['都道府県（特別区－指定都市再掲）'] != '全国')]
map_df = map_df.reset_index().drop(['index', '時間軸(年次)', '性別'], axis=1)
map_df.rename(columns={'都道府県（特別区－指定都市再掲）': 'name', '人口': 'population_jp'}, inplace=True)


@app.route('/api/ice_data/', methods=['GET'])
def get_ice_data():
    # 辞書型をJSON型にして返す
    return jsonify(ice_df.to_dict(orient='records'))

@app.route('/api/map_data/', methods=['GET'])
def get_map_data():
    # 辞書型をJSON型にして返す
    return jsonify(map_df.to_dict(orient='records'))

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)