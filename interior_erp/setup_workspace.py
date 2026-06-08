import frappe

def create_dashboard_elements():
    """Create Number Cards and Charts for the Dashboard."""
    elements = []
    
    # 1. Total Active Projects (Number Card)
    if not frappe.db.exists("Number Card", "Total Active Projects"):
        doc = frappe.new_doc("Number Card")
        doc.name = "Total Active Projects"
        doc.label = "Total Active Projects"
        doc.document_type = "Project"
        doc.function = "Count"
        doc.is_public = 1
        doc.show_percentage_stats = 1
        doc.stats_time_interval = "Monthly"
        doc.filters_json = '[["Project","status","=","Open",false]]'
        try:
            doc.insert(ignore_permissions=True)
        except Exception as e:
            print(f"Number card failed: {e}")
            
    # 2. Total Leads (Number Card)
    if not frappe.db.exists("Number Card", "New Leads This Month"):
        doc = frappe.new_doc("Number Card")
        doc.name = "New Leads This Month"
        doc.label = "New Leads This Month"
        doc.document_type = "Lead"
        doc.function = "Count"
        doc.is_public = 1
        doc.show_percentage_stats = 1
        doc.stats_time_interval = "Monthly"
        try:
            doc.insert(ignore_permissions=True)
        except Exception:
            pass

    # 3. Project Status Chart (Dashboard Chart)
    if not frappe.db.exists("Dashboard Chart", "Project Pipeline"):
        doc = frappe.new_doc("Dashboard Chart")
        doc.name = "Project Pipeline"
        doc.chart_name = "Project Pipeline"
        doc.document_type = "Project"
        doc.chart_type = "Group By"
        doc.group_by_type = "Count"
        doc.group_by_based_on = "status"
        doc.filters_json = "[]"
        doc.is_public = 1
        try:
            doc.insert(ignore_permissions=True)
        except Exception as e:
            print(f"Chart creation failed: {e}")


def create_react_page():
    """Create the custom Frappe Page for Vite React App."""
    if not frappe.db.exists("Page", "project_analytics"):
        doc = frappe.new_doc("Page")
        doc.page_name = "project_analytics"
        doc.title = "Project Analytics Dashboard"
        doc.module = "Interior Erp"
        doc.standard = "No"
        doc.content = """
<div id="vite-root" style="min-height: calc(100vh - 100px); background: #F8F5F0;"></div>
<link rel="stylesheet" href="/assets/interior_erp/frontend/assets/index.css">
"""
        doc.script = """
frappe.pages['project_analytics'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Project Analytics',
        single_column: true
    });
    
    $( `
<div id="vite-root" style="min-height: calc(100vh - 100px); background: #F8F5F0;"></div>
<link rel="stylesheet" href="/assets/interior_erp/frontend/assets/index.css">
    ` ).appendTo(page.main);

    // Load the vite bundle dynamically
    let script = document.createElement('script');
    script.type = 'module';
    script.src = '/assets/interior_erp/frontend/assets/index.js';
    document.body.appendChild(script);
}
"""
        try:
            doc.insert(ignore_permissions=True)
            print("✓ Created Custom Page: Project Analytics Dashboard")
        except Exception as e:
            print(f"✗ Failed to create page: {e}")

