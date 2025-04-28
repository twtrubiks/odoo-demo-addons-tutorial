# odoo 18 OWL tutorial

我自己對前端也不是很熟. 這邊寫個範例紀錄一下.

要注意這個 OWL, [odoo16](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/16.0/demo_owl_tutorial), [odoo17](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/17.0/demo_owl_tutorial), [odoo18](https://github.com/twtrubiks/odoo-demo-addons-tutorial/tree/18.0/demo_owl_tutorial) 寫法都有點差異 :unamused:

這個範例是嘗試 odoo 的 OWL, 我建議大家直接參考既有的 addons,

像我就是參考 [purchase/static/src/toaster_button](https://github.com/odoo/odoo/tree/18.0/addons/purchase/static/src/toaster_button)

裡面有 `toaster_button_widget.js` 以及 `toaster_button_widget.xml`

整個流程是這樣, 我們先用 OWL 寫一個 widget button, 點擊這個 button後, 會觸發前端的 OWL JS,

然後這個 OWL JS 可以再從前端呼叫後端的 ORM.

[static/src/xml/custom_button_widget.xml](static/src/xml/custom_button_widget.xml) 定義 widget view.

[static/src/js/custom_button_widget.js](static/src/js/custom_button_widget.js) 註冊 widget 以及寫對應邏輯(呼叫 ORM).

```js
/** @odoo-module */
// 必須要加
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { standardWidgetProps } from "@web/views/widgets/standard_widget_props";
```

注意 :exclamation: :exclamation: `/** @odoo-module */` 這個不是注解, 也不能刪除, 刪除你的程式可能會有問題,

詳細說明可參考 [Javascript Modules](https://www.odoo.com/documentation/18.0/developer/reference/frontend/javascript_modules.html)

在 odoo 中 js 檔案有三種, 分別是

- plain javascript files (no module system)
- native javascript module
- Odoo modules (using a custom module system)

說明如下

```text
There is a very important point to know: Odoo needs to know which files should be translated into Odoo modules and which files should not be translated. This is an opt-in system: Odoo will look at the first line of a JS file and check if it contains the string @odoo-module. If so, it will automatically be converted to an Odoo module.
```

[`__manifest__.py`](__manifest__.py) 記得加入 [static/src/js/custom_button_widget.js](static/src/js/custom_button_widget.js), 以及 [static/src/xml/custom_button_widget.xml](static/src/xml/custom_button_widget.xml)

```python
{
    'name': "demo_owl_tutorial",
    ......
    'assets': {
        'web.assets_backend': [
            'demo_owl_tutorial/static/src/xml/custom_button_widget.xml',
            'demo_owl_tutorial/static/src/js/custom_button_widget.js',
        ],
    },
    'application': True,
    'license': 'LGPL-3',
}
```

在 [view.xml](views/view.xml) 加上我們客製化的 widget

```xml
<?xml version="1.0"?>
<odoo>
  <record id="view_form_demo_owl_tutorial" model="ir.ui.view">
    <field name="name">Demo OWL Tutorial Form</field>
    <field name="model">demo.owl.tutorial</field>
    <field name="arch" type="xml">
      <form string="Demo OWL Tutorial">
        <header>
          <widget name="custom_owl_button" button_name="call_odoo_method" title="OWL 按鈕"/>
        </header>
        ......
```

畫面如下, 當你點了 button

![alt tag](https://i.imgur.com/ziBsISc.png)

console.log 會有值, 你的後端 `call_odoo_method` 也會收到對應的資料.

![alt tag](https://i.imgur.com/7XlGQPj.png)

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
