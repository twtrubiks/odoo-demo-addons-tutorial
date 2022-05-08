# odoo 15 教學 - 透過 controller http 建立簡易 REST API

* [Youtube Tutorial - 透過 controller http 建立簡易 REST API](https://youtu.be/pyy1AQh_Tlo)

之前在 [odoo 14 教學 - 透過 controller 建立簡單 api](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_controller_json) 這篇文章中,

有教大家簡單的透過 controller 建立 api,

今天要更進一步, 加上 `auth=users` 以及透過 `http` 打造類似 REST API 的範例.

## 說明

首先把 addons 裝起來,

[demo_controller_api_http/controllers/api.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/15.0/demo_controller_api/demo_controller_api_http/controllers/api.py)

```python
from odoo import http, _
from odoo.http import request
import json

class DemoApiControllerHttp(http.Controller):
    def get_res_users(self, pk=None):
        if pk:
            domain = [("id", "=", pk)]
        else:
            domain = []

        return [
            {
                "id": record.id,
                "name": record.name,
                "company": record.company_id.name,
                "phone": record.phone,
                "email": record.email,
            }
            for record in request.env["res.users"].sudo().search(domain)
        ]

    @http.route("/api/users/<string:pk>", methods=["GET"], type="http", auth="user", csrf=False)
    def api_get_res_users(self, pk=None):
        return json.dumps(self.get_res_users(pk))

    @http.route("/api/users/", methods=["GET"], type="http", auth="user", csrf=False)
    def api_get_res_user(self):
        return json.dumps(self.get_res_users())

    @http.route("/api/users/", methods=["POST"], type="http", auth="user", csrf=False)
    def api_post_res_user(self):
        param = request.params

        if not param["login"]:
            return json.dumps("login not allow empty")

        vals = {
            "name": param["name"],
            "phone": param["phone"],
            "email": param["email"],
            "login": param["login"],
        }
        if request.env["res.users"].sudo().search([("login", "=", param["login"])]):
            return json.dumps("user already exists")

        res_user = request.env["res.users"].sudo().create(vals)
        return json.dumps(self.get_res_users(res_user.id))

    @http.route("/api/users/<string:pk>", methods=["PATCH"], type="http", auth="user", csrf=False)
    def api_patch_res_user(self, pk=None):
        param = request.params
        res_user = request.env["res.users"].sudo().search([("id", "=", pk)])
        if not res_user:
            return json.dumps("user not exists")

        res_user.phone = param["phone"]
        return json.dumps(self.get_res_users(pk))

```

這邊和 [demo_controller_api_jsonrpc](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/15.0/demo_controller_api/demo_controller_api_jsonrpc) 比較不同的地方有幾個,

首先是改成了 `type="http"`, 然後加上了 `csrf=False`, 因為 odoo 定義

```text
* if the form is accessed by an external third party (e.g. REST API
  endpoint, payment gateway callback) you will need to disable CSRF
  protection (and implement your own protection if necessary) by
  passing the `csrf=False` parameter to the `route` decorator.
```

這邊主要建立了幾個 api, 分別是

`GET` `/api/users/` 取得全部 `res_users`.

`GET` `/api/users/<string:pk>` 取得特定 `res_users`.

`POST` `/api/users/` 新增 `res_users`.

`PATCH` `/api/users/<string:pk>` 修改特定 `res_users` 資料.

## client 端

[client.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/15.0/demo_controller_api/demo_controller_api_http/client.py) 端的部份就是直接執行

```cmd
python3 client.py
```

執行畫面, 這邊用 `get_users()` 示範,

![alt tag](https://i.imgur.com/At4wBFy.png)

```python
import requests
import json

HOST = "http://0.0.0.0:8069"
AUTH_URL = "{}/web/session/authenticate/".format(HOST)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

session_data = {
    "jsonrpc": "2.0",
    "params": {
        "login": "admin",
        "password": "admin",
        "db": "odoo",
    },
}


def get_session_id():
    res = requests.post(AUTH_URL, data=json.dumps(session_data), headers=headers)
    return res.cookies["session_id"]


def get_users():
    base_url = "{}/api/users/".format(HOST)

    res = requests.get(
        base_url,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def get_user():
    base_url = "{}/api/users/3/".format(HOST)

    res = requests.get(
        base_url,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def add_user():
    base_url = "{}/api/users/".format(HOST)
    param = {
        "login": "test_user",
        "name": "test_user",
        "phone": "00000",
        "email": "xxx@test.com",
    }

    res = requests.post(
        base_url,
        data=param,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


def edit_user():
    base_url = "{}/api/users/3/".format(HOST)
    param = {
        "phone": "0000000000",
    }

    res = requests.patch(
        base_url,
        data=param,
        cookies={"session_id": get_session_id()},
    )

    print(res.json())


if __name__ == "__main__":
    get_users()
    # get_user()
    # add_user()
    # edit_user()
```

odoo 整個流程是要先取得 `session_id`(對 `/web/session/authenticate/` 發送請求),

( 請輸入正確的 db, login, password, host )

`/web/session/authenticate/` 還是需要使用 `jsonrpc` 的方式呼叫,

原因是 `addons/web/controllers/main.py` 底下的定義就是 `type='json'`,

```python
class Session(http.Controller):

    ......

    @http.route('/web/session/authenticate', type='json', auth="none")
    def authenticate(self, db, login, password, base_location=None):
        request.session.authenticate(db, login, password)
        return request.env['ir.http'].session_info()

```

再去發送對應的 api ( 這邊都是使用 `http` 的方式 ).