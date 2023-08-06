# Copyright (c) 2023, Hamza Abuabada and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ReminderSettings(Document):
    def generate_fields(self):
        for doctype in self.doctypes:
            data = self.get_fields(doctype)
            for field in data:
                fieldname = f"{field['dt']}-{(field['label'].lower() if 'label' in field else 'column_break_0').replace(' ', '_')}"
                cf_check = frappe.db.sql("SELECT * FROM `tabCustom Field` WHERE name=%s", fieldname)
                if not cf_check:
                    frappe.get_doc(field).insert(ignore_mandatory=1)

    def get_fields(self, doc):
        return [
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "label": "Messages",
                "fieldtype": "Tab Break"
            },
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "insert_after": "messages",
                "label": "Message",
                "fieldtype": "Small Text",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "insert_after": "message",
                "label": "Date and Time",
                "fieldtype": "Datetime",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "insert_after": "date_and_time",
                "fieldtype": "Column Break"
            },
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "label": "Emails",
                "fieldtype": "Table",
                "options": "Reminder Recipients",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": doc.document_type,
                "label": "Send Email",
                "insert_after": "emails",
                "fieldtype": "Button"
            }
        ]
