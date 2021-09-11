# odoo-demo-addons-tutorial-odoo-12

此版本為 odoo12, odoo14 版本請參考 [odoo14](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0) 分支.

本文章會持續更新:smile:

這邊文章主要是會手把手教大家撰寫 odoo 的 addons, 建議再閱讀這篇文章之前, 你已經看過以下的文章

[odoo-development-environment-tutorial](https://github.com/twtrubiks/odoo-development-environment-tutorial) - 建立 odoo 開發環境 ( source code )

[odoo-docker-tutorial](https://github.com/twtrubiks/odoo-docker-tutorial) - 利用 docker 快速建立 odoo 環境

## 前言

為甚麼我要寫一堆 addons, 因為其實 odoo 和 django 一樣的點是都很麻煩, 要寫個範例超級麻煩的,

因為一個小地方錯可能就會造成錯誤之類的:sweat:

## addons 目錄

非常建議按照順序看, 因為會一步一步帶大家:smile:

1. [odoo 手把手建立第一個 addons](demo_odoo_tutorial)

2. [odoo 入門篇](demo_expense_tutorial_v1)

3. [odoo 繼承 - class inheritance](demo_class_inheritance)

4. [odoo 繼承 - prototype inheritance](demo_prototype_inheritance)

5. [odoo 繼承 - delegation inheritance](demo_delegation_inheritance)

6. [odoo 觀念 - actions 和 singleton](demo_actions_singleton)

7. [odoo 觀念 - scheduler](demo_scheduler)

8. [odoo 觀念 - sequence](demo_sequence)

9. [odoo 觀念 - activity](demo_activity)

10. [odoo 觀念 - TransientModel-Wizard](demo_odoo_tutorial_wizard)

11. [odoo 觀念 - AbstractModel](demo_abstractmodel_tutorial)

12. [odoo 觀念 - 實作 config settings](demo_config_settings)

13. [odoo 觀念 - datetime 教學](demo_datetime_tutorial)

14. [odoo 觀念 - 實作 scan barcode](demo_sale_scan_barcode)

15. [odoo 觀念 - 實作 hierarchy](demo_hierarchy_tutorial)

16. [odoo 觀念 - 如何使用 python xmlrpc 連接 odoo](xml-rpc-odoo)

17. [odoo 觀念 - Translating 翻譯教學 i18n](demo_i18n_expense_tutorial)

18. [odoo 觀念 - recruitment_website_form 介紹](demo_recruitment_website_form)

19. [odoo 觀念 - 實作 init hook](demo_hook_tutorial)

20. [odoo 教學 - 如何繼承 inherit controller](demo_inherit_controller)

21. [odoo 教學 - fields_view_get 介紹教學](demo_fields_view_get_tutorial)

22. [odoo 教學 - multi company](demo_multi_company)

23. [odoo 教學 - testing 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#odoo-testing-%E6%95%99%E5%AD%B8)

24. [odoo 觀念 - orm cache 說明](demo_orm_cache)

25. [odoo 觀念 - 使用 RAW SQL 說明](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E4%BD%BF%E7%94%A8-raw-sql-%E8%AA%AA%E6%98%8E)

26. [odoo 14 觀念 - image mixin 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_image_mixin)

27. [odoo 14 觀念 - Active Archive Ribbon 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_expense_tutorial_v1#odoo14-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---active-archive-ribbon-%E6%95%99%E5%AD%B8---part10)

28. [odoo 14 觀念 - Search Panel 教學](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_expense_tutorial_v1#odoo14-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---search-panel-%E6%95%99%E5%AD%B8---part11)

29. [Odoo Domain 教學]()

## 其他

* [Youtube Tutorial - 使用 CLI 安裝,更新 addons](https://youtu.be/k19N2x8f4gw)

建立 addons 模組

```cmd
./odoo-bin scaffold your_addons_name my-addons/
```

在介紹如何透過 cli 安裝 addons 之前, 請先知道一件事情,

就是你可以選擇將指令全部放到 cli 中, 或是在 `odoo.conf` 設定,

像是如果有設定 `odoo.conf`

```cmd
[options]
......
db_user = odoo
db_password = odoo
db_port = 5432
```

這樣我們直接執行以下指令即可

```cmd
python3 odoo-bin -d odoo -c /home/twtrubiks/work/odoo12/odoo/config/odoo.conf
```

如果你沒有設定 `odoo.conf` , 也可以在 cli 中設定

```cmd
python3 odoo-bin -r odoo -w odoo  -d odoo -c /home/twtrubiks/work/odoo12/odoo/config/odoo.conf
```

`-r` 代表 db_user. `-w` 代表 db_password. `-d` 代表指定 database.

安裝 addons

```cmd
python3 odoo-bin -i addons_1 -d odoo
```

更新 addons

```cmd
python3 odoo-bin -u addons_1 -d odoo
```

也可以一次更新或安裝多個 addons

```cmd
python3 odoo-bin -u addons_1,addons_2 -d odoo
```

例外還有比較進階的用法 `--dev`

```cmd
python3 odoo-bin -u addons_1 -d odoo --dev=all
```

`--dev=all` 代表全部都啟用.

`--dev=xml` 代表當 xml 改變的時候, 會自動幫你更新(不用手動更新).

`--dev=reload` 代表當 python code 改變時, 自動更新(不用手動更新).

但有時候如果你覺得怪怪的, 我還是建議手動重新直接更新 addons 的指令比較好:smile:

注意:exclamation:沒有刪除 addons 的指令, 只能從 web 上移除.

### shell

* [Youtube Tutorial - odoo shell 基本教學 - CRUD](https://youtu.be/kmbiT54hUkw)

```cmd
python odoo-bin shell -w odoo -r odoo -d odoo --db_port=5432 --db_host=localhost --addons-path='/home/twtrubiks/odoo/addons'
```

如果有很多路徑請使用 `,` 隔開

```cmd
--addons-path='/home/twtrubiks/odoo/addons,/home/twtrubiks/odoo/addons2'
```

`search`

```python
>>> self.env['res.partner'].search([])
res.partner(14, 26, 33, 27, 10, 35, 18, 19, 11, 20, 22, 31, 23, 15, 34, 12, 21, 25, 37, 24, 36, 30, 38, 13, 29, 28, 9, 17, 32, 16, 1, 39, 40, 8, 7, 3)
>>> self.env['res.partner'].search([('name', 'like', 'kim')])
res.partner(24,)
>>> self.env['res.partner'].browse([11, 20])
res.partner(11, 20)
```

* [Youtube Tutorial - odoo shell orm 基本教學 - search_read](https://youtu.be/AzGnFX4pHWI)

`search_read`

通常比較常使用在 js 呼叫 odoo 或是第三方呼叫 odoo api,

```python
>>> self.env['hr.expense'].search_read([], ['id', 'employee_id'])
[{'id': 4, 'employee_id': (7, 'Marc Demo')}, {'id': 3, 'employee_id': (7, 'Marc Demo')}, {'id': 2, 'employee_id': (1, 'Mitchell Admin')}, {'id': 1, 'employee_id': (1, 'Mitchell Admin')}]

>>> self.env['hr.expense'].search_read([('employee_id', '=', 1)], ['id', 'name', 'employee_id'])
[{'id': 2, 'name': 'Hotel Expenses', 'employee_id': (1, 'Mitchell Admin')}, {'id': 1, 'name': 'Travel by Air', 'employee_id': (1, 'Mitchell Admin')}]
```

* [Youtube Tutorial - odoo orm group 基本教學 - read_group](https://youtu.be/ALq6CcADygs)

`read_group`

通常使用在 SQL 中的 GROUP BY (很適合拿來處理比較大的資料, 效能應該也會比較好:smile:).

read_group 的定義可參考原始碼中的 `odoo/models.py`

```python
......
@api.model
def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
    """
    Get the list of records in list view grouped by the given ``groupby`` fields

    :param domain: list specifying search criteria [['field_name', 'operator', 'value'], ...]
    :param list fields: list of fields present in the list view specified on the object.
            Each element is either 'field' (field name, using the default aggregation),
            or 'field:agg' (aggregate field with aggregation function 'agg'),
            or 'name:agg(field)' (aggregate field with 'agg' and return it as 'name').
            The possible aggregation functions are the ones provided by PostgreSQL
            (https://www.postgresql.org/docs/current/static/functions-aggregate.html)
            and 'count_distinct', with the expected meaning.
    :param list groupby: list of groupby descriptions by which the records will be grouped.
            A groupby description is either a field (then it will be grouped by that field)
            or a string 'field:groupby_function'.  Right now, the only functions supported
            are 'day', 'week', 'month', 'quarter' or 'year', and they only make sense for
            date/datetime fields.
......
```

比較特別要注意的地方是 fields, groupby, lazy 這幾個欄位 (請參考註解說明:smile:).

如果你想參考寫法, 建議參考 odoo14 的, odoo12 也可以使用, 但是有些寫法比較舊了.

這邊使用 `sale.order` 當作範例,

假設想要得到每個 partner_id 的平均 amount_total,

```python
self.env['sale.order'].read_group([], ['partner_id', 'amount_total:avg'], ['partner_id'])
```

![alt tag](https://i.imgur.com/6eyegIE.png)

同等如下 SQL

```sql
SELECT partner_id, avg(amount_total)
FROM sale_order
GROUP BY partner_id;
```

注意:exclamation::exclamation:這邊 field 的格式為 `field:agg`.

agg 代表 aggregate, odoo 的 orm 是有支援的, 更多詳細可參考 [postgresql functions-aggregate](https://www.postgresql.org/docs/current/functions-aggregate.html).

假設想要得到每個 partner_id 的平均 amount_total 以及 總和 amount_total,

```python
self.env['sale.order'].read_group([], ['partner_id', 'total:sum(amount_total)', 'avg_total:avg(amount_total)'], ['partner_id'])
```

![alt tag](https://i.imgur.com/BhNR227.png)

同等如下 SQL

```sql
SELECT partner_id, avg(amount_total), sum(amount_total)
FROM sale_order
GROUP BY partner_id;
```

注意:exclamation::exclamation:這邊的 fields 的格式為 `name:agg(field)`

(因為是相同的 fields 名稱, 如果使用前一種寫法會錯誤)

如果想要分的更細, 甚至可以再加上 fields, 這邊增加一個狀態

```python
self.env['sale.order'].read_group([], ['partner_id', 'total:sum(amount_total)', 'avg_total:avg(amount_total)'], ['partner_id', 'state'], lazy=False)
```

![alt tag](https://i.imgur.com/IaaFXae.png)

同等如下 SQL

```sql
SELECT partner_id, state, avg(amount_total), sum(amount_total)
FROM sale_order
GROUP BY partner_id, state;
```

`lazy` 這個參數預設為 True, 也就代表只會拿第一個 field 下去分組,

如果設定為 False, 就會把全部你所指定的 fields 都拿進去分組.

根據 date_order 下去分組

```python
self.env['sale.order'].read_group([], ['total:sum(amount_total)'], ['date_order:month'])
```

同等如下 SQL

```sql
SELECT  DATE_TRUNC('month', date_order),
		sum(amount_total)
FROM sale_order
GROUP BY DATE_TRUNC('month', date_order);
```

`day` `week` `month` `quarter` `year` 這些都是可用的參數.

![alt tag](https://i.imgur.com/cp1zX6P.png)

`search_count`

```python
>>> self.env['res.partner'].search_count([])
73
```

`recordset.ids` 回傳 recordset 全部的 id

```python
>>> recordset = self.env['res.partner'].search([])
>>> recordset.ids
[14, 26, 33, 27, 10, 35, 18, 19, 11, 20, 22, 31, 23, 15, 34, 12, 21, 25, 37, 24, 36, 30, 38, 13, 29, 28, 9, 17, 32, 16, 1, 39, 40, 8, 7, 3]
```

繼續使用上面的範例

`recordset.filtered(func)` 和 python 中的 [filter](https://github.com/twtrubiks/python-notes/blob/master/filter.py) 類似

```python
>>> recordset.filtered(lambda r: r.name.startswith('C'))
res.partner(33, 39)
```

`recordset.mapped(func)` 和 python 中的 [map](https://github.com/twtrubiks/python-notes/blob/master/map_tutorial.py) 類似

```python
>>> recordset.mapped('name')
['Azure Interior', 'Brandon Freeman', 'Colleen Diaz', 'Nicole Ford', 'Deco Addict', 'Addison Olson', 'Douglas Fletcher', 'Floyd Steward',...
```

`recordset.sorted(func)` 和 python 中的 [sorted](https://github.com/twtrubiks/python-notes/blob/master/sorted.py) 類似

```python
>>> recordset.sorted(key=lambda r: r.id, reverse=True)
res.partner(40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, ...
```

`create`

```python
>>> partner = self.env['res.partner']
>>> partner.create({'name': 'twtrubiks', 'is_company': True})
res.partner(66)
>>> self.env.cr.commit() # 需要特別執行這行才會寫進資料庫中
```

`write`

update data

```python
>>> partner = self.env['res.partner'].browse([2])
>>> partner
res.partner(2,)
>>> partner.name
'OdooBot'
>>> partner.write({'name': 'hello'})
True
>>> partner.name
'hello'
>>> self.env.cr.commit() # 需要特別執行這行才會寫進資料庫中
```

當你更新 `One2many` 和 `Many2many` 時, 要使用比較特別的語言,

我之後會補充上來.

`copy`

如果 fields 有定義 `copy=False`, 就沒有辦法複製.

```python
# odoo/addons/base/data/res_users_demo.xml
>>> demo = self.env.ref('base.user_demo')
>>> demo.copy({'name': 'twtrubiks', 'login': 'twtrubiks', 'email':''})
>>> self.env.cr.commit() # 需要特別執行這行才會寫進資料庫中
```

`delete`

```python
>>> user = self.env['res.users'].browse([3])
>>> user.unlink()
2020-06-21 06:45:51,958 19735 INFO odoo odoo.models.unlink: User #1 deleted ir.model.data records with IDs: [1884]
2020-06-21 06:45:51,996 19735 INFO odoo odoo.models.unlink: User #1 deleted res.users records with IDs: [3]
True
>>> self.env.cr.commit() # 需要特別執行這行才會寫進資料庫中
```

`sudo`

* [Youtube Tutorial - odoo 基本教學 - sudo](https://youtu.be/nAmNmPCSbGg)

可參考 odoo 原始碼的 `odoo/models.py`

```python
def sudo(self, user=SUPERUSER_ID):
    """ sudo([user=SUPERUSER])

    Returns a new version of this recordset attached to the provided
    user.

    By default this returns a ``SUPERUSER`` recordset, where access
    control and record rules are bypassed.

    .. note::

        Using ``sudo`` could cause data access to cross the
        boundaries of record rules, possibly mixing records that
        are meant to be isolated (e.g. records from different
        companies in multi-company environments).

        It may lead to un-intuitive results in methods which select one
        record among many - for example getting the default company, or
        selecting a Bill of Materials.

    .. note::

        Because the record rules and access control will have to be
        re-evaluated, the new recordset will not benefit from the current
        environment's data cache, so later data access may incur extra
        delays while re-fetching from the database.
        The returned recordset has the same prefetch object as ``self``.

    """
    return self.with_env(self.env(user=user))
```

`sudo([user=SUPERUSER])` 如果裡面沒有填入 user id, 預設就是使用 SUPERUSER, 如果

有帶入 user id, 就是使用指定的 user 的權限.

來看下面這個例子,

因為沒有指定 user id, 所以是使用 SUPERUSER, 自然可以看到全部的 records,

```python
>>> self.env['hr.expense'].sudo().search([])
hr.expense(4, 3, 2, 1)
```

再來看這個例子, user_id = 6 只能看到自己的 records, 因為他是一般的 user,

```python
>>> self.env['hr.expense'].sudo(user=6).search([])
hr.expense(4, 3)
```

也就是說, 知道這個特性, 我們甚至可以讓沒有權限的人看到 records (請依照自己的需求去調整):smile:

`with_context`

可參考 odoo 原始碼的 `odoo/models.py`

```python
def with_context(self, *args, **kwargs):
    """ with_context([context][, **overrides]) -> records

    Returns a new version of this recordset attached to an extended
    context.

    The extended context is either the provided ``context`` in which
    ``overrides`` are merged or the *current* context in which
    ``overrides`` are merged e.g.::

        # current context is {'key1': True}
        r2 = records.with_context({}, key2=True)
        # -> r2._context is {'key2': True}
        r2 = records.with_context(key2=True)
        # -> r2._context is {'key1': True, 'key2': True}

    .. note:

        The returned recordset has the same prefetch object as ``self``.
    """
    context = dict(args[0] if args else self._context, **kwargs)
    return self.with_env(self.env(context=context))
```

`with_context` 可以用在很多地方, 這邊用一個翻譯的舉例, 如果我同時有 `en_US` 和 `zh_TW`

這兩個語言, 可以使用 `with_context`帶入不同的語言, 會自動依照語言進行翻譯,

```python
>>> self.env['product.product'].with_context(lang='zh_TW').browse(41).name
'飛機票'
>>> self.env['product.product'].with_context(lang='en_US').browse(41).name
'Air Flight'
```

`with_context` 也常使用在傳值中, 可參考 [odoo 觀念-TransientModel-Wizard](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial_wizard)

### odoo shell 注意事項

* [Youtube Tutorial - odoo shell 教學 - 注意事項](https://youtu.be/YS6mGE3-y1k)

odoo-shell 下 command 無法 save 問題,

當使用 Odoo Shell 測試資料時, 會發現當我們下了指令時, db 裡面的值沒有改變,

這時候必須另外執行

```cmd
self.env.cr.commit()
```

在非 Odoo Shell 中會自動執行, 在 Odoo Shell 中不會自動執行 (需要手動執行).

除非你不想要把修改資料寫進去資料庫.

## odoo log 說明

```log
2019-12-05 03:04:15,734 1 INFO localhost werkzeug: 172.18.0.1 - - [05/Dec/2019 03:04:15] "POST /longpolling/poll HTTP/1.0" 200 - {query_count} {query_time} {remaining_time}
```

query_count = query 次數

query_time = query 時間

remaining_time = 剩餘時間

如何透過 elk 搭配 odoo, 請參考 [docker-elk-tutorial 7.6.0](https://github.com/twtrubiks/docker-elk-tutorial/tree/elk-7.6.0)

## odoo 使用 gmail 發信

* [Youtube Tutorial - odoo 教學 - 使用 gmail 發信](https://youtu.be/CkFHCQuzEoo)

gmail 需要一些前製作業, 建議先閱讀 [使用 Gmail 寄信 - 前置作業](https://github.com/twtrubiks/Flask-Mail-example#%E4%BD%BF%E7%94%A8-gmail-%E5%AF%84%E4%BF%A1---%E5%89%8D%E7%BD%AE%E4%BD%9C%E6%A5%AD) 這篇的 gmail 設定

Technical -> Email -> Outgoing Mail Servers

![alt tag](https://i.imgur.com/mZpaHWu.png)

SMTP Server	填入 `smtp.gmail.com`

SMTP Port 填入 `465`

Connection Security 填入 `SSL/TLS`

填入自己的 Username 和 Password

![alt tag](https://i.imgur.com/V77o0hY.png)

建議輸入資料後, 可以先點選測試連接 (以下是成功的畫面)

![alt tag](https://i.imgur.com/rIXcdnH.png)

如果出現錯誤, 請確認你的帳密是否有錯誤

![alt tag](https://i.imgur.com/yMVWVF5.png)

以及把權限安全性調整為低一點, 可參考以下的兩個連結

[https://www.google.com/settings/security/lesssecureapps](https://www.google.com/settings/security/lesssecureapps)

[https://www.google.com/accounts/DisplayUnlockCaptcha](https://www.google.com/accounts/DisplayUnlockCaptcha)

接著可以使用 odoo 內的 email 測試看是否可以成功發信

![alt tag](https://i.imgur.com/sy1A69K.png)

成功發信

![alt tag](https://i.imgur.com/CvMuelM.png)

## 如何全域修改時間日期格式

路徑為 Translations -> Languages, 點選語言, 就會看到以下的畫面,

圖片下方有一些參數的說明(可自行依照需求調整)

![alt tag](https://i.imgur.com/Z66LDIC.png)

## 其他注意事項

`odoo.conf` 中的 `data_dir` 參數建立好了就不要亂改,

因為亂改動可能會導致你的 odoo 打開時一片空白或是破圖的狀況.

```conf
[options]
......
data_dir = /home/twtrubiks/work/odoo12/odoo-data
```

另外如果你的 odoo 不知道甚麼原因導致破圖(非上述的狀況),

錯誤訊息通常可能是遺失 filestore, 這時候可以嘗試以下的幾個方法,

可以試試看更新 odoo 中的 `base`,

或是從 db 中刪除 `ir_attachment` table,

重新使用 debug mode 中的 Regenerate Assets Bundles.

(assets 這個的功能是刪除舊的 css 和 js, 然後重新產生新的, 有時遇到 assets 快取的問題, 可以選這個選項)

![alt tag](https://i.imgur.com/EJTK0KY.png)

## 建議使用繼承 addons 的方式修改 odoo

[Youtube Tutorial - odoo 教學 - 建議使用繼承 addons 的方式修改 odoo](https://youtu.be/Yncbx95YT1Q)

這邊提醒大家, 建議在修改 odoo 的時候, 儘量使用 addons 繼承的方式去修改 code,

原因是維護性的問題, 原生的 code 保持乾淨,

雖然用 odoo developer mode 可以很快的修改 view,

但是 :exclamation::exclamation:

只要你一更新你修改的那個 addons, 就會自動還原 :exclamation::exclamation:

這邊使用 `hr_expense` 舉的例子,

我透過 Edit View 修改了 view,

![alt tag](https://i.imgur.com/M6goe84.png)

當你保存是會生效的.

可是當你去更新 `hr_expense` 的時候, 你會發生他被還原了.

所以, 使用 Edit View 選項去修改 view 可以使用在測試時.

正式的修改, 還是推薦使用 addons 繼承的方式:smile:

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡:laughing:

綠界科技ECPAY ( 不需註冊會員 )

![alt tag](https://payment.ecpay.com.tw/Upload/QRCode/201906/QRCode_672351b8-5ab3-42dd-9c7c-c24c3e6a10a0.png)

[贊助者付款](http://bit.ly/2F7Jrha)

歐付寶 ( 需註冊會員 )

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## 贊助名單

[贊助名單](https://github.com/twtrubiks/Thank-you-for-donate)

## License

MIT license
