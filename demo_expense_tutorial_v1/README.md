# odoo 17 教學

更新到 odoo17

官方也有整理改動的內容 [Migration-to-version-17.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-17.0)

我也蠻推薦官方的影片介紹 [What changed in the ORM for Odoo 17](https://www.youtube.com/live/Fmr4JBzlDyY)

我這邊是自己再整理, 然後寫一些範例.

# 目錄

- [odoo17 "attrs" and "states"](#odoo17-attrs-and-states)

- [odoo17 any domain](#odoo17-any-domain)

- [odoo17 _name_search api](#odoo17-_name_search-api)

- [odoo17 tree invisible](#odoo17-tree-invisible)

- [odoo17 hook change](#odoo17-hook-change)

- [odoo17 deprecate active_*](#odoo17-deprecate-active_)

- [odoo17 deprecate name_get](#odoo17-deprecate-name_get)

- [odoo17 Access Rights](#odoo17-access-rights)

- [odoo17 onchange](#odoo17-onchange)

- [odoo17 compute](#odoo17-compute)

- [odoo17 constrains](#odoo17-constrains)

- [odoo17 batch create](#odoo17-batch-create)

- [Youtube Tutorial - odoo 17 手把手教學 - obfuscate 混淆](https://youtu.be/AJksUa9GLP4) - [文章快速連結 - odoo17 obfuscate](#odoo17-obfuscate)

- [odoo17 report render data](#odoo17-report-render-data)

- [odoo17 report page break](#odoo17-report-page-break)

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

如果你不想自己轉換, 可以考慮使用 OCA 的 [views_migration_17](https://github.com/OCA/server-tools/tree/17.0/views_migration_17)

* [Youtube Tutorial - odoo 17 手把手教學 - Views migration](https://youtu.be/G_r0g_Rj9Xk)

使用方法如下, 不須要安裝 addons, 直接使用以下的指令

```cmd
python odoo-bin -d odoo17 -i demo_expense_tutorial_v1 --load=base,web,views_migration_17 --stop-after-init -c /config/odoo.conf
```

如果順利執行, 你會發現你指定的 demo_expense_tutorial_v1 addons 已經被成功轉換了.

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

## odoo17 Access Rights

odoo17 Access Rights 的 `ir.model.access.csv` 群組不能設定空值

(這個 feature deprecated 了),

如果你在 odoo17 底下使用以下寫法

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_demo_expense_sheet_manager,Demo Expense Sheet Manager Tutorial Access,model_demo_expense_sheet_tutorial,,1,1,1,1
```

會出現類似的 WARNING

```text
WARNING odoo odoo.addons.base.models.ir_model: Rule Demo Expense Sheet Manager Tutorial Access has no group, this is a deprecated feature. Every access-granting rule should specify a group.
```

請填上正確的 group, 或是補上 `base.group_user`

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_demo_expense_sheet_manager,Demo Expense Sheet Manager Tutorial Access,model_demo_expense_sheet_tutorial,demo_expense_tutorial_group_manager,1,1,1,1
```

## odoo17 onchange

這並不是 odoo17 的主要特色, 只是我的一些經驗整理,

直接看一個例子, 簡稱為 方法 A,

簡單說就是在 onchange 底下跳出 raise,

```python
@api.onchange('debug_field')
def _onchange_debug_field(self):
    for _ in self:
        raise UserError('error1')
        # or
        # raise ValidationError('error2')
```

另一種方法為方法 B,

```python
@api.onchange('debug_field')
def _onchange_debug_field(self):
    for _ in self:
        return {'warning': {
            'title': "title_1",
            'message': "message_1"
        }}

# 或是

@api.onchange('debug_field')
def _onchange_debug_field(self):
    for — in self:
        result = dict()
        result['warning'] = {
            'title': 'title_1',
            'message': 'message_1'
        }
        return result
```

在 odoo17 中, 請盡量用方法 B, 除非真的必要,

再用 方法 A ‼ (我查了 odoo17 的 code, 有極少部份的 code 也有始使用 方法 A)

(使用 方法 A 的時候, 也不要關聯太多的欄位, 不然你會發現你一直無法 save, 要整個網頁重新整理才會正常)

方法 A 和 方法 B 的差異是, 方法 A 會強制阻擋, 方法 B 只是一個 WARNING, 仍然可以 save.

建議大家可以自己嘗試看看 😀

## odoo17 compute

這並不是 odoo17 的主要特色, 只是我的一些經驗整理,

在 odoo17 中, compute 不要用 raise, 這會導致很奇怪的問題,

(我查了 odoo17 的 code, 找不到 compute 有 raise 的 case)

如果真的要使用, 請用 `constrains` (搭配 ValidationError) 代替.

順便說明一下 `compute_sudo` (這個不是 odoo17 的主要特色),

範例如下,

```python
authorized_transaction_ids = fields.Many2many(
        string="Authorized Transactions", comodel_name='payment.transaction',
        compute='_compute_authorized_transaction_ids', readonly=True, copy=False,
        compute_sudo=True)

used_in_bom_count = fields.Integer('# BoM Where Used',
        compute='_compute_used_in_bom_count', compute_sudo=False)

:param bool compute_sudo: whether the field should be recomputed as superuser
to bypass access rights (by default ``True`` for stored fields, ``False``
for non stored fields)
```

通常不用特別設定, 因為多數情況, 都是用 `True` 的情境, 也就是會 pass 掉 odoo 內的 access rights.

## odoo17 constrains

這並不是 odoo17 的主要特色, 只是我的一些經驗整理,

constrains 必須是 `compute=Ture`,  如果是 `compute=False` 會跳出以下 WARNING,

底下舉個錯誤的例子

```python
test_constrains_field = fields.Char('test_constrains_field', compute='_compute_test_constrains_field', store=False)

def _compute_test_constrains_field(self):
    for rec in self:
        rec.test_constrains_field = 'test'

@api.constrains('test_constrains_field')
def _constrains_test_constrains_field(self):
    pass
```

當你執行的時候, 會發現有以下的 WARNING

```text
WARNING odoo odoo.models: method demo.expense.tutorial._constrains_test_constrains_field: @constrains parameter 'test_constrains_field' is not writeable
```

如果要修正, 設定為 `store=True` 即可.

## odoo17 batch create

這特性不是 odoo17 才有的, 只是特別提一下, 在 odoo 中, 並沒有明確的 batch create,

但是, 我們可以透過一些寫法改善它, 像之前介紹的 [odoo 觀念 - odoo12 和 odoo14 的 ORM Write 差異](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/odoo_write_tutorial)

假如我們有一個 model 是 `demo.expense.tutorial`,

這種寫法會產生 N 個 insert SQL

```python
model = self.env['demo.expense.tutorial']

# 會有 n 次 sql
for rec in range(1,5):
  model.create({'name': rec})
```

使用以下的只會有 **一次** insert SQL

```python
# 一次 insert sql 效能比較好
model.create([ {'name': rec} for rec in range(1,5)])
```

## odoo17 obfuscate

obfuscate 混淆 這功能目前 odoo16, odoo17, odoo18 都有,

目的是讓因為一些原因不讓別人看到真實資料.

相關原始碼可參考 [odoo/cli/obfuscate.py](https://github.com/odoo/odoo/blob/17.0/odoo/cli/obfuscate.py)

使用方法,

```python
# 密碼一定要填入
python odoo-bin obfuscate -d odoo17 --pwd odoo -c odoo.conf
```

之後它會問你是否要執行, 選 y, 接著它會要你再次輸入 db name, 並且要輸入大寫(都成功後還會執行)

如下圖

![alt tag](https://i.imgur.com/ItnUzzg.png)

紅色框起來的地方是你要輸入的, 綠色的部份是只會對這些 table 以及 fields 去做 obfuscate 而已.

打開 odoo, 去找 res.partner, 你會發現成功被 混淆 了 :blush:

![alt tag](https://i.imgur.com/0FTYz5w.png)

如果你要還原也很簡單

```cmd
python odoo-bin obfuscate -d odoo17 --pwd odoo -c odoo.conf --unobfuscate
```

那你現在一定問我, 如果我要 obfuscate 其他的 table 以及 fields 該怎麼辦 :question:

很簡單, 指定 model 和 fields 即可,

例如有一個 model 名稱為 `demo.expense.tutorial`, 然後有一個 fields 為 name,

obfuscate

```cmd
python odoo-bin obfuscate --fields demo_expense_tutorial.name -d odoo17 --pwd odoo -c odoo.conf
```

unobfuscate

```cmd
python odoo-bin obfuscate --fields demo_expense_tutorial.name -d odoo17 --pwd odoo -c odoo.conf --unobfuscate
```

## odoo17 report render data

這並不是 odoo17 特有的, 只是紀錄一下用法,

可以從 xml report 中去呼叫 python 的 function,

以下介紹如何 render dict 和 list

```python

class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'

    ......

    def demo_render_dict_data(self):
        result = dict()
        for rec in self.tag_ids:
            result[rec.name] = rec
        return result

    def demo_render_list_data(self):
        result = []
        for rec in self.tag_ids:
            result.append({
                'name': rec.name,
                'id': rec.id,
                'data': rec,
            })
        return result
```

report render 使用方法可參考 [report_views.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_expense_tutorial_v1/report/report_views.xml)

## odoo17 report page break

這並不是 odoo17 特有的, 只是紀錄一下用法,

報表設定分頁

[report/report_page_break_views.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_expense_tutorial_v1/report/report_page_break_views.xml)

關鍵是下面這行

```xml
<div style="page-break-before:always;background-color:blue">
  ......
</div>
```

效果如下

![alt tag](https://i.imgur.com/4YPoa1h.png)

[report/report_sheet_page_break_views.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_expense_tutorial_v1/report/report_sheet_page_break_views.xml)

關鍵是下面這行

```xml
<p style="page-break-before:always;background-color:green"/>
```

效果如下

![alt tag](https://i.imgur.com/Ckxupc4.png)

以下效果大家可以自行嘗試

```xml
<p style="page-break-before:always;"> </p>
<p style="page-break-after:always;"> </p>
<p style="page-break-inside:avoid;"> </p>
```