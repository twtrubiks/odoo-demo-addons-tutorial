# odoo-demo-addons-tutorial

本文章會持續更新:smile:

這邊文章主要是會手把手教大家撰寫 odoo 的 addons, 建議再閱讀這篇文章之前, 你已經看過以下的文章

[odoo-development-environment-tutorial](https://github.com/twtrubiks/odoo-development-environment-tutorial) - 建立 odoo 開發環境 ( source code )

[odoo-docker-tutorial](https://github.com/twtrubiks/odoo-docker-tutorial) - 利用 docker 快速建立 odoo 環境

## 前言

為甚麼我要寫一堆 addons, 因為其實 odoo 和 django 一樣的點是都很麻煩, 要寫個範例超級麻煩的,

因為一個小地方錯可能就會造成錯誤之類的:sweat:

## addons 目錄

非常建議按照順序看, 因為會一步一步帶大家:smile:

1. [demo_odoo_tutorial](demo_odoo_tutorial) - odoo 手把手建立第一個 addons

2. [demo_expense_tutorial_v1](demo_expense_tutorial_v1) - odoo 入門篇

3. [demo_class_inheritance](demo_class_inheritance) - odoo 繼承 - class inheritance

4. [demo_prototype_inheritance](demo_prototype_inheritance) - odoo 繼承 - prototype inheritance

5. [demo_delegation_inheritance](demo_delegation_inheritance) - odoo 繼承 - delegation inheritance

6. [demo_actions_singleton](demo_actions_singleton) - odoo 觀念 - actions 和 singleton

7. [demo_scheduler](demo_scheduler) - odoo 觀念 - scheduler

8. [demo_sequence](demo_sequence) - odoo 觀念 - sequence

9. [demo_activity](demo_activity) - odoo 觀念 - activity

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

* [Youtube Tutorial -(等待新增) odoo shell orm 基本教學 - search_read]()

`search_read`

通常比較常使用在 js 呼叫 odoo 或是第三方呼叫 odoo api,

```python
>>> self.env['hr.expense'].search_read([], ['id', 'employee_id'])
[{'id': 4, 'employee_id': (7, 'Marc Demo')}, {'id': 3, 'employee_id': (7, 'Marc Demo')}, {'id': 2, 'employee_id': (1, 'Mitchell Admin')}, {'id': 1, 'employee_id': (1, 'Mitchell Admin')}]

>>> self.env['hr.expense'].search_read([('employee_id', '=', 1)], ['id', 'name', 'employee_id'])
[{'id': 2, 'name': 'Hotel Expenses', 'employee_id': (1, 'Mitchell Admin')}, {'id': 1, 'name': 'Travel by Air', 'employee_id': (1, 'Mitchell Admin')}]
```

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

### odoo shell 注意事項

* [Youtube Tutorial - odoo shell 教學 - 注意事項](https://youtu.be/YS6mGE3-y1k)

odoo-shell 下 command 無法 save 問題,

當使用 Odoo Shell 測試資料時, 會發現當我們下了指令時, db 裡面的值沒有改變,

這時候必須另外執行

```cmd
self.env.cr.commit()
```

在非 Odoo Shell 中會自動執行, 在 Odoo Shell 中不會自動執行 (需要手動執行)

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

![alt tag](https://i.imgur.com/EJTK0KY.png)

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
