const { useState, useEffect, useRef } = React;

function App() {
    // スタイルオブジェクトの定義
    const styles = {
        columnFlex: 'flex flex-col',
        bottunBase: 'py-1.5 px-4 transition-colors border font-medium rounded-lg disabled:opacity-50 mb-4',
        bottunColorGray: 'bg-gray-50 active:bg-gray-200 border-gray-200 text-gray-900 hover:bg-gray-100',
        bottunColorGreen: 'bg-green-600 active:bg-green-800 border-green-700 text-white hover:bg-green-700',

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
                    <canvas ref={chartRef} width="600" height="400"></canvas>
                </div>
            );
            case 'Contact':
                return (
                <div>Contact Content</div>
            );
            default:
                return (
                <div>左のサイドメニューから選択して下さい。</div>
            );
        }
    };

    // コンポーネントのレンダリング
    return (
        <div className="flex w-full h-screen">
            <div className="w-1/4 bg-green-200 text-white p-4">
                <ul className= {styles.columnFlex}>
                    <button className={`${styles.bottunBase} ${styles.bottunColorGreen}`} onClick={() => setSelectedMenu('Api')}>アイスクリーム年間消費</button>
                    <button className={`${styles.bottunBase} ${styles.bottunColorGray} w-2/3`}><a href="./japanMapPage.html">日本人口統計</a></button>
                    <button className={`${styles.bottunBase} ${styles.bottunColorGray} w-1/2`} onClick={() => setSelectedMenu('Contact')}>Contact</button>
                </ul>
            </div>
            <div className="w-3/4 p-4">
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