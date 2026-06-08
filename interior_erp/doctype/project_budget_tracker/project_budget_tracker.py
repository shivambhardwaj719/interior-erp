import frappe
from frappe.model.document import Document

class ProjectBudgetTracker(Document):
    def validate(self):
        self.fetch_customer()
        self.calculate_actuals()
        self.calculate_variance()

    def fetch_customer(self):
        if self.proposal and not self.customer:
            self.customer = frappe.db.get_value("Proposal BOQ", self.proposal, "customer")

    def calculate_actuals(self):
        for item in self.get("budget_items"):
            item.actual_amount = 0.0

        pos = frappe.get_all("Purchase Order", 
            filters={"custom_proposal": self.proposal, "docstatus": 1},
            fields=["name"]
        )
        for po in pos:
            po_items = frappe.get_all("Purchase Order Item", filters={"parent": po.name}, fields=["item_group", "amount"])
            for po_item in po_items:
                self._add_to_actuals(po_item.item_group, po_item.amount)

        diaries = frappe.get_all("Daily Site Diary", filters={"proposal": self.proposal, "docstatus": 1}, fields=["name"])
        for diary in diaries:
            labor_logs = frappe.get_all("Site Labor Log", filters={"parent": diary.name}, fields=["trade_type", "number_of_workers", "hours_worked"])
            for labor in labor_logs:
                cost = (labor.number_of_workers or 0) * (labor.hours_worked or 0) * 500
                self._add_to_actuals("Labor", cost)

    def _add_to_actuals(self, group, amount):
        matched = False
        for item in self.get("budget_items"):
            if item.item_group == group:
                item.actual_amount += amount
                matched = True
                break
        
        if not matched and group == "Labor":
            self.append("budget_items", {
                "item_group": "Labor",
                "estimated_amount": 0,
                "actual_amount": amount
            })

    def calculate_variance(self):
        tot_est = 0.0
        tot_act = 0.0
        
        for item in self.get("budget_items"):
            item.variance = item.estimated_amount - item.actual_amount
            tot_est += item.estimated_amount
            tot_act += item.actual_amount
            
        self.total_estimated_cost = tot_est
        self.total_actual_cost = tot_act
        self.total_variance = tot_est - tot_act
        
        if self.total_variance < 0:
            self.budget_status = "Over Budget"
        elif self.total_actual_cost > (self.total_estimated_cost * 0.9):
            self.budget_status = "On Track"
        else:
            self.budget_status = "Under Budget"
