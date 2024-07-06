const { useState, useEffect, useRef } = React;

function App() {
    // スタイルオブジェクトの定義
    const styles = {
        sMadeBtn: 'btn btn-custom flex-fill',

    };

    // 状態管理
    const [selectedMenu, setSelectedMenu] = useState('Home');
    const [data, setData] = useState([]);
    // Chart.jsで使用するためのcanvas要素への参照を作成
    const chartRef = useRef(null);

    // メニューが選択された時にデータを取得
    useEffect(() => {
        if (selectedMenu === 'Api'){
            // エンドポイントからデータ取得
            fetch('http://localhost:5000/api/ice_data/')
            .then(response => response.json())
            .then(data => setData(data));
        }
    }, [selectedMenu]);

    // データが更新された時にチャートを描画
    useEffect(() => {
        if (data.length > 0 && selectedMenu === 'Api'){
            // Chart.jsの2Dコンテキストを取得
            const ctx = chartRef.current.getContext("2d");
            // バー型チャートを描画
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.年度),
                    datasets: [{
                        label: '金額(円)',
                        data: data.map(item => item['金額(円)']),
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
    }, [data]);

    const renderContent = () => {
        switch (selectedMenu) {
            case 'Api':
                return (
                <div>
                    <h1>Data Annual expenditure on ice cream</h1>
                    <div class="canvas-container">
                        <canvas ref={chartRef} ></canvas>
                    </div>
                </div>
            );
            case 'Contact':
                return (
                <div>準備中です。上記メニューから再度選択してください。</div>
            );
            default:
                return (
                <div>上記メニューから選択して下さい。</div>
            );
        }
    };

    // コンポーネントのレンダリング
    return (
        <div>
            <div className="navbar navbar-expand navbar-dark custom-bg">
                <div className="container-fluid">
                    <p className="navbar-brand text-black">Data</p>
                    <div className="navbar-collapse">
                        <ul className="navbar-nav">
                            <button className={`${styles.sMadeBtn} `} onClick={() => setSelectedMenu('Api')}>アイスクリーム年間消費</button>
                            <a className={`${styles.sMadeBtn}`} href="./japanMapPage.html">日本人口統計</a>
                            <button className={`${styles.sMadeBtn} `} onClick={() => setSelectedMenu('Contact')}>Preparation</button>
                        </ul>
                    </div>
                </div>
            </div>
            <div className="">
                {renderContent()}
            </div>
        </div>
    );
}

// ルート要素にAppコンポーネントをレンダリング
let root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);