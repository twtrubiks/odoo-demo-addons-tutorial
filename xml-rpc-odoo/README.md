# 如何使用 python xmlrpc 連接 odoo-12

此版本為 odoo12, odoo14 版本請參考 [odoo14](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/xml-rpc-odoo) 分支.

建議觀看影片, 會更清楚 :smile:

* [Youtube Tutorial - 如何使用 python xmlrpc 連接 odoo - part1](https://youtu.be/MuMBF8a9ko8)

* [Youtube Tutorial - 如何使用 python xmlrpc 連接 odoo - part2](https://youtu.be/KFBaTB_XRJM)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[demo_odoo_tutorial](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) -  odoo 手把手建立第一個 addons

主要介紹 xmlrpc

## 說明

External API 官方文件

[https://www.odoo.com/documentation/12.0/webservices/odoo.html](https://www.odoo.com/documentation/12.0/webservices/odoo.html)

`xmlrpc/2/common`

provides meta-calls which don’t require authentication.

`xmlrpc/2/object`

is used to call methods of odoo models via the execute_kw RPC function.

程式碼請參考 [demo.py](demo.py), 每個 function 都能執行,

(記得要先啟動一個 odoo 並填上 url, name, password, 也要選擇載入 demo data 哦)

此外, 裡面用到很多的 m2x 的 add, edit, update, delete 語法, 請參考下方

```xml
(0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
(1, ID, { values })    update the linked record with id = ID (write *values* on it)
(2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
(3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
(4, ID)                link to existing record with id = ID (adds a relationship)
(5)                    unlink all (like using (3,ID) for all linked records)
(6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
```

## 自定義 function

有時候使用標準的 xml rpc 的 `read_search` 不是那麼方便, 像是我要拿 Many2one 的東西,

就必須透過 id 再 access 一次, 蠻麻煩的, 所以還可以自己定義 function 以及 回傳格式.

在 odoo 端要這樣寫, 記得要加上 `@api.model`,

```python
class HrExpenseCustom(models.Model):
    _inherit = "hr.expense"

    @api.model
    def custom_func(self, expense_sheet_id):
        sheet = self.env['hr.expense.sheet'].browse(expense_sheet_id)
        return {
            'name': sheet.name,
            'line_ids': [{
                'id': rec.id,
                'name': rec.name,
            } for rec in sheet.expense_line_ids]
        }
```

透過 xml rpc 呼叫的方式如下,

```python
......

data = models.execute_kw(db, uid, password,
    'hr.expense', 'custom_func', [], {'expense_sheet_id': 5})

# print(data)
# {'name': 'Screen', 'line_ids': [{'id': 3, 'name': 'Travel by car'}, {'id': 1, 'name': 'Screen'}]}
```

這樣整體方便不少, 開發也比較快速.

## 遇到 None 值

在使用 xmlrpc 的時候, 如果你會傳 null 值, 可能會出現以下的錯誤

```text
cannot marshal None unless allow_none is enabled
```

要修正這個錯誤也很簡單, 加上 `allow_none=True`

```python
common = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

# 如果值傳 None 會出現以上錯誤, 要記得加上 allow_none=True
models = xmlrpc.client.ServerProxy(f'{odoo_url}/xmlrpc/2/object', allow_none=True)
```

## 其他第三方工具

多數都是從 xmlrpc 衍生出來的

[https://github.com/OCA/odoorpc](https://github.com/OCA/odoorpc)

[https://github.com/tinyerp/erppeek](https://github.com/tinyerp/erppeek)