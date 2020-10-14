# odoo 觀念 - scheduler

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - scheduler](https://youtu.be/uvQTHsKu3Ic)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 scheduler 這部份

## 說明

先來看 [models/models.py](models/models.py)

```python
......

_logger = logging.getLogger(__name__)

class DemoScheduler(models.Model):
    _name = 'demo.scheduler'
    _description = 'Demo Scheduler'

    def action_schedule(self):
        _logger.warning('============= Action Schedule ==================')

```

簡單定義一個 class, 裡面就只有一個 function ( 用來測試 schedule ),

雖然沒有定義 fields, 但是還是會在 db 中建立 model `demo_scheduler`,

![alt tag](https://i.imgur.com/w8ztB9s.png)

也請記得設定 security

[security/ir.model.access.csv](security/ir.model.access.csv)

[security/security.xml](security/security.xml)

接著看 [views/scheduler.xml](views/scheduler.xml), schedule 的重點

```xml
<?xml version="1.0" ?>
<odoo>
  <data noupdate="0">
    <record id="demo_scheduler" model="ir.cron">
      <field name="interval_type">days</field>
      <field name="name">demo scheduler</field>
      <field name="numbercall">-1</field>
      <field name="priority">5</field>
      <field name="doall">False</field>
      <field name="active">True</field>
      <field name="interval_number">1</field>
      <field name="model_id" ref="model_demo_scheduler"/>
      <field name="state">code</field>
      <field name="code">model.action_schedule()</field>
    </record>
  </data>
</odoo>
```

`interval_type` 分, 小時, 天, 禮拜, 月, 最小單位為 1 分鐘:exclamation::exclamation:

`interval_number` 次數, 搭配 `interval_type`, 像範例就是一天執行一次.

`numbercall` `-1` 代表不限制(無線循環), 如果今天設定為 `2`, 代表執行兩次之後就不會執行了.

`model_id` 指定 model.

`state` 使用的方式, 這邊使用 python code.

`code` 呼叫 `model.action_schedule()` models 中的 methond.

`priority` 0 最優先, 10最不重要(不優先).

安裝完 addons 之後, 也可以到 odoo 中的後台查看 schedule, 請到以下的路徑

Technical -> Automation -> Scheduled Actions

![alt tag](https://i.imgur.com/JFZD2Io.png)

你應該會看到一個 demo schedule

![alt tag](https://i.imgur.com/PVvYzl0.png)

你也可以在這邊改細項(設定)

![alt tag](https://i.imgur.com/EOsdBGg.png)

Run Manually

也可以手動觸發 schedule, 確保他是正常的:smile:

![alt tag](https://i.imgur.com/OrCh1mr.png)

最後記得也要將 `scheduler.xml` 加入 `__manifest__.py` 哦

```python
......
  # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/scheduler.xml',
    ],
    'application': True,
}
```