/** @odoo-module */
// 必須要加
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const { Component } = owl;

class ButtonWithNotification extends Component {
    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
    }

    async onClick() {
        // debugger
        console.log("js 被觸發了")
        const result = await this.orm.call(this.props.record.resModel, this.props.method, [this.props.record.resId]);
        // console.log(result)
        this.notification.add(result, { type: "success" });
    }
}
ButtonWithNotification.template = "demo_owl_tutorial.ButtonWithNotification";
ButtonWithNotification.extractProps = ({ attrs }) => {
    return {
        method: attrs.button_name,
        title: attrs.title,
    };
};

registry.category("view_widgets").add("custom_owl_button", ButtonWithNotification);
