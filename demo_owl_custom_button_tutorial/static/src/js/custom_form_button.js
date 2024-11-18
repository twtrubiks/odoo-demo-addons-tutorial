/** @odoo-module */
// 必須要加

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FormController.prototype, "hr_expense", {
       setup(){
          this._super.apply();
          this.action = useService("action")
          this.dialog = useService("dialog");
       },
       CustomButtonClicked(){
          this.action.doAction({
               type: 'ir.actions.act_window',
               name: 'All HR Expense',
               view_mode: 'form',
               views:[[false, 'list']],
               res_model: 'hr.expense',
            //    target: 'new',
               target: 'current',
          })
       },
       async ReloadCurrentForm() {
          this.action.doAction({type: 'ir.actions.client', tag: 'reload'});
       },
       ClickDialog() {
            this.dialog.add(ConfirmationDialog, {
                title: this.env._t("TITLE"),
                body: this.env._t("BODY"),
                confirm: () => {},
                cancel: () => {},
            });
       }
});
