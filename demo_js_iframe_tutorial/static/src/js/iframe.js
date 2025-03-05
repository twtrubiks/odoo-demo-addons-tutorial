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