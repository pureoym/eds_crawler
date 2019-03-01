# 说明文档

![scpray系统流程图](https://github.com/pureoym/eds_crawler/blob/master/scrapy_pic.png)

## 运行需求
python 3.6  
scrapy  
pymysql  
redis    
twisted  
DBUtils  
selenium  
phantomjs  

## 业务逻辑
定期执行cookie爬虫获取登录cookie并入库；定期执行微博爬虫，通过库中cookie登录，获取微博内容并入库。

### 微博爬虫  
1 执行策略：每5分钟执行一次，每次爬取至上次爬取最新条目，至多爬取12页  
2 超时时间：290秒    
3 请求时间间隔：3秒  
4 执行方式：阻塞式单线程  
5 执行逻辑：  
启动爬虫，中间件获取库中cookie；  
判断是否需要爬取下一页；  
爬取本页微博列表，根据需要爬取子页面；    

### cookie爬虫  
1 执行策略：每天执行，根据更新时间与超时时间判断是否过期，如果过期则爬取新cookie并更新  
2 更新超时时间：15天  
3 执行逻辑：  
进入未登录列表页，点击登录；    
进入登录页，输入用户名密码，点击登录；    
进入登录后列表页，获取cookie并入库； 

## 部署与运行
### 部署配置
服务器： 10.10.   
日志路径：/data0/search/eds_crawler/logs/  

### 部署流程
1 sh bin/script/publish_eds_crawler.sh  
2 创建日志路径：/data0/search/eds_crawler/logs/  
3 执行一次或周期执行

### 服务器上执行一次
sh /application/search/eds_crawler/start.sh  
vi /application/search/eds_crawler/start.sh  
:set ff=unix  

### 服务器上周期执行
crantab -e  
查看日志 cat /var/spool/mail/search
  
## 环境搭建
### scrapy
```commandline
pip install scrapy  
```

### selenium  
```commandline
pip install selenium  
```

### phantomjs
```commandline
cd /applcation/search
wget 'https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2'
tar -jxvf phantomjs-2.1.1-linux-x86_64.tar.bz2
mv phantomjs-2.1.1-linux-x86_64 phantomjs
```

### chrome  
```commandline
wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm  
yum localinstall google-chrome-stable_current_x86_64.rpm  
```

### chromedirver  
linux:  
```commandline
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip  
unzip chromedriver_linux64.zip  
mv chromedriver /application/search/anaconda3/bin/  
```
win:  
1 下载 https://chromedriver.storage.googleapis.com/index.html?path=2.38/  
2 解压   
3 将chromedrive.exe拷贝至python安装路径  

### 验证
```python  
from selenium import webdriver  
# d = webdriver.Chrome() 
d=webdriver.PhantomJS('/application/search/phantomjs/bin/phantomjs') 
d.get('https://www.baidu.com')  
print(d.title) 
d.find_element_by_xpath('//*[@id="u1"]/a[1]').click()
print(d.title) 
d.quit()
```