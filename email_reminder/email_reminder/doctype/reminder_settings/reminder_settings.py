# Copyright (c) 2023, Hamza Abuabada and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

class ReminderSettings(Document):
    def validate(self):
        self.doctypes = []
    
    @frappe.whitelist()
    def generate_fields(self, docs):
        if not isinstance(docs,list) or len(docs) == 0:return
        frappe.db.sql("""UPDATE `tabCustom Field` SET
                       hidden = 1 where CONCAT(dt, '-', LOWER(dt), '_messages') = name
                       AND fieldtype='Tab Break'""")
        frappe.db.commit()
        for doc in docs :
            if not doc or frappe.db.exists("Doctype",doc):continue
            fields = self.get_fields(doc)
            create_custom_fields(fields)

    def get_fields(self, doc):
        dfs = {doc:[
            frappe._dict(fieldname = f"{doc.lower()}_messages",label = "Messages",fieldtype = "Tab Break", hidden = 0),
            frappe._dict(fieldname = f"{doc.lower()}_message",label = "Message",fieldtype = "Small Text" , insert_after = f"{doc.lower()}_messages",allow_on_submit = 1),
            frappe._dict(fieldname = f"{doc.lower()}_date_and_time",label = "Date and Time",fieldtype = "Datetime", insert_after =f"{doc.lower()}_message",allow_on_submit = 1),
            frappe._dict(fieldname = f"{doc.lower()}_column_break",fieldtype = "Column Break" ,insert_after = f"{doc.lower()}_date_and_time"),
            frappe._dict(fieldname = f"{doc.lower()}_emails",label = "Emails",fieldtype = "Table", options= "Reminder Recipients",allow_on_submit = 1,insert_after =f"{doc.lower()}_column_break"),
            frappe._dict(fieldname = f"{doc.lower()}_send_email",label = "Send Email",fieldtype = "Button",insert_after = f"{doc.lower()}_emails"),
        ]}
        return dfs
