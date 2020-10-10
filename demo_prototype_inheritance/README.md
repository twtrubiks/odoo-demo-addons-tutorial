# demo_prototype_inheritance

建議觀看影片, 會更清楚:smile:

[Youtube Tutorial - odoo demo_prototype_inheritance](https://youtu.be/sJrik0jjuas)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[demo_class_inheritance](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_class_inheritance) - demo_class_inheritance

本篇文章主要介紹 prototype inheritance 這部份

## 說明

`_inherit` prototype inheritance

注意:exclamation: 還有一個是 `_inherits`, 不要搞錯了哦.

![alt tag](https://i.imgur.com/kjtCar6.png)

注意:exclamation: Stored in different tables.

注意:exclamation: 此類別會擁有父類別的所有特性, 在此類別中的任何修改, 都不會去影響到父類別.

class inheritance 和 prototype inheritance 其實很好分辨,

prototype inheritance 會自己額外定義新的 `_name`,

(注意:exclamation: 如果 `_name` 和被繼承/父類別的名稱一樣, 就等同是 **class inheritance** 哦)

使用的時機通常是繼承 `mail.thread` 這類的 `models.AbstractModel`,

可參考 [odoo 手把手教學 - AbstractModel](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_abstractmodel_tutorial).

[models/model.py](models/model.py)

```python
......
class PrototypeInheritance(models.Model):
    _name = 'demo.prototype'
    _description = 'PrototypeInheritance'
    _inherit = ['mail.thread']

    # 'demo.prototype' 擁有 'mail.thread'(父類別) 的所有特性,
    # 在這裡面的修改, 都不會去影響到 'mail.thread'(父類別).

    test_field = fields.Char('test_field')

```

db 中的狀況

![alt tag](https://i.imgur.com/DdOAF2b.png)

[views/views.xml](views/views.xml)

```xml
......
<record id="view_tree_demo_prototype_tutorial" model="ir.ui.view">
<field name="name">Demo Prototype List</field>
<field name="model">demo.prototype</field>
<field name="arch" type="xml">
    <tree>
        <field name="test_field"/>
    </tree>
</field>
</record>
......
```

[views/views.xml](views/views.xml)

form 的部份

```xml
......
  <record id="view_form_demo_prototype_tutorial" model="ir.ui.view">
    <field name="name">Demo Prototype Form</field>
    <field name="model">demo.prototype</field>
    <field name="arch" type="xml">
        <form>
          <sheet>
            <group>
              <field name="test_field"/>
            </group>
          </sheet>
          <div class="oe_chatter">
              <field name="message_follower_ids" widget="mail_followers"/>
              <field name="message_ids" widget="mail_thread"/>
          </div>
        </form>
    </field>
  </record>
......
```

在這邊可以使用 `message_follower_ids` `message_ids` 的原因是因為繼承了 `mail.thread`

![alt tag](https://i.imgur.com/1x3qwGZ.png)

![alt tag](https://i.imgur.com/NGhD6H9.png)

因為它是 prototype inheritance, 所以在 db 中的 `demo_prototype` 是不會有 message 的資訊的.

`mail.thread` odoo 原始碼的路徑 `addons/mail/models/mail_thread.py`

```python
class MailThread(models.AbstractModel):
  ......
  _name = 'mail.thread'
  _description = 'Email Thread'
  _mail_flat_thread = True  # flatten the discussino history
  _mail_post_access = 'write'  # access required on the document to post on it
  _Attachment = namedtuple('Attachment', ('fname', 'content', 'info'))

  ......
  message_follower_ids = fields.One2many(
        'mail.followers', 'res_id', string='Followers')

  ......

  message_ids = fields.One2many(
          'mail.message', 'res_id', string='Messages',
          domain=lambda self: [('message_type', '!=', 'user_notification')], auto_join=True)
  ......
```

從 `mail.thread` 可以看出它分別儲存在 `mail.followers` 和 `mail.message` table 中.
