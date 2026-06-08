frappe.ui.form.on('Purchase Order', {
    refresh: function(frm) {
        if (frm.doc.custom_proposal) {
            frm.dashboard.add_indicator(__('Linked to Interior Project'), 'blue');
        }
    },
    
    validate: function(frm) {
        if (frm.doc.custom_proposal && frm.doc.items.length > 0) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Proposal BOQ',
                    name: frm.doc.custom_proposal
                },
                callback: function(r) {
                    if (r.message) {
                        let boq_items = r.message.items.map(i => i.item_code || i.description);
                        let warnings = [];
                        
                        frm.doc.items.forEach(po_item => {
                            if (!boq_items.includes(po_item.item_code) && !boq_items.includes(po_item.item_name)) {
                                warnings.push(po_item.item_name);
                            }
                        });
                        
                        if (warnings.length > 0) {
                            frappe.msgprint({
                                title: __('Budget Warning'),
                                indicator: 'orange',
                                message: __('The following items are being purchased but were not found in the original Proposal BOQ: <br><br><b>' + warnings.join(', ') + '</b>')
                            });
                        }
                    }
                }
            });
        }
    }
});
