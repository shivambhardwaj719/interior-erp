frappe.ui.form.on('Project Budget Tracker', {
    refresh: function(frm) {
        if (frm.doc.budget_status === 'Over Budget') {
            frm.dashboard.add_indicator(__('Project is Over Budget!'), 'red');
        } else if (frm.doc.budget_status === 'Under Budget') {
            frm.dashboard.add_indicator(__('Project is Under Budget'), 'green');
        }
        
        if (frm.doc.docstatus === 0 && frm.doc.proposal) {
            frm.add_custom_button(__('Fetch Estimates from BOQ'), function() {
                frappe.call({
                    method: 'frappe.client.get',
                    args: { doctype: 'Proposal BOQ', name: frm.doc.proposal },
                    callback: function(r) {
                        if (r.message) {
                            frm.clear_table('budget_items');
                            
                            let group_totals = {};
                            r.message.items.forEach(i => {
                                let grp = i.item_group || 'Misc';
                                group_totals[grp] = (group_totals[grp] || 0) + i.amount;
                            });
                            
                            for (const [group, amount] of Object.entries(group_totals)) {
                                let row = frm.add_child('budget_items');
                                row.item_group = group;
                                row.estimated_amount = amount;
                            }
                            frm.refresh_field('budget_items');
                            frm.save();
                        }
                    }
                });
            }).addClass('btn-primary');
        }
    }
});
