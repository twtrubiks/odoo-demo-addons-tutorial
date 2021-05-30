# odoo 觀念 - TransientModel - Wizard

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 觀念 - TransientModel - Wizard](https://youtu.be/Gc-wRnAhbKs)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 wizard 這部份

## 說明

在 odoo 中, wizard 是一個很特別的 model, 之前除了介紹過最基本的 BaseModel (可參考 [demo_odoo_tutorial](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial))
之外,

今天要來介紹另一個 model, 也就是 TransientModel,

`TransientModel` 繼承自 Model, `_transient = True`,

先簡單看一下它的定義,

```python
class TransientModel(Model):
    """ Model super-class for transient records, meant to be temporarily
    persisted, and regularly vacuum-cleaned.

    A TransientModel has a simplified access rights management, all users can
    create new records, and may only access the records they created. The super-
    user has unrestricted access to all TransientModel records.
    """
    _auto = True                # automatically create database backend
    _register = False           # not visible in ORM registry, meant to be python-inherited only
    _abstract = False           # not abstract
    _transient = True           # transient
```

TransientModel 是一種特殊的 model, TransientModel 所產生的 model 會在一個時間定期被刪除,

所以 TransientModel 只適合建立暫時的數據, 也就是接著要介紹的 wizard.

先來看 [wizard/model_wizard.py](wizard/model_wizard.py)

```python
class DemoWizard(models.TransientModel):
    _name = "demo.wizard"
    _description = "Demo Wizard"

    wizard_partner_id = fields.Many2one('res.partner', string='Partner')
    wizard_test_context = fields.Char('wizard_test_context')

    @api.model
    def default_get(self, fields):
        res = super(DemoWizard, self).default_get(fields)
        default_partner_id = self.env.context.get('default_partner_id', [])
        res.update({
            'wizard_partner_id': default_partner_id,
        })
        # or
        # res['wizard_partner_id'] = default_partner_id
        return res

    def btn_validate(self):
        self.ensure_one()
        context = dict(self._context or {})
        default_test_pass_data = context.get('default_test_pass_data', [])

        _logger.warning('============= btn_validate ==================')
        _logger.warning('default_test_pass_data: %s', default_test_pass_data)
        _logger.warning('wizard_test_context: %s', self.wizard_test_context)

        return {'type': 'ir.actions.act_window_close'}
```

注意:exclamation: 這邊是使用 `models.TransientModel`.

注意:exclamation: Transient models 是不需要 access rules

( odoo14 開始 Transient models 需要設定 access rules, 可參考 [odoo14 分支](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/14.0/demo_odoo_tutorial_wizard))

(因為它們是 disposable 一次性的資料), 所以不需要加入 `security/ir.model.access.csv`

在路徑中的 [security/ir.model.access.csv](security/ir.model.access.csv) 裡面定義的東西是

屬於 [models/models.py](models/models.py) 中的哦, 請不要搞錯:smile:

[views/view.xml](views/view.xml)

```xml
......

  <record id="view_form_demo_odoo_tutorial" model="ir.ui.view">
    <field name="name">Demo Odoo Tutorial Form</field>
    <field name="model">demo.odoo.wizard.tutorial</field>
    <field name="arch" type="xml">
      <form string="Demo Odoo Tutorial">
        <header>
          <button name="%(demo_odoo_tutorial_wizard.demo_wizard_action)d"
                  type="action"
                  string="Call Wizard"
                  class="oe_highlight"
                  context="{'default_partner_id': partner_id}"/>
        </header>
        <sheet>
          <group>
            <field name="name"/>
            <field name="partner_id"/>
          </group>
        </sheet>
      </form>
    </field>
  </record>
......
```

重點在 button 這段, 這段是去呼叫 `demo_wizard_action`,

寫法是 `name="%(demo_odoo_tutorial_wizard.demo_wizard_action)d"`,

這邊提醒一下大家:exclamation::exclamation: 如果你把 developer mode 打開,

你會發現他沒有 name, 只會有 Action ID

![alt tag](https://i.imgur.com/dxkPuY0.png)

如果你想快速找到這個 ID 是屬於哪一個 name (反查),

你可以進入 Technical -> Actions -> Window Actions 尋找

![alt tag](https://i.imgur.com/zzi1lJh.png)

路徑在 [wizard/model_wizard.xml](wizard/model_wizard.xml)

```xml
......
    <record id="demo_wizard_view_form" model="ir.ui.view">
        <field name="name">demo.wizard.form</field>
        <field name="model">demo.wizard</field>
        <field name="arch" type="xml">
            <form string="Wizard Form">
                <sheet>
                    <div class="oe_title">
                        <h1>Wizard Title</h1>
                    </div>
                    <group>
                        <field name="wizard_partner_id"/>
                        <field name="wizard_test_context"/>
                    </group>
                </sheet>
                <footer>
                    <button string='Validate' name="btn_validate" type="object" class="btn-primary"/>
                    <button string="Cancel" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>

    <!-- demo_wizard_action -->
    <record id="demo_wizard_action" model="ir.actions.act_window">
        <field name="name">Demo Wizard Action</field>
        <field name="res_model">demo.wizard</field>
        <field name="view_type">form</field>
        <field name="view_mode">form</field>
        <field name="view_id" ref="demo_wizard_view_form"/>
        <field name="target">new</field>
        <field name="context">{'default_test_pass_data': 'hello 123'}</field>
    </record>
......

```

點選 Call Wizard,

![alt tag](https://i.imgur.com/CXK9ePn.png)

會跳出 Wizard,

![alt tag](https://i.imgur.com/aIOT2mI.png)

Partner 會幫你自動帶入 partner_id,

原因是因為使用了 context `{'default_partner_id': partner_id`,

以及 `def default_get(self, fields)` 的方法實現.

當你在 `wizard_test_context` 輸入任何內容 (twtrubiks), 然後點選 Validate

![alt tag](https://i.imgur.com/2WWQQCj.png)

它會 call `def btn_validate`,

然後從 CLI 你會看到兩條 log,

![alt tag](https://i.imgur.com/nZDDTmp.png)

log 1, `default_test_pass_data: hello 123`

會出現這條訊息的原因是因為設定了預設的 context,

`<field name="context">{'default_test_pass_data': 'hello 123'}</field>`

log 2, `wizard_test_context: twtrubiks`

這條訊息則是顯示剛剛輸入的內容.

另一種傳值的方式, 也可以全部透過 python 來完成,

可參考 [models/models.py](models/models.py)

```python
......
@api.multi
def action_context_demo(self):
    # if self._context.get('context_data', False):
    if self.env.context.get('context_data'):
        raise ValidationError('have context data')
    raise ValidationError('hello')

@api.multi
def action_button(self):
    for record in self:
        record.with_context(context_data=True).action_context_demo()
......
```

[views/view.xml](views/view.xml) 的部份,

```xml
......
  <button name="action_context_demo"
          type="object"
          string="action context demo"
          class="oe_highlight"/>

  <button name="action_button"
          type="object"
          string="action button"
          class="oe_highlight"/>
......
```

![alt tag](https://i.imgur.com/oqnr1Ox.png)

當點下 `action context demo` button 時,

會跳出 hello, 因為 `context_data` 為 `False`.

![alt tag](https://i.imgur.com/6rMlJHK.png)

當點下 `action button` button 時,

會跳出 have context data, 因為 `context_data` 為 `True`,

主要透過 `record.with_context(context_data=True).action_context_demo()` 這段,

將 `context_data` 送進去.

![alt tag](https://i.imgur.com/YIoy0yL.png)