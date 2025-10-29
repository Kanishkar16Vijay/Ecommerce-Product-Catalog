frappe.ui.form.on("Stock Entry", {
	// refresh(frm) {

	// },
	product: function (frm) {
		frappe.db.get_value("Product", frm.doc.product, "price").then((r) => {
			if (r.message.price === 0) {
				frm.set_df_property("price", "reqd", 1);
			}
		});
	},
});
