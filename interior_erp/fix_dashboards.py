import frappe

def fix_dashboards():
    cards = frappe.get_all("Number Card", filters={"is_standard": 0, "is_public": 0})
    for c in cards:
        frappe.db.set_value("Number Card", c.name, "is_public", 1)
        
    charts = frappe.get_all("Dashboard Chart", filters={"is_standard": 0, "is_public": 0})
    for c in charts:
        frappe.db.set_value("Dashboard Chart", c.name, "is_public", 1)
        
    frappe.db.commit()
    print("Fixed Dashboards visibility!")
