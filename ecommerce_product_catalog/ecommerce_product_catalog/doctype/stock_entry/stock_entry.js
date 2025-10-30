frappe.ui.form.on("Stock Entry", {
	// refresh(frm) {

	// },
	product: function (frm) {
		frappe.db.get_value("Product", frm.doc.product, "price").then((r) => {
			frm.set_df_property("price", "reqd", r.message.price === 0);
		});
	},
});
