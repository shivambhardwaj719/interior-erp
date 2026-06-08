import frappe
from frappe.utils import today, getdate

def before_save(doc, method):
    """DocEvent: Triggered before a Lead is saved."""
    if doc.custom_next_followup_date:
        if getdate(doc.custom_next_followup_date) < getdate(today()):
            doc.custom_followup_status = "Missed"
        else:
            doc.custom_followup_status = "Pending"
    else:
        doc.custom_followup_status = ""
