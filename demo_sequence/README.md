# odoo 觀念 - sequence

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo 手把手教學 - sequence](https://youtu.be/u8v0hzEXwpc)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

本篇文章主要介紹 odoo 中的 sequence 這部份

## 說明

先來看 [data/sequence_data.xml](data/sequence_data.xml)

```xml
<data noupdate="0">
  <record id="demo_sequence_id" model="ir.sequence">
      <field name="name">demo_sequence_sequence</field>
      <field name="code">demo.sequence</field>
      <field name="active">True</field>
      <field name="prefix">%(year)s%(month)s%(day)s</field>
      <field name="padding">5</field>
      <field name="number_next">1</field>
      <field name="number_increment">1</field>
  </record>
</data>
```

這邊是設定 sequence 的資料, 以下說明參數所代表的意義,

`name` sequence 名稱.

`code` sequence 的 code. (通常我會把它定義和 model 名稱一樣).

`active` 是否 active.

`prefix` 依照自己的需求定義, 這邊範例式增加 年月日.

`padding` sequence size (字元數).

`number_next` 下一個顯示的數字.

`number_increment` 每次增加數字的單位.

這些資訊也可以在 odoo 的介面上看到

路徑 Technical -> Sequences & Identifiers -> Sequences

![alt tag](https://i.imgur.com/pEQQonC.png)

點進去會看到

![alt tag](https://i.imgur.com/0g87J44.png)

當然, 你也可以在這邊修改.

再來看 [models/models.py](models/models.py)

```python
......
class DemoSequence(models.Model):
    _name = 'demo.sequence'
    _description = 'Demo Sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Char(string="sequence", readonly=True)

    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].next_by_code('demo.sequence') or '/'
        vals['name'] = '{}_{}'.format(seq, vals['name'])
        new_record = super().create(vals)
        return new_record
```

重點就在 `create` 裡面, 在 odoo 中, 只要你建立一比 record, 就會去呼叫 `create`,

這邊我們去覆寫它, 將 name 加上 sequence.

`next_by_code('demo.sequence')` 這端就是去呼叫你自己定義的 sequence code.

來看一下效果,

新建一筆 record, 名稱為 test

![alt tag](https://i.imgur.com/9vL348K.png)

儲存後你會發現加上了你自己定義的 sequence

![alt tag](https://i.imgur.com/62Sg69B.png)

這邊要另外說明一下 `Implementation` 這個參數, 它有兩個選項,

分別是 `Standard`(預設), `No gap`

![alt tag](https://i.imgur.com/TRSEzrZ.png)

假設今天的 sequence 是 001, 我們再建立一比, 這時候是 002,

當我們把 002 這筆刪除, 然後再建立一筆新的, 這時候差異就多來了:smile:

`Standard`(預設)

新的那一筆會是 003.

`No gap`

新的那一筆會是 002.

如果你把此範例改成 `No gap`, 是不會產生效果的, 應該是要搭配其他的 code.

(以後我再補充給大家, 或自行去閱讀 source code 參考寫法:smile:)
