$(document).on('app_ready', function() {
	frappe.call({
		method: "email_reminder.utils.reminder.fetch_reminder_doctypes",
		async: false,
		callback: function (r) {
			$.each(r.message, function(i, doctype) {
				frappe.ui.form.on(doctype, "send_email", function(frm) {
					frappe.call({
							method: "email_reminder.utils.reminder.send_email",
							args: {
								message: cur_frm.doc.message,
								recipients: cur_frm.doc.emails,
								reminder_schedule_date: cur_frm.doc.date_and_time,
								doctype: cur_frm.doc.doctype,
								docname: cur_frm.doc.name,
								site: window.origin
							},
							async: false,
							callback: function (r) {
								var message = r.message === 'Success'
									? { message: __('Email added to Email Queue'), indicator: 'green' }
									: { message: __('Error in sending email, Check Error Log or contact technical team'), indicator: 'red' };
					
								frappe.show_alert(message, 5);
							}
						})
				});
			});
        }
	})

});


function send_email(cur_frm) {
	frappe.call({
		method: "email_reminder.utils.reminder.send_email",
		args: {
			message: document.getElementById('reminder').value,
			recipients: document.getElementById('recipients').value,
			reminder_schedule_date: document.getElementById('reminder_time').value,
			doctype: cur_frm.doc.doctype,
			docname: cur_frm.doc.name,
		},
		async: false,
		callback: function(r) {
            var message = r.message === 'Success'
                ? { message: __('Email added to Email Queue'), indicator: 'green' }
                : { message: __('Error in sending email, Check Error Log or contact technical team'), indicator: 'red' };

            frappe.show_alert(message, 5);
        }
	})
}
function filterFunction() {
	var input = document.getElementById("toggleInput");
    var filter = input.value.toUpperCase();
    var div = document.getElementById("toggleDropdown");
    var a = div.getElementsByTagName("a");

  for (i = 0; i < a.length; i++) {
    var txtValue = a[i].textContent || a[i].innerText;
            a[i].style.display = txtValue.toUpperCase().indexOf(filter) > -1 ? "" : "none";
  }
}

function toggleDropdown(display) {
    var a = document.querySelectorAll("#toggleDropdown a");

    a.forEach(function(link) {
        link.style.display = display;
    });
}

function focusIn() {
    console.log("test onclick focus in");
    field_clicked = true;
    toggleDropdown("");
}

function focusOut() {
    toggleDropdown("none");
}

