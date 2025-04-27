# odoo 實作 scan barcode

建議觀看影片, 因為 scanner 會看的更清楚 :smile:

[Youtube Tutorial - odoo - 實作 scan barcode](https://youtu.be/o2THTpLmUec)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

odoo 搭配 scanner,

主要介紹 odoo 中如何實作 scan barcode.

## 說明

首先是 [__manifest__.py](__manifest__.py) 的部份,  記得要加上 `barcodes`

```python
......

'depends': [......, 'barcodes'],
......
```

接著看 [models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_sale_scan_barcode/models/models.py)


```python
......

class SaleOrderBarcodes(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "barcodes.barcode_events_mixin"]

    _barcode_scanned = fields.Char(string='Barcode', help="Here you can provide the barcode for the product")

    @api.multi
    def on_barcode_scanned(self, barcode):
        product_obj = self.env['product.product'].search([('barcode', '=', barcode)], limit=1)
        val = {
            'product_id': product_obj,
            'product_uom_qty': 1,
            'price_unit': product_obj.lst_price
        }
        self.order_line = [(0, 0, val)]
```

`_inherit` 必須繼承 `barcodes.barcode_events_mixin`,

然後要定義 `_barcode_scanned`,

資料庫中是不會有 `_barcode_scanned` 的欄位, 因為 BarcodeEventsMixin 是 AbstractModel,

如果不了解甚麼是 AbstractModel, 請參考 [odoo 手把手教學 - AbstractModel](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_abstractmodel_tutorial).

也需要實作 `on_barcode_scanned`, 當 scanner 掃描到 barcode 時, 就會去觸發這個 method.

實作的邏輯很簡單,

就是使用所掃描到的 barcode 去 `product.product` 中尋找對應的產品,

如果有, 就自動增加到 sale order line 中.

如果不知道如何增加 One2many M2X record,

可參考 [odoo 手把手教學 - 使用 python 增加取代 One2many M2X record](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_expense_tutorial_v1#odoo-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---%E4%BD%BF%E7%94%A8-python-%E5%A2%9E%E5%8A%A0%E5%8F%96%E4%BB%A3-one2many-m2x-record---part8)

`barcode_events_mixin.py` 可參考原始碼中的 `addons/barcodes/models/barcode_events_mixin.py`

```python
......
class BarcodeEventsMixin(models.AbstractModel):
    """ Mixin class for objects reacting when a barcode is scanned in their form views
        which contains `<field name="_barcode_scanned" widget="barcode_handler"/>`.
        Models using this mixin must implement the method on_barcode_scanned. It works
        like an onchange and receives the scanned barcode in parameter.
    """

    _name = 'barcodes.barcode_events_mixin'
    _description = 'Barcode Event Mixin'

    _barcode_scanned = fields.Char("Barcode Scanned", help="Value of the last barcode scanned.", store=False)

    @api.onchange('_barcode_scanned')
    def _on_barcode_scanned(self):
        barcode = self._barcode_scanned
        if barcode:
            self._barcode_scanned = ""
            return self.on_barcode_scanned(barcode)

    def on_barcode_scanned(self, barcode):
        raise NotImplementedError("In order to use barcodes.barcode_events_mixin, method on_barcode_scanned must be implemented")
```

views 的部份可參考 [views/view.xml](https://github.com/twtrubiks/demo_config_settings/tree/master/demo_sale_scan_barcode/views/view.xml)

```xml
<?xml version="1.0"?>
<odoo>
    <record id="view_order_form_scan_barcode" model="ir.ui.view">
        <field name="name">sale.order.form.scan.barcode</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="arch" type="xml">
            <field name="partner_id"  position="after">
                <!-- invisible="1" -->
                <field name="_barcode_scanned" widget="barcode_handler"/>
            </field>
        </field>
    </record>
</odoo>
```

這邊主要是加上 `<field name="_barcode_scanned" widget="barcode_handler"/>`,

也可以選擇將它隱藏起來, 是不影響工作的.

將 addons 裝起來之後, 先到 Product Variants 設定 barcode,

![alt tag](https://i.imgur.com/m9o8vHY.png)

範例 barcode

![alt tag](https://i.imgur.com/0S5Bsu9.png)

記住一定要進入編輯 (Edit) 狀態, 否則會出現錯誤 :exclamation: :exclamation:

![alt tag](https://i.imgur.com/cNzb2VJ.png)

也請記得要 focus 在當下的 odoo 畫面 (否則系統會抓不到) :exclamation: :exclamation:

scanner 掃到條碼後, 就會將對應的產品帶入 sale order line 中.

這邊建議觀看影片, 會比較清楚 :smile:

scanner 其實也是將 barcode 或是 qrcode 內的資料讀取出來而已

![alt tag](https://i.imgur.com/K457P5w.png)