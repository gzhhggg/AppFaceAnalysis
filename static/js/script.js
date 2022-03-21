
function displayChart_face(name,angry,contempt,disgust,fear,happiness,neutral,sad,surprise){
    var ctx = document.getElementById(name);
    var name  = new Chart(ctx, {
        //グラフの種類
        type: 'radar',
        //データの設定
        data: {
                labels: ['怒り', '軽蔑', '不愉快', '恐れ', '幸福','無関心','悲しみ','驚き'],
                datasets: [{
                label: '表情分析',
                //グラフのデータ
                data: [Number(angry), Number(contempt), Number(disgust), Number(fear), Number(happiness),Number(neutral),Number(sad),Number(surprise)],
                // データライン
                borderColor: 'red',
                borderWidth: 2,
                backgroundColor:"rgba(255, 0, 0, 0.3)"
            }],
        },
        //オプションの設定
        options: {
            scales: {
                r: {
                    //グラフの最小値・最大値
                    min: 0,
                    max: 100,
                    //背景色
                    backgroundColor: 'snow',
                    //グリッドライン
                    grid: {
                    color: 'black',
                    },
                    //アングルライン
                    angleLines: {
                    color: 'black',
                    },
                    //各項目のラベル
                    pointLabels: {
                    color: 'black',
                    },
                },
            },
        }, 
    });
}


function displayChart_hair(name,black,brown,gray,other,blond,red,white){
    var ctx = document.getElementById(name);
    var name  = new Chart(ctx, {
        //グラフの種類
        type: 'radar',
        //データの設定
        data: {
                labels: ['黒髪', '茶髪', 'グレー', 'その他', '金髪','赤髪','白色'],
                datasets: [{
                label: '髪色分析',
                //グラフのデータ
                data: [Number(black), Number(brown), Number(gray), Number(other), Number(blond),Number(red),Number(white)],
                // データライン
                borderColor: 'bule',
                borderWidth: 2,
                backgroundColor:"rgba(0, 0, 255, 0.3)"
            }],
        },
        //オプションの設定
        options: {
            scales: {
                r: {
                    //グラフの最小値・最大値
                    min: 0,
                    max: 100,
                    //背景色
                    backgroundColor: 'snow',
                    //グリッドライン
                    grid: {
                    color: 'black',
                    },
                    //アングルライン
                    angleLines: {
                    color: 'black',
                    },
                    //各項目のラベル
                    pointLabels: {
                    color: 'black',
                    },
                },
            },
        }, 
    });
}
