# 介紹 AbstractModel

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - AbstractModel](https://youtu.be/jsMTVe12vRY)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

主要介紹 demo_abstractmodel_tutorial

## 說明

`AbstractModel` AbstractModel = BaseModel,

注意:exclamation::exclamation: AbstractModel **不會** 在資料庫中產生對應的 table.

AbstractModel 除了常常使用在之前介紹的 [demo_prototype_inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_prototype_inheritance) 中,

也很常使用在 report 中 (自定義一些額外的邏輯),

可參考 odoo code 中的 `addons/sale/report/sale_report.py`,

```python
......
class SaleOrderReportProforma(models.AbstractModel):
    _name = 'report.sale.report_saleproforma'
    _description = 'Proforma Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'proforma': True
        }
```

假如你的 report 有額外的邏輯, 可以將邏輯寫在 `_get_report_values` 中.

請一定要先了解 Transient Model, 如果不了解可參考 [demo_odoo_tutorial_wizard](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial_wizard).

開始今天的介紹:smile:

先來看 [wizard/model_wizard.py](wizard/model_wizard.py)

```python
class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = "Report Wizard"

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)

    @api.multi
    def download_report(self):

        _logger.warning('=== CALL get_report ===')

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }
        return self.env.ref('demo_abstractmodel_tutorial.action_report_abstractmodel').report_action(self, data=data)
......
```

頁面上會有一個按鈕觸發 `download_report`,

`demo_abstractmodel_tutorial.action_report_abstractmodel` 為

addons name + report id (report id 後面會說明) `addons_name.report_id`

`report_action()` 會去 call `_get_report_values()`.

[wizard/model_wizard.xml](wizard/model_wizard.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record model="ir.ui.view" id="custom_report_wizard">
    <field name="name">Custom Report</field>
    <field name="model">report.wizard</field>
    <field name="type">form</field>
    <field name="arch" type="xml">
        <form string="Custom Report">
            <group>
                <group>
                    <field name="date_start"/>
                </group>
                <group>
                    <field name="date_end"/>
                </group>
            </group>
            <footer>
                <button name="download_report" string="Download Report" type="object" class="oe_highlight"/>
                <button string="Cancel" special="cancel"/>
            </footer>
        </form>
    </field>
    </record>

    <act_window id="action_custom_report_wizard"
                name="Action Custom Report"
                res_model="report.wizard"
                view_mode="form"
                target="new"/>

    <menuitem action="action_custom_report_wizard"
              id="menu_custom_report_wizard"
              parent="hr_expense.menu_hr_expense_reports"/>

</odoo>
```

這邊定義了基本的 form, 並且將 menu 設定在 `hr_expense.menu_hr_expense_reports` 之下.

![alt tag](https://i.imgur.com/BL4en9D.png)

![alt tag](https://i.imgur.com/VnuJXrI.png)

剛剛前面提到 report id `action_report_abstractmodel` 在 [reports/report.xml](reports/report.xml)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_wizard_template">
        <t t-call="web.html_container">
            <div class="header">
                <h3 class="text-center">Expense Wizard Report</h3>
                <h4 class="text-center">
                    <strong>From</strong>:
                    <t t-esc="date_start"/>
                    <strong>To</strong>:
                    <t t-esc="date_end"/>
                </h4>
            </div>
            <div>
                <table>
                    <thead>
                        <th class="text-center">Name</th>
                        <th class="text-center">Date</th>
                        <th class="text-center">Unit_amount</th>
                    </thead>
                    <tbody>
                        <t t-foreach="docs" t-as="doc">
                            <tr>
                                <td>
                                    <span t-esc="doc['name']"/>
                                </td>
                                <td class="text-center">
                                    <span t-esc="doc['date']"/>
                                </td>
                                <td class="text-center">
                                    <span t-esc="doc['unit_amount']"/>
                                </td>
                            </tr>
                        </t>
                    </tbody>
                </table>
            </div>
        </t>
    </template>

    <report
        id="action_report_abstractmodel"
        string="Demo Report"
        model="report.wizard"
        report_type="qweb-pdf"
        name="demo_abstractmodel_tutorial.report_wizard_template"
        print_report_name="Demo Report"
    />

</odoo>
```

分別設定了 template id `report_wizard_template` 以及 report id `action_report_abstractmodel`.

`name` 的部份為 adddons name + template id.

也就是 `adddons_name.template_id`.

接著看 [wizard/model_wizard.py](wizard/model_wizard.py) 的後半段,

```python
......
class ReportExpenseAbstractModel(models.AbstractModel):
    _name = 'report.demo_abstractmodel_tutorial.report_wizard_template'
    _description = 'Report Expense Wizard'

    @api.model
    def _get_report_values(self, docids, data=None):
        _logger.warning('=== CALL get_report_values ===')

        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        docs = self.env['hr.expense'].search([
            ('date', '>=', date_start),
            ('date', '<=', date_end)], order='date asc')
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }

```

前面說過了 `report_action()` 會去 call `_get_report_values()`,

所以這邊定義了 `AbstractModel` 並且實作 `_get_report_values`.

`_name` 這邊的比較特別, 要注意一下, 它的結構是由以下幾部份組成,

report + addons name + template id

`report.addons_name.template_id`

也就是 `report.demo_abstractmodel_tutorial.report_wizard_template`,

report 這個 prefix 很重要, 請不要任意的拿掉:exclamation::exclamation:

`_get_report_values` 則是我們額外的邏輯, 最後將資料回傳給

`report_wizard_template` 並且 render.

![alt tag](https://i.imgur.com/XqmRovl.png)