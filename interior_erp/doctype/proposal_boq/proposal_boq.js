frappe.ui.form.on('Proposal BOQ', {
    setup: function(frm) {
        if(frm.is_new() && !frm.doc.designer) {
            frm.set_value('designer', frappe.session.user);
        }
    },
    
    refresh: function(frm) {
        if (frm.doc.site_visit) {
            frm.add_custom_button(__('View Site Measurements'), function() {
                frappe.db.get_doc('Site Visit', frm.doc.site_visit).then(sv => {
                    let html = `<table class="table table-bordered">
                        <tr><th>Room</th><th>L x W</th><th>Area</th></tr>`;
                    sv.rooms.forEach(r => {
                        html += `<tr><td>${r.room_name}</td><td>${r.length} x ${r.width}</td><td>${r.area}</td></tr>`;
                    });
                    html += `<tr><td colspan="2"><b>Total Area</b></td><td><b>${sv.total_area}</b></td></tr></table>`;
                    
                    frappe.msgprint({
                        title: __('Measurements from ' + sv.name),
                        message: html,
                        wide: true
                    });
                });
            }, __('Reference'));
        }
    }
});

frappe.ui.form.on('BOQ Item', {
    qty: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    rate: function(frm, cdt, cdn) {
        calculate_amount(frm, cdt, cdn);
    },
    items_remove: function(frm) {
        calculate_total(frm);
    }
});

function calculate_amount(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    let amount = (row.qty || 0) * (row.rate || 0);
    frappe.model.set_value(cdt, cdn, 'amount', amount);
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    if (frm.doc.items) {
        frm.doc.items.forEach(row => {
            total += (row.amount || 0);
        });
    }
    frm.set_value('total_amount', total);
}
