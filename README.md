# iSPark: 大数据驱动的智能路内停车管理
旧版：http://62.234.214.208:8080/visualization <br>旧版在服务器端使用Matplotlib绘图，并传输到网页进行显示。<br>
新版：http://62.234.214.208:8080/visualization/test <br>新版将数据传输到网页端，并在网页端使用ECharts绘图并显示。

服务器端语言是Python，依赖的库有：`Django`、`pandas`、`mysqlclient`

## 使用方式（涉及数据库密码，若需运行，请在群里私聊我要配置文件）
本机运行：在项目根目录下运行命令`python manage.py runserver 127.0.0.1:8000`<br>
然后在浏览器访问旧版： http://127.0.0.1:8000/visualization 或新版：http://127.0.0.1:8000/visualization/test

服务器远程运行：在项目根目录下运行命令`python manage.py runserver 0.0.0.0:8000`<br>
然后在浏览器访问旧版： http://服务器IP:8000/visualization 或新版：http://服务器IP:8000/visualization/test

## 本文档为临时整理，会继续更新。Feel free to ask me any question !!!
