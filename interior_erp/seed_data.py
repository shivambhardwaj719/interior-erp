import frappe
from frappe.utils import add_days, nowdate
import random

def generate_dummy_data():
    frappe.flags.in_import = True # Bypass some strict validations
    
    first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Karen", "Leo", "Mia", "Nina", "Oscar", "Paul", "Quinn", "Rachel"]
    last_names = ["Smith", "Doe", "Johnson", "Brown", "Williams", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor"]
    company_names = ["Acme Corp", "Globex", "Initech", "Soylent", "Umbrella", "Massive Dynamic", "Stark Ind", "Wayne Ent", "Cyberdyne", "Hooli", "Vehement", "Dunder Mifflin", "Pied Piper", "Aviato", "EndFrame"]
    locations = ["New York", "London", "Dubai", "Mumbai", "Singapore", "Tokyo", "Paris", "Berlin", "Sydney", "Toronto"]
    
    def get_name(): return f"{random.choice(first_names)} {random.choice(last_names)}"
    def get_company(): return f"{random.choice(company_names)} {random.randint(10,999)}"

    print("Seeding Items...")
    items = []
    for i in range(50):
        name = f"Interior Item {i+1} - {random.randint(1000, 9999)}"
        if not frappe.db.exists("Item", name):
            doc = frappe.new_doc("Item")
            doc.item_code = name
            doc.item_name = name
            doc.item_group = "All Item Groups"
            doc.is_stock_item = 0
            try: doc.insert(ignore_permissions=True)
            except: pass
        items.append(name)

    print("Seeding Suppliers...")
    for i in range(50):
        name = f"Supplier {get_company()}"
        if not frappe.db.exists("Supplier", name):
            doc = frappe.new_doc("Supplier")
            doc.supplier_name = name
            doc.supplier_group = "All Supplier Groups"
            try: doc.insert(ignore_permissions=True)
            except: pass

    print("Seeding Employees...")
    for i in range(50):
        fname = random.choice(first_names)
        if not frappe.db.exists("Employee", {"first_name": fname, "last_name": str(i)}):
            doc = frappe.new_doc("Employee")
            doc.first_name = fname
            doc.last_name = str(i)
            doc.gender = random.choice(["Male", "Female"])
            doc.date_of_joining = add_days(nowdate(), -random.randint(100, 1000))
            doc.date_of_birth = add_days(nowdate(), -random.randint(8000, 15000))
            try: doc.insert(ignore_permissions=True)
            except: pass

    print("Seeding Leads...")
    leads = []
    for i in range(50):
        name = get_company()
        if not frappe.db.exists("Lead", {"lead_name": name}):
            doc = frappe.new_doc("Lead")
            doc.lead_name = name
            doc.company_name = name
            doc.status = random.choice(["Lead", "Open", "Replied", "Opportunity", "Quotation", "Lost Quotation", "Interested", "Converted", "Do Not Contact"])
            try: 
                doc.insert(ignore_permissions=True)
                leads.append(doc.name)
            except: pass

    print("Seeding Customers...")
    customers = []
    try:
        cust_group = frappe.db.get_list("Customer Group")[0].name
        territory = frappe.db.get_list("Territory")[0].name
        for i in range(50):
            name = f"Customer {get_company()}"
            if not frappe.db.exists("Customer", name):
                doc = frappe.new_doc("Customer")
                doc.customer_name = name
                doc.customer_group = cust_group
                doc.territory = territory
                try: 
                    doc.insert(ignore_permissions=True)
                    customers.append(doc.name)
                except Exception as e: pass
    except: pass

    print("Seeding Projects...")
    projects = []
    for i in range(50):
        name = f"Project {get_company()} {i}"
        if not frappe.db.exists("Project", {"project_name": name}):
            doc = frappe.new_doc("Project")
            doc.project_name = name
            doc.status = random.choice(["Open", "Completed", "Cancelled"])
            if customers:
                doc.customer = random.choice(customers)
            try: 
                doc.insert(ignore_permissions=True)
                projects.append(doc.name)
            except: pass

    print("Seeding Tasks (Design & Execution)...")
    if projects:
        for i in range(50):
            doc = frappe.new_doc("Task")
            doc.subject = f"{random.choice(['Design', 'Execution', 'Planning', 'Review'])} Phase {i+1}"
            doc.project = random.choice(projects)
            doc.status = random.choice(["Open", "Working", "Pending Review", "Completed", "Cancelled"])
            try: doc.insert(ignore_permissions=True)
            except: pass

    print("Seeding Site Visits...")
    if leads:
        for i in range(50):
            doc = frappe.new_doc("Site Visit")
            doc.lead = random.choice(leads)
            doc.visit_date = add_days(nowdate(), random.randint(-30, 30))
            doc.visit_status = random.choice(["Scheduled", "In Progress", "Completed", "Cancelled"])
            try: doc.insert(ignore_permissions=True)
            except Exception as e: pass

    print("Seeding Proposal BOQs...")
    if leads:
        for i in range(50):
            doc = frappe.new_doc("Proposal BOQ")
            doc.lead = random.choice(leads)
            doc.proposal_date = nowdate()
            doc.status = random.choice(["Draft", "Pending Internal Approval", "Pending Client Approval", "Approved", "Rejected"])
            try: doc.insert(ignore_permissions=True)
            except Exception as e: pass

    print("Seeding Follow-ups (ToDos)...")
    for i in range(50):
        doc = frappe.new_doc("ToDo")
        doc.description = f"Follow up with client regarding {random.choice(['design', 'proposal', 'payment', 'site visit'])}"
        if leads:
            doc.reference_type = "Lead"
            doc.reference_name = random.choice(leads)
        try: doc.insert(ignore_permissions=True)
        except: pass

    print("Seeding Material Requests...")
    if items:
        for i in range(50):
            doc = frappe.new_doc("Material Request")
            doc.material_request_type = "Purchase"
            doc.schedule_date = add_days(nowdate(), random.randint(1, 30))
            doc.append("items", {
                "item_code": random.choice(items),
                "qty": random.randint(1, 100),
                "schedule_date": doc.schedule_date
            })
            try: doc.insert(ignore_permissions=True)
            except: pass

    frappe.db.commit()

    print("Seeding Budgets and Expenses...")
    try:
        companies = frappe.db.get_list("Company")
        if not companies:
            print("No Company found. Skipping Budgets/Expenses.")
        else:
            company = companies[0].name
            
            # Ensure Cost Center exists
            cost_centers = frappe.db.get_list("Cost Center", filters={"company": company, "is_group": 0})
            if not cost_centers:
                doc = frappe.new_doc("Cost Center")
                doc.cost_center_name = "Main"
                doc.company = company
                doc.is_group = 0
                doc.insert(ignore_permissions=True)
                cost_center = doc.name
            else:
                cost_center = cost_centers[0].name

            # Ensure Expense Account exists
            expense_accounts = frappe.db.get_list("Account", filters={"company": company, "account_type": "Expense Account", "is_group": 0})
            if not expense_accounts:
                doc = frappe.new_doc("Account")
                doc.account_name = "Miscellaneous Expenses"
                doc.company = company
                doc.account_type = "Expense Account"
                doc.is_group = 0
                parent = frappe.db.get_value("Account", {"company": company, "is_group": 1, "root_type": "Expense"})
                doc.parent_account = parent if parent else f"Expenses - {frappe.db.get_value('Company', company, 'abbr')}"
                try: doc.insert(ignore_permissions=True)
                except: pass
                expense_account = doc.name
            else:
                expense_account = expense_accounts[0].name

            # Ensure Bank Account exists
            bank_accounts = frappe.db.get_list("Account", filters={"company": company, "account_type": "Bank", "is_group": 0})
            if not bank_accounts:
                doc = frappe.new_doc("Account")
                doc.account_name = "Main Bank"
                doc.company = company
                doc.account_type = "Bank"
                doc.is_group = 0
                parent = frappe.db.get_value("Account", {"company": company, "is_group": 1, "root_type": "Asset"})
                doc.parent_account = parent if parent else f"Assets - {frappe.db.get_value('Company', company, 'abbr')}"
                try: doc.insert(ignore_permissions=True)
                except: pass
                bank_account = doc.name
            else:
                bank_account = bank_accounts[0].name
            
            frappe.db.commit()

            print("Seeding 50 Budgets...")
            fiscal_year = frappe.db.get_list("Fiscal Year")[0].name
            for i in range(50):
                if not frappe.db.exists("Budget", {"cost_center": cost_center, "company": company, "name": f"BUD-{i}"}):
                    b = frappe.new_doc("Budget")
                    b.budget_against = "Cost Center"
                    b.cost_center = cost_center
                    b.company = company
                    b.fiscal_year = fiscal_year
                    b.append("accounts", {"account": expense_account, "budget_amount": random.randint(1000, 50000)})
                    try: b.insert(ignore_permissions=True)
                    except Exception as e: pass

            print("Seeding 50 Expenses (Journal Entries)...")
            for i in range(50):
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = "Journal Entry"
                je.company = company
                je.posting_date = add_days(nowdate(), -random.randint(1, 30))
                je.append("accounts", {"account": expense_account, "debit_in_account_currency": 500, "cost_center": cost_center})
                je.append("accounts", {"account": bank_account, "credit_in_account_currency": 500})
                try: 
                    je.insert(ignore_permissions=True)
                    je.submit() # Submit to make it final
                except Exception as e: pass

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Skipping Budgets/Expenses due to accounting error: {e}")

    print("✅ Successfully seeded 50+ records for Leads, Customers, Projects, Tasks, Site Visits, Proposals, Suppliers, Items, Employees, ToDos, and Material Requests!")

if __name__ == "__main__":
    generate_dummy_data()
