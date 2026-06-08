import frappe

def restore():
    # 1. Delete our custom workspaces
    custom_ws = [
        "Home Dashboard", "CRM", "Leads", "Site Visits", "Projects", 
        "Design", "Proposals", "Payments", "Procurement", "Inventory", 
        "Budget Tracker", "Reports", "ERP Settings", "Interior Dashboard",
        "Interior CRM", "Interior Leads", "Interior Site Visits", "Interior Projects",
        "Interior Design", "Interior Proposals", "Interior Payments", "Interior Procurement",
        "Interior Inventory", "Interior Budget", "Interior Reports", "Interior Settings",
        "Interior ERP"
    ]
    
    for ws_name in custom_ws:
        if frappe.db.exists("Workspace", ws_name):
            try:
                frappe.delete_doc("Workspace", ws_name, ignore_permissions=True, force=True)
            except Exception:
                pass

    # 2. Unhide all standard workspaces
    all_workspaces = frappe.get_all("Workspace", filters={"is_hidden": 1})
    for w in all_workspaces:
        try:
            doc = frappe.get_doc("Workspace", w.name)
            doc.is_hidden = 0
            doc.save(ignore_permissions=True)
            print(f"Restored: {w.name}")
        except Exception as e:
            pass

    frappe.db.commit()
    print("Restore complete.")
