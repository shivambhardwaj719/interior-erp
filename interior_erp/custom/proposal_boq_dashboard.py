from frappe import _

def get_data(data=None):
    if not data:
        data = {}
        
    data.setdefault("transactions", []).append({
        "label": _("Execution Logs"),
        "items": ["Daily Site Diary", "Project Payment"]
    })
    
    data.setdefault("transactions", []).append({
        "label": _("Procurement"),
        "items": ["Material Request", "Purchase Order", "Purchase Receipt"]
    })
    
    data.setdefault("fieldname", "custom_proposal")
    
    return data
