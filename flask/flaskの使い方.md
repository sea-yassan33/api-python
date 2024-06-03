## Flaskの準備とインストール

## インストール
'''
pip install Flask
'''

## フォルダーの作成
- フォルダー内にpythonファイルを作成

## 階層例
```
flask
├── ****.py
└── templates
    └── index.html
``` 

## ****.py
'''
## ライブラリをインポート
from flask import Flask , render_template 
@app.route('/')
def index():
    text_str = 'Hello Flask'
    return render_template("index.html", text = text_str)

# アプリケーションを実行
if __name__ == '__main__':
    app.run(debug=True)
'''

## index.html
```
<html>
	<head>
		<title>サンプル</title>
	</head>
	<body>
		<h1>{{text}}</h1>
	</body>
</html>
```

## 実行
'''
python ****.py

'''

## アクセス
```
http://localhost:5000/
```