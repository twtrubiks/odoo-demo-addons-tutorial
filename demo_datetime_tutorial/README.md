# odoo datetime 教學

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo datetime 教學](https://youtu.be/Ha0YNFm6KzI)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章將說明 odoo 中的 datetime 機制.

## 說明

注意:exclamation:

在 odoo 中所有的 date 和 datetime 都是使用 UTC 的時間 (包含保存進資料庫 db 的資料).

這樣你可能會問我, odoo 不是可以選時區, 這樣頁面上是怎麼呈現時區正確的時間的:question:

odoo 會透過 session (或是你的設定) 去做 time zone 的轉換.

每個 user 都可以設定自己的時區, 系統會建議你設定和瀏覽器一樣的時區

![alt tag](https://i.imgur.com/cl34SUC.png)

先來看一下 python 的 datetime

```python
>>> from datetime import datetime
>>> datetime(2020, 1, 10, 0, 0)
datetime.datetime(2020, 1, 10, 0, 0)

# strptime, python 的 str -> datetime
>>> my_datetime = datetime.strptime('2020/11/23', '%Y/%m/%d')
>>> my_datetime
datetime.datetime(2020, 11, 23, 0, 0)

# strftime, python 的 datetime -> str
>>> datetime.strftime(my_datetime, '%Y-%m-%d')
'2020-11-23'
```

python 的 timedelta

```python
>>> from datetime import date
>>> from datetime import timedelta
>>> date.today()
datetime.date(2020, 10, 14)

>>> date.today() + timedelta(days=7)
datetime.date(2020, 10, 21)
```

python 的時區轉換

```python
>>> ## Asia/Taipei -> UTC
>>> from pytz import timezone
>>> from datetime import datetime
>>> today = datetime(2022, 7, 7, 10, 0)
>>> user_tz = timezone('Asia/Taipei')

>>> today = user_tz.localize(today)
>>> today
datetime.datetime(2022, 7, 7, 10, 0, tzinfo=<DstTzInfo 'Asia/Taipei' CST+8:00:00 STD>)

>>> today = today.astimezone(timezone('UTC'))
>>> today
datetime.datetime(2022, 7, 7, 2, 0, tzinfo=<UTC>)


>>> ## UTC -> Asia/Taipei
>>> from pytz import timezone
>>> from datetime import datetime
>>> today = datetime(2022, 7, 7, 10, 0)
>>> user_tz = timezone('UTC')

>>> today = user_tz.localize(today)
>>> today
datetime.datetime(2022, 7, 7, 10, 0, tzinfo=<UTC>)

>>> today = today.astimezone(timezone('Asia/Taipei'))
>>> today
datetime.datetime(2022, 7, 7, 18, 0, tzinfo=<DstTzInfo 'Asia/Taipei' CST+8:00:00 STD>)
```

odoo 中的 odoo.tools.date_utils

`start_of(value, granularity)`

`end_of(value, granularity)`

`add(value, **kwargs)`

`subtract(value, **kwargs)`

```python
from odoo.tools import date_utils
from datetime import date

>>> date.today()
datetime.date(2020, 10, 14)

>>> date_utils.add(date.today(), days=2)
datetime.date(2020, 10, 16)

>>> date_utils.subtract(date.today(), months=2)
datetime.date(2020, 8, 14)
```

odoo 中的 `fields.Date.today()` `fields.Datetime.now()`

```python
>>> from odoo import fields
>>> fields.Date.today()
datetime.date(2020, 10, 14)
>>> fields.Datetime.now()
datetime.datetime(2020, 10, 14, 10, 48, 25)
```

fields.Date `to_date` converts a string into a date object.

fields.Datetime `to_datetime(value)` converts a string into a datetime object.

fields.Date, fields.Datetime `to_string(value)` converts a date or datetime object into a string in the format expected by the Odoo server.

( 其實這個 `to_string(value)` 也只是使用 python 的 `strftime` 去轉換而已, 格式是預設的 DATETIME_FORMAT)

`fields.Date.context_today(record, timestamp=None)`

`fields.Datetime.context_timestamp(record, timestamp)`

```python
>>> from odoo import fields
>>> my_datetime = fields.Datetime.to_datetime('2020-02-10 10:00:00')
>>> my_datetime
datetime.datetime(2020, 2, 10, 10, 0)

>>> my_datetime = fields.Datetime.from_string('2020-02-10 10:00:00')
>>> my_datetime
datetime.datetime(2020, 2, 10, 10, 0)

>>> fields.Datetime.to_string(my_datetime)
'2020-02-10 10:00:00'
```

寫入資料時, 可以直接輸入 string, 會自動轉換成 date / datetime

```python
>>> demo = self.env['demo.datetime'].browse(1)
>>> demo.my_datetime
datetime.datetime(2020, 10, 14, 9, 30, 8)
>>> demo.my_datetime = '2020-01-01 09:00:00'
>>> demo.my_datetime
datetime.datetime(2020, 1, 1, 9, 0)
```

轉換時區

```python
from pytz import timezone

# Convert to Asia/Taipei time zone

>>> demo = self.env['demo.datetime'].browse(1)
>>> demo.my_datetime
datetime.datetime(2020, 1, 1, 9, 0)

>>> demo.my_datetime.astimezone(timezone('Asia/Taipei'))
datetime.datetime(2020, 1, 1, 17, 0, tzinfo=<DstTzInfo 'Asia/Taipei' CST+8:00:00 STD>)
```

將 addons 裝起來之後, 來看 [models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_datetime_tutorial/models/models.py)

```python
......
       @api.multi
       def demo1(self):
           _logger.warning('db datetime')
           _logger.warning(self.my_datetime )

           _logger.warning('Asia/Taipei datetime')
           _logger.warning(self.my_datetime.astimezone(timezone('Asia/Taipei')))
......
```

![alt tag](https://i.imgur.com/C4yMCYb.png)

可以從輸出中看到一個是 db 保存的 utc 時間, 一個是轉換後的 Taipei 時間.

![alt tag](https://i.imgur.com/rprCbmE.png)

db 中保存的時間

![alt tag](https://i.imgur.com/kp4NkiS.png)
