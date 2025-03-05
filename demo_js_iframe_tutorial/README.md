# odoo 17 js - iframe demo

主要透過 `ir.actions.client` 來完成 :blush:

[views/menus.xml](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_js_iframe_tutorial/views/menus.xml)

```xml
<record id="action_demo_iframe" model="ir.actions.client">
    <field name="name">iframe測試</field>
    <field name="tag">custom_menu_iframe_js</field>
    <field name="target">main</field>
</record>
```

tag 很重要  :exclamation:  :exclamation: 他是對應 [demo_js_iframe_tutorial/static/src/js/iframe.js](https://github.com/twtrubiks/odoo-demo-addons-tutorial/blob/17.0/demo_js_iframe_tutorial/static/src/js/iframe.js) 裡面的 registry,

```js
/** @odoo-module */

import { registry } from '@web/core/registry';
import { Component } from "@odoo/owl";

export class Dashboard extends Component {
    setup(){
        console.log("testing odoo iframe");
    }
}
Dashboard.template = "DemoMenu"

registry.category("actions").add("custom_menu_iframe_js", Dashboard);
```
registry 的概念是 `Registry.add(key, value[, options])`

詳細請參考 [Registry API](https://www.odoo.com/documentation/18.0/developer/reference/frontend/registries.html#registry-api)

iframe 效果如下

![alt tag](https://i.imgur.com/wOWYL2j.png)
