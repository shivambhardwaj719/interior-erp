frappe.ui.form.on('Lead', {
    refresh: function(frm) {
        if (frm.doc.custom_followup_status === 'Missed') {
            frm.dashboard.add_indicator(__('Missed Follow-up'), 'red');
        }
        
        if (frm.doc.custom_followup_status === 'Pending' || frm.doc.custom_followup_status === 'Missed') {
            frm.add_custom_button(__('Log Follow-up'), function() {
                frappe.prompt([
                    {
                        fieldname: 'notes',
                        fieldtype: 'Small Text',
                        label: __('Meeting/Call Notes'),
                        reqd: 1
                    },
                    {
                        fieldname: 'next_date',
                        fieldtype: 'Date',
                        label: __('Next Follow-up Date'),
                        reqd: 1
                    }
                ], function(values) {
                    frm.set_value('custom_next_followup_date', values.next_date);
                    frm.set_value('custom_followup_status', 'Pending');
                    
                    frappe.call({
                        method: "frappe.desk.form.utils.add_comment",
                        args: {
                            reference_doctype: "Lead",
                            reference_name: frm.doc.name,
                            content: values.notes,
                            comment_email: frappe.session.user,
                            comment_by: frappe.session.user
                        },
                        callback: function(r) {
                            frm.save();
                        }
                    });
                }, __('Log Follow-up Interaction'), __('Save'));
            }).addClass('btn-primary');
        }
    },
    
    custom_next_followup_date: function(frm) {
        if (frm.doc.custom_next_followup_date && frm.doc.custom_next_followup_date < frappe.datetime.get_today()) {
            frappe.msgprint(__('Follow-up date cannot be in the past.'));
            frm.set_value('custom_next_followup_date', '');
        }
    }
});
