import frappe

def on_submit(doc, method):
    if doc.custom_proposal:
        notify_site_team(doc)

def notify_site_team(doc):
    site_visit = frappe.db.get_value("Proposal BOQ", doc.custom_proposal, "site_visit")
    if not site_visit:
        return
        
    site_engineer = frappe.db.get_value("Site Visit", site_visit, "site_engineer")
    if not site_engineer:
        return
        
    engineer_email = frappe.db.get_value("User", site_engineer, "email")
    if engineer_email:
        items_html = "<ul>"
        for item in doc.get("items"):
            items_html += f"<li>{item.qty} {item.uom} of {item.item_name}</li>"
        items_html += "</ul>"

        frappe.sendmail(
            recipients=[engineer_email],
            subject=f"Materials Received for Project: {doc.custom_proposal}",
            message=f"""
            <h3>Materials Delivered to Site</h3>
            <p>Hello,</p>
            <p>A delivery has just been logged and confirmed for your project (Receipt: <b>{doc.name}</b>).</p>
            {items_html}
            <p>Please update your Daily Site Diary accordingly.</p>
            """,
            reference_doctype="Purchase Receipt",
            reference_name=doc.name
        )
