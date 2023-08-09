// Copyright (c) 2023, Hamza Abuabada and contributors
// For license information, please see license.txt

frappe.ui.form.on('Reminder Settings', {
    refresh:function(frm){
        cur_frm.disable_save() 
    },
	generate_fields: function(frm) {
        cur_frm.call({
            doc: cur_frm.doc,
            method: "generate_fields",
            async: false,
            args: {
                docs:frm.doc.doctypes.filter(row => row.document_type && row.document_type != "").map(row => row.document_type)
            } ,
            callback: function () {
                 frappe.show_alert({
                    message:__('Fields Created'),
                    indicator:'green'
                }, 3);
            }
        })
	}
});
