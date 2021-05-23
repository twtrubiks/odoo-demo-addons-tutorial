# odoo 觀念 - multi company

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - multi company - part1](https://youtu.be/u8u0eRzY8kg)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 multi company 的一小部份:smile:

因為 multi company 的方法有很多種.

## 說明

首先, odoo 在 Multi-company 的設計上是有很多想法以及方法的,

可參考官方文件 [Multi-company Guidelines](https://www.odoo.com/documentation/14.0/developer/howtos/company.html) 觀看.

(補充一下, 從 odoo13 開始, Multi-company 的概念有改動, 但不影響本篇的教學:relaxed:)

今天主要是要介紹 fields 中的一個參數 `company_dependent=True`,

這個參數主要是為了 Multi-company 設計的.

寫法很簡單, 就是在 model 中加入參數即可

[models/model.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/master/demo_multi_company/models/model.py)

```python
......

class DemoCompany(models.Model):
    _name = 'demo.company'
    _description = 'Demo Company'

    name = fields.Char('Description', required=True)

    property_account_receivable_id = fields.Many2one('account.account',
        company_dependent=True,
        string="Account Receivable",
        domain="[('internal_type', '=', 'receivable'), ('deprecated', '=', False)]",
        required=True)

    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True, default=lambda self: self.env.user.company_id)
......
```

主要就是 `property_account_receivable_id` 中的 `company_dependent=True`.

在 view 的介面底下是可以看到這個欄位

![alt tag](https://i.imgur.com/fRZ4ioI.png)

如果你有多公司, 切換到其他的公司, 你會發現這個欄位有可能會變空的.

(切換公司時, 內容也會不一樣, 注意這邊是相同的 record)

![alt tag](https://i.imgur.com/HCFwDd3.png)

但你在 db 中的 `demo_company` 不會有 `property_account_receivable_id` 的欄位

![alt tag](https://i.imgur.com/fz0aK8h.png)

這邊你可能會覺得很奇怪, 但這就是他特別的地方:smile:

那他會存在哪裡呢:question:

他會存在 `ir_property` 中

![alt tag](https://i.imgur.com/I9T8uVx.png)

在後台的部份, 也可以看到 `ir_property` 的東西

路徑在 `Technical -> Parameters -> Company Properties`

![alt tag](https://i.imgur.com/Xf55Oip.png)

裡面的值, 紀錄著 model 和 id

![alt tag](https://i.imgur.com/k3VIApY.png)

然後請把 Resource(res_id) 手動清空,

![alt tag](https://i.imgur.com/AZir7v0.png)

等下要示範使用以下的 code 來取值

```python
self.env['ir.property'].with_context(force_company=self.company_id.id).get('property_account_receivable_id', 'demo.company')
```

要清空的原因是因為其他的 Company Properties 很多是使用 code 的方式產生的

原始碼中的 `odoo/addons/account/models/chart_template.py`

```python
@api.multi
def generate_properties(self, acc_template_ref, company):
    ......
    PropertyObj = self.env['ir.property']
    todo_list = [
        ('property_account_receivable_id', 'res.partner', 'account.account'),
        ('property_account_payable_id', 'res.partner', 'account.account'),
        ('property_account_expense_categ_id', 'product.category', 'account.account'),
        ('property_account_income_categ_id', 'product.category', 'account.account'),
        ('property_account_expense_id', 'product.template', 'account.account'),
        ('property_account_income_id', 'product.template', 'account.account'),
    ]
```

`property_account_receivable_id` `property_account_payable_id` ... 都是 code 產生的.

(這些透過 code 產生的值 res_id 都是 False)

而 Resource(res_id) 清空的原因則是因為原始碼中的 `odoo/addons/base/models/ir_property.py`

```python
......

def _get_property(self, name, model, res_id):
    domain = self._get_domain(name, model)
    if domain is not None:
        domain = [('res_id', '=', res_id)] + domain
        #make the search with company_id asc to make sure that properties specific to a company are given first
        return self.search(domain, limit=1, order='company_id')
    return self.browse(())

......
```

通常 domain 這邊的 res_id 會是 False. (如果有值就會被過濾掉)

```python
class DemoCompany(models.Model):
    _name = 'demo.company'
    _description = 'Demo Company'

    ......

    def action_get_default_account(self):
        default_account = self.env['ir.property'].with_context(force_company=self.company_id.id).get('property_account_receivable_id', 'demo.company')
        _logger.warning(default_account)
        _logger.warning(self.property_account_receivable_id)
        _logger.warning('============= HELLO ==================')

```

點選這個按鈕可以觸發這個 function

![alt tag](https://i.imgur.com/X5xPuZ5.png)

你會發現輸出一樣的資訊

一個是透過 company_id 找出當下對應的 model 中的 `property_account_receivable_id`,

另一個則是直接呼叫 model 中的 `property_account_receivable_id`.

![alt tag](https://i.imgur.com/k5KTLXH.png)

當你嘗試著新增 record, 你會發現 `property_account_receivable_id` 預設都會有值

(這也是為甚麼我和大家說要清空 res_id 的原因, 因為 odoo 的 code 中是這樣設定的, 前面有說明)

![alt tag](https://i.imgur.com/e4vLm0A.png)
