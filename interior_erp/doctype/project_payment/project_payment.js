frappe.ui.form.on('Project Payment', {
    refresh: function(frm) {
        if (frm.doc.status === 'Paid') {
            frm.dashboard.add_indicator(__('Payment Completed'), 'green');
        } else if (frm.doc.status === 'Overdue') {
            frm.dashboard.add_indicator(__('Payment Overdue'), 'red');
        } else if (frm.doc.status === 'Partially Paid') {
            frm.dashboard.add_indicator(__('Partial Payment Received'), 'orange');
        }
        
        if (frappe.user_roles.includes("Accountant") && frm.doc.status !== 'Paid') {
            frm.add_custom_button(__('Log Payment Received'), function() {
                frappe.prompt([
                    {
                        fieldname: 'amount',
                        fieldtype: 'Currency',
                        label: __('Amount Received'),
                        reqd: 1,
                        default: frm.doc.expected_amount - frm.doc.amount_paid
                    },
                    {
                        fieldname: 'date',
                        fieldtype: 'Date',
                        label: __('Payment Date'),
                        reqd: 1,
                        default: frappe.datetime.get_today()
                    },
                    {
                        fieldname: 'ref',
                        fieldtype: 'Data',
                        label: __('Reference (Cheque/Txn ID)')
                    }
                ], function(values) {
                    frm.set_value('amount_paid', (frm.doc.amount_paid || 0) + values.amount);
                    frm.set_value('payment_date', values.date);
                    frm.set_value('payment_reference', values.ref);
                    frm.save();
                }, __('Receive Payment'), __('Update Record'));
            }).addClass('btn-primary');
        }
    }
});
