# odoo14 觀念 - image mixin

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo14 手把手教學 - image mixin](https://youtu.be/2EJNTLldHOA)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 14 中的 `image.mixin` 這個 model.

這個 model 適合使用在需要產生不同尺寸大小的圖片.

## 說明

這邊要注意一下, `image.mixin` 是 odoo13 odoo14 開始才有的,

(odoo12 是沒有這個 `image.mixin` model)

如果你對 Mixin 有興趣, 也可參考 [什麼是 Mixin in python](https://github.com/twtrubiks/python-notes/tree/master/what_is_the_mixin):smile:

可參考 odoo14 原始碼中的 `odoo/addons/base/models/image_mixin.py`

```python
......

class ImageMixin(models.AbstractModel):
    _name = 'image.mixin'
    _description = "Image Mixin"

    # all image fields are base64 encoded and PIL-supported

    image_1920 = fields.Image("Image", max_width=1920, max_height=1920)

    # resized fields stored (as attachment) for performance
    image_1024 = fields.Image("Image 1024", related="image_1920", max_width=1024, max_height=1024, store=True)
    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512, store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256, store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
......
```

這邊也請特別注意一下他是 `AbstractModel`.

關於 `AbstractModel` 的特性, 之前的文章裡也有介紹過,

請參考 [介紹 AbstractModel](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_abstractmodel_tutorial)


寫法很簡單, 只需要繼承 `image.mixin` 即可,

先來看 [models/model.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/14.0/demo_image_mixin/models/model.py)

```python
from odoo import models, fields, api

class DemoImage(models.Model):
    _name = 'demo.image'
    _description = 'Demo Image'
    _inherit = ['image.mixin']

    name = fields.Char(string='Name', required=True)
    # image_1920 = fields.Image(required=True)
```

你沒看錯, 就是直接繼承 `image.mixin`.

然後他會有幾個特性,

首先, 這些 images fields 不會在資料庫中產生對應的 table (但你可以使用 fields).

再來是只有 `image_1920` 是可編輯(寫)得, 其他的 `image_1024` `image_512`......

都是只能讀而已 (原因是他們都有 `related="image_1920"`),

當你編輯 `image_1920` 時, 會自動產生出其他的尺寸.

如果今天你想要讓 `image_1920` 必填, 也直接覆蓋掉即可, 如同我註解寫的那樣.

[views/view.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/14.0/demo_image_mixin/views/view.xml) 的部份

```xml
......
<record id="view_form_demo_image" model="ir.ui.view">
    <field name="name">Demo Image Form</field>
    <field name="model">demo.image</field>
    <field name="arch" type="xml">
      <form>
        <group>
          <field name="name"/>
          <field name="image_1920" widget="image" options="{'preview_image': 'image_128'}" />
          <field name="image_256" widget="image"/>
          <field name="image_128" widget="image"/>
        </group>
      </form>
    </field>
</record>
......
```

你可以看到這邊除了 `image_1920` fields 之外, 也可以使用其他的尺寸

`image_128` `image_256`....

![alt tag](https://i.imgur.com/cIaIBUX.png)

![alt tag](https://i.imgur.com/bzbzNOP.png)

如果你只想要產生單一圖片, 不需要其他的尺寸, 還是可以直接使用 `fields.Binary`.

最後提醒大家, 超大容量的圖片, 對網站絕對是一個負擔, 不只網路變慢, SEO的排名

可能也會往後掉, 所以, 建議使用適合的圖片大小:smile:
