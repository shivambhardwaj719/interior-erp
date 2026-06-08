import frappe

def test_nc():
    try:
        nc = frappe.new_doc("Number Card")
        nc.name = "Test Card"
        nc.label = "Test Card"
        nc.document_type = "Lead"
        nc.function = "Count"
        nc.is_standard = 0
        nc.insert(ignore_permissions=True)
        print("Success")
    except Exception as e:
        import traceback
        traceback.print_exc()

    try:
        c = frappe.new_doc("Dashboard Chart")
        c.chart_name = "Test Chart"
        c.document_type = "Lead"
        c.chart_type = "Count"
        c.timeseries = 1
        c.time_interval = "Monthly"
        c.type = "Line"
        c.is_standard = 0
        c.insert(ignore_permissions=True)
        print("Chart Success")
    except Exception as e:
        import traceback
        traceback.print_exc()
