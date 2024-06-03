## ライブラリをインポート
from flask import Flask , render_template 
import io
import base64
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import japanize_matplotlib

# Matplotlibのバックエンドを非GUIバックエンドに設定
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def index():
    text_str = 'Flaskを使用して作成した図をブラウザに出力'
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
    ## 作成したリストをpandasのデータフレームの形式に変換
    df = pd.DataFrame(data)
    # データフレームから年度と金額の列を取得
    years = df["年度"]
    amounts = df["金額(円)"]
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.bar(years, amounts, width=0.5, color='#4161A3', edgecolor='000')
    # グラフのタイトルとラベル
    plt.title('アイスクリーム年間支出額')
    plt.xlabel('年度')
    plt.ylabel('金額(円)')
    # 縦軸の範囲を設定
    plt.ylim(6000, 15000)
    # フィギュアをキャンバスに描画
    canvas = FigureCanvasAgg(fig)
    # バッファを作成
    s = io.BytesIO()
    # キャンバスの内容をPNG形式でバッファに書き込む
    canvas.print_png(s)
    # バッファの内容をBase64にエンコード、データをUTF-8形式の文字列に変換
    s = "data:image/png;base64," + base64.b64encode(s.getvalue()).decode("utf-8").replace("\n", "")
    return render_template("index.html",text = text_str,plot=s)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)
