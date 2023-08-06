import frappe
import json


@frappe.whitelist()
def get_doctypes():
    docs = frappe.db.sql("""SELECT * FROM `tabReminder Doctypes`""", as_dict=1)
    return [doc.document_type for doc in docs]


@frappe.whitelist()
def send_email(message, recipients, reminder_schedule_date, doctype, docname, site):
    try:
        data = json.loads(recipients)
        emails_ = [email["email"] for email in data if email]
        if not emails_:
            frappe.throw("Please add at least one email")

        message = doctype + "<br>" + "Reminder on Document " + docname
        +"<br><br>" + message + "<br><br> <a href='" + site + "/app/"
        +doctype.lower().replace(" ", "-")
        + "/" + docname + "' >Open Document</a>"

        create_reminder(message, emails_, doctype, docname)

        frappe.sendmail(
            recipients=emails_,
            subject="Details",
            message=message,
            send_after=reminder_schedule_date,
        )

        return "Success"

    except:
        frappe.log_error(frappe.get_traceback())
        return "Failed"


@frappe.whitelist()
def create_reminder(message, emails_, doctype, docname):
    reminder = frappe.get_doc(
        {
            "doctype": "Reminder",
            "message": message,
            "document_type": doctype,
            "document_no": docname,
            "emails": get_emails(emails_),
        }
    )
    reminder.flags.ignore_permissions = True
    reminder.insert()
    reminder.submit()


def get_emails(emails_):
    emails = []
    for email in emails_:
        if "@" not in email:
            frappe.throw("Invalid Email, Please Check It ! " + email)
        emails.append({"email": email})
    return emails
