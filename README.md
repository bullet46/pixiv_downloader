# pixiv_downloader
##### A script which can download pixiv pic by author's name or search result
---
### 一个正在不断完善的pixiv图片内容多线程下载爬虫

### 2020.2.14 版本更新：
      1.修复了只能获取画册第一张图的bug
      2.优化了爬虫速度
### 2020.2.15 版本更新：
      1.加入搜索爬取功能，可以通过指定词条进行爬取
      2.加入代理检测功能，若未连接至国际互联网则中断程序


### 2020.2.19 版本更新:
      1.使用Pyqt构建出了相关控件
      2.可自定义下载线程数
      3.加入了获取每日排行的相关控件
      4.可选择保存目录


### 2020.2.20 图形版本更新:
    图像界面已完工
   ![avatar](README.assets/3308be8081090815.png)

### 2020.2.21 图形版本更新
      1.修复了无法停止爬取的问题
      2.为应用添加图标，提高辨识度
### 2020.2.23 图形版本更新
      1.修改了部分bug，降低了应用闪退的几率
      2.将默认线程数设置为8，尽量跑满宽带

### 注
      该爬虫需要开启代理才能运行，否则将会报错
      本程序能够多线程创建文件，可能会被杀毒软件误报
      若出现误报请退出杀毒软件