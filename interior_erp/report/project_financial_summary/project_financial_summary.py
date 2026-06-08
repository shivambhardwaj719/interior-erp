import frappe
from frappe import _

def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    report_summary = get_report_summary(data)
    
    return columns, data, None, chart, report_summary

def get_columns():
    return [
        {"fieldname": "proposal", "label": _("Proposal / Project"), "fieldtype": "Link", "options": "Proposal BOQ", "width": 150},
        {"fieldname": "customer", "label": _("Customer"), "fieldtype": "Link", "options": "Customer", "width": 150},
        {"fieldname": "designer", "label": _("Designer"), "fieldtype": "Link", "options": "User", "width": 120},
        {"fieldname": "estimated_cost", "label": _("Est. Budget"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "actual_cost", "label": _("Actual Cost"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "variance", "label": _("Profit Variance"), "fieldtype": "Currency", "width": 120},
        {"fieldname": "budget_status", "label": _("Budget Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "expected_collection", "label": _("Expected Payment"), "fieldtype": "Currency", "width": 130},
        {"fieldname": "actual_collection", "label": _("Received Payment"), "fieldtype": "Currency", "width": 130},
        {"fieldname": "pending_collection", "label": _("Pending Payment"), "fieldtype": "Currency", "width": 130}
    ]

def get_data(filters):
    conditions = ""
    if filters.get("designer"):
        conditions += f" AND p.designer = '{filters.get('designer')}'"
        
    query = f"""
        SELECT 
            p.name as proposal,
            p.customer,
            p.designer,
            IFNULL(b.total_estimated_cost, 0) as estimated_cost,
            IFNULL(b.total_actual_cost, 0) as actual_cost,
            IFNULL(b.total_variance, 0) as variance,
            IFNULL(b.budget_status, 'No Budget') as budget_status,
            (SELECT SUM(expected_amount) FROM `tabProject Payment` WHERE proposal = p.name AND docstatus=1) as expected_collection,
            (SELECT SUM(amount_paid) FROM `tabProject Payment` WHERE proposal = p.name AND docstatus=1) as actual_collection
        FROM `tabProposal BOQ` p
        LEFT JOIN `tabProject Budget Tracker` b ON b.proposal = p.name AND b.docstatus = 1
        WHERE p.docstatus = 1 {conditions}
    """
    
    data = frappe.db.sql(query, as_dict=True)
    
    for row in data:
        row['pending_collection'] = (row['expected_collection'] or 0) - (row['actual_collection'] or 0)
        
    return data

def get_chart(data):
    labels = []
    estimated = []
    actual = []
    
    for row in data:
        labels.append(row['proposal'])
        estimated.append(row['estimated_cost'])
        actual.append(row['actual_cost'])
        
    return {
        "data": {
            "labels": labels,
            "datasets": [
                {"name": "Estimated", "values": estimated},
                {"name": "Actual", "values": actual}
            ]
        },
        "type": "bar",
        "colors": ["#28a745", "#dc3545"]
    }

def get_report_summary(data):
    total_variance = sum([row['variance'] for row in data])
    total_pending = sum([row['pending_collection'] for row in data])
    
    return [
        {
            "value": total_variance,
            "indicator": "Green" if total_variance > 0 else "Red",
            "label": _("Total Profit Variance"),
            "datatype": "Currency",
        },
        {
            "value": total_pending,
            "indicator": "Orange",
            "label": _("Total Pending Payments"),
            "datatype": "Currency",
        }
    ]
