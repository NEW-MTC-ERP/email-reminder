import frappe
import json
from frappe import __
import re

@frappe.whitelist()
def fetch_reminder_doctypes():
    reminder_doctypes = frappe.db.sql("""SELECT * FROM `tabReminder Doctypes`""", as_dict=1)
    return [doc.document_type for doc in reminder_doctypes]


@frappe.whitelist()
def send_email(message, recipients, reminder_schedule_date, doctype, docname, site):
    try:
        data = json.loads(recipients)
        emails = [email["email"] for email in data if email]
        if not emails:
            frappe.throw(__("Please add at least one email"))
            
        message = f"""{doctype}<br>" Reminder on Document {docname}<br><br>"{message}<br><br>"
                <a href='{site}/app/{doctype.lower().replace(' ', '-')}/{docname}'>Open Document</a>"""

        create_reminder(message, emails, doctype, docname)

        frappe.sendmail(
            recipients=emails,
            subject="Details",
            message=message,
            send_after=reminder_schedule_date,
        )

        return __("Success")
    
    except json.JSONDecodeError:
        frappe.log_error(f"JSON decoding error: {frappe.get_traceback()}")
        return __("Invalid JSON format , Check It and Try Again")
    
    except Exception as e:
        frappe.log_error(f"An Error Occurred: {e}\n{frappe.get_traceback()}")
        return __("Failed")


@frappe.whitelist()
def create_reminder(message, emails, doctype, docname):
    reminder = frappe.get_doc(
        {
            "doctype": "Reminder",
            "message": message,
            "document_type": doctype,
            "document_no": docname,
            "emails": get_emails(emails),
        }
    )
    reminder.flags.ignore_permissions = True
    reminder.insert()
    reminder.submit()


def get_emails(emails):
    emails_list = []
    for email in emails:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            frappe.throw(__(f"Invalid Email, Please Check It ! {email}"))
        emails_list.append({"email": email})
    return emails_list
