# odoo 16 教學

更新到 odoo16

* [Youtube Tutorial - odoo 16 手把手教學 - compute fields - precompute](https://youtu.be/WtwU_ry-goI) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#compute-fields---precompute)

* [Youtube Tutorial - odoo 16 手把手教學 - fake Binary fields](https://youtu.be/iCaTDiSV_6g) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#fake-binary-fields)

* [Youtube Tutorial - odoo 16 手把手教學 - json fields - 改善效能](https://youtu.be/vYJSszNysts) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#json-fields---%E6%94%B9%E5%96%84%E6%95%88%E8%83%BD)

* [Youtube Tutorial - odoo 16 手把手教學 - Command 操作 M2M O2M](https://youtu.be/8vqi0r3ba5E) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#command-%E6%93%8D%E4%BD%9C-m2m-o2m)

* [Youtube Tutorial - odoo 16 手把手教學 - 新功能 Neutralize](https://youtu.be/Kq7Ti_gMU0U) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#neutralize)

## index 更新

除了原本的 btree, 多了 btree_not_null 和 trigram,

btree_not_null 適合大多數是 null 的資料.

trigram 適合 full-text search, 像是 like `%search%` 這類的.

(建議可以直接看一下原始碼, 看看 odoo 怎麼使用這個 index )

說明一下 index,

可以吃到 index -> `text%`

無法吃到 index -> `%text%` `%text`, 建議改用 full-text search.

原始碼說明如下,

```python
"""
:param str index: whether the field is indexed in database, and the kind of index.
        Note: this has no effect on non-stored and virtual fields.
        The possible values are:

        * ``"btree"`` or ``True``: standard index, good for many2one
        * ``"btree_not_null"``: BTREE index without NULL values (useful when most
                                values are NULL, or when NULL is never searched for)
        * ``"trigram"``: Generalized Inverted Index (GIN) with trigrams (good for full-text search)
        * ``None`` or ``False``: no index (default)
"""

```

相關教學可參考 [odoo index 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/odoo_index_tutorial)

## compute fields - precompute

* [Youtube Tutorial - odoo 16 手把手教學 - compute fields - precompute](https://youtu.be/WtwU_ry-goI) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_expense_tutorial_v1#compute-fields---precompute)

在 compute fields 中多了一個 `precompute` 參數,

詳細的 commit 可參考 [[REF] core: compute fields before database insertion.](https://github.com/odoo/odoo/commit/d04a5b5c8c7dc13e4e911a29d1944e90587e2883)


```python
class Field(MetaField('DummyField', (object,), {})):
        ......

        :param bool precompute: whether the field should be computed before record insertion
                in database.  Should be used to specify manually some fields as precompute=True
                when the field can be computed before record insertion.
                (e.g. avoid statistics fields based on search/read_group), many2one
                linking to the previous record, ... (default: `False`)
```

當你設定 `precompute=True` 的時候, `store=True` 也必須設定, 否則會跳出 Warning.

如果你用中斷點觀看 compute 的狀況,

`precompute=True` 新的 record.

`precompute=False` 已經存在的 record.

建議使用 log_level = debug_sql 觀看過程,

`precompute=True`   流程是 compute -> insert

`precompute=False`  流程是 insert -> compute -> update

簡單說, 正常 compute 的時機是先建立 record 之後, 再去更新 compute 欄位,

但是這個新的特性, 可以讓 compute 在建立 record 之前, 就先去 compute 欄位,

之後直接寫入 db, 這樣就不需要多一次更新了.

另外, 多說明一個小細節, 就是有時候你會發現 compute 的欄位無法用 ORM 搜尋,

```python
# 情境一
is_done = fields.Boolean(compute='_compute_is_done', store=True)

# 結果
# 如果用 orm search, 可以搜尋 is_done 欄位
```

```python
# 情境二
is_done = fields.Boolean(compute='_compute_balance', store=False)

# 結果
# 如果用 orm search, 會 "無法搜尋" is_done 欄位 (因為沒有存進 db).
```

區別很簡單, 就是當你的 compute 沒有保存進 db 的時候, ORM search 是沒辦法去搜尋的.

當你去搜尋 情境二, 你會發現搜尋結果是撈出全部的資料.

詳細說明可參考 [odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) 中的 inverse

## fake Binary fields

* [Youtube Tutorial - odoo 16 手把手教學 - fake Binary fields](https://youtu.be/iCaTDiSV_6g)

這功能在 odoo15 就有了, 只不過沒那麼完善,

在 odoo16 中更完善了, 基本概念, 就是使用 Binary 當作暫存的變數,

(以前通常 Binary fields 都是用在圖片)

你可以把他想成是 fake Binary fields,

目的是改善效能, 相關可參考 [[REF] accounting v16. ](https://github.com/odoo/odoo/commit/d8d47f9ff8554f4b39487fd2f13c153c7d6f958d)

```python
......

class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    _description = 'Demo Expense Tutorial'

    ......

    data_vals = fields.Binary(compute='_compute_data_vals', exportable=False)

    @api.depends('name')
    def _compute_data_vals(self):
        for rec in self:
            rec.data_vals = {"tmp_data": "hello"}
......
```

通常這個 fields, 在 view 裡面是會隱藏的, 只有在需要的時候,

才會去取這個 fields 做相關的運算.

至於這個 `exportable=False`, 就只是是否可以 export,

如果是 `exportable=True`, 你會可以匯出這個 fields

![alt tag](https://i.imgur.com/Z9tIZ16.png)

反之, 你會看不到這個欄位, 也就是不能匯出.

## json fields - 改善效能

* [Youtube Tutorial - odoo 16 手把手教學 - json fields - 改善效能](https://youtu.be/vYJSszNysts)

odoo16 新的 fields

```python
class Json(Field):
    """ JSON Field that contain unstructured information in jsonb PostgreSQL column.
    This field is still in beta
    Some features have not been implemented and won't be implemented in stable versions, including:
    * searching
    * indexing
    * mutating the values.
    """
    ......

```

目前使用比較多的部份就是 analytic_distribution 這個,

但這功能算是開發中, 所以如果你定義這個欄位, 會無法用 ORM 的方式去搜尋.

```python
......
class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    ......
    _inherit = "analytic.mixin"

    ......
    analytic_distribution = fields.Json()
    ......
```

使用方法如上, 要去繼承 `analytic.mixin`, 然後定義 analytic_distribution.

接著看 `translate=True`,

當 fields 中加入 `translate=True` 會變成 json fields,

主要目的是改善效能, 原本是會去 join 其他的表格找翻譯, 現在直接找尋該表格即可.

相關文章可參考 [PostgreSQL jsonb](https://github.com/twtrubiks/postgresql-note/tree/main/pg-jsonb-tutorial)

## Command 操作 M2M O2M

* [Youtube Tutorial - odoo 16 手把手教學 - Command 操作 M2M O2M](https://youtu.be/8vqi0r3ba5E)

這個功能 odoo15 就有了, 在這邊再提一次,

以前再加 M2M 或 O2M 的欄位都需要去記很多數字

```python
(0, _ , {'field': value}) creates a new record and links it to this one.
(1, id, {'field': value}) updates the values on an already linked record.
(2, id, _) removes the link to and deletes the id related record.
(3, id, _) removes the link to, but does not delete, the id related record. This is usually what you will use to delete related records on many-to-many fields.
(4, id, _) links an already existing record.
(5, _, _) removes all the links, without deleting the linked records.
(6, _, [ids]) replaces the list of linked records with the provided list.
```

但是現在有一個新的指令更直觀, 就是 Command,

```python
def add_demo_expense_record_old(self):
    # (0, _ , {'field': value}) creates a new record and links it to this one.

    data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

    tag_data_1 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_1')
    tag_data_2 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_2')

    for record in self:
        # creates a new record
        val = {
           'name': 'test_data',
           'employee_id': data_1.employee_id,
           'tag_ids': [(6, 0, [tag_data_1.id, tag_data_2.id])]
        }
        self.expense_line_ids = [(0, 0, val)]

def add_demo_expense_record(self):
    data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

    tag_data_1 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_1')
    tag_data_2 = self.env.ref('demo_expense_tutorial_v1.demo_tag_data_2')

    for _ in self:
        val = {
            'name': 'test_data',
            'employee_id': data_1.employee_id.id,
            'tag_ids': [Command.set([tag_data_1.id, tag_data_2.id])]
        }
        self.expense_line_ids = [Command.create(val)]
```

以前要用 `[(6, 0, [id, id])]` 這個來代表,

現在可以透過 `Command.set` 和 `Command.create`

```python
def link_demo_expense_record_old(self):
        # (4, id, _) links an already existing record.

    data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

    for record in self:
        # link already existing record
        self.expense_line_ids = [(4, data_1.id, 0)]

def link_demo_expense_record(self):
        data_1 = self.env.ref('demo_expense_tutorial_v1.demo_expense_tutorial_data_1')

    for _ in self:
        # link already existing record
        self.expense_line_ids = [Command.link(data_1.id)]

```

以前要用 `[(4, id, 0)]` 這個來代表,

現在可以透過 `Command.link`

也支援 clear

```python

def clear_demo_expense_record(self):
    for _ in self:
        self.expense_line_ids = [Command.clear()]
```

## account move 以及 account invoice 改變

從 odoo13 開始改變,

```text
account.invoice and account.invoice.line is removed from Odoo13.
Instead of this two models odoo will use account.move and account.move.line
```

簡單說, 沒有 `account.invoice` 和 `account.invoice.line` 了,

只剩下, `account.move` 和 `account.move.line`,

然後會使用 `move_type` 去區分各種類型,

```python
move_type = fields.Selection(selection=[
        ('entry', 'Journal Entry'),
        ('out_invoice', 'Customer Invoice'),
        ('out_refund', 'Customer Credit Note'),
        ('in_invoice', 'Vendor Bill'),
        ('in_refund', 'Vendor Credit Note'),
        ('out_receipt', 'Sales Receipt'),
        ('in_receipt', 'Purchase Receipt'),
    ], string='Type', required=True, store=True, index=True, readonly=True, tracking=True,
    default="entry", change_default=True)
```

## Neutralize

* [Youtube Tutorial - odoo 16 手把手教學 - 新功能 Neutralize](https://youtu.be/Kq7Ti_gMU0U)

這個功能是 odoo16 新增的,

主要目的是當我們從正式機複製(或還原)一個 db 時,

透過這個設定, 可以將排程以及一些收發信的功能關閉.

我的法想是這個功能不錯, 原因是我很多時候需要把正式機的資料放到測試機,

每次都還要寫程式關閉一些排程或寄信的 server 相關設定,

有了這個功能後就方便多了😀

[neutralize.py](https://github.com/odoo/odoo/blob/16.0/odoo/modules/neutralize.py)

```python
class Neutralize(Command):
    """Neutralize a production database for testing: no emails sent, etc."""
```

相關 commit 可以看這邊,

[[IMP] core: use inert SQL based neutralization](https://github.com/odoo/odoo/commit/e5dbded9bb363351feff7ca8a56c7f8a6860f492)

原本是用 ORM 的方式, 後來改成了 RAW SQL,

原因是如果用 ORM 的方式, 有可能會不小心 trigger 一些內部邏輯.

主要的運作方式是會去每個 addons 底下找是否有 `data/neutralize.sql`,

```python
def get_neutralization_queries(modules):
    # neutralization for each module
    for module in modules:
        filename = odoo.modules.get_module_resource(module, 'data/neutralize.sql')
        if filename:
            with odoo.tools.misc.file_open(filename) as file:
                yield file.read().strip()
```

如果有, 就去執行它.

如果你想透過 vscode 去找 `neutralize.sql`, 直接使用 `ctrl + p` 去搜尋檔名.

每個 `neutralize.sql`,

多數都是關閉 `ir.cron` 也就是 Scheduled,

也有些是 Archive email 的相關設定.

實際的頁面,

還原資料庫

![alt tag](https://i.imgur.com/csdGXes.png)

複製資料庫

![alt tag](https://i.imgur.com/5fNP9jt.png)

如果有 Neutralize 的, 上方也會和你說有 Neutralize.

![alt tag](https://i.imgur.com/R9yeigg.png)
