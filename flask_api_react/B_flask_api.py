from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
# UTF-8に変換（日本語をJSONで返す場合は必要）
app.config["JSON_AS_ASCII"] = False
# アプリ全体に対してCORSを有効化にする
CORS(app)

# データフレームに格納
data = [
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
df = pd.DataFrame(data)

@app.route('/api/data/', methods=['GET'])
def get_data():
    # 辞書型をJSON型にして返す
    return jsonify(df.to_dict(orient='records'))

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)