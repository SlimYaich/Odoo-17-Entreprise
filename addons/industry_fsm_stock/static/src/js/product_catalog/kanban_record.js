/** @odoo-module */
import { FSMProductCatalogKanbanRecord } from "@industry_fsm_sale/components/product_catalog/kanban_record";

import { patch } from "@web/core/utils/patch";

patch(FSMProductCatalogKanbanRecord.prototype, {
    updateQuantity(quantity) {
        super.updateQuantity(Math.max(quantity, this.productCatalogData.minimumQuantityOnProduct));
    },
});
