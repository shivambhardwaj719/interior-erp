import frappe
from frappe.model.document import Document
from frappe.utils import getdate, today

class DailySiteDiary(Document):
    def validate(self):
        self.fetch_customer()
        self.validate_dates()

    def fetch_customer(self):
        if self.proposal and not self.customer:
            self.customer = frappe.db.get_value("Proposal BOQ", self.proposal, "customer")

    def validate_dates(self):
        if getdate(self.diary_date) > getdate(today()):
            frappe.throw("You cannot create a Daily Site Diary for a future date.")
            
    def on_submit(self):
        self.notify_project_coordinator()
        
    def notify_project_coordinator(self):
        pc_users = [u.parent for u in frappe.get_all("Has Role", filters={"role": "Project Coordinator"}, fields=["parent"])]
        pc_emails = frappe.get_all("User", filters={"name": ("in", pc_users)}, pluck="email")
        
        if not pc_emails:
            return
            
        subject = f"Site Report: {self.name} for {self.customer}"
        if self.issues_and_delays:
            subject = f"[ATTENTION REQUIRED] {subject}"
            
        message = f"""
        <h3>Daily Site Update</h3>
        <p><b>Date:</b> {self.diary_date}</p>
        <p><b>Engineer:</b> {self.site_engineer}</p>
        <hr>
        <h4>Work Completed:</h4>
        {self.work_completed}
        """
        
        if self.issues_and_delays:
            message += f"""
            <hr>
            <h4><span style="color:red;">Issues & Delays:</span></h4>
            {self.issues_and_delays}
            """
            
        frappe.sendmail(
            recipients=pc_emails,
            subject=subject,
            message=message,
            reference_doctype="Daily Site Diary",
            reference_name=self.name
        )
