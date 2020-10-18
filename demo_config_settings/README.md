# 實作 config settings

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo - 實作 config settings]()

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

有時候會需要對 addons 做一些參數的 settings,

所以這篇主要介紹 odoo 中如何實現 config settings 的部份.

## 說明

[models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_config_settings/models/models.py)

```python
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    demo_prefix = fields.Char(string="Demo Prefix")

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