# odoo 16 觀念 - TransientModel - Wizard

建議在閱讀這篇文章之前, 請先確保了解看過 odoo 12 的教學,

[odoo 觀念 - TransientModel - Wizard](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial_wizard)

因為本篇只會說明差異的部份,

## 說明

- get_view

odoo16 移除 `fields_view_get`

```python
'Method `fields_view_get` is deprecated, use `get_view` instead',
```

odoo16 使用 `get_view`

```python
def get_view(self, view_id=None, view_type='form', **options):
    pass
```

- clean_context

詳細哪個版本才有就不管了, 可以透過它快速取出 self.env.context 的內容, 但是會 pass 掉 "default_" 開頭的.

```python
from odoo.tools.misc import clean_context
context = clean_context(self.env.context) # pass "default_"
```

- depends_context

[官網文件可參考 depends_context](https://www.odoo.com/documentation/16.0/zh_TW/developer/reference/backend/orm.html#odoo.api.depends_context)

```text
We use the '@api.depends_context' decorator for non-stored 'compute' methods to indicate the context dependencies for these methods.
```

簡單說可以透過這個 decorator 去偵測 context 裡面的內容去做 compute 運算.

```python
......

uid = fields.Char(compute='_compute_uid')

@api.depends_context('uid')
def _compute_uid(self):
    context = clean_context(self.env.context)
    for rec in self:
        rec.uid = context.get('uid')
```