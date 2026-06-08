frappe.ui.form.on('Daily Site Diary', {
    setup: function(frm) {
        if(frm.is_new() && !frm.doc.site_engineer) {
            frm.set_value('site_engineer', frappe.session.user);
        }
    },
    
    refresh: function(frm) {
        if (!frm.is_new() && frm.doc.issues_and_delays) {
            frm.dashboard.add_indicator(__('Site Issues Reported'), 'red');
        }
    },
    
    before_submit: function(frm) {
        if (frm.attachments && frm.attachments.get_attachments().length === 0) {
            frappe.throw(__('Please attach at least one site photo before submitting the diary.'));
        }
    }
});
