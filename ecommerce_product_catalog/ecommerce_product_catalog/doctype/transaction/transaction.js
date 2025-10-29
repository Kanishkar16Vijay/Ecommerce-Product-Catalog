frappe.ui.form.on("Transaction", {
	refresh(frm) {
        if(frm.doc.docstatus != 1) frm.set_value('user', frappe.session.user);
	},
});
