frappe.ui.form.on('Employee Scorecard', {
    refresh: function(frm) {
        if (frm.doc.docstatus === 0) {
            frm.add_custom_button(__('Recalculate Incentive'), function() {
                frm.save();
                frappe.show_alert({message:__('Metrics and Incentives updated!'), indicator:'green'});
            }).addClass('btn-primary');
        }
        
        if (frm.doc.incentive_amount > 0) {
            frm.dashboard.add_indicator(__('Eligible for Incentive'), 'green');
        } else {
            frm.dashboard.add_indicator(__('No Incentive Available'), 'orange');
        }
    }
});