def create_and_hide_workspaces():
    """Create exact requested hierarchy for Interior ERP."""

    # First ensure analytics elements and page exist
    create_react_page()
    create_dashboard_elements()

    # 1. Delete ALL custom workspaces from previous attempts
    custom_ws = [
        "Home Dashboard", "CRM", "Leads", "Site Visits", "Projects", 
        "Design", "Proposals", "Payments", "Procurement", "Inventory", 
        "Budget Tracker", "Reports", "ERP Settings", "Dashboard",
        "Follow-ups", "Customers", "Design Workflow", "Project Execution",
        "Finance", "Budget", "Expenses", "Vendors", "Purchase Requests",
        "Purchase Orders", "Employees", "Settings", "Main Dashboard", "Project Budget"
    ]
    for w in custom_ws:
        if frappe.db.exists("Workspace", w):
            try:
                frappe.delete_doc("Workspace", w, ignore_permissions=True, force=True)
            except:
                pass

    frappe.db.commit()

    # 2. Hide ALL standard workspaces to keep sidebar perfectly clean
    all_std = frappe.get_all("Workspace", filters={"is_hidden": 0, "name": ["not in", custom_ws]})
    for w in all_std:
        frappe.db.set_value("Workspace", w.name, "is_hidden", 1)

    # 3. Define the exact requested structure
    workspaces = [
        # --- TOP LEVEL ---
        {
            "title": "Dashboard\u200b", 
            "id": "Main Dashboard", 
            "icon": "dashboard", 
            "seq": 1, 
            "parent": "",
            "shortcuts": [
                {"type": "DocType", "link_to": "Lead", "label": "Leads"},
                {"type": "DocType", "link_to": "Customer", "label": "Customers"},
                {"type": "DocType", "link_to": "ToDo", "label": "Follow-ups"},
                {"type": "DocType", "link_to": "Project", "label": "Projects"},
                {"type": "DocType", "link_to": "Proposal BOQ", "label": "Proposals"},
                {"type": "DocType", "link_to": "Site Visit", "label": "Site Visits"},
                {"type": "DocType", "link_to": "Task", "label": "Tasks & Execution"},
                {"type": "DocType", "link_to": "Budget", "label": "Budgets"},
                {"type": "DocType", "link_to": "Payment Entry", "label": "Payments"},
                {"type": "DocType", "link_to": "Journal Entry", "label": "Expenses"},
                {"type": "DocType", "link_to": "Supplier", "label": "Vendors"},
                {"type": "DocType", "link_to": "Material Request", "label": "Purchase Requests"},
                {"type": "DocType", "link_to": "Purchase Order", "label": "Purchase Orders"},
                {"type": "DocType", "link_to": "Item", "label": "Inventory"},
                {"type": "DocType", "link_to": "Employee", "label": "Employees"},
            ]
        },
        
        {"title": "CRM", "icon": "users", "seq": 2, "parent": ""},
        {"title": "Leads", "parent": "CRM", "doctype_link": "Lead"},
        {"title": "Follow-ups", "parent": "CRM", "doctype_link": "ToDo"},
        {"title": "Customers", "parent": "CRM", "doctype_link": "Customer"},

        {"title": "Projects", "icon": "folder", "seq": 3, "parent": ""},
        {"title": "Site Visits", "parent": "Projects", "doctype_link": "Site Visit"},
        {"title": "Proposals", "parent": "Projects", "doctype_link": "Proposal BOQ"},
        {"title": "Design Workflow", "parent": "Projects", "doctype_link": "Task"},
        {"title": "Project Execution", "parent": "Projects", "doctype_link": "Task"},

        {"title": "Finance", "icon": "money", "seq": 4, "parent": ""},
        {"title": "Payments", "parent": "Finance", "doctype_link": "Payment Entry"},
        {"title": "Budget\u200b", "id": "Project Budget", "parent": "Finance", "doctype_link": "Budget"},
        {"title": "Expenses", "parent": "Finance", "doctype_link": "Journal Entry"},

        {"title": "Procurement", "icon": "stock", "seq": 5, "parent": ""},
        {"title": "Vendors", "parent": "Procurement", "doctype_link": "Supplier"},
        {"title": "Purchase Requests", "parent": "Procurement", "doctype_link": "Material Request"},
        {"title": "Purchase Orders", "parent": "Procurement", "doctype_link": "Purchase Order"},
        {"title": "Inventory", "parent": "Procurement", "doctype_link": "Item"},

        {"title": "Reports", "icon": "chart", "seq": 6, "parent": "",
            "shortcuts": [
                {"type": "Report", "link_to": "General Ledger", "label": "General Ledger"},
                {"type": "Report", "link_to": "Accounts Receivable", "label": "Accounts Receivable"},
                {"type": "Report", "link_to": "Accounts Payable", "label": "Accounts Payable"},
                {"type": "Report", "link_to": "Sales Register", "label": "Sales Register"},
                {"type": "Report", "link_to": "Purchase Register", "label": "Purchase Register"},
                {"type": "Report", "link_to": "Stock Balance", "label": "Stock Balance"},
            ]
        },
        {"title": "Employees", "icon": "users", "seq": 7, "parent": "", "doctype_link": "Employee"},
        {"title": "Settings", "icon": "setting", "seq": 8, "parent": "",
            "shortcuts": [
                {"type": "DocType", "link_to": "User", "label": "Users"},
                {"type": "DocType", "link_to": "Role", "label": "Roles"},
                {"type": "Page", "link_to": "permission-manager", "label": "Role Permissions"},
                {"type": "DocType", "link_to": "User Permission", "label": "User Permissions"},
                {"type": "DocType", "link_to": "Data Import", "label": "Data Import"},
                {"type": "DocType", "link_to": "Data Export", "label": "Data Export"},
                {"type": "DocType", "link_to": "Workflow", "label": "Workflows"},
                {"type": "DocType", "link_to": "Custom Field", "label": "Custom Fields"},
                {"type": "DocType", "link_to": "Company", "label": "Company"},
                {"type": "DocType", "link_to": "System Settings", "label": "System Settings"},
                {"type": "DocType", "link_to": "Print Format", "label": "Print Formats"},
            ]
        },
    ]

    for ws in workspaces:
        ws_name = ws["title"]

        doc = frappe.new_doc("Workspace")
        doc.title = ws_name
        doc.label = ws_name
        doc.name = ws.get("id", ws_name)
        doc.module = "Interior Erp"
        doc.public = 1
        doc.is_hidden = 0
        
        if ws.get("parent"):
            doc.parent_page = ws["parent"]
        else:
            doc.icon = ws.get("icon", "folder")
            doc.sequence_id = ws.get("seq", 99)

        # Add shortcuts and build content JSON
        content = []
        if ws.get("shortcuts"):
            header_text = "Project Analytics & Quick Links" if "Dashboard" in ws_name else f"{ws_name} Shortcuts"
            content.append({
                "id": frappe.generate_hash(length=10), 
                "type": "header", 
                "data": {"text": header_text, "level": 4}
            })
            for s in ws.get("shortcuts", []):
                doc.append("shortcuts", {
                    "type": s["type"],
                    "link_to": s["link_to"],
                    "label": s["label"]
                })
                content.append({
                    "id": frappe.generate_hash(length=10),
                    "type": "shortcut",
                    "data": {
                        "shortcut_name": s["label"],
                        "col_span": 12 if "Vite React" in s["label"] else 3
                    }
                })
        
        # Manually add the number cards and charts for Dashboard
        if "Dashboard" in ws_name:
            content.append({
                "id": frappe.generate_hash(length=10),
                "type": "number_card",
                "data": {
                    "number_card_name": "Total Active Projects"
                }
            })
            content.append({
                "id": frappe.generate_hash(length=10),
                "type": "number_card",
                "data": {
                    "number_card_name": "New Leads This Month"
                }
            })
            content.append({
                "id": frappe.generate_hash(length=10),
                "type": "chart",
                "data": {
                    "chart_name": "Project Pipeline",
                    "col_span": 12
                }
            })
        # Automatically add Dashboards for child pages
        if ws.get("doctype_link"):
            dt = ws["doctype_link"]
            
            # 1. Ensure a "Total" Number Card exists
            nc_name = f"Total {ws_name}"
            if not frappe.db.exists("Number Card", nc_name):
                try:
                    nc = frappe.new_doc("Number Card")
                    nc.name = nc_name
                    nc.label = nc_name
                    nc.document_type = dt
                    nc.function = "Count"
                    nc.is_standard = 0
                    nc.is_public = 1
                    nc.insert(ignore_permissions=True)
                except: pass
            
            # 2. Ensure a "Monthly" Dashboard Chart exists
            chart_name = f"Monthly {ws_name}"
            if not frappe.db.exists("Dashboard Chart", chart_name):
                try:
                    c = frappe.new_doc("Dashboard Chart")
                    c.chart_name = chart_name
                    c.document_type = dt
                    c.chart_type = "Count"
                    c.timeseries = 1
                    c.based_on = "creation"
                    c.filters_json = "{}"
                    c.type = "Line"
                    c.is_standard = 0
                    c.is_public = 1
                    c.insert(ignore_permissions=True)
                except Exception as e: 
                    print(f"Chart error for {dt}: {e}")

            # 3. Inject the Dashboard into the Workspace
            content.append({"id": frappe.generate_hash(length=10), "type": "header", "data": {"text": f"{ws_name} Analytics", "level": 4}})
            content.append({"id": frappe.generate_hash(length=10), "type": "number_card", "data": {"number_card_name": nc_name}})
            content.append({"id": frappe.generate_hash(length=10), "type": "chart", "data": {"chart_name": chart_name, "col_span": 12}})
            
            # Provide quick list at the bottom just in case
            doc.append("quick_lists", {"document_type": dt, "label": f"All {ws_name}"})
            content.append({"id": frappe.generate_hash(length=10), "type": "header", "data": {"text": f"{ws_name} Data", "level": 4}})
            content.append({"id": frappe.generate_hash(length=10), "type": "quick_list", "data": {"quick_list_name": f"All {ws_name}"}})

        import json
        doc.content = json.dumps(content) if content else "[]"

        # Add a dummy link to ensure Frappe doesn't auto-hide the workspace
        dummy_doctype = "User" if ws_name == "Settings" else "Lead"
        doc.append("links", {
            "type": "Link",
            "link_type": "DocType",
            "link_to": dummy_doctype,
            "label": f"{ws_name} Records"
        })

        try:
            doc.insert(ignore_permissions=True)
            print(f"✓ Created: {ws_name}")
        except Exception as e:
            import traceback
            print(f"✗ Failed {ws_name}: {e}")

    frappe.db.commit()
    print("\n✅ Exact workspace hierarchy created with Analytics!")

