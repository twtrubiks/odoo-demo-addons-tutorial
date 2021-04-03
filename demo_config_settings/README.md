# 實作 config settings

建議觀看影片, 會更清楚:smile:

* [實作 config settings](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings#%E8%AA%AA%E6%98%8E) - [Youtube Tutorial - odoo - 實作 config settings](https://youtu.be/5k_TYBNs_uc)

* [implied_group 用法說明](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings#implied_group-%E7%94%A8%E6%B3%95%E8%AA%AA%E6%98%8E) - [Youtube Tutorial - odoo - implied_group 進階用法說明(等待新增)]()

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

有時候會需要對 addons 做一些參數的 settings,

所以這篇主要介紹 odoo 中如何實現 config settings 的部份.

## 說明

[models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings/models/models.py)

```python
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    demo_prefix = fields.Char(
                string="Demo Prefix",
                # config_parameter='demo_config_settings.config.demo_prefix',
                )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        demo_prefix = self.env["ir.config_parameter"].get_param("demo_config_settings.config.demo_prefix", False)
        res.update({
            'demo_prefix': demo_prefix,
        })
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('demo_config_settings.config.demo_prefix', self.demo_prefix)
```

這邊是使用 TransientModel, 如果不知道這個是甚麼, 建議先了解之前的文章

[demo_odoo_tutorial_wizard](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial_wizard) - TransientModel 範例.

這邊的重點在需要實作 `set_values` 以及 `get_values`,

`set_values`

將 `demo_prefix` 設定到 `ir.config_parameter` model 的 `demo_config_settings.config.demo_prefix` (這個名稱可以自己自訂) 中.

`get_values`

從 `ir.config_parameter` model 的 param 找是否有 `demo_config_settings.config.demo_prefix`.

如果你沒有特殊的邏輯要處理, 可以直接使用 `config_parameter='demo_config_settings.config.demo_prefix'` 代替,

也就是說 `set_values` `get_values` 可以使用 `config_parameter=...` 替代.

views 的部份可參考 [views/view.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings/views/view.xml).

然後不需要 security 資料夾, 因為它是 TransientModel.

裝好 addons, debug developer mode 請打開, 可參考 [odoo12 如何開啟 odoo developer mode](https://github.com/twtrubiks/odoo-docker-tutorial#odoo12-%E5%A6%82%E4%BD%95%E9%96%8B%E5%95%9F-odoo-developer-mode),

Odoo Setup Demo 就是我們加上去的 (在這裡填入 hello123, 記得 Save)

![alt tag](https://i.imgur.com/b6HFz7O.png)

然後到 Technical -> Parameters -> System Parameters

![alt tag](https://i.imgur.com/jNHjHhX.png)

在這裡你會看到剛剛定義的 `demo_config_settings.config.demo_prefix` 為 hello123

![alt tag](https://i.imgur.com/QbJYLGo.png)

這樣子就可以在程式需要取設定值時, 直接到 `ir.config_parameter` model 裡找:smile:

## implied_group 用法說明

[Youtube Tutorial - odoo - implied_group 用法說明(等待新增)]()

這部份稍微比較進階一點,

原始碼的路徑可參考 `odoo/addons/base/models/res_config.py`

```python
......

class ResConfigSettings(models.TransientModel, ResConfigModuleInstallationMixin):
    """ Base configuration wizard for application settings.  It provides support for setting
        default values, assigning groups to employee users, and installing modules.
        To make such a 'settings' wizard, define a model like::

            class MyConfigWizard(models.TransientModel):
                _name = 'my.settings'
                _inherit = 'res.config.settings'

                default_foo = fields.type(..., default_model='my.model'),
                group_bar = fields.Boolean(..., group='base.group_user', implied_group='my.group'),
                module_baz = fields.Boolean(...),
                config_qux = fields.Char(..., config_parameter='my.parameter')
                other_field = fields.type(...),

......

```

`implied_group` 這個的功能主要是用來管理 user 擁有哪些 groups 的權限.

( 其實他的概念和 `implied_ids` 是一樣的, 但這個用法更進階一點:smirk: )

詳細說明請看下方的 demo,

[models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings/models/models.py)

```python
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ......

    group_demo_config_setting = fields.Boolean("Demo Config",
        group='base.group_user', # default
        # group='demo_config_settings.demo_config_settings_tutorial_group',
        implied_group='sale.group_delivery_invoice_address',
        )
    ......
```

`group='base.group_user'` 為預設, 如果你不設定, 就是會預設這個值.

`implied_group='sale.group_delivery_invoice_address'` 這邊使用內建的

`sale.group_delivery_invoice_address` 來當作範例.

`sale.group_delivery_invoice_address` 路徑在 `addons/sale/security/sale_security.xml`

```xml
<record id="group_delivery_invoice_address" model="res.groups">
    <field name="name">Addresses in Sales Orders</field>
    <field name="category_id" ref="base.module_category_hidden"/>
</record>
```

當這個 field 為 True 的時候, 所有的 `group='base.group_user'` 都會擁有

`sale.group_delivery_invoice_address` groups 的權限.

(注意:exclamation::exclamation: field 命名一定要是 `group_xxx` )

當設定為 True 時

![alt tag](https://i.imgur.com/gmfqIju.png)

你會發現全部的 `group='base.group_user'` 都擁有 `sale.group_delivery_invoice_address` groups 的權限.

![alt tag](https://i.imgur.com/yGTegQ6.png)

上面註解的 `group='demo_config_settings.demo_config_settings_tutorial_group'`

只針對 admin user, 也就是設定為 True 時, 只會對擁有 admin 的 user 生效.

(請自行修改測試, 這邊就不打字了, 影片內說明, 因為大同小異:smile:)

記得加入 [security/security.xml](security/security.xml)

```xml
......
    <record id="demo_config_settings_tutorial_group" model="res.groups">
        <field name="name">Config Settings User</field>
        <field name="category_id" ref="base.module_category_hidden"/>
        <field name="users"
            eval="[(4, ref('base.user_root')),
                    (4, ref('base.user_admin'))]"/>
    </record>
......
```

`<field name="category_id" ref="base.module_category_hidden"/>`

這代表這個 groups 是被隱藏的.

也就是不會出現在 user 設定 groups 的地方.
