# odoo 手把手建立第一個 addons

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part1](https://youtu.be/GMrPakLNh8g) - 介紹 model - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E4%BB%8B%E7%B4%B9-model)

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part2](https://youtu.be/EnD-VxuILWM) - 介紹 security, menu, tree, form - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E4%BB%8B%E7%B4%B9-security-menu-tree-form)

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part3](https://youtu.be/25MSbidCf1U) - 介紹 report, controller - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E4%BB%8B%E7%B4%B9-report-controller)

* [Youtube Tutorial - 說明 odoo manifest 中的 auto_install](https://youtu.be/xTezPfJAJ_Q) - [文章快速連結](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial#%E8%AA%AA%E6%98%8E-odoo-manifest-%E4%B8%AD%E7%9A%84-auto_install)

建議觀看影片, 會更清楚:smile:

以下將介紹這個 addons 的結構

## 說明

### 介紹 model

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part1](https://youtu.be/GMrPakLNh8g) - 介紹 model

首先是 `__manifest__.py`, 比較重要的是 `depends`,

```python
{
    'name': "demo odoo tutorial",
    ......

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data_demo_odoo.xml',
        'views/menu.xml',
        'views/view.xml',
        'reports/report.xml',
        'views/demo_odoo_template.xml',
    ],
    ......
}

```

在 odoo 的世界中, 一定會看到某個 addons 依賴 xxx addons, 想簡單一點,

你可以把它想成是模組化(方便管理), `data` 的部份我等等再回來介紹.

看 [models](models) 資料夾, 裡面有 `__init__.py` 和 `models.py`,

`__init__.py` 單純就是 import `models.py` 而已.

`models.py` 這邊就很重要了

```python
class DemoOdooTutorial(models.Model):
    _name = 'demo.odoo.tutorial'
    _description = 'Demo Odoo Tutorial'
    _inherit = ['mail.thread', 'mail.activity.mixin'] # track_visibility
```

odoo 中的 model 主要有幾個, 分別是 AbstractModel、Model、TransientModel,

最基本的 BaseModel, 其實 BaseModel = AbstractModel,

[https://www.odoo.com/documentation/13.0/reference/orm.html#abstractmodel](https://www.odoo.com/documentation/13.0/reference/orm.html#abstractmodel)

```python
@pycompat.implements_to_string
class BaseModel(MetaModel('DummyModel', (object,), {'_register': False})):
    """ Base class for Odoo models.

    Odoo models are created by inheriting:

    *   :class:`Model` for regular database-persisted models

    *   :class:`TransientModel` for temporary data, stored in the database but
        automatically vacuumed every so often

    *   :class:`AbstractModel` for abstract super classes meant to be shared by
        multiple inheriting models

    The system automatically instantiates every model once per database. Those
    instances represent the available models on each database, and depend on
    which modules are installed on that database. The actual class of each
    instance is built from the Python classes that create and inherit from the
    corresponding model.

    Every model instance is a "recordset", i.e., an ordered collection of
    records of the model. Recordsets are returned by methods like
    :meth:`~.browse`, :meth:`~.search`, or field accesses. Records have no
    explicit representation: a record is represented as a recordset of one
    record.

    To create a class that should not be instantiated, the _register class
    attribute may be set to False.
    """
    ....
```

今天只會先提到 Model, `Model` 繼承自 AbstractModel

```python
class Model(AbstractModel):
    """ Main super-class for regular database-persisted Odoo models.

    Odoo models are created by inheriting from this class::

        class user(Model):
            ...

    The system will later instantiate the class once per database (on
    which the class' module is installed).
    """
    _auto = True                # automatically create database backend
    _register = False           # not visible in ORM registry, meant to be python-inherited only
    _abstract = False           # not abstract
    _transient = False          # not transient
```

`_auto = True` 會自動在 db 中建立 table.

`_name` 為 model 的名稱, 請注意幾件事情, model 名稱建議都使用單數, 然後不要使用 `_` 分隔名稱,

請使用 `.` 像是範例中的 `demo.odoo.tutorial` (在 db 中, table 名稱會顯示 `demo_odoo_tutorial`, 如下圖)

![alt tag](https://i.imgur.com/s6ngYGo.png)

`_inherit` 在 odoo 中不管是 model 還是 view, 甚至是權限, 都會使用繼承 (這邊先知道這樣即可:smile:).

再來說明 field

```python
    ......
    name = fields.Char('Description', required=True)

    # track_visibility='always' 和 track_visibility='onchange'
    is_done_track_onchange = fields.Boolean(
        string='Is Done?', default=False, track_visibility='onchange')
    name_track_always = fields.Char(string="track_name", track_visibility='always')

    start_datetime = fields.Datetime('Start DateTime', default=fields.Datetime.now())
    stop_datetime = fields.Datetime('End Datetime')

    field_onchange_demo = fields.Char('onchange_demo')
    field_onchange_demo_set = fields.Char('onchange_demo_set', readonly=True)

    # float digits
    # field tutorial
    input_number = fields.Float(string='input number', digits=(10,3))
    ......
```

`track_visibility` 為追蹤值的改變, 這也是為甚麼要繼承 `mail.thread` 以及 `mail.activity.mixin` 的原因,

如果你有修改值, 會紀錄改變(如下圖),

![alt tag](https://i.imgur.com/XjCwGHQ.png)

`start_datetime` field 有 default, 設定為當天的時間,

當建立一筆資料時, 會顯示當下的時間,

![alt tag](https://i.imgur.com/VYPAz9S.png)

`field_onchange_demo_set` field 中的 `readonly=True`,

你可以發現是無法修改的 (可能是根據其他欄位透過 code 改變它的值)

![alt tag](https://i.imgur.com/1A5RIDH.png)

`input_number` Float field 中的 digits 為設定進位以及小數點, 像這邊是算到小數點第3位並使用10進位

![alt tag](https://i.imgur.com/0ZXafMi.png)

下一部份的 code

```python
......
field_compute_demo = fields.Integer(compute="_get_field_compute") # readonly

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Description must be unique'),
    ]

    @api.constrains('start_datetime', 'stop_datetime')
    def _check_date(self):
        for data in self:
            if data.start_datetime > data.stop_datetime:
                raise ValidationError(
                    "data.stop_datetime  > data.start_datetime"
                )

    @api.depends('input_number')
    def _get_field_compute(self):
        for data in self:
            data.field_compute_demo = data.input_number * 1000

    @api.onchange('field_onchange_demo')
    def onchange_demo(self):
        if self.field_onchange_demo:
            self.field_onchange_demo_set = 'set {}'.format(self.field_onchange_demo)
        ......
......

```

`field_compute_demo` field 為 compute field, compute field 預設為 readonly,

而且這個 field 預設是不會存在 db 中的 (`store=False`, 也就是每次都是計算出來的),

如果想要將值保存在 db 中 , 需再加上 `store=True` ,

`compute` 為 `_get_field_compute`, 透過 `@api.depends` 裝飾器的幫忙,

這邊會根據 `input_number` field 的值 * 1000 之後,

將值餵給 `field_compute_demo`.

![alt tag](https://i.imgur.com/FQOPZTH.png)

特別補充說明一下 onchange 也可以 return 一個 dict.

```python
......
    @api.onchange('field_onchange_demo')
    def onchange_demo(self):
        ......

        # warning message
        result = dict()
        result['warning'] = {
            'title': 'HELLO',
            'message': 'I am warning'
        }
        return result
```

透過上方的寫法, 使用者會跳出提醒視窗 (但不會中斷使用者)

![alt tag](https://i.imgur.com/hO9rE2y.png)

`_sql_constraints` 這個為設定一些限制(直接寫 postgresql),

避免不允許(錯誤)的資料進入 db,

像這邊設定 `name` field 必須為 unique,

假如你有重複的 `name`, 系統就會提醒你(如下圖),

![alt tag](https://i.imgur.com/4fOtkpJ.png)

`def _check_date(self)` 這段是另一種方式限制, 透過 `@api.constrains` 裝飾器的幫忙,

這邊限制了 `start_datetime` 必須大於 `stop_datetime`, 否則會出現 error,

![alt tag](https://i.imgur.com/PtSLNjx.png)

`def onchange_demo(self)` 這個則是使用了 `@api.onchange` 裝飾器的幫忙,

主要是根據 `field_onchange_demo` 的改變, 將值餵給 `field_onchange_demo_set`,

注意 view 中要有 `force_save="1"`, 否則儲存時會消失.

![alt tag](https://i.imgur.com/5Iq4Rgb.png)

你可能會發現 `@api.depends` 和 `@api.onchange` 幾乎一樣,

其實主要區分兩個比較容易的方法, 就是 `@api.depends` 可以使用在 `related` 欄位,

像是之後會介紹的 `Many2one` `Many2many` `One2many` 之類的.

而 `@api.onchange` 只能使用在同一個 model 上.

### 介紹 security, menu, tree, form

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part2](https://youtu.be/EnD-VxuILWM) - 介紹 security, menu, tree, form

接下來來看 [security](security) 這個很重要的資料夾, 既然有了 model,

這樣要如何控制誰有權限讀寫修改刪除呢:question:

就是依靠 `ir.model.access.csv` 和 `security.xml` 這個檔案:exclamation:

`security.xml`

```xml
  <record id="module_demo_odoo_tutorial" model="ir.module.category">
    <field name="name">Demo odoo tutorial category</field>
  </record>

  <record id="demo_odoo_tutorial_group_user" model="res.groups">
    <field name="name">User</field>
    <field name="category_id"
           ref="module_demo_odoo_tutorial"/>
    <field name="implied_ids"
           eval="[(4, ref('base.group_user'))]"/>
  </record>

  <record id="demo_odoo_tutorial_group_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="category_id"
           ref="module_demo_odoo_tutorial"/>
    <field name="implied_ids"
           eval="[(4, ref('demo_odoo_tutorial_group_user'))]"/>
    <field name="users"
           eval="[(4, ref('base.user_root')),
                  (4, ref('base.user_admin'))]"/>
  </record>
```

通常會先建立一個 category, 然後建立兩個 group, 分別是 User 和 Manager,

這邊使用線性的繼承方式, 也就是 Manager 擁有 User 一切的權限.

`implied_ids` 也就是繼承, 裡面的數字分別代表不同的意思,

```text

(0, _ , {'field': value}) creates a new record and links it to this one.
(1, id, {'field': value}) updates the values on an already linked record.
(2, id, _) removes the link to and deletes the id related record.
(3, id, _) removes the link to, but does not delete, the id related record. This is usually what you will use to delete related records on many-to-many fields.
(4, id, _) links an already existing record.
(5, _, _) removes all the links, without deleting the linked records.
(6, _, [ids]) replaces the list of linked records with the provided list.
```

`_` 也可以改成 `0` or `False`,

尾巴不相關的可以被, 像是 `(4, id, _)` 也可以寫成 `(4, id)`.

`ir.model.access.csv` 為管理 user 和 manager CRUD 的權限,

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_demo_odoo_user,Demo Odoo Tutorial User Access,model_demo_odoo_tutorial,demo_odoo_tutorial_group_user,1,0,0,0
access_demo_odoo_manager,Demo Odoo Tutorial Manager Access,model_demo_odoo_tutorial,demo_odoo_tutorial_group_manager,1,1,1,1
```

比較需要注意的地方是 model_id 的部份, 像這邊的 model 為 `demo.odoo.tutorial`,

但這邊必須填入 `model_demo_odoo_tutorial`, 規則很簡單, 就是要前面要補上 `model`,

然後將全部的 `.` 改成 `_` .

到 user 中可以切換 group,

![alt tag](https://i.imgur.com/CclfzfB.png)

接著來看 [views](views) 資料夾,

先看 `menu.xml`

```xml
    <!-- demo_odoo_tutorial App Menu -->
    <menuitem id="demo_odoo_tutorial_menu"
              name="Demo Odoo Tutorial" />

    <!-- Action to open the demo_odoo_tutorial -->
    <act_window id="action_odoo_tutorial"
      name="Demo Odoo Tutorial Action"
      res_model="demo.odoo.tutorial"
      view_mode="tree,form"/>

    <!-- Menu item to open the demo_odoo_tutorial -->
    <menuitem id="menu_odoo_tutorial"
              name="Demo Odoo Tutorial"
              action="action_odoo_tutorial"
              parent="demo_odoo_tutorial_menu" />
```

建立一個 menuitem, 然後去定義它的 Action, Action 中比較重要的是 `res_model` 和 `view_mode`,

`res_model` 就填入對應的 model, `view_mode` 先簡單填入 tree 和 form,

在 odoo 中有很多 view, 像是 pivot kanban 之類的.

再來看 `view.xml`,

這邊指定兩個最簡單的,

首先是 tree, 記得將對應的 model 填進去,

```xml
......
  <record id="view_tree_demo_odoo_tutorial" model="ir.ui.view">
    <field name="name">Demo Odoo Tutorial List</field>
    <field name="model">demo.odoo.tutorial</field>
    <field name="arch" type="xml">
      <tree>
        <field name="name"/>
        <field name="name_track_always"/>
        <field name="is_done_track_onchange"/>
        <field name="start_datetime"/>
        <field name="stop_datetime"/>
      </tree>
    </field>
  </record>
......
```

tree 如下

![alt tag](https://i.imgur.com/Kz2iniQ.png)

接著是 form, 記得將對應的 model 填進去,

(如果都沒寫, 系統會自己產生對應的 form view, 但很醜:sob:)

```xml
......
<record id="view_form_demo_odoo_tutorial" model="ir.ui.view">
    <field name="name">Demo Odoo Tutorial Form</field>
    <field name="model">demo.odoo.tutorial</field>
    <field name="arch" type="xml">
      <form string="Demo Odoo Tutorial">
        <sheet>
          <group>
            <field name="name"/>
            <field name="name_track_always"/>
            <field name="is_done_track_onchange"/>
            <field name="start_datetime"/>
            <field name="stop_datetime"/>
            <field name="field_onchange_demo"/>
            <field name="field_onchange_demo_set" force_save="1"/>
            <field name="input_number"/>
            <field name="field_compute_demo"/>
          </group>
        </sheet>
        <div class="oe_chatter">
          <field name="message_follower_ids" widget="mail_followers"/>
          <field name="activity_ids" widget="mail_activity"/>
          <field name="message_ids" widget="mail_thread"/>
        </div>
      </form>
    </field>
</record>
......
```

form 如下

![alt tag](https://i.imgur.com/vuQd9Bx.png)

請注意最後一段的 `message_follower_ids` `activity_ids` `message_ids`,

這並不是我們所建立的 field, 而是繼承 `mail.thread` `mail.activity.mixin` 所擁有的,

這段 code 主要是產生這個區塊

![alt tag](https://i.imgur.com/FOPV6i5.png)

最後回到 `__manifest__.py` 中, 記得將對應的路徑填入 `data` 中,

```python
# always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data_demo_odoo.xml',
        'views/menu.xml',
        'views/view.xml',
        'reports/report.xml',
        'views/demo_odoo_template.xml',
    ],
```

接著來看 [data/data_demo_odoo.xml](data/data_demo_odoo.xml),

```xml
  <record id="demo_odoo_1" model="demo.odoo.tutorial">
      <field name="name">demo_odoo_1</field>
      <field name="name_track_always">demo_name_track_always_1</field>
      <field name="is_done_track_onchange">True</field>
  </record>

  <record id="demo_odoo_2" model="demo.odoo.tutorial">
      <field name="name">demo_odoo_2</field>
      <field name="name_track_always">demo_name_track_always_2</field>
      <field name="is_done_track_onchange">True</field>
  </record>
```

這邊做的事情就是當你安裝了 addons, 它會預設幫你建立一些相關的資料.

注意:exclamation: 它和 [demo/demo.xml](demo/demo.xml) 資料夾不太一樣, demo 資料夾是當你有勾選

產生 demo 資料時, 你安裝 addons 會自動產生 demo data (如下圖).

![alt tag](https://i.imgur.com/LbcOiJL.png)

### 介紹 report, controller

* [Youtube Tutorial - odoo 手把手建立第一個 addons - part3](https://youtu.be/25MSbidCf1U) - 介紹 report, controller

再來是報表的部份 [reports/report.xml](reports/report.xml),

這邊是定義 report 的 template,

`t-as="o"` 你可以定義你喜歡的變數

```xml
    <template id="report_demo_odoo_tutorial">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="o">
                <t t-call="web.external_layout">
                    <div class="page">
                        <h2>Odoo Report</h2>
                        <div>
                            <strong>Name:</strong>
                            <p t-field="o.name"/>
                        </div>
                        <div>
                            <strong>Name_track_always:</strong>
                            <p t-field="o.name_track_always"/>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>

    ......
```

後面這段則是定義 report 的檔名, report_type, 指定 model

```xml
    <report
        id="action_report_demo"
        string="Demo Report"
        model="demo.odoo.tutorial"
        report_type="qweb-pdf"
        name="demo_odoo_tutorial.report_demo_odoo_tutorial"
        file="demo_odoo_tutorial.report_demo_odoo_tutorial"
        print_report_name="'Demo Report - %s' % ((object.name).replace('/', ''))"
    />
```


記得要將路徑填入 `__manifest__.py`

```python
'data': [
        ......
        'reports/report.xml',
        ......
    ],
```

會顯示在這邊

![alt tag](https://i.imgur.com/nHf4bxy.png)

報表如下

![alt tag](https://i.imgur.com/VoY55io.png)

再來是 [controllers](controllers) 這個資料夾,

如果你學過 Django,Flask 你會發現蠻像的:smile:

因為就是定義 route , 然後撈資料, 最後回傳到對應的 view,

(記得要將 controller 填入 `__init__.py` 中)

[controllers/controllers.py](controllers/controllers.py)

```python
class DemoOdoo(http.Controller):

    @http.route('/demo/odoo', auth='user')
    def list(self, **kwargs):
        obj = http.request.env['demo.odoo.tutorial']
        objs = obj.search([])
        return http.request.render(
            'demo_odoo_tutorial.demo_odoo_template',{'objs': objs})
```

至於它的 view, 在 [views/demo_odoo_template.xml](views/demo_odoo_template.xml)

```xml
<template id="demo_odoo_template" name="Demo odoo List">
  <div id="wrap" class="container">
    <h1>Demo Odoo</h1>
      <t t-foreach="objs" t-as="obj">
        <div class="row">
          <span t-field="obj.name" />,
          <span t-field="obj.is_done_track_onchange" />,
          <span t-field="obj.name_track_always" />
        </div>
      </t>
  </div>
</template>
```

route 我們定義是 `@http.route('/demo/odoo', auth='user')`,

`auth='user'` 代表要登入才可以觀看, 所以只要瀏覽 [http://0.0.0.0:8069/demo/odoo/](http://0.0.0.0:8069/demo/odoo/)

就會看到下圖,

![alt tag](https://i.imgur.com/kHYQhGR.png)

### 說明 odoo manifest 中的 auto_install

* [Youtube Tutorial - 說明 odoo manifest 中的 auto_install](https://youtu.be/xTezPfJAJ_Q)

特別說明一下 `__manifest__.py` 裡的 `auto_install`,

```python
    'installable': True,
    'auto_install': False,
    'application': True,
```

`auto_install`

這個值很重要, 如果你不懂, 建議設定 `False`, 原因是假如你設定為 `True`,

它會找到你路徑的全部 addons 中的 `__manifest__.py` 裡找 depends,

你其實可以把他想成是一種反向的依賴, 很容易不小心被它雷到:scream:

舉個例子來看這個問題, 當你安裝 `hr_expense` addons 時, `sale_expense` addons 會自動被安裝起來 :exclamation::exclamation:

`hr_expense` addons 看不到相關 depends,

![alt tag](https://i.imgur.com/NW5efUr.png)

`sale_expense` addons 可以看到相關 depends

![alt tag](https://i.imgur.com/i5N52OT.png)

也就是當你安裝 `hr_expense` 時, 因為 `sale_expense` 裡的 `'auto_install': True`,

所以自動會把 `sale_expense` 裝起來.

以下為 `sale_expense` 的 `__manifest__.py`

```python
{
    'name': 'Sales Expense',
    ......
    'depends': ['sale_management', 'hr_expense'],
    ......
    'auto_install': True,
}

```