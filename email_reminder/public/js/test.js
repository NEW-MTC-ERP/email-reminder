var field_clicked = false

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
								recipients: cur_frm.doc.emails ? cur_frm.doc.emails : [],
								reminder_schedule_date: cur_frm.doc.date_and_time ? cur_frm.doc.date_and_time : "" ,
								doctype: cur_frm.doc.doctype,
								docname: cur_frm.doc.name,
								site: window.origin
							},
							async: false,
							callback: function (r) {
								if(r.message === 'Success'){
									 frappe.show_alert({
												message:__('Email added to Email Queue'),
												indicator:'green'
											}, 5);
								} else {
									frappe.show_alert({
												message:__('Error in sending email. Check Error Log or contact technical team'),
												indicator:'red'
											}, 5);
								}
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
		callback: function (r) {
			if(r.message === 'Success'){
				 frappe.show_alert({
                            message:__('Email added to Email Queue'),
                            indicator:'green'
                        }, 5);
			} else {
				frappe.show_alert({
                            message:__('Error in sending email. Check Error Log or contact technical team'),
                            indicator:'red'
                        }, 5);
			}
        }
	})
}
function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  var div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    var txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

function focusIn() {
console.log("test onclick focus in")

	field_clicked = true
 	var a, i;
	  var div = document.getElementById("myDropdown");
	  a = div.getElementsByTagName("a");
	  for (i = 0; i < a.length; i++) {
			a[i].style.display = "";
	  }

}
function focusOut() {
	 var a, i;
  var div = document.getElementById("myDropdown");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
  		a[i].style.display = "None";
  }

}

