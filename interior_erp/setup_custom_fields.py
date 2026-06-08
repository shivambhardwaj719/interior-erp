import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    create_custom_fields(get_custom_fields())

def get_custom_fields():
    return {
        "Lead": [
            {
                "fieldname": "custom_interior_details_section",
                "fieldtype": "Section Break",
                "label": "Interior Design Details",
                "insert_after": "company"
            },
            {
                "fieldname": "custom_property_type",
                "fieldtype": "Select",
                "label": "Property Type",
                "options": "Residential\nCommercial\nRetail\nHospitality",
                "insert_after": "custom_interior_details_section"
            },
            {
                "fieldname": "custom_carpet_area",
                "fieldtype": "Float",
                "label": "Carpet Area (sq ft)",
                "insert_after": "custom_property_type"
            },
            {
                "fieldname": "custom_project_budget",
                "fieldtype": "Currency",
                "label": "Estimated Budget",
                "insert_after": "custom_carpet_area"
            },
            {
                "fieldname": "custom_preferred_style",
                "fieldtype": "Data",
                "label": "Preferred Style (e.g. Modern, Minimalist)",
                "insert_after": "custom_project_budget"
            },
            {
                "fieldname": "custom_followup_section",
                "fieldtype": "Section Break",
                "label": "Follow-up Tracking",
                "insert_after": "custom_preferred_style"
            },
            {
                "fieldname": "custom_next_followup_date",
                "fieldtype": "Date",
                "label": "Next Follow-up Date",
                "insert_after": "custom_followup_section"
            },
            {
                "fieldname": "custom_followup_status",
                "fieldtype": "Select",
                "label": "Follow-up Status",
                "options": "Pending\nCompleted\nMissed",
                "default": "Pending",
                "insert_after": "custom_next_followup_date",
                "read_only": 1
            }
        ],
        "Material Request": [
            {
                "fieldname": "custom_interior_project_section",
                "fieldtype": "Section Break",
                "label": "Interior Project Details",
                "insert_after": "transaction_date"
            },
            {
                "fieldname": "custom_proposal",
                "fieldtype": "Link",
                "options": "Proposal BOQ",
                "label": "Project Proposal (BOQ)",
                "insert_after": "custom_interior_project_section"
            }
        ],
        "Purchase Order": [
            {
                "fieldname": "custom_proposal",
                "fieldtype": "Link",
                "options": "Proposal BOQ",
                "label": "Project Proposal (BOQ)",
                "insert_after": "transaction_date"
            }
        ],
        "Purchase Receipt": [
            {
                "fieldname": "custom_proposal",
                "fieldtype": "Link",
                "options": "Proposal BOQ",
                "label": "Project Proposal (BOQ)",
                "insert_after": "posting_date"
            }
        ]
    }
