from frappe import _

def get_data(data=None):
    if not data:
        data = {}
        
    data.setdefault("transactions", []).append({
        "label": _("Interior Operations"),
        "items": ["Site Visit"]
    })
    
    return data
