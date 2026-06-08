frappe.ui.form.on('Site Visit', {
    setup: function(frm) {
        if(frm.is_new() && !frm.doc.site_engineer) {
            frm.set_value('site_engineer', frappe.session.user);
        }
    }
});

frappe.ui.form.on('Site Visit Room', {
    length: function(frm, cdt, cdn) {
        calculate_area(frm, cdt, cdn);
    },
    width: function(frm, cdt, cdn) {
        calculate_area(frm, cdt, cdn);
    },
    rooms_remove: function(frm) {
        calculate_total(frm);
    }
});

function calculate_area(frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    let area = (row.length || 0) * (row.width || 0);
    frappe.model.set_value(cdt, cdn, 'area', area);
    calculate_total(frm);
}

function calculate_total(frm) {
    let total = 0;
    if (frm.doc.rooms) {
        frm.doc.rooms.forEach(row => {
            total += (row.area || 0);
        });
    }
    frm.set_value('total_area', total);
}
