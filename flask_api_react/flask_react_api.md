## 概要
- データフレームで作成したデータをAPIで返す。
- そのAPIを受取り、React(CDN)とライブラリを組み合わせてレンダリングする。

## フォルダーの作成
- pythonファイルを作成
- HTMLファイルを作成
```html
<!-- tailwingの読み込み -->
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<!-- React(CDN)を読み込み -->
<script src="https://unpkg.com/react/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/babel-standalone@6/babel.min.js"></script>
```

- JavaScriptファイルを作成

## JSのライブラリ
- [Chart.js](https://www.chartjs.org/)
  - データを可視化するためのライブラリ
  - [使い方参考](https://qiita.com/Haruka-Ogawa/items/59facd24f2a8bdb6d369)
  