# odoo fields_view_get 介紹教學

建議觀看影片, 會更清楚:smile:

* [Youtube Tutorial - odoo fields_view_get 介紹教學](https://youtu.be/TpEw3TQiZ_M)

建議在閱讀這篇文章之前, 請先確保了解看過以下的文章 (因為都有連貫的關係)

[odoo 手把手建立第一個 addons](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/master/demo_odoo_tutorial)

主要介紹 odoo 中 fields_view_get 這個 function 的功能以及用法.

## 說明

先說結論, 透過 `fields_view_get` 這個方法, 我們可以動態的做很多常規方法無法做到的事情,

今天就來舉個例子, 我希望除了 Billing Manager 這個 gropus 之外, 其他的人對 `account.invoice` 中的

`invoice_line_ids` field 都必須是 readonly (如圖下方).

![alt tag](https://i.imgur.com/VuIMx64.png)

讓我們使用 `fields_view_get` 他來解決這個問題吧:smile: (常規的方法不好解決:sob:)

請參考 [models/account_invoice.py](models/account_invoice.py)

```python
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        print('view_type:', view_type)

        if not self.env.user.has_group('account.group_account_manager'):
            if view_type == 'form':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//field[@name="invoice_line_ids"]'):
                    print('node.attrib dict:', node.attrib)
                    node_values = node.get('modifiers')
                    modifiers = json.loads(node_values)
                    modifiers['readonly'] = True
                    node.set('modifiers', json.dumps(modifiers))
                res['arch'] = etree.tostring(doc)

        ......

        return res

```

先把這個 addons 裝起來, 當你在 invoice form 的介面底下看 terminal 的輸出訊息,

![alt tag](https://i.imgur.com/nMW9NQF.png)

(你也可以把 `res['arch']` print 出來, 你就會發現 xml 的資料都包含在裡面)

很明顯的, 當 type 要是 form 的時候才會有 xml 的資料, 主要是去修改 modifiers 裡面

的資料, 要讓他變成是 `readonly=True`.

(程式碼如上, 邏輯就是先抓到 `modifiers` 這個 node, 接著透過 json 的方式下去修改,

最後記得要放回 arch, 也就是 `res['arch'] = etree.tostring(doc)`)

所以透過這段 code, 邏輯就是, 只有擁用 Billing Manager(`account.group_account_manager`)

的 groups 才**不是** readonly, 否則都是 readonly. (建議看影片的 demo:smirk:)

剛剛的 type 是 form, 接著來看看 tree 的狀況,

```python
class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(AccountInvoice, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        print('view_type:', view_type)

        .......

        if self.env.user.has_group('account.group_account_manager'):
            if view_type == 'tree':
                doc = etree.XML(res['arch'])
                for node in doc.xpath('//field[@name="partner_id"]'):
                    node.addnext(
                        etree.Element('field', {'string': 'test partner_id fields',
                                                'name': 'partner_id'}))
                res['arch'] = etree.tostring(doc)

        return res
```

當我們發現 type 是 tree 的時候, 且權限是 Billing Manager(`account.group_account_manager`),

我們在 `partner_id` 的欄位後面再動態加一個 `partner_id` (名稱改為 test partner_id fields)

![alt tag](https://i.imgur.com/OMElix0.png)

快速總結, 透過這個 `fields_view_get` 你可以做到很多非常規的變化, 也可以對 xml 做進一步的修改,

達到動態的邏輯變化.
