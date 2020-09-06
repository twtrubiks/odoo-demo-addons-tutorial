# demo_delegation_inheritance

建議觀看影片, 會更清楚:smile:

[(等待新增)Youtube Tutorial - odoo demo_delegation_inheritance]()

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[demo_odoo_tutorial](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) -  odoo 手把手建立第一個 addons

本篇文章主要介紹 demo_delegation_inheritance 這部份

## 說明

在開始介紹範例之前, 請先看下圖

Model inheritance ( `_inherit` vs `_inherits` ),

[inheritance](https://www.odoo.com/documentation/12.0/howtos/backend.html#inheritance)

![alt tag](https://i.imgur.com/IRPk1By.png)

`_inherits` 以下為官方說明

```txt
The second inheritance mechanism (delegation) allows to link every record of a model to a record in a parent model, and provides transparent access to the fields of the parent record.
```

```python
class DelegationInheritance(models.Model):
    _name = 'new'
    _inherits = 'obj1'
```

幾個重點,

Stored in different tables (會儲存在不同的 table 中)

`new` instances contain am embedded.

`obj1` instance with synchronized values.

(同步的意思就是會幫你自動建立, 等等來看實例說明)

先來看 [models/models.py](models/models.py)

```python
class DelegationInheritance(models.Model):
    _name = 'demo.delegation'
    _description = 'Demo DelegationInheritance'
    _inherits = {"res.partner": "partner_id"}

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, ondelete="cascade")

    first_name = fields.Char('First Name', size=16)
    ......
```

再來看 [views/view.xml](views/view.xml)

```xml
......
<record id="view_form_demo_delegation_tutorial" model="ir.ui.view">
<field name="name">Demo Delegation Tutorial Form</field>
<field name="model">demo.delegation</field>
<field name="arch" type="xml">
    <form string="Demo Delegation Tutorial">
    <sheet>
        <group>
            <!-- res.partner -->
            <field name="partner_id" invisible="1" attrs="{'required': [('id', '!=', False)]}"/>
            <field name="name"/>
            <field name="company_id"/>
            <!-- res.partner -->

            <!-- demo.delegation -->
            <field name="first_name"/>
            <!-- demo.delegation -->
        </group>
    </sheet>
    </form>
</field>
</record>
......
```

其實它有點特殊, 在裡面甚至可以使用 (委派 Delegation) `res.partner` 的欄位.

當建立 `demo.delegation` 時, 也會自動幫你建立 `partner_id`.

你可能會問我為甚麼沒有 `name` field, 但是卻可以使用 `name`:question:

因為這個 `name` 其實是屬於 `res.partner` 的:smile:

以下操作一遍流程,

在 `demo.delegation` 中建立一筆資料

![alt tag](https://i.imgur.com/vfPNsva.png)

在 `res.partner` 中也會自動建立一筆資料

![alt tag](https://i.imgur.com/JZ2EUv1.png)

接著從 db 中看資料怎麼跑

在 `demo.delegation` 中只紀錄了 `partner_id` 而已, 當然還有 `first_name`.

![alt tag](https://i.imgur.com/i7SyECl.png)

其他的 `name` `company_id` 都是儲存在 `res.partner` 中的.

(雖然是在 `demo.delegation` 中輸入的, 但這就是委派的概念)

![alt tag](https://i.imgur.com/UHOqrwx.png)

小結論, 父類別`res.partner`的 field 會儲存在父類別`res.partner`的 table 中,

而新的模型`demo.delegation`的 field 則會儲存在新的模型`demo.delegation`的 table 中.

當使用新的模型`demo.delegation`時, 可以看到父類別`res.partner`的資料.

當使用父類別`res.partner`時, **只能看到**父類別`res.partner`的資料.

委派最重要的目的就是避免在很多的 table 中建立重複的資料. (達到共用的效果:smile:)

在原始碼中, 也有幾個範例可以參考:smile:

第一個範例為 `res.users` 以及 `res.partner`

```python
# odoo/addons/base/models/res_users.py
class Users(models.Model):
    """ User class. A res.users record models an OpenERP user and is different
        from an employee.

        res.users class now inherits from res.partner. The partner model is
        used to store the data related to the partner: lang, name, address,
        avatar, ... The user model is now dedicated to technical data.
    """
    _name = "res.users"
    _description = 'Users'
    _inherits = {'res.partner': 'partner_id'}

    ......

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
            string='Related Partner', help='Partner-related data of the user')

    ......

# odoo/addons/base/models/res_partner.py
class Partner(models.Model):
    _description = 'Contact'
    _inherit = ['format.address.mixin']
    _name = "res.partner"
    _order = "display_name"

    ......
```

當你建立 `res.users` 時, 也會自動建立一個 `res.partner`. (可搭配 db 觀看結果)

在 `res.users` 底下, 可以任意得使用 `res.partner` field, 但相反過來,

在 `res.partner` 底下, 只可以使用 `res.partner` 自己的 field.

第二個範例為 `product.product` 以及 `product.template`

```python
# addons/product/models/product.py
class ProductProduct(models.Model):
    _name = "product.product"
    _description = "Product"
    _inherits = {'product.template': 'product_tmpl_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'default_code, name, id'

    ......
	product_tmpl_id = fields.Many2one(
		'product.template', 'Product Template',
		auto_join=True, index=True, ondelete="cascade", required=True)
    ......

# addons/product/models/product_template.py
class ProductTemplate(models.Model):
    _name = "product.template"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'image.mixin']
    _description = "Product Template"
    _order = "name"
    ......
```

