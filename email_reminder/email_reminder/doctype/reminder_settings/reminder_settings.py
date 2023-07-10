# Copyright (c) 2023, Hamza Abuabada and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ReminderSettings(Document):
    @frappe.whitelist()
    def generate_fields(self):
        for i in self.doctypes:
            data = self.get_fields(i)
            for x in data:
                fieldname = x['dt'] + "-" + ((x['label'].lower() if 'label' in x else "column_break_0")).replace(" ",
                                                                                                                 "_")
                cf_check = frappe.db.sql(""" SELECT * FROm `tabCustom Field` WHERE name=%s """, fieldname)
                if len(cf_check) == 0:
                    frappe.get_doc(x).insert(ignore_mandatory=1)

    def get_fields(self, i):
        return [
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "label": "Messages",
                "fieldtype": "Tab Break",
            },
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "insert_after": "messages",
                "label": "Message",
                "fieldtype": "Small Text",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "insert_after": "message",
                "label": "Date and Time",
                "fieldtype": "Datetime",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "insert_after": "date_and_time",
                "fieldtype": "Column Break"
            },
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "label": "Emails",
                "fieldtype": "Table",
                "options": "Reminder Recipients",
                "allow_on_submit": 1
            },
            {
                "doctype": "Custom Field",
                "dt": i.document_type,
                "label": "Send Email",
                "insert_after": "emails",
                "fieldtype": "Button"
            },

        ]
