import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class SiteVisit(Document):
    def validate(self):
        self.calculate_total_area()
        self.validate_dates()

    def validate_dates(self):
        if self.visit_status == "Completed" and getdate(self.visit_date) > getdate(today()):
            frappe.throw("A Site Visit cannot be marked as 'Completed' if the Visit Date is in the future.")

    def calculate_total_area(self):
        total = 0.0
        for room in self.get("rooms"):
            room.area = (room.length or 0) * (room.width or 0)
            total += room.area
            
        self.total_area = total
        
    def on_submit(self):
        if self.lead:
            frappe.get_doc({
                "doctype": "Comment",
                "comment_type": "Info",
                "reference_doctype": "Lead",
                "reference_name": self.lead,
                "content": f"Site Visit {self.name} has been completed and submitted."
            }).insert(ignore_permissions=True)
