import frappe

def test_account():
    company = frappe.db.get_list("Company")[0].name
    try:
        doc = frappe.new_doc("Account")
        doc.account_name = "Miscellaneous Expenses"
        doc.company = company
        doc.account_type = "Expense Account"
        doc.is_group = 0
        parent = frappe.db.get_value("Account", {"company": company, "is_group": 1, "root_type": "Expense"})
        doc.parent_account = parent if parent else f"Expenses - {frappe.db.get_value('Company', company, 'abbr')}"
        doc.insert(ignore_permissions=True)
        print("Expense Account created:", doc.name)
    except Exception as e:
        import traceback
        traceback.print_exc()

    try:
        doc = frappe.new_doc("Account")
        doc.account_name = "Main Bank"
        doc.company = company
        doc.account_type = "Bank"
        doc.is_group = 0
        parent = frappe.db.get_value("Account", {"company": company, "is_group": 1, "root_type": "Asset"})
        doc.parent_account = parent if parent else f"Assets - {frappe.db.get_value('Company', company, 'abbr')}"
        doc.insert(ignore_permissions=True)
        print("Bank Account created:", doc.name)
    except Exception as e:
        import traceback
        traceback.print_exc()
