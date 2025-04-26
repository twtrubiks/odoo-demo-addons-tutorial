# 透過 AbstractModel 擴充 Model

建議觀看影片, 會更清楚 :smile:

[Youtube Tutorial - odoo 手把手教學 - 透過 AbstractModel 擴充 Model](https://youtu.be/uW1PsDPcJF4)

之前有介紹過 AbstractModel 的文章

* [介紹 AbstractModel](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_abstractmodel_tutorial) 搭配 report 使用

* [odoo 繼承 - prototype inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_prototype_inheritance) 有提到 MailThread 這個 AbstractModel

今天要來進一步介紹, 如何透過 AbstractModel 擴充 Model :smile:

## 說明

首先, 再提一次

`AbstractModel` AbstractModel = BaseModel,

注意 :exclamation: :exclamation: AbstractModel **不會** 在資料庫中產生對應的 table.

先來看這個範例 [models/models.py](models/models.py)

```python
from odoo import models, fields, api

class DemoMixin(models.AbstractModel):
    _name = 'demo.mixin'
    _description = 'Demo Mixin'

    test_1 = fields.Float(
        string='test_1',
        default='2.2'
    )

    test_2 = fields.Float(
        string="test_2",
        compute="_compute_field",
    )

    def _compute_field(self):
        for record in self:
            record.test_2 = 3.0

class DemoModelTutorial(models.Model):
    _name = 'demo.model.tutorial'
    _inherit = 'demo.mixin'
    _description = 'Demo Model Tutorial'

    name = fields.Char(required=True, string="名稱")

```

這邊 `demo.model.tutorial` 繼承了 `demo.mixin`, 所以在 db table 中,

會看到 `demo.mixin` 中的 fields.

![alt tag](https://i.imgur.com/0fYEUiS.png)

這邊稍微注意注意一下,

在 db 中只會有 `demo.model.tutorial` 的 table, 不會有 `demo.mixin` 的 table,

但是會有 `demo.mixin` 中的 fields, 也看不到 `test_2` fields, 原因是他是 _compute_field,

如果你想要看到包含 `test_2` fields, 可以到 odoo 的 model 後台觀看

![alt tag](https://i.imgur.com/oiASNIP.png)

`demo.mixin` 的 model 在 odoo 的後台也可以觀看 (但 db 中不會出現)

![alt tag](https://i.imgur.com/HkftQT3.png)

![alt tag](https://i.imgur.com/3ttRkzP.png)

在 tree, form ...... 都可以使用 `demo.mixin` 的 fields

![alt tag](https://i.imgur.com/hFCf2mR.png)

因為這個範例剛好只有一個 model 被繼承, 如果有兩個以上的 model 就更適合這樣寫了, 如下

```python
......

class DemoModelTutorial(models.Model):
    _name = 'demo.model.tutorial'
    _inherit = 'demo.mixin'
    _description = 'Demo Model Tutorial'

    ......

class DemoModelTutorial_v2(models.Model):
    _name = 'demo.model.tutorial.v2'
    _inherit = 'demo.mixin'
    _description = 'Demo Model Tutorial v2'

    ......

class DemoModelTutorial_v3(models.Model):
    _name = 'demo.model.tutorial.v3'
    _inherit = 'demo.mixin'
    _description = 'Demo Model Tutorial v3'

    ......
```

這樣每個 model, 都會擁有 `demo.mixin` 的 fields, 不需要把重複的 code

在每個 model 中都寫一遍.

剛剛介紹的 model 是我們新建立的, 假如今天有一個 model 已經存在了,

想要用同樣的方式擴充 model, 可參考 [models/models_v2.py](models/models_v2.py)

```python
from odoo import models, fields, api

class DemoMixin2(models.AbstractModel):
    _name = 'demo.mixin2'
    _description = 'Demo Mixin2'

    test_v2 = fields.Float(
        string='test_v2',
        default='2.2'
    )

class DemoModelTutorial(models.Model):
    _name = 'demo.model.tutorial'
    _inherit = ['demo.model.tutorial', 'demo.mixin2']

    pass

```

這篇文章其實就是將 [odoo 實作 scan barcode](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_sale_scan_barcode) 的概念再說一次.

也可以去了解一下 [什麼是 Mixin in python](https://github.com/twtrubiks/python-notes/tree/master/what_is_the_mixin),

相信這樣大家會更了解他們的概念 :smile: