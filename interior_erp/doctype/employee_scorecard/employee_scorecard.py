import frappe
from frappe.model.document import Document
import calendar

class EmployeeScorecard(Document):
    def validate(self):
        self.calculate_score()

    def calculate_score(self):
        month_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
        month_num = month_dict.get(self.evaluation_month)
        
        if not month_num:
            return

        month_str = f"{month_num:02d}"
        year_str = str(self.evaluation_year)
        
        if self.role_type == "Designer":
            self.calculate_designer_incentive(month_str, year_str)
        elif self.role_type == "Site Engineer":
            self.calculate_engineer_score(month_str, year_str)

    def calculate_designer_incentive(self, month, year):
        start_date = f"{year}-{month}-01"
        _, last_day = calendar.monthrange(int(year), int(month))
        end_date = f"{year}-{month}-{last_day}"

        proposals = frappe.get_all(
            "Proposal BOQ",
            filters={
                "designer": self.employee_user,
                "status": "Approved",
                "modified": ["between", [start_date, end_date]]
            },
            fields=["name", "total_amount"]
        )

        self.projects_converted = len(proposals)
        self.total_project_value = sum([p.total_amount for p in proposals])
        
        self.incentive_amount = self.total_project_value * 0.02
        
        project_names = [p.name for p in proposals]
        if project_names:
            self.notes = f"Calculated based on approved proposals: {', '.join(project_names)}"
        else:
            self.notes = "No approved proposals found for this period."

    def calculate_engineer_score(self, month, year):
        self.projects_converted = 0
        self.total_project_value = 0
        self.incentive_amount = 0
        self.notes = "Site Engineer metrics are currently based on qualitative review."
