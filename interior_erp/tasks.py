import frappe
from frappe.utils import today, format_date

def check_missed_followups():
    leads = frappe.get_all(
        "Lead",
        filters={
            "custom_next_followup_date": ("<", today()),
            "custom_followup_status": "Pending",
            "status": ("!=", "Converted")
        },
        fields=["name", "lead_owner", "lead_name"]
    )
    
    for lead in leads:
        frappe.db.set_value("Lead", lead.name, "custom_followup_status", "Missed")
        
        if lead.lead_owner:
            owner_email = frappe.db.get_value("User", lead.lead_owner, "email")
            if owner_email:
                frappe.sendmail(
                    recipients=[owner_email],
                    subject=f"Alert: Missed Follow-up for {lead.lead_name}",
                    message=f"""
                    <p>Hello,</p>
                    <p>You missed a scheduled follow-up for Lead: <b>{lead.lead_name}</b> ({lead.name}).</p>
                    <p>Please review the lead and update the next follow-up date.</p>
                    """,
                    reference_doctype="Lead",
                    reference_name=lead.name
                )

def check_overdue_payments():
    overdue_payments = frappe.get_all(
        "Project Payment",
        filters={
            "due_date": ("<", today()),
            "status": ("in", ["Unpaid", "Partially Paid"])
        },
        fields=["name", "customer", "milestone_name", "expected_amount", "amount_paid", "due_date"]
    )
    
    for pay in overdue_payments:
        frappe.db.set_value("Project Payment", pay.name, "status", "Overdue")
        
        customer_email = frappe.db.get_value("Contact", {"links.link_doctype": "Customer", "links.link_name": pay.customer}, "email_id")
        
        accountants = [u.name for u in frappe.get_all("Has Role", filters={"role": "Accountant"}, fields=["parent"]) if u.parent]
        accountant_emails = frappe.get_all("User", filters={"name": ("in", accountants)}, pluck="email")

        recipients = accountant_emails
        if customer_email:
            recipients.append(customer_email)
            
        if recipients:
            balance = pay.expected_amount - pay.amount_paid
            frappe.sendmail(
                recipients=recipients,
                subject=f"Overdue Payment Reminder: {pay.milestone_name}",
                message=f"""
                <h3>Payment Reminder</h3>
                <p>Dear Client/Team,</p>
                <p>This is a reminder that the payment for <b>{pay.milestone_name}</b> was due on {format_date(pay.due_date)}.</p>
                <ul>
                    <li><b>Total Expected:</b> {pay.expected_amount}</li>
                    <li><b>Amount Paid:</b> {pay.amount_paid}</li>
                    <li><b>Pending Balance:</b> {balance}</li>
                </ul>
                <p>Please process the pending amount at the earliest.</p>
                """,
                reference_doctype="Project Payment",
                reference_name=pay.name
            )

def refresh_active_budgets():
    budgets = frappe.get_all("Project Budget Tracker", filters={"docstatus": 1})
    for b in budgets:
        doc = frappe.get_doc("Project Budget Tracker", b.name)
        doc.calculate_actuals()
        doc.calculate_variance()
        doc.save(ignore_permissions=True)
