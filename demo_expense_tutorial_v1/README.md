# odoo 17 教學

更新到 odoo17

官方也有整理改動的內容 [Migration-to-version-17.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-17.0)

我也蠻推薦官方的影片介紹 [What changed in the ORM for Odoo 17](https://www.youtube.com/live/Fmr4JBzlDyY)

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

## odoo17 any domain

建議可以打開 `log_level = debug_sql` 觀看 SQL 變化.

目的是合併 subqueries.

odoo16 中

```python
obj = self.env['demo.expense.tutorial']

domain_1 = ['|', ('employee_id.name', 'like', 'Administrator'),
                 ('employee_id.mobile_phone', 'like', '000000000')]
obj.search(domain_1)
```

對應的 SQL 如下

```sql
SELECT "demo_expense_tutorial".id
FROM "demo_expense_tutorial"
WHERE (("demo_expense_tutorial"."active" = TRUE)
       AND (("demo_expense_tutorial"."employee_id" in
               (SELECT "hr_employee".id
                FROM "hr_employee"
                WHERE ("hr_employee"."name"::text like '%Administrator%')))
            OR ("demo_expense_tutorial"."employee_id" in
                  (SELECT "hr_employee".id
                   FROM "hr_employee"
                   WHERE ("hr_employee"."mobile_phone"::text like '%000000000%')))))
ORDER BY "demo_expense_tutorial"."sequence",
         "demo_expense_tutorial"."id" DESC
```

odoo17, 多了新的 `any` domain, 但你也可以使用舊的寫法, 因為自動幫你優化了,

以下三種寫法, 都是想同的結果, 相同的 SQL

```python
obj = self.env['demo.expense.tutorial']

domain_1 = ['|', ('employee_id.name', 'like', 'Administrator'),
                 ('employee_id.mobile_phone', 'like', '000000000')]
obj.search(domain_1)

domain_2 = ['|', ('employee_id', 'any', [('name', 'like', 'Administrator')]),
                 ('employee_id', 'any', [('mobile_phone', 'like', '000000000')])]
obj.search(domain_2)

domain_3 = [('employee_id', 'any', ['|', ('name', 'like', 'Administrator'),
                                         ('mobile_phone', 'like', '000000000')])]
obj.search(domain_3)
```

不管是 domain_1 or domain_2 or domain_3, 最終的 SQL 都是下方

```sql
SELECT "demo_expense_tutorial"."id"
FROM "demo_expense_tutorial"
WHERE (("demo_expense_tutorial"."active" = TRUE)
       AND ("demo_expense_tutorial"."employee_id" IN
              (SELECT "hr_employee"."id"
               FROM "hr_employee"
               WHERE (("hr_employee"."name"::text LIKE '%Administrator%')
                      OR ("hr_employee"."mobile_phone"::text LIKE '%000000000%')))))
ORDER BY "demo_expense_tutorial"."sequence" ,
         "demo_expense_tutorial"."id" DESC demo.expense.tutorial(2, 1)
```

你可以發現, subquery 只有一個.

簡單說, 就是把在 odoo16 中的 Multiple subqueries(slow) 優化為 Merge subqueries(fast).

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

<!-- user_id 會顯示, 但是內容會是空的, 注意, 只在 tree 上會有這種行為 -->
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

## odoo17 deprecate active_*

active_id, active_ids or active_model 這些未來都不能使用,

odoo17 中會建議你改, 但不強制, 預計 odoo18 會完全棄用.

詳細可參考 [views: deprecate active_* keys from evalContext](https://github.com/odoo/odoo/commit/daf05d48ac76d500aa1285184bdddc4c67641d58)

## odoo17 deprecate name_get

odoo17 放棄 `name_get`, 改為使用 `_compute_display_name`,

範例如下,

odoo16

```python
@api.multi
def name_get(self):
    names = []
    for record in self:
        name = '%s-%s' % (record.create_date.date(), record.name)
        names.append((record.id, name))
    return names
```

odoo17 寫法

```python
@api.depends('name')
def _compute_display_name(self):
    for record in self:
        record.display_name = f'{record.create_date.date()}-{record.name}'

```

如果不太了解這個可參考之前的 [odoo 手把手教學 - 說明 name_get 和 _name_search](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_expense_tutorial_v1#odoo-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---%E8%AA%AA%E6%98%8E-name_get-%E5%92%8C-_name_search---part7)
