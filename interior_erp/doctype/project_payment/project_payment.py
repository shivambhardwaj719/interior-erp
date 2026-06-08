import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class ProjectPayment(Document):
    def before_save(self):
        self.fetch_customer()
        self.update_status()

    def fetch_customer(self):
        if self.proposal and not self.customer:
            self.customer = frappe.db.get_value("Proposal BOQ", self.proposal, "customer")

    def update_status(self):
        if self.status == "Paid":
            return

        if self.amount_paid >= self.expected_amount:
            self.status = "Paid"
            self.payment_date = self.payment_date or today()
        elif self.amount_paid > 0:
            self.status = "Partially Paid"
        elif getdate(self.due_date) < getdate(today()):
            self.status = "Overdue"
        else:
            self.status = "Unpaid"
