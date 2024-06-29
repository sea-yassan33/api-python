document.addEventListener('DOMContentLoaded', function() {
    // APIからデータを取得
    fetch("http://localhost:5000/api/map_data/")
        .then(response => response.json())
        .then(data => {
            // 地図を描画する
            var d = new jpmap.japanMap(document.getElementById("my-map"), {
                //APIから取得したデータを使用
                areas: data,
                //地図の幅を設定(単位：ピクセル)
                width: 1000,
                //都道府県名を表示設定
                showsPrefectureName: true,
                //文字色の設定
                fontColor: '#B9ADB6',
                //沖縄地方が地図の左上の分離されたスペースに移動する
                movesIslands: true,
                //都道府県の境界線の色を設定
                borderLineColor: "#FFFE41",
                //表示させている都道府県名を日本語にする
                lang: 'ja',
                //都道府県が選択されたときのコールバック関数を設定
                onSelect: function(data) {
                    alert(data.area.name +"の人口：" + data.area.number.toLocaleString() +"人");
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});