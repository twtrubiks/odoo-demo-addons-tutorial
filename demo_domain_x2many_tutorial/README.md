# odoo 17 domain one2many many2many 教學

這篇文章會寫個簡單的範例, 當 domain 遇到 One2many 或 Many2many 的使用方法,

## 說明

- seller_ids (One2many)

```python

......

class DemoDomainTutorial(models.Model):
    _name = 'demo.domain.tutorial'
    _description = 'Demo Domain Tutorial'

    name = fields.Char('Description', required=True)
    partner_id = fields.Many2one('res.partner', string="Partner")
    product_id = fields.Many2one('product.product', string="Product",
        domain="[('seller_ids.partner_id', '=', partner_id)]")
......
```

當今天 seller_ids (One2many) 底下的 partner_id 有包含在當下選擇的 partner_id 時,

才會是對應的 product

例如 Individual Workplace 有設定 Vendor Deco Addict

![alt tag](https://i.imgur.com/99OKpuO.png)

就會發現 Product 可以選這個產品.

![alt tag](https://i.imgur.com/zTDLabs.png)

前面是在 model 定義 domain, 也可以在 xml 底下定義,

```xml
<page string="Line">
    <field name="line_ids" >
    <tree editable="top">
        <!-- example 1 -->
        <field name="product_id" domain="[('seller_ids.partner_id', '=', parent.partner_id)]" options="{'no_create': True}"/>
    </tree>
    </field>
</page>
```

這邊你可能會注意到 parent, 這個是 odoo 的用法, 可以去取 父親parent 的值來使用.

- taxes_id (Many2many)

例如 15 這個設定 15%

![alt tag](https://i.imgur.com/eSavWZi.png)

當選下 15% 的時候, 也可以選擇 15

![alt tag](https://i.imgur.com/IDkWmRM.png)

這邊使用了 `in`, 因為都是多對多的關係

```xml
<page string="Line">
    <field name="line_ids" >
    <tree editable="top">
        <!-- example 2 -->
        <field name="product_id" domain="[('taxes_id', 'in', parent.taxes_ids)]" options="{'no_create': True}"/>
    </tree>
    </field>
</page>
```