# AppFaceAnalysis
タイトル：「[AppFaceAnalysis](https://appfaceanalysis.herokuapp.com/)」

pythonライブラリOpenCVを使い画像を取得して、np配列に変化してAzureFaceAPIを使用して顔位置を取得している。  
開発当初は顔認識をcascadesで取得していたが精度が低かったためAzureに変更した。  
グラフはjavaScriptのChart.jsで表示している。  
デプロイはHerokuで行っているため苦労はしなかったが起動までに時間がかかってしまう。  
私の顔でテストを行ったら20～30歳とかなりバラツキがあった。  

# DEMO
トップページ  
<img src="https://user-images.githubusercontent.com/93046615/163682083-cc02c0e2-d49c-41ab-953f-3446e1c9784c.png" width="800px">  
分析結果画面①   
<img src="https://user-images.githubusercontent.com/93046615/163682251-7f8979ea-e1b5-43f9-b3f7-e9971f6709e7.png" width="800px">  
分析結果画面②  
<img src="https://user-images.githubusercontent.com/93046615/163682274-b36cff34-8e7f-4538-a766-35bf5230d6f8.png" width="800px">  

# LINK  
「[AppFaceAnalysis](https://appfaceanalysis.herokuapp.com/)」  
※Herokuでデプロイしているため、アクセスに時間がかかります。  

# Requirement
 
Python ライブラリ
* certifi==2021.10.8  
* charset-normalizer==2.0.12  
* Flask==2.0.3  
* Flask-Uploads==0.2.1  
* Jinja2==3.0.3  
* MarkupSafe==2.1.0
* numpy==1.22.3
* opencv-python--headless==4.5.5.62
* pandas==1.4.1
* requests==2.27.1
* six==1.16.0
* urllib3==1.26.8
* Werkzeug==2.0.2  
※requriements-dev.txtをご確認ください  

フレームワーク  
* Flask  

クラウドサービス    
* Heroku  

# Point    
検出された顔はトリミングされ角度を修正している  
<img src="https://user-images.githubusercontent.com/93046615/163683090-b3283615-547a-4ac8-b5ad-b45930abfc7a.png" width="300px">
<img src="https://user-images.githubusercontent.com/93046615/163683076-83ef31eb-ee53-4c14-9ba3-52aeda9af27a.png" width="300px">  
Azure FaceAPIで取得できる髪色値を元にChart.jsにでグラフを表示している  
<img src="https://user-images.githubusercontent.com/93046615/163683189-0e6befa5-0f1c-495e-a2c0-9efa3a5ee4bf.png" width="300px">  


構成イメージ  
<img src="https://user-images.githubusercontent.com/93046615/163683449-6926ccad-688d-4a08-b532-04a672a1bcb6.png" width="800px">
 
# Note
 
AWSで実装を検討中
 
# Author

* 作成者 KeiichiAdachi
* 所属 Japan/Aichi
* E-mail keiichimonoo@gmail.com
 
# License
なし  
