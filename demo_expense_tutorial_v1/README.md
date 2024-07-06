# odoo 17 教學

更新到 odoo17

* [TODO - 文章快速連結]()

官方也有整理改動的內容 [Migration-to-version-17.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-17.0)

我這邊是自己再整理, 然後寫一些範例.

## odoo17 "attrs" and "states"

在升級 odoo17 的時候, 你可能會場看到這個錯誤訊息

```text
Since 17.0, the "attrs" and "states" attributes are no longer used.
```

在 odoo17 中, 語法改了, 改成更像 python.

odoo16 寫法如下,

```xml
<label string="Default Income Account" attrs="{'invisible': [('type', '!=', 'sale')]}"/>

<field name="email" attrs="{'readonly': [('parent.partner_readonly', '=', True)]}"/>
```

odoo17 必須這樣寫, 寫法變成如下

```xml
<label string="Default Income Account" invisible="type != 'sale'"/>

<field name="email" readonly="parent.partner_readonly"/>
```

## odoo17 any 的用法

等待新增 any, 以及對應 sql

## odoo17 _name_search api

`_name_search` 多了 order

odoo16

```python
@api.model
def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    args = args or []
    if name:
        args = args + ['|', ('id', operator, name), ('name', operator, name)]
    return self._search(args, limit=limit, access_rights_uid=name_get_uid)
```

odoo17 改寫成如下

```python
@api.model
def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
    domain = domain or []
    if name:
        domain = domain + ['|', ('id', operator, name), ('name', operator, name)]
    return self._search(domain, limit=limit, order=order)
```

## odoo17 tree invisible

可參考 [View architectures](https://www.odoo.com/documentation/17.0/developer/reference/user_interface/view_architectures.html)

在 odoo17 中的 tree 的 invisible 有一些改變

```xml
<field name="user_id"/>

<!-- user_id 會顯示, 但是內容會是空的 -->
<field name="user_id" invisible="1"/>

<!-- 隱藏 user_id-->
<field name="user_id" column_invisible="True"/>

<!-- 也可以更據其他條件是決定 -->
<field name="user_id" column_invisible="has_late_products == False"/>
```

## odoo17 hook change

原本是 `cr` 和 `registry`, 現在改成了 `env`

```python

# odoo16
def post_init_hook(cr, registry):
    pass

# odoo17
def post_init_hook(env):
    pass
```

## 其他

odoo16 移除 `fields_view_get`

```python
'Method `fields_view_get` is deprecated, use `get_view` instead',
```

新的 `get_view`

```python
def get_view(self, view_id=None, view_type='form', **options):
    pass
```
