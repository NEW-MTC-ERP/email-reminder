import frappe
import json
from frappe import _
import re

@frappe.whitelist()
def fetch_reminder_doctypes():
    reminder_doctypes = frappe.db.sql("""SELECT * FROM `tabReminder Doctypes`""", as_dict=1)
    return [doc.document_type for doc in reminder_doctypes]

@frappe.whitelist()
def send_email(message, recipients, reminder_schedule_date, doctype, docname, site):
    if message and recipients and reminder_schedule_date:
        try:
            data = json.loads(recipients)
            emails = [email["email"] for email in data if email]
            if not emails:
                frappe.throw(_("Please add at least one email"))
            
            doctype_fr = doctype.lower().replace(' ', '-')
            document_link = f"<a href='{site}/app/{doctype_fr}/{docname}'>Open Document</a>"
            message = f"""{doctype}<br>" Reminder on Document {docname}<br><br>"{message}<br><br>"
                    {document_link}"""
            
            create_reminder(message, emails, doctype, docname)

            frappe.sendmail(
                recipients=emails,
                subject=_("Details"),
                message=_(message),
                send_after=reminder_schedule_date,
            )

            return "Success"
        
        except json.JSONDecodeError:
            frappe.log_error(f"JSON decoding error: {frappe.get_traceback()}")
        
        except frappe.exceptions.ValidationError as ve:
            frappe.log_error(f"Validation Error: {ve}\n{frappe.get_traceback()}")

        except frappe.exceptions.LinkValidationError as lve:
            frappe.log_error(f"Link Validation Error: {lve}\n{frappe.get_traceback()}")

        except frappe.exceptions.PermissionError as pe:
            frappe.log_error(f"Permission Error: {pe}\n{frappe.get_traceback()}")

    else :
        
        frappe.throw(_("Please Check if All Feilds in Messaging is Full !!"))



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
    invalid_emails = []
    for email in emails:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            invalid_emails.append(email)
        else:
            emails_list.append({"email": email})

    if invalid_emails:
        error_message = f"Invalid Emails: {', '.join(invalid_emails)}"
        frappe.throw(_(error_message))

    return emails_list

