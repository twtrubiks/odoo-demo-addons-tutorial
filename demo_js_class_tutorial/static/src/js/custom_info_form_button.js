/** @odoo-module */
// 必須要加

import { FormController } from "@web/views/form/form_controller";
import { ListController } from "@web/views/list/list_controller";
import { listView } from '@web/views/list/list_view';
import { formView } from "@web/views/form/form_view";
import { registry } from "@web/core/registry";
import { jsClassDialog } from "@demo_js_class_tutorial/js/js_custom_dialog";
import { useService } from "@web/core/utils/hooks";

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

