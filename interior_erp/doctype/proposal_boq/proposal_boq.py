import frappe
from frappe.model.document import Document
from frappe.utils import getdate

class ProposalBOQ(Document):
    def validate(self):
        self.validate_dates()
        self.calculate_totals()

    def validate_dates(self):
        if self.valid_till and self.proposal_date:
            if getdate(self.valid_till) < getdate(self.proposal_date):
                frappe.throw("The 'Valid Till' date cannot be earlier than the Proposal Date.")

    def calculate_totals(self):
        total = 0.0
        for item in self.get("items"):
            item.amount = (item.qty or 0) * (item.rate or 0)
            total += item.amount
            
        self.total_amount = total
        
    def on_submit(self):
        if self.lead and not self.customer:
            self.convert_lead_to_customer()
            
    def convert_lead_to_customer(self):
        lead_doc = frappe.get_doc("Lead", self.lead)
        
        customer_name = frappe.db.get_value("Customer", {"lead_name": self.lead}, "name")
        
        if not customer_name:
            customer = frappe.new_doc("Customer")
            customer.customer_name = lead_doc.company or lead_doc.lead_name
            customer.customer_type = "Company" if lead_doc.company else "Individual"
            customer.customer_group = "Commercial"
            customer.territory = lead_doc.territory or "All Territories"
            customer.lead_name = self.lead
            customer.insert(ignore_permissions=True)
            
            frappe.db.set_value("Proposal BOQ", self.name, "customer", customer.name)
            frappe.db.set_value("Lead", self.lead, "status", "Converted")
            
            frappe.msgprint(f"Customer {customer.name} created automatically from Lead.")
