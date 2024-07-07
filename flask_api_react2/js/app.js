const { useState, useEffect, useRef } = React;

function App() {
    // スタイルオブジェクトの定義
    const styles = {
        sMadeBtn: 'btn btn-custom flex-fill',
        prSkipContent: 'sr-only sr-only-focusable',
        prNaveBar: 'navbar  fixed-top flex-md-nowrap p-0 shadow custom-bg',
        prNaveBarContent: 'navbar-brand col-sm-3 col-md-2 mr-0',
        prNaveBarContent02: 'col d-flex align-items-center justify-content-center',
        prMainDisplay: 'px-4 min-vh-100',
        prMainOption: 'd-flex justify-content-between flex-wrap flex-md-nowrap align-items-center pt-3 pb-2 mb-3 border-bottom',
        prBtn01:'btn btn-sm btn-outline-secondary',
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
                    <div className={`${styles.prMainOption}`}>
                        <h2 class="h2">Data Annual expenditure on ice cream</h2>
                    </div>
                    <div class="canvas-container">
                        <canvas ref={chartRef} ></canvas>
                    </div>
                </div>
            );
            case 'Contact':
                return (
                <div>
                    <div className={`${styles.prMainOption}`}>
                        <h2 class="h2">準備中です。上記メニューから再度選択してください。</h2>
                    </div>
                </div>
            );
            default:
                return (
                <div>
                    <div className={`${styles.prMainOption}`}>
                        <h2 class="h2">上記メニューから選択して下さい。</h2>
                    </div>
                </div>
            );
        }
    };

    // コンポーネントのレンダリング
    return (
        <div>
            <a id="skippy" className={`${styles.prSkipContent} `} href="#content">
                <div className="container">
                    <span className="skiplink-text">Skip to main content</span>
                    
                </div>
            </a>
            <nav className={`${styles.prNaveBar} `}>
                <div className='row'>
                    <div className={`${styles.prNaveBarContent02}`}>
                        <p className={`${styles.prNaveBarContent}`} >Open Data</p>
                    </div>
                    <div className={`${styles.prNaveBarContent02}`}>
                        <button className={`${styles.sMadeBtn}`} onClick={() => setSelectedMenu('Api')}>アイスクリーム年間消費</button>
                    </div>
                    <div className={`${styles.prNaveBarContent02}`}>
                        <a className={`${styles.sMadeBtn}`} href="./japanMapPage.html">日本人口統計</a>
                    </div>
                    <div className={`${styles.prNaveBarContent02}`}>
                        <button className={`${styles.sMadeBtn}`} onClick={() => setSelectedMenu('Contact')}>Preparation</button>
                    </div>
                </div>
                <ul className="navbar-nav px-3">
                    <li className="nav-item text-nowrap">
                        <div className="nav-link">React Page</div>
                    </li>
                </ul>
            </nav>
            <div className="mt-5">
                <div className={`${styles.prMainDisplay}`}>
                    <div className="btn-toolbar mb-2 mb-md-0">
                        <div className="btn-group mr-2">
                            <button type="button" className={`${styles.prBtn01}`}>Share</button>
                            <button type="button" className={`${styles.prBtn01}`}>Export</button>
                        </div>
					</div>
                    {renderContent()}
                </div>
            </div>
        </div>
    );
}

// ルート要素にAppコンポーネントをレンダリング
let root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <App />
);