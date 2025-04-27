# odoo 14 教學 - 透過 controller 建立簡單 api

* [Youtube Tutorial - 透過 controller 建立簡單 api](https://youtu.be/q8ec5m4hyEo)

除了之前教大家 [如何使用 python xmlrpc 連接 odoo-14](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/xml-rpc-odoo#%E5%A6%82%E4%BD%95%E4%BD%BF%E7%94%A8-python-xmlrpc-%E9%80%A3%E6%8E%A5-odoo-14) 之外,

也可以透過 controller 建立簡單 api :smile:

這篇文章會教大家如何透過 controller 建立簡單 api,

你可能會問我說是不是 RESTful API, 答：不是 :smirk:

在 odoo 中如果要建立 RESTful API,

要透過第三方 addons, 可參考 [https://github.com/OCA/rest-framework](https://github.com/OCA/rest-framework)

這部份我以後來研究看看 :smile:

但我個人覺得如果真的要建立 RESTful API,

可能使用我以前介紹的 [Django-REST-framework 基本教學 - 從無到有 DRF-Beginners-Guide](https://github.com/twtrubiks/django-rest-framework-tutorial)

會比較理想 :smile:

## 說明

練習這個範例時, 請留一個 db 就好 ( 因為如果同個網址底下有很多 db, 會抓不到 :sob: )

主要看 [controllers/controllers.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/14.0/demo_controller_json/controllers/controllers.py) 即可,

先來看 `type='http'` 的範例,

```python
......
    @http.route('/get_res_users/type1', type='http', auth='none')
    def get_res_users_http(self):

        ......

        return json.dumps(data)
......
```

當 odoo 執行起來後, 測試 api 指令如下,

```python
import requests
r = requests.get('http://0.0.0.0:8069/get_res_users/type1')
r.text
r.json()
```

![alt tag](https://i.imgur.com/yYo4Lyr.png)

再來看 `type='json'` 的範例,

```python
......
    @http.route('/get_res_users/type2', type='json', auth='none')
    def get_res_users_json(self):
        ......
        return json.dumps(data)
......
```

這邊要注意 :exclamation: 如果使用 `type='json'`,

就只能使用 `jsonrpc` 呼叫, 不能使用前面教的方法呼叫,

當 odoo 執行起來後, 測試 api 指令如下,

```cmd
curl -X POST -H "Content-Type: application/json" -d "{}" http://0.0.0.0:8069/get_res_users/type2
```

參數說明

`-H` `--header`

`-d` `--data` HTTP POST data

`-X` `--request` 使用指定的 request

![alt tag](https://i.imgur.com/wlxJr2i.png)

