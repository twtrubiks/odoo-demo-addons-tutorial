# Odoo 19 JSON-2 API 完整使用指南

* [Youtube Tutorial - Odoo 19 JSON-2 API 完整教學！告別 XML-RPC 迎接新世代](https://youtu.be/edWMCN6z6nw)

也推薦看官方的相關影片

* [Odoo API 101: discover the new blazing fast api](https://www.youtube.com/watch?v=CgKvr_OUGTY&list=PL1-aSABtP6ADR0TO3dNYuSBbuRJPHcF_l&index=101) 2:33:30 ~ 2:58:34

這邊主要講了 JSON-2 API

## 簡介

### 什麼是 JSON-2 API？

JSON-2 API 是 Odoo 19 引入的新一代 JSON-based RPC API，

用於取代即將在 Odoo 20 中移除的 XML-RPC 和 JSON-RPC API。

### 主要特點

1. **RPC 風格設計**：所有操作統一使用 POST 方法
2. **Bearer Token 認證**：使用 API Key 進行安全認證
3. **簡化的 URL 結構**：`/json/2/<model>/<method>`
4. **更好的錯誤處理**：結構化的錯誤回應
5. **原生 JSON 支援**：不需要額外的包裝層

### 新舊 API 對比

| 特性 | XML-RPC/JSON-RPC (舊) | JSON-2 API (新) |
|-----|---------------------|----------------|
| API 風格 | RPC (Remote Procedure Call) | RPC (Remote Procedure Call) |
| URL 格式 | `/xmlrpc/2/object` | `/json/2/<model>/<method>` |
| HTTP 方法 | POST | POST (所有操作) |
| 認證方式 | 用戶名/密碼 以及 API Key | Bearer Token (API Key) (不提供 用戶名/密碼) |
| 請求格式 | XML/JSON-RPC 包裝 | 純 JSON |
| 錯誤處理 | 非標準格式 | 標準 HTTP 狀態碼 + JSON |
| 效能 | 一樣 | 一樣 |
| 棄用狀態 | Odoo 19 棄用，Odoo 20 移除 | 推薦使用 |

效能的部份, 基本上沒有改變, 主要影響的部份是你 odoo 那端怎麼寫的.

HTTP 狀態碼的部份, XML-RPC 不管你是錯誤還是成功都會回傳 200, 這會導致很難判斷狀態,

在新的 JSON-2 API 中,

有更好的 HTTP 狀態碼, 例如 4xx, 這類的狀態碼會優先 200, 可以更好的判斷目前的狀態.

XML-RPC 之前我介紹過了, 可參考 [Youtube Tutorial - odoo14 Developer API Keys 教學 - python xmlrpc](https://youtu.be/__RcLpcRF2g)

## API Key 設置

在 Odoo 中生成 API Key

## 從舊 API 遷移

### XML-RPC 到 JSON-2 對照表

| 操作 | XML-RPC (舊) | JSON-2 (新) |
|-----|------------|-----------|
| 認證 | `common.authenticate()` | Bearer Token in header |
| 搜尋 | `models.execute_kw(db, uid, password, model, 'search', [[domain]])` | `POST /json/2/{model}/search` |
| 讀取 | `models.execute_kw(db, uid, password, model, 'read', [ids])` | `POST /json/2/{model}/read` |
| 創建 | `models.execute_kw(db, uid, password, model, 'create', [values])` | `POST /json/2/{model}/create` |
| 更新 | `models.execute_kw(db, uid, password, model, 'write', [[ids], values])` | `POST /json/2/{model}/write` |
| 刪除 | `models.execute_kw(db, uid, password, model, 'unlink', [[ids]])` | `POST /json/2/{model}/unlink` |

### 遷移前：XML-RPC 程式碼

```python
# 舊的 XML-RPC 程式碼
import xmlrpc.client

url = 'http://localhost:8069'
db = 'mydb'
username = 'admin'
password = 'admin'

# 認證
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# 操作
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

# 搜尋
partner_ids = models.execute_kw(db, uid, password,
    'res.partner', 'search',
    [[['is_company', '=', True]]])

# 讀取
partners = models.execute_kw(db, uid, password,
    'res.partner', 'read',
    [partner_ids, ['name', 'email']])

# 創建
new_id = models.execute_kw(db, uid, password,
    'res.partner', 'create',
    [{'name': 'New Partner'}])

# 更新
models.execute_kw(db, uid, password,
    'res.partner', 'write',
    [[new_id], {'phone': '123456'}])

# 刪除
models.execute_kw(db, uid, password,
    'res.partner', 'unlink',
    [[new_id]])
```

### 遷移後：JSON-2 程式碼

```python
# 新的 JSON-2 程式碼
import requests

url = 'http://localhost:8069'
api_key = 'your_api_key_here'

# 設置 headers（取代認證步驟）
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# 搜尋
response = requests.post(
    f'{url}/json/2/res.partner/search',
    headers=headers,
    json={'domain': [['is_company', '=', True]]}
)
partner_ids = response.json()

# 讀取
response = requests.post(
    f'{url}/json/2/res.partner/read',
    headers=headers,
    json={'ids': partner_ids, 'fields': ['name', 'email']}
)
partners = response.json()

# 創建
response = requests.post(
    f'{url}/json/2/res.partner/create',
    headers=headers,
    json={'values': {'name': 'New Partner'}}
)
new_id = response.json()

# 更新
response = requests.post(
    f'{url}/json/2/res.partner/write',
    headers=headers,
    json={'ids': [new_id], 'values': {'phone': '123456'}}
)

# 刪除
response = requests.post(
    f'{url}/json/2/res.partner/unlink',
    headers=headers,
    json={'ids': [new_id]}
)
```

## api doc 頁面

`http://127.0.0.1:8069/doc`

現在打開你的 odoo, 結尾加上 `/doc`, 你會看到類似的界面,

填入你的 api key, 就可以測試你想要的 api, 幫助開發者更容易的串接

![alt text](https://cdn.imgpile.com/f/XpHbZFK_xl.png)

也可以看到 method

![alt text](https://cdn.imgpile.com/f/xn2tKfF_xl.png)

如果你不想要讓人看到這個 doc,

可以把 user 的權限關掉 Technical Documentation `api_doc.group_allow_doc`,

或是更暴力, 直接註解掉相關的 Controller,

```python
......

class DocController(http.Controller):
    """
    A single page application that provides an OpenAPI-like interface
    feeded by a reflection of the registry (fields and methods) in JSON
    documents.
    """

    @http.route(['/doc', '/doc/<model_name>', '/doc/index.html'], type='http', auth='user')
    def doc_client(self, mod=None, **kwargs):
        if not self.env.user.has_group('api_doc.group_allow_doc'):
            raise AccessError(self.env._(
                "This page is only accessible to %s users.",
                self.env.ref('api_doc.group_allow_doc').sudo().name))
        res = request.render('api_doc.docclient')
        res.headers['X-Frame-Options'] = 'deny'
        return res

......
```

## 總結

JSON-2 API 是 Odoo 19 的重要更新，

建議所有使用外部 API 的開發者儘快開始遷移到 JSON-2 API，為 Odoo 20 的升級做好準備。

## 範例

範例可參考 [json2_client_demo.py](json2_client_demo.py)

依照你想要測試的

```python
......
    # 執行測試
    if test_connection(client):
        test_crud_operations(client)
        # test_model_methods(client)  # 測試呼叫模型方法
        # test_many2many_operations(client)  # 測試 M2M 欄位操作
        # test_error_handling(client)
    else:
        _logger.error("\n❌ 連線失敗，請檢查配置")
        sys.exit(1)
......
```

## odoo-client-lib 2.0.0

也可以透過 [odoo-client-lib](https://pypi.org/project/odoo-client-lib/2.0.0/) 呼叫 odoo,

```cmd
pip install odoo-client-lib==2.0.0
```

讓你少寫一點 code,

範例可參考 [json2_client_odoolib_demo.py](json2_client_odoolib_demo.py)

## 參考資源

- [Odoo 19 官方文檔](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html)
- [API 遷移指南](https://www.odoo.com/documentation/19.0/developer/reference/external_api.html#migrating-from-xml-rpc-json-rpc)

---
