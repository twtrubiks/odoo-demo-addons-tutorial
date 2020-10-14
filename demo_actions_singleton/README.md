# odoo 觀念 - actions 和 singleton

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - actions and singleton](https://youtu.be/rRD9j4IAHWY)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇主要介紹 actions and singleton

以下將介紹這個 addons 的結構

## 說明

[data/action_data.xml](data/action_data.xml)

首先, 先來建立一個 action

```xml
......
<odoo>
    <data>
        <record id="action_action_demo" model="ir.actions.server">
            <field name="name">Action Demo</field>
            <field name="model_id" ref="model_demo_actions_singleton"/>
            <field name="binding_model_id" ref="demo_actions_singleton.model_demo_actions_singleton"/>
            <field name="state">code</field>
            <field name="code">
                records.action_demo()
            </field>
        </record>
    </data>
</odoo>
```

`model_id` `binding_model_id` 綁定 model.

`state` 選擇使用的方式, 這邊使用 python code.

`code` 執行的程式碼, `records` 代表所選的 record, `action_demo()` 代表呼叫的 function.

記得也要將它加入 `__manifest__.py`.

先來看 [models/models.py](models/models.py)

```python
......

class DemoActionsSingleton(models.Model):
    _name = 'demo.actions.singleton'
    _description = 'Demo Actions Singleton'

    name = fields.Char('Description', required=True)

    @api.multi
    def action_demo(self):
        self.ensure_one()
        _logger.warning('=== CALL action_demo ===')
```

`action_demo` 裡面就只是單純的 print.

至於要在 odoo 中的那邊呼叫 Action Demo, 請看下圖,

在 record 中的 action

![alt tag](https://i.imgur.com/cf6NeMr.png)

當你點下去, 會觸發你的 logger

![alt tag](https://i.imgur.com/wbkWbDV.png)

接下來說說 `self.ensure_one()`, 這就是確認是否為 `singleton`,

假如跳出 `raise ValueError exception`, 代表它非為 singleton

舉個例子, 像這邊選 兩條 record, 點下 Action Demo,

![alt tag](https://i.imgur.com/HMV3CHS.png)

你會發現跳出 error

![alt tag](https://i.imgur.com/tpti9Lb.png)

原因就是在這邊我們使用了 `self.ensure_one()` 確認 (確保只使用一條 record),

所以選兩條 reocrd 就會錯誤:exclamation::exclamation:

所以結論就是 `self.ensure_one()` 是要讓你檢查是否為 `singleton`.

另外, 空的 recordset 行為也像是 singleton, 當你 accessing fields 時,

它不會回傳 error ( 而是會回傳 `False`),

也因為這個特性, 所以我們才可以使用 `.` 歷遍 (traverse) records 而不用擔心錯誤:smile:

(舉例, 下面的例子)

```python
>>> self.company_id.parent_id
res.company()
>>> self.company_id.parent_id.name
False
```

並不會發生錯誤, 只會回傳 `False`.