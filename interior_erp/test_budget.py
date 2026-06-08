import frappe

def test_budget():
    try:
        company = frappe.db.get_list("Company")[0].name
        cost_center = frappe.db.get_list("Cost Center", filters={"company": company})[0].name
        expense_account = frappe.db.get_list("Account", filters={"company": company, "account_type": "Expense Account"})[0].name
        
        b = frappe.new_doc("Budget")
        b.budget_against = "Cost Center"
        b.cost_center = cost_center
        b.company = company
        b.append("accounts", {"account": expense_account, "budget_amount": 5000})
        b.insert(ignore_permissions=True)
        print("Budget created successfully!")
    except Exception as e:
        import traceback
        traceback.print_exc()
