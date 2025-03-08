# odoo 17 tree 搭配 action 教學

這東西不是 odoo17 特有的.

今天來介紹 tree 搭配 action 這個東西,

會介紹這個東西, 主要是在原生模組中發現相關 code,

```xml
<record id="view_move_line_tree" model="ir.ui.view">
    <field name="name">stock.move.line.tree</field>
    <field name="model">stock.move.line</field>
    <field name="arch" type="xml">
        <tree string="Move Lines" create="0" default_order="id desc" action="action_open_reference" type="object" duplicate="0">
    ...........
```

那時候就在想, 他是如何辦到點了 `stock.move.line` 跑到 `stock.picking` 的 model 中的.

[views/view.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_tree_action_tutorial/views/view.xml)

```xml
  <record id="view_tree_demo_tutorial" model="ir.ui.view">
    <field name="name">Demo Tutorial List</field>
    <field name="model">demo.tutorial</field>
    <field name="arch" type="xml">
      <tree action="action_open_sheet" type="object">
        <field name="name"/>
        <field name="sheet_id" widget="many2onebutton"/>
      </tree>
    </field>
  </record>
```

關鍵是 `type="object"` 和 `action="action_open_sheet"`

當我們點下 tree 會去呼叫 [models/models.py](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_tree_action_tutorial/models/models.py)

邏輯是如果有 sheet_id, 就會跑到 `demo.sheet.tutorial` 底下,

如果沒有 sheet_id, 就會跑到 `demo.tutorial` 底下

```python
def action_open_sheet(self):
    self.ensure_one()
    if self.sheet_id:
        return {
            'res_model': self.sheet_id._name,
            'type': 'ir.actions.act_window',
            'views': [[False, "form"]],
            'res_id': self.sheet_id.id,
        }
    return {
        'res_model': self._name,
        'type': 'ir.actions.act_window',
        'views': [[False, "form"]],
        'res_id': self.id,
    }
```

當我點了沒有 sheet_id

![alt tag](https://i.imgur.com/F01eFZ8.png)

會到 `demo.tutorial` 底下.

![alt tag](https://i.imgur.com/fdhnjHs.png)

如果我點了有 sheet_id

![alt tag](https://i.imgur.com/SL5S2Rm.png)

會到 `demo.sheet.tutorial` 底下.

![alt tag](https://i.imgur.com/k2cIghM.png)

## Donation

文章都是我自己研究內化後原創，如果有幫助到您，也想鼓勵我的話，歡迎請我喝一杯咖啡 :laughing:

綠界科技ECPAY ( 不需註冊會員 )

![alt tag](https://payment.ecpay.com.tw/Upload/QRCode/201906/QRCode_672351b8-5ab3-42dd-9c7c-c24c3e6a10a0.png)

[贊助者付款](http://bit.ly/2F7Jrha)

歐付寶 ( 需註冊會員 )

![alt tag](https://i.imgur.com/LRct9xa.png)

[贊助者付款](https://payment.opay.tw/Broadcaster/Donate/9E47FDEF85ABE383A0F5FC6A218606F8)

## 贊助名單

[贊助名單](https://github.com/twtrubiks/Thank-you-for-donate)

## License

MIT license