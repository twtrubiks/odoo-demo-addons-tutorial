# odoo 17 js_class 教學

今天來介紹 `js_class` 這個東西,

首先要有 [Owl components](https://www.odoo.com/documentation/17.0/developer/reference/frontend/owl_components.html) 的概念,

把他想成一種元件, 需要的時候可以 import 必且使用它.

如下兩個按鈕, 都是用 `js_class` 完成的.

我會分兩個部份介紹, 一個是 tree 比較簡單, 一個是 form 加了一點變化

- tree 的部份

![alt tag](https://i.imgur.com/ybCEIvT.png)

先建立 template

```xml
<templates>
   ......

   <t t-name="demo_js_class_tutorial.ListView.Buttons" t-inherit="web.ListView.Buttons">
       <xpath expr="//div[hasclass('o_list_buttons')]" position="after">
           <button type="button" class="btn btn-primary" style="margin-left: 10px;"  t-on-click="TestClick">
               Click me
           </button>
       </xpath>
   </t>

</templates>
```

接著開始註冊(這個非常重要)以及撰寫邏輯

```js
/** @odoo-module */
// 必須要加
......
import { ListController } from "@web/views/list/list_controller";
import { listView } from '@web/views/list/list_view';
import { registry } from "@web/core/registry";
import { jsClassDialog } from "@demo_js_class_tutorial/js/js_custom_dialog";
import { useService } from "@web/core/utils/hooks";
......
// 要註冊畫面才會有東西
export class ExpenseListController extends ListController {
    setup() {
        super.setup();
        this.notification = useService("notification");
    }
    TestClick() {
        this.notification.add("test work", { type: "success" });
    }
}
registry.category("views").add("button_in_tree", {
    ...listView,
    Controller: ExpenseListController,
    buttonTemplate: "demo_js_class_tutorial.ListView.Buttons",
});
```

首先, 先拓展了 ListController, 必且加上對應的 `TestClick` 功能,

最後, 一定要註冊, 這邊定義為 `button_in_tree`.

也請注意, `buttonTemplate: "demo_js_class_tutorial.ListView.Buttons",`

這是 odoo 規定的格式, 要去綁定你對應的 template, 也就是

`t-name="demo_js_class_tutorial.ListView.Buttons"`

到這邊定義完了, 最後一步只需要使用 `js_class` 去放在你要的地方.

```xml
.......
<record id="hr_expense_custom_tree" model="ir.ui.view">
    <field name="name">hr.expense.view.custom.tree</field>
    <field name="model">hr.expense</field>
    <field name="inherit_id" ref="hr_expense.view_my_expenses_tree"/>
    <field name="arch" type="xml">
        <xpath expr="//tree" position="attributes">
            <attribute name="js_class">button_in_tree</attribute>
        </xpath>
    </field>
</record>
.......
```

- form 的部份

![alt tag](https://i.imgur.com/oCMfilV.png)

一樣先建立 template,

```xml
<templates>
   <t t-name="demo_js_class_tutorial.modelInfoBtn" t-inherit="web.FormView">
       <xpath expr="//t[@t-set-slot='layout-actions']" position="inside">
           <button class="btn btn-primary" t-on-click="actionInfoForm">Info
           </button>
       </xpath>
   </t>

   ......

</templates>
```

接著開始註冊(這個非常重要)以及撰寫邏輯

```js
/** @odoo-module */
// 必須要加

import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { jsClassDialog } from "@demo_js_class_tutorial/js/js_custom_dialog";

class jsClassModelInfo extends FormController {
   actionInfoForm(){
       this.env.services.dialog.add(jsClassDialog, {
           resModel: this.props.resModel,
           resDesc: "test123"
       });
   }
}
jsClassModelInfo.template = "demo_js_class_tutorial.modelInfoBtn";

export const modelInfoView = {
   ...formView,
   Controller: jsClassModelInfo,
};
registry.category("views").add("model_info", modelInfoView);

```

首先先拓展了 FormController, 必且加上對應的 `actionInfoForm` 功能,

最後, 一定要註冊, 這邊定義 `model_info`.

到這邊定義完了, 最後一步只需要使用 `js_class` 去放在你要的地方.

但這邊有一個比較特別的地方, 注意底下這段 code

```js
import { jsClassDialog } from "@demo_js_class_tutorial/js/js_custom_dialog";
```

這邊 import 了一個客製化的 component.

那當然必須實做這個 component 的 view 和 js,

首先是 view, 流程和前面都一樣, 因為都是 component 的概念,

```xml
<templates>
   <t t-name="demo_js_class_tutorial.infoDialog">
       <Dialog size="'md'" title="'Model Info'" modalRef="modalRef">
           <div class="">
               <h6>Model:</h6>
               <span>
                   <t t-esc="props.resModel"/>
               </span><br/>
               <h6>Description:</h6>
               <span>
                   <t t-esc="props.resDesc"/>
               </span>
           </div>
           <t t-set-slot="footer">
               <button class="btn" t-att-class="props.confirmClass"
                       t-on-click="clickClose" t-esc="props.confirmLabel"/>
           </t>
       </Dialog>
   </t>
</templates>
```

接著去定義對應邏輯,

```js
/** @odoo-module **/

import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

export class jsClassDialog extends Component{
    clickClose() {
        this.props.close()
    }
}
jsClassDialog.template = "demo_js_class_tutorial.infoDialog";
jsClassDialog.components = { Dialog };
jsClassDialog.title = _t("Model Info"),
jsClassDialog.props = {
    confirmLabel: { type: String, optional: true },
    confirmClass: { type: String, optional: true },
    resModel: { type: String, optional: true },
    resDesc: { type: String, optional: true },
    close: { type: Function, optional: true },
    };
jsClassDialog.defaultProps = {
    confirmLabel: _t("Close"),
    confirmClass: "btn-primary",
};
```

最後一步只需要使用 `js_class` 去放在你要的地方.

```xml
......
<record id="hr_expense_custom_view_form" model="ir.ui.view">
    <field name="name">hr.expense.view.custom.form</field>
    <field name="model">hr.expense</field>
    <field name="inherit_id" ref="hr_expense.hr_expense_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//form" position="attributes">
            <attribute name="js_class">model_info</attribute>
        </xpath>
    </field>
</record>
......
```

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
