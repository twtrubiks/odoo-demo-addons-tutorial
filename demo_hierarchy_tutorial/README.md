# odoo hierarchy 實作

建議觀看影片, 會更清楚:smile:

* [Youtube Tutorial - odoo 手把手教學 hierarchy - part1]() - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_hierarchy_tutorial#%E8%AA%AA%E6%98%8E)

* [Youtube Tutorial - odoo 手把手教學 hierarchy - part2]() - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_hierarchy_tutorial#%E8%AA%AA%E6%98%8E-child_of-%E5%92%8C-parent_of)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

主要介紹 odoo 中如何實現 階層(hierarchy) 的關係.

## 說明

* [Youtube Tutorial - odoo 手把手教學 hierarchy - part1]()

之前不管是介紹 Many2one 還是 One2many, 都是對別的 model 產生關聯,

那有沒有和自己產生關聯的呢:smile:

* [odoo 手把手教學 - Many2one - part1](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_expense_tutorial_v1#odoo-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---many2one---part1)

* [odoo 手把手教學 - One2many - part3](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_expense_tutorial_v1#odoo-%E6%89%8B%E6%8A%8A%E6%89%8B%E6%95%99%E5%AD%B8---one2many---part3)

答案是有的哦, 就是 odoo 中的 階層(hierarchy) 的關係:satisfied:

階層(hierarchy) 的關係範例圖如下,

![alt tag](https://i.imgur.com/jFmmet1.png)

接著來看教學的範例,

[models/models.py](models/models.py)

```python
class DemoHierarchyTutorial(models.Model):
    _name = 'demo.hierarchy'
    _description = 'Demo Hierarchy Tutorial'

    name = fields.Char(string='name', index=True)
    parent_id = fields.Many2one('demo.hierarchy', string='Related Partner', index=True)
    parent_name = fields.Char(related='parent_id.name', readonly=True, string='Parent name')
    child_ids = fields.One2many('demo.hierarchy', 'parent_id', string='Contacts', domain=[('active', '=', True)])
    active = fields.Boolean(default=True)
```

比較特別的就是 `parent_id` 和 `child_ids` 都關聯到同一個 model (也就是自己本身 `demo.hierarchy`),

然後一個是 Many2one `parent_id` 和 One2many `child_ids`.

[views/view.xml](views/view.xml)

```xml
<record id="view_form_demo_hierarchy" model="ir.ui.view">
<field name="name">Demo Hierarchy Form</field>
<field name="model">demo.hierarchy</field>
<field name="arch" type="xml">
    <form string="Demo Hierarchy">
    <sheet>
        <group>
        <field name="name"/>
        <field name="active"/>
        <field name="parent_id"/>
        <field name="parent_name"/>
        </group>
        <notebook>
        <page string="Hierarchy">
            <field name="child_ids" mode="kanban">
            <form string="Contact / Address">
                <sheet>
                <field name="parent_id" invisible="1"/>
                <hr/>
                <group>
                    <field name="name" string="Contact Name"/>
                </group>
                </sheet>
            </form>
            </field>
        </page>
        </notebook>
    </sheet>
    </form>
</field>
</record>
```

寫法和一般的 Many2one 或 One2many 是一樣的, 然後在 One2many 裡面,

將 `parent_id` 隱藏起來, 因為不需要.

`<field name="parent_id" invisible="1"/>`

先來建立一比 `demo.hierarchy` (test1), `parent_id` 先不填

![alt tag](https://i.imgur.com/sZGTOvZ.png)

點選 add 再建立一比 `demo.hierarchy` (test2)

![alt tag](https://i.imgur.com/EfUkYeN.png)

呈現效果如下, test2 的 parent 就是 test1

![alt tag](https://i.imgur.com/pHWlbU5.png)

點選 add 再建立一比 `demo.hierarchy` (test3),

呈現效果如下, test2 和 test1 的 parent 都是 test1

![alt tag](https://i.imgur.com/yVhz0Be.png)

tree 的部份

![alt tag](https://i.imgur.com/6Hsl2Gp.png)

db 中的狀態

![alt tag](https://i.imgur.com/kuHStcy.png)

## 說明 child_of 和 parent_of

* [Youtube Tutorial - odoo 手把手教學 hierarchy - part2]()

在 odoo 中很常看到 child_of 和 parent_of,

可以參考 Contact `res.partner`.

odoo 原始碼中的範例, 路徑 `odoo/addons/base/models/res_partner.py`

```python
class Partner(models.Model):
    _description = 'Contact'
    _inherit = ['format.address.mixin']
    _name = "res.partner"
    _order = "display_name"

    ......
    parent_id = fields.Many2one('res.partner', string='Related Company', index=True)
    parent_name = fields.Char(related='parent_id.name', readonly=True, string='Parent name')
    child_ids = fields.One2many('res.partner', 'parent_id', string='Contacts', domain=[('active', '=', True)])
    ref = fields.Char(string='Internal Reference', index=True)
    ......
```

其中 parent_id 是 Many2one 的關係 , 而 child_ids 則是 One2many的關係.

階層關係如下

![alt tag](https://i.imgur.com/jFmmet1.png)

db 關係如下

![alt tag](https://i.imgur.com/4TOjc8k.png)

階層關係如下

![alt tag](https://i.imgur.com/cCAonbi.png)

db 關係如下

![alt tag](https://i.imgur.com/FQ7s9C0.png)

`child_of`

```python
>>> self.env['res.partner'].search([('id', 'child_of', 14)])  #(小技巧, 從後面看回來, 14 的孩子)
res.partner(14, 26, 33, 27, 68)
```

```python
>>> self.env['res.partner'].search([('id', 'child_of', [11])])
res.partner(11, 20, 22, 31, 23)
```

child_of 也可以一次找多個

```python
>>> self.env['res.partner'].search([('id', 'child_of', [14, 11])])
res.partner(14, 26, 33, 27, 68......)
```

`parent_of`

```python
>>> self.env['res.partner'].search([('id', 'parent_of', 68)]) #(小技巧, 從後面看回來, 68 的父親)
res.partner(14, 68, 26)
```

在 odoo 原始碼中, 可能會看到以下的 code

`('company_id','child_of',[user.company_id.id])]`

問題點在於為甚麼要別使用 `[]`

我這邊猜測應該是為了要避免 WARNING

```python
>>> self.env['res.partner'].search([('id', 'parent_of', [False])])
res.partner()
>>> self.env['res.partner'].search([('id', 'parent_of', False)])  # 會有 WARNING
2020-07-29 WARNING odoo919 odoo.osv.expression: Unexpected domain [('id', 'parent_of', False)], interpreted as False
res.partner()
```