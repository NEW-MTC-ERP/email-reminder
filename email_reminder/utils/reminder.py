import frappe, json


@frappe.whitelist()
def get_doctypes():
    docs = frappe.db.sql(""" SELECT * FROM `tabReminder Doctypes` """, as_dict=1)

    return [i.document_type for i in docs]


@frappe.whitelist()
def send_email(message, recipients, reminder_schedule_date, doctype, docname, site):
    try:
        data = json.loads(recipients)
        emails_ = [i['email'] for i in data if i]
        if not emails_:
            frappe.throw("Please add emails")
        f_message = doctype + "<br>" + "Reminder on Document " + docname + "<br><br>" + message + "<br><br> <a href='" + site + "/app/" + doctype.lower().replace(
            " ", "-") + "/" + docname + "' >Open Document</a>"
        create_reminder(message, emails_, doctype, docname)
        print(f_message)
        frappe.sendmail(
            recipients=emails_,
            subject="Details",
            message=f_message,
            send_after=reminder_schedule_date
        )
        return "Success"
    except:

        frappe.log_error(frappe.get_traceback())
        return "Failed"


@frappe.whitelist()
def create_reminder(message, emails_, doctype, docname):
    obj = {
        "doctype": "Reminder",
        "message": message,
        "document_type": doctype,
        "document_no": docname,
        "emails": get_emails(emails_)
    }
    rem = frappe.get_doc(obj).insert()
    rem.submit()


def get_emails(emails_):
    emails = []

    for i in emails_:
        if "@" not in i:
            frappe.throw("Invalid Email " + i)
        emails.append({"email": i})
