/** @odoo-module */
// 必須要加

import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";
import { useService } from "@web/core/utils/hooks";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

patch(FormController.prototype, {
   setup() {
       super.setup();
       this.actionService = useService("action");
       this.dialogService = useService("dialog");
   },
   CustomButtonClicked(){
        this.actionService.doAction({
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
       this.actionService.doAction({type: 'ir.actions.client', tag: 'reload'});
   },
   ClickDialog() {
        this.dialogService.add(ConfirmationDialog, {
            title: _t("TITLE"),
            body: _t("BODY"),
            confirm: () => {},
            cancel: () => {},
        });
    },
})
