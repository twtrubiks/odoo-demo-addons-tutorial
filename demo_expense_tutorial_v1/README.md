# demo_expense_tutorial_v1

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - (等待新增)odoo 手把手建立第一個 addons - Many2one, Many2many, One2many]()

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[demo_odoo_tutorial](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial) -  odoo 手把手建立第一個 addons

這篇主要介紹 Many2one, Many2many, One2many 這三個東西,

以下將介紹這個 addons 的結構

## 說明

先來看 [models/models.py](models/models.py)

`Many2one`

```python
......
class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    _description = 'Demo Expense Tutorial'

    name = fields.Char('Description', required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
......
```

![alt tag](https://i.imgur.com/lBj9pgz.png)

一個 `hr.employee` 可以對到很多個 `demo.expense.tutorial`,

所以是 多(`demo.expense.tutorial`) 對 一(`hr.employee`) 的關係,

來看 db 中的狀況

`demo_expense_tutorial` 會多出一個欄位 ( 對應 `hr_employee` 的 id )

![alt tag](https://i.imgur.com/8BVrrJa.png)

`user_id` field 中的 `default=lambda self: self.env.user` 代表預設的值會設定當前登入的 user

![alt tag](https://i.imgur.com/QiDj6iM.png)

因為 One2many 比較特別, 所以我們先介紹 Many2many:laughing:

`Many2many`

要建立 Many2many 之前, 一定要先定義一個 model,

先定義 DemoTag (也請記得設定 [security/ir.model.access.csv](security/ir.model.access.csv) )

[models/models.py](models/models.py)

```python
......
class DemoTag(models.Model):
    _name = 'demo.tag'
    _description = 'Demo Tags'

    name = fields.Char(string='Tag Name', index=True, required=True)
    active = fields.Boolean(default=True, help="Set active.")
......
```

然後接著到底下 [models/models.py](models/models.py)

```python
......
class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
......
    # https://www.odoo.com/documentation/12.0/reference/orm.html#odoo.fields.Many2many
    # Many2many(comodel_name=<object object>, relation=<object object>, column1=<object object>, column2=<object object>, string=<object object>, **kwargs)
    #
    # relation: database table name
    #

    # By default, the relationship table name is the two table names
    # joined with an underscore and _rel appended at the end.
    # In the case of our books or authors relationship, it should be named demo_expense_tutorial_demo_tag_rel.

    tag_ids = fields.Many2many('demo.tag', 'demo_expense_tag', 'demo_expense_id', 'tag_id', string='Tges')
......
```

Many2many 比較多欄位, 我來說明一下,

`comodel_name` 為 `demo.tag` (需要對應的 model)

`relation` 為 `demo_expense_tag` (table 名稱),

Many2many 會多出一個 table, 這邊是針對 table 命名,

也就是 db 中的 table 名稱,

![alt tag](https://i.imgur.com/B7ren2r.png)

如果你沒填 `relation` 這個值, 預設的 table 名稱會是 model名稱 + comodel_name + `_rel`,

所以也就會是 `demo_expense_tutorial_demo_tag_rel`.

`column1` 為 `demo_expense_id`, `demo.expense.tutorial` table 中對應的 id.

`column2` 為 `tag_id`, `demo.tag` table 中對應的 id.

繼續看 [models/models.py](models/models.py)

```python
......
    # Related (Reference) fields (不會存在 db)
    # readonly default 為 True
    # store default 為 False
    gender = fields.Selection('Gender', related='employee_id.gender')
......
```

`fields.Selection` 就只是下拉選單而已, 比較特別的是 `related` 這個,

`related='employee_id.gender'` 這邊的意思是, 會自己去找 employee_id 中的 gender,

到 employee 中找到 gender 為 Male

![alt tag](https://i.imgur.com/GDOC0hS.png)

DemoExpenseTutorial 中的 `gender` 自然會是 Male,

![alt tag](https://i.imgur.com/mJrzLjk.png)

但要注意幾件事情,

`related` 預設的 field 是不會儲存在 db 中的, store default 為 False,

你在 table 中是找不到 `gender` field 的 (如下圖),

如果你想要儲存在 db 中的, 請另外設定 `store=Ture`,

![alt tag](https://i.imgur.com/0Xcvzas.png)

然後 readonly default 為 True, 也就是說你是不可以去修改的,

( 如果要修改請去 employee 中找到 gender 修改 )

![alt tag](https://i.imgur.com/mJrzLjk.png)

接著來看最後一個

`One2many`

![alt tag](https://i.imgur.com/lV2J3Tu.png)

[models/models.py](models/models.py)

一個 `demo.expense.sheet.tutorial` 可以對應很多個 `demo.expense.tutorial`

所以是 一(`demo.expense.sheet.tutorial`) 對 多(`demo.expense.tutorial`) 的關係,

```python
......
class DemoExpenseSheetTutorial(models.Model):
    _name = 'demo.expense.sheet.tutorial'
    _description = 'Demo Expense Sheet Tutorial'

    name = fields.Char('Expense Demo Report Summary', required=True)

    # One2many is a virtual relationship, there must be a Many2one field in the other_model,
    # and its name must be related_field
    expense_line_ids = fields.One2many(
        'demo.expense.tutorial', # related model
        'sheet_id', # field for "this" on related model
        string='Expense Lines')
```

說明 expense_line_ids 裡面的參數意義,

`demo.expense.tutorial` 代表關連的 model (必填)

`sheet_id` 代表所關連 model 的 field (必填)

也就是說如果你要建立 One2many, 一定也要有一個 Many2one,

但如果建立 Many2one 則不一定要建立 One2many.

One2many 是一個虛擬的欄位, 你在資料庫中是看不到它的存在(如下圖)

![alt tag](https://i.imgur.com/F6YTOdq.png)

你只會看到 Many2one 中的 sheet_id

![alt tag](https://i.imgur.com/lsiLpZK.png)

[models/models.py](models/models.py), `demo.expense.tutorial` 中的 sheet_id

```python
class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    _description = 'Demo Expense Tutorial'
    ......
    sheet_id = fields.Many2one('demo.expense.sheet.tutorial', string="Expense Report")
    ......
```

記得也要設定對應的 [security/ir.model.access.csv](security/ir.model.access.csv) 和 [security/security.xml](security/security.xml).

[views/view.xml](views/view.xml)

```xml
......
  <record id="view_form_demo_expense_tutorial" model="ir.ui.view">
    <field name="name">Demo Expense Tutorial Form</field>
    ......
            <!-- <field name="tag_ids"/> -->
            <field name="tag_ids" widget="many2many_tags"/> <!-- widget -->
            <field name="sheet_id"/>
......

```

在 odoo 中很有多 widget, 大家可以改成其他的 widget 試試看, 像是 many2many_tags 的 widget

![alt tag](https://i.imgur.com/UBYyUcf.png)

[views/view.xml](views/view.xml)

```xml
......
    <record id="view_form_demo_expense_sheet_tutorial" model="ir.ui.view">
    <field name="name">Demo Expense Sheet Tutorial Form</field>
    <field name="model">demo.expense.sheet.tutorial</field>
    <field name="arch" type="xml">
      <form string="Demo Expense Sheet Tutorial">
        <sheet>
          <group>
            <field name="name"/>
          </group>
          <notebook>
              <page string="Expense">
                <field name="expense_line_ids">
                  <tree>
                    <field name="name"/>
                    <field name="employee_id"/>
                    <field name="tag_ids" widget="many2many_tags"/>
                  </tree>
                </field>
              </page>
          </notebook>
        </sheet>
      </form>
    </field>
  </record>
......
```

在 `view_form_demo_expense_sheet_tutorial` 裡的 One2many 中的 expense_line_ids fields,

就把需要的欄位填進去即可,

![alt tag](https://i.imgur.com/jiFHHST.png)

[views/view.xml](views/view.xml)

來看這個 filter 的功能

```xml
......
<record id="view_filter_demo_expense_tutorial" model="ir.ui.view">
  <field name="name">Demo Expense Tutorial Filter</field>
  <field name="model">demo.expense.tutorial</field>
  <field name="arch" type="xml">
      <search string="Demo Expense Tutorial Filter">
          <field name="name" string="Name"/>
          <group expand="0" string="Group By">
            <filter string="Sheet" name="sheet" domain="[]" context="{'group_by': 'sheet_id'}"/>
            <filter string="Employee" name="employee" domain="[]" context="{'group_by': 'employee_id'}"/>
          </group>
      </search>
  </field>
</record>
......
```

`<field name="name" string="Name"/>` 主要是在 tree 中搜尋

![alt tag](https://i.imgur.com/eBmc2Je.png)

`<filter string="Sheet" name="sheet" domain="[]" context="{'group_by': 'sheet_id'}"/>`

`<filter string="Employee" name="employee" domain="[]" context="{'group_by': 'employee_id'}"/>`

依照特定的 fields 分組

![alt tag](https://i.imgur.com/jojaYtz.png)

點選後的狀態

![alt tag](https://i.imgur.com/acyqVIA.png)

再來看看

[security/ir_rule.xml](security/ir_rule.xml)

```xml
......
    <data noupdate="1">

        <record id="ir_rule_demo_expense_user" model="ir.rule">
            <field name="name">Demo Expense User</field>
            <field name="model_id" ref="model_demo_expense_tutorial"/>
            <field name="domain_force">[('employee_id.user_id.id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('demo_expense_tutorial_group_user'))]"/>
        </record>

        <record id="ir_rule_demo_expense_manager" model="ir.rule">
            <field name="name">Demo Expense Manager</field>
            <field name="model_id" ref="model_demo_expense_tutorial"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('demo_expense_tutorial_group_manager'))]"/>
        </record>
    </data>
......
```

`noupdate="1"`的意思為當更新 addons 時, 是不是允許重新 import data,

`noupdate="1"`

假如我們在安裝完 addons 之後, 去刪除 record data, 然後再重新去更新 addons,

你會發現你刪除的 data 並沒有被安裝回來 (只能先移除 addons 再重新安裝).

`noupdate="0"`

假如我們在安裝完 addons 之後, 去刪除 record data, 然後再重新去更新 addons,

你會發現你刪除的 data 會被安裝回來.

`id="ir_rule_demo_expense_user"` 第一段為針對 `demo_expense_tutorial_group_user`

限制 `domain_force`, 規則很簡單, 這類的 user 只能看到自己的單子, 也就是

`[('employee_id.user_id.id', '=', user.id)]`.

`id="ir_rule_demo_expense_manager"` 針對 `demo_expense_tutorial_group_manager`

限制 `domain_force`, 這邊比較特別 `[(1, '=', 1)]`, 代表沒有限制, 也就是全部的單子都

可以看到.

`demo` 用戶為 User, 所以只能看到自己的單子

![alt tag](https://i.imgur.com/dX9QuMj.png)

`Admin` 用戶為 Manager, 所以能看到全部的單子

![alt tag](https://i.imgur.com/CFMsgie.png)

接下來介紹前面跳過的部份, 也就是透過 button 的方式呼叫 view, form,

[models/models.py](models/models.py)

```python
class DemoExpenseTutorial(models.Model):
    _name = 'demo.expense.tutorial'
    _description = 'Demo Expense Tutorial'
    ......

    @api.multi
    def button_sheet_id(self):
        return {
            'view_mode': 'form',
            'res_model': 'demo.expense.sheet.tutorial',
            'res_id': self.sheet_id.id,
            'type': 'ir.actions.act_window'
        }
```

透過前端呼叫 `button_sheet_id`, 會回傳屬於它的 sheet_id

![alt tag](https://i.imgur.com/gUUgk9g.png)

點進去會直接進入 sheet 中的 form

![alt tag](https://i.imgur.com/lU6P9Oj.png)

[views/view.xml](views/view.xml)

前端的部份就是呼叫 `button_sheet_id`

```xml
<record id="view_form_demo_expense_tutorial" model="ir.ui.view">
  <field name="name">Demo Expense Tutorial Form</field>
  <field name="model">demo.expense.tutorial</field>
  <field name="arch" type="xml">
    <form string="Demo Expense Tutorial">
      <sheet>
        <div class="oe_button_box" name="button_box">
          <button class="oe_stat_button" name="button_sheet_id"
                  string="SHEET ID" type="object"
                  attrs="{'invisible':[('sheet_id','=', False)]}" icon="fa-bars"/>
        </div>
        ......
      </sheet>
    </form>
  </field>
</record>
```

既然找了 sheet_id, 也來做一個反查回來的, 也就是透過 sheet_id 找到 `demo.expense`,

[models/models.py](models/models.py)

```python
class DemoExpenseSheetTutorial(models.Model):
    _name = 'demo.expense.sheet.tutorial'
    _description = 'Demo Expense Sheet Tutorial'

    ......

    @api.multi
    def button_line_ids(self):
        return {
            'name': 'Demo Expense Line IDs',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'demo.expense.tutorial',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('sheet_id', '=', self.id)],
        }
```

`res_model` 為目標的 model `demo.expense.tutorial`.

`domain` 稍微說明一下 `[('sheet_id', '=', self.id)],`,

`sheet_id` 是指目標 model `demo.expense.tutorial` 的 sheet_id,

`self.id` 是指當下 model `demo.expense.sheet.tutorial` 的 id.

![alt tag](https://i.imgur.com/oqDOi3p.png)

點下去會帶出它的 `demo.expense.tutorial`

![alt tag](https://i.imgur.com/2ZSl9Qj.png)

[views/view.xml](views/view.xml) 的部份

```xml
......
<record id="view_form_demo_expense_sheet_tutorial" model="ir.ui.view">
  <field name="name">Demo Expense Sheet Tutorial Form</field>
  <field name="model">demo.expense.sheet.tutorial</field>
  <field name="arch" type="xml">
    <form string="Demo Expense Sheet Tutorial">
      <sheet>
        <div class="oe_button_box" name="button_box">
          <button class="oe_stat_button" name="button_line_ids"
                  string="SHEET IDs" type="object"
                  attrs="{'invisible':[('expense_line_ids','=', False)]}" icon="fa-bars"/>
        </div>
        ......
      </sheet>
    </form>
  </field>
</record>
```