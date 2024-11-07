# odoo18 教學

這個分支主要是紀錄 odoo18 一些新的特性,

以下紀錄就按照我的摸索慢慢補充 :smile:

官方也有整理改動的內容 [Migration-to-version-18.0](https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-18.0)

odoo18 推薦官方影片 [What's New in the Python Framework?](https://www.youtube.com/watch?v=4XVkNRp8Fc4)

- [odoo 18 範例 addons](demo_expense_tutorial_v1)

- [odoo 18 OWL 範例 addons](demo_owl_tutorial)

## 網址終於改了

以前是這樣

`http://0.0.0.0:8069/web#id=6&cids=1&menu_id=178&action=297&model=sale.order&view_type=form`

odoo18 現在是這樣

`http://0.0.0.0:8069/odoo/sales/6`

## tree 改成 list

odoo17

```xml
<record id="hr_expense_view_expenses_analysis_tree" model="ir.ui.view">
    <field name="name">hr.expense.tree</field>
    <field name="model">hr.expense</field>
    <field name="arch" type="xml">
        <tree string="Expenses" multi_edit="1" sample="1" js_class="hr_expense_tree" decoration-info="state == 'draft'">
            <field name="is_editable" column_invisible="True"/>
            ......
        </tree>
    </field>
</record>
```

odoo18

```xml
<record id="hr_expense_view_expenses_analysis_tree" model="ir.ui.view">
    <field name="name">hr.expense.list</field>
    <field name="model">hr.expense</field>
    <field name="arch" type="xml">
        <list string="Expenses" multi_edit="1" sample="1" js_class="hr_expense_tree" decoration-info="state == 'draft'">
            <field name="is_editable" column_invisible="True"/>
            ......
        </list>
    </field>
</record>
```

odoo18 有多一個指令 `upgrade_code` 可以用來初步轉換 (將 tree 轉換為 list).

```cmd
python odoo-bin upgrade_code --addons-path addons
```

## 新的 _search_display_name

odoo18 棄用 `_name_search`, 改 `_search_display_name`.

odoo17 寫法

```python
@api.model
def _name_search(self, name, domain=None, operator='ilike', limit=None, order=None):
    domain = domain or []
    if name:
        domain = domain + ['|', ('id', operator, name), ('name', operator, name)]
    return self._search(domain, limit=limit, order=order)
```

odoo18 寫法

```python
def _search_display_name(self, operator, value):
    name = value or ''
    if name and operator == 'ilike':
        return ['|', ('id', operator, name), ('name', operator, name)]
    return super()._search_display_name(operator, value)
```

## 簡化 chatter

odoo17

```xml
<div class="oe_chatter">
    <field name="message_follower_ids"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

odoo18 精簡為這樣

```xml
<chatter/>
```

## 不要搜尋 Non-stored field

經過我測試 odoo16, odoo17, odoo18 都會顯示相同的錯誤訊息

```text
ERROR odoo odoo.osv.expression: Non-stored field demo.expense.tutorial.data_vals cannot be searched.
```

## 新的 _has_cycle

棄用 `_check_recursion()`, 改為 `_has_cycle()`.

這個功能主要是要檢查你的 [odoo hierarchy 實作](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_hierarchy_tutorial) 是否正確.

## 新的 self.env.user.has_group

odoo17 為

```python
self.user_has_groups('account.group_account_manager')
```

odoo18 修改為

```python
self.env.user.has_group('account.group_account_manager')
```

也可參考相關 [PR](https://github.com/odoo/odoo/pull/151597)

## 開始引入 Typing

這個終於慢慢引入了, 在 odoo19 後會越來越多

```python
from typing import List, Optional

......

def generate_authentication_options(
    *,
    rp_id: str,
    challenge: Optional[bytes] = None,
    timeout: int = 60000,
    allow_credentials: Optional[List[PublicKeyCredentialDescriptor]] = None,
    user_verification: UserVerificationRequirement = UserVerificationRequirement.PREFERRED,
) -> PublicKeyCredentialRequestOptions:
    """Generate options for retrieving a credential via navigator.credentials.get()
```

## Read-only Transactions

這個是要給 Master Slave Replication 架構使用的

```python
@api.readonly
def activity_format(self):
    return Store(self).get_result()
```

## 新的測試框架

等待測試

