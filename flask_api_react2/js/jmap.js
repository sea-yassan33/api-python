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
                width: 800,
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
            // テーブルにデータを表示
            var tableBody = document.getElementById('data-table-body');
            data.forEach(function(area) {
                // タグの作成
                var row = document.createElement('tr');
                var nameCell = document.createElement('td');
                var populationCell = document.createElement('td');
                var colorCell = document.createElement('td');
                // タグ内のテキスト挿入
                nameCell.textContent = area.name;
                populationCell.textContent = area.number.toLocaleString();
                colorCell.textContent = area.color;
                // テーブルタグ内に作成したタグを挿入
                row.appendChild(nameCell);
                row.appendChild(populationCell);
                row.appendChild(colorCell);
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching data:', error));
});