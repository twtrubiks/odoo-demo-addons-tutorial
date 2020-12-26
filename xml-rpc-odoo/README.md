# 如何使用 python xmlrpc 連接 odoo-14

此版本為 odoo14, odoo12 版本請參考 [master](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/xml-rpc-odoo) 分支.

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo14 Developer API Keys 教學 - python xmlrpc](https://youtu.be/__RcLpcRF2g)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為這篇只會說明 odoo 14 不同的地方 )

[xml-rpc-odoo](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/xml-rpc-odoo) -  如何使用 python xmlrpc 連接 odoo-12

## 說明

External API 官方文件

[https://www.odoo.com/documentation/14.0/webservices/odoo.html](https://www.odoo.com/documentation/14.0/webservices/odoo.html)

odoo14 多了 Developer API Keys, 這個 keys 產生的流程如下,

請記得打開 Activate the developer mode

如果不知道如何打開, 請參考 [odoo12 如何開啟 odoo developer mode](https://github.com/twtrubiks/odoo-docker-tutorial#odoo12-%E5%A6%82%E4%BD%95%E9%96%8B%E5%95%9F-odoo-developer-mode)

點選右上方的 My Profile

![alt tag](https://i.imgur.com/dL9jGtU.png)

找到 Developer API Keys

![alt tag](https://i.imgur.com/Yz2w8SC.png)

他會要你輸入目前的密碼以及 API Keys 的名稱(可以任意定義)

![alt tag](https://i.imgur.com/AHuh60H.png)

這串就是你的 Developer API Keys

![alt tag](https://i.imgur.com/8PQlxkv.png)

使用方法很簡單,

只需要將連接 xmlrpc 的 password 改掉就可以了( 改成這組 API Key )

```python
url = 'http://0.0.0.0:8069'
db = 'odoo'
username = 'admin'
password = 'admin' # change API Key
```

注意, 這組 API Keys 只能使用在 xmlrpc 裡面,

當你正常從 odoo 登入, 這組密碼是無法使用的.

因為他是 **Developer** API Keys.
