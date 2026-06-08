import frappe

def create_and_hide_workspaces():
    workspaces = frappe.get_all("Workspace", filters={"public": 1, "is_hidden": 0, "name": ("!=", "Home")})
    for w in workspaces:
        try:
            doc = frappe.get_doc("Workspace", w.name)
            doc.is_hidden = 1
            doc.save(ignore_permissions=True)
            print(f"Hidden workspace: {w.name}")
        except Exception as e:
            print(f"Failed to hide {w.name}: {e}")

    workspace_name = "Interior ERP"
    if not frappe.db.exists("Workspace", workspace_name):
        doc = frappe.new_doc("Workspace")
        doc.title = workspace_name
        doc.label = workspace_name
        doc.name = workspace_name
        doc.module = "Interior Erp"
        doc.public = 1
        doc.is_hidden = 0
        doc.sequence_id = 1
        doc.icon = "project"
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Site Visit",
            "label": "Site Visit"
        })
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Proposal BOQ",
            "label": "Proposal BOQ"
        })
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Project Budget Tracker",
            "label": "Project Budget Tracker"
        })
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Daily Site Diary",
            "label": "Daily Site Diary"
        })
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Project Payment",
            "label": "Project Payment"
        })
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": "Employee Scorecard",
            "label": "Employee Scorecard"
        })
        
        doc.insert(ignore_permissions=True)
        print("Created Interior ERP Workspace!")
    else:
        print("Workspace Interior ERP already exists.")
        
    frappe.db.commit()

