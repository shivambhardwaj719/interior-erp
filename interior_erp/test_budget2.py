import frappe

def test_budget():
    try:
        company = frappe.db.get_list("Company")[0].name
        cost_center = frappe.db.get_list("Cost Center", filters={"company": company})[0].name
        expense_account = f"Miscellaneous Expenses - {frappe.db.get_value('Company', company, 'abbr')}"
        bank_account = f"Main Bank - {frappe.db.get_value('Company', company, 'abbr')}"
        
        fiscal_year = frappe.db.get_list("Fiscal Year")[0].name
        
        b = frappe.new_doc("Budget")
        b.budget_against = "Cost Center"
        b.cost_center = cost_center
        b.company = company
        b.fiscal_year = fiscal_year
        b.append("accounts", {"account": expense_account, "budget_amount": 5000})
        b.insert(ignore_permissions=True)
        print("Budget created successfully!")

        je = frappe.new_doc("Journal Entry")
        je.voucher_type = "Journal Entry"
        je.company = company
        je.append("accounts", {"account": expense_account, "debit_in_account_currency": 500, "cost_center": cost_center})
        je.append("accounts", {"account": bank_account, "credit_in_account_currency": 500})
        je.insert(ignore_permissions=True)
        print("Journal Entry created successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
