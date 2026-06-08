app_name = "interior_erp"
app_title = "Interior Erp"
app_publisher = "Telepathy"
app_description = "Custom ERP system for an Interior Design company"
app_email = "test@example.com"
app_license = "mit"

doc_events = {
    "Lead": {
        "before_save": "interior_erp.custom.lead.before_save"
    },
    "Purchase Receipt": {
        "on_submit": "interior_erp.custom.purchase_receipt.on_submit"
    }
}

app_include_js = "/assets/interior_erp/js/interior_erp.js"

scheduler_events = {
    "daily": [
        "interior_erp.tasks.check_missed_followups",
        "interior_erp.tasks.check_overdue_payments",
        "interior_erp.tasks.refresh_active_budgets"
    ]
}

override_doctype_dashboards = {
    "Lead": "interior_erp.custom.lead_dashboard.get_data",
    "Proposal BOQ": "interior_erp.custom.proposal_boq_dashboard.get_data"
}

fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Interior Erp"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Interior Erp"]]},
    {"dt": "Workflow", "filters": [["name", "in", ["Proposal BOQ Approval", "Project Budget Approval"]]]},
    {"dt": "Workflow State", "filters": [["name", "in", ["Draft", "Pending Internal Approval", "Pending Client Approval", "Approved", "Rejected", "Pending Owner Approval", "Active"]]]},
    {"dt": "Workflow Action Master", "filters": [["name", "in", ["Submit for Review", "Approve Internally", "Reject Internally", "Client Approved", "Client Rejected", "Needs Revision"]]]},
    {"dt": "Notification", "filters": [["name", "in", ["Project Over Budget Alert", "New Interior Lead Assigned", "Send Proposal to Client", "New Material Request from Site"]]]},
    {"dt": "Workspace", "filters": [["name", "=", "Interior Owner Dashboard"]]},
    {"dt": "Number Card", "filters": [["module", "=", "Interior Erp"]]},
    {"dt": "Dashboard Chart", "filters": [["module", "=", "Interior Erp"]]}
]
