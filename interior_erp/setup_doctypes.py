import frappe

def create_doctypes():
    doctypes = [
        # Site Visit Room (Child Table)
        {
            "doctype": "DocType",
            "name": "Site Visit Room",
            "module": "Interior Erp",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "room_name", "fieldtype": "Data", "label": "Room Name", "in_list_view": 1},
                {"fieldname": "length", "fieldtype": "Float", "label": "Length (ft)", "in_list_view": 1},
                {"fieldname": "width", "fieldtype": "Float", "label": "Width (ft)", "in_list_view": 1},
                {"fieldname": "area", "fieldtype": "Float", "label": "Area (sq ft)", "read_only": 1, "in_list_view": 1}
            ]
        },
        # Site Visit
        {
            "doctype": "DocType",
            "name": "Site Visit",
            "module": "Interior Erp",
            "custom": 1,
            "is_submittable": 1,
            "naming_rule": "Expression",
            "autoname": "SV-.YYYY.-.####",
            "fields": [
                {"fieldname": "lead", "fieldtype": "Link", "options": "Lead", "label": "Lead", "reqd": 1, "in_list_view": 1},
                {"fieldname": "visit_date", "fieldtype": "Date", "label": "Visit Date", "reqd": 1, "in_list_view": 1},
                {"fieldname": "site_engineer", "fieldtype": "Link", "options": "User", "label": "Site Engineer", "in_list_view": 1},
                {"fieldname": "visit_status", "fieldtype": "Select", "label": "Status", "options": "Scheduled\nIn Progress\nCompleted\nCancelled", "default": "Scheduled"},
                {"fieldname": "rooms_section", "fieldtype": "Section Break", "label": "Measurements"},
                {"fieldname": "rooms", "fieldtype": "Table", "options": "Site Visit Room", "label": "Rooms"},
                {"fieldname": "total_area", "fieldtype": "Float", "label": "Total Area", "read_only": 1}
            ]
        },
        # BOQ Item (Child Table)
        {
            "doctype": "DocType",
            "name": "BOQ Item",
            "module": "Interior Erp",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "item_code", "fieldtype": "Link", "options": "Item", "label": "Item Code", "in_list_view": 1},
                {"fieldname": "item_name", "fieldtype": "Data", "label": "Item Name"},
                {"fieldname": "description", "fieldtype": "Text Editor", "label": "Description"},
                {"fieldname": "qty", "fieldtype": "Float", "label": "Qty", "reqd": 1, "in_list_view": 1},
                {"fieldname": "rate", "fieldtype": "Currency", "label": "Rate", "reqd": 1, "in_list_view": 1},
                {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "read_only": 1, "in_list_view": 1},
                {"fieldname": "item_group", "fieldtype": "Link", "options": "Item Group", "label": "Item Group"}
            ]
        },
        # Proposal BOQ
        {
            "doctype": "DocType",
            "name": "Proposal BOQ",
            "module": "Interior Erp",
            "custom": 1,
            "is_submittable": 1,
            "naming_rule": "Expression",
            "autoname": "BOQ-.YYYY.-.####",
            "fields": [
                {"fieldname": "lead", "fieldtype": "Link", "options": "Lead", "label": "Lead", "reqd": 1},
                {"fieldname": "customer", "fieldtype": "Link", "options": "Customer", "label": "Customer", "read_only": 1},
                {"fieldname": "site_visit", "fieldtype": "Link", "options": "Site Visit", "label": "Reference Site Visit"},
                {"fieldname": "designer", "fieldtype": "Link", "options": "User", "label": "Designer"},
                {"fieldname": "proposal_date", "fieldtype": "Date", "label": "Date", "reqd": 1},
                {"fieldname": "valid_till", "fieldtype": "Date", "label": "Valid Till"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Draft\nPending Internal Approval\nPending Client Approval\nApproved\nRejected", "default": "Draft"},
                {"fieldname": "items_section", "fieldtype": "Section Break", "label": "Costing"},
                {"fieldname": "items", "fieldtype": "Table", "options": "BOQ Item", "label": "Items"},
                {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount", "read_only": 1}
            ]
        },
        # Project Payment
        {
            "doctype": "DocType",
            "name": "Project Payment",
            "module": "Interior Erp",
            "custom": 1,
            "naming_rule": "Expression",
            "autoname": "PAY-.YYYY.-.####",
            "fields": [
                {"fieldname": "proposal", "fieldtype": "Link", "options": "Proposal BOQ", "label": "Project/Proposal", "reqd": 1},
                {"fieldname": "customer", "fieldtype": "Link", "options": "Customer", "label": "Customer", "read_only": 1},
                {"fieldname": "milestone_name", "fieldtype": "Data", "label": "Milestone Name", "reqd": 1},
                {"fieldname": "due_date", "fieldtype": "Date", "label": "Due Date", "reqd": 1},
                {"fieldname": "expected_amount", "fieldtype": "Currency", "label": "Expected Amount", "reqd": 1},
                {"fieldname": "amount_paid", "fieldtype": "Currency", "label": "Amount Paid", "default": "0"},
                {"fieldname": "status", "fieldtype": "Select", "label": "Status", "options": "Unpaid\nPartially Paid\nPaid\nOverdue", "default": "Unpaid"},
                {"fieldname": "payment_date", "fieldtype": "Date", "label": "Last Payment Date", "read_only": 1},
                {"fieldname": "payment_reference", "fieldtype": "Data", "label": "Payment Reference"}
            ]
        },
        # Site Labor Log
        {
            "doctype": "DocType",
            "name": "Site Labor Log",
            "module": "Interior Erp",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "trade_type", "fieldtype": "Select", "options": "Carpenter\nElectrician\nPlumber\nPainter\nHelper\nMason", "label": "Trade Type"},
                {"fieldname": "number_of_workers", "fieldtype": "Int", "label": "Number of Workers"},
                {"fieldname": "hours_worked", "fieldtype": "Float", "label": "Hours Worked"}
            ]
        },
        # Daily Site Diary
        {
            "doctype": "DocType",
            "name": "Daily Site Diary",
            "module": "Interior Erp",
            "custom": 1,
            "is_submittable": 1,
            "naming_rule": "Expression",
            "autoname": "DSD-.YYYY.-.####",
            "fields": [
                {"fieldname": "proposal", "fieldtype": "Link", "options": "Proposal BOQ", "label": "Project/Proposal", "reqd": 1},
                {"fieldname": "customer", "fieldtype": "Link", "options": "Customer", "label": "Customer", "read_only": 1},
                {"fieldname": "diary_date", "fieldtype": "Date", "label": "Date", "reqd": 1},
                {"fieldname": "site_engineer", "fieldtype": "Link", "options": "User", "label": "Site Engineer"},
                {"fieldname": "work_completed", "fieldtype": "Text Editor", "label": "Work Completed Today"},
                {"fieldname": "issues_and_delays", "fieldtype": "Text Editor", "label": "Issues and Delays"},
                {"fieldname": "labor_section", "fieldtype": "Section Break", "label": "Labor Log"},
                {"fieldname": "labor_logs", "fieldtype": "Table", "options": "Site Labor Log", "label": "Labor Logs"}
            ]
        },
        # Project Budget Item
        {
            "doctype": "DocType",
            "name": "Project Budget Item",
            "module": "Interior Erp",
            "custom": 1,
            "istable": 1,
            "fields": [
                {"fieldname": "item_group", "fieldtype": "Data", "label": "Category / Item Group"},
                {"fieldname": "estimated_amount", "fieldtype": "Currency", "label": "Estimated Budget"},
                {"fieldname": "actual_amount", "fieldtype": "Currency", "label": "Actual Cost"},
                {"fieldname": "variance", "fieldtype": "Currency", "label": "Variance"}
            ]
        },
        # Project Budget Tracker
        {
            "doctype": "DocType",
            "name": "Project Budget Tracker",
            "module": "Interior Erp",
            "custom": 1,
            "is_submittable": 1,
            "naming_rule": "Expression",
            "autoname": "BUD-.YYYY.-.####",
            "fields": [
                {"fieldname": "proposal", "fieldtype": "Link", "options": "Proposal BOQ", "label": "Project/Proposal", "reqd": 1},
                {"fieldname": "customer", "fieldtype": "Link", "options": "Customer", "label": "Customer", "read_only": 1},
                {"fieldname": "budget_status", "fieldtype": "Select", "options": "On Track\nUnder Budget\nOver Budget", "label": "Budget Status"},
                {"fieldname": "items_section", "fieldtype": "Section Break"},
                {"fieldname": "budget_items", "fieldtype": "Table", "options": "Project Budget Item", "label": "Budget Breakdown"},
                {"fieldname": "totals_section", "fieldtype": "Section Break"},
                {"fieldname": "total_estimated_cost", "fieldtype": "Currency", "label": "Total Estimated", "read_only": 1},
                {"fieldname": "total_actual_cost", "fieldtype": "Currency", "label": "Total Actual", "read_only": 1},
                {"fieldname": "total_variance", "fieldtype": "Currency", "label": "Total Variance", "read_only": 1}
            ]
        },
        # Employee Scorecard
        {
            "doctype": "DocType",
            "name": "Employee Scorecard",
            "module": "Interior Erp",
            "custom": 1,
            "is_submittable": 1,
            "naming_rule": "Expression",
            "autoname": "ESC-.YYYY.-.####",
            "fields": [
                {"fieldname": "employee_user", "fieldtype": "Link", "options": "User", "label": "Employee", "reqd": 1},
                {"fieldname": "role_type", "fieldtype": "Select", "options": "Designer\nSite Engineer\nProject Coordinator", "label": "Role", "reqd": 1},
                {"fieldname": "evaluation_month", "fieldtype": "Select", "options": "January\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember", "label": "Month", "reqd": 1},
                {"fieldname": "evaluation_year", "fieldtype": "Int", "label": "Year", "reqd": 1},
                {"fieldname": "metrics_section", "fieldtype": "Section Break"},
                {"fieldname": "projects_converted", "fieldtype": "Int", "label": "Projects Converted", "read_only": 1},
                {"fieldname": "total_project_value", "fieldtype": "Currency", "label": "Total Value Driven", "read_only": 1},
                {"fieldname": "incentive_amount", "fieldtype": "Currency", "label": "Calculated Incentive", "read_only": 1},
                {"fieldname": "notes", "fieldtype": "Text Editor", "label": "Calculation Notes", "read_only": 1}
            ]
        }
    ]

    for d in doctypes:
        if not frappe.db.exists("DocType", d["name"]):
            doc = frappe.get_doc(d)
            doc.insert(ignore_permissions=True)
            print(f"Created DocType: {d['name']}")
        else:
            print(f"DocType {d['name']} already exists.")
            
    try:
        from interior_erp.setup_custom_fields import after_install
        after_install()
        print("Applied Custom Fields!")
    except Exception as e:
        print(f"Could not apply custom fields automatically: {e}")
