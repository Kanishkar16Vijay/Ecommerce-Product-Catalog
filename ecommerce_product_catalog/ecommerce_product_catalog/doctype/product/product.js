frappe.ui.form.on("Product", {
	refresh(frm) {
		if (frappe.user.has_role("Customer") && frappe.session.user != "Administrator") {
			frm.add_custom_button("Add to Cart", () => {
				frappe.call({
					method: "ecommerce_product_catalog.cart_fun.add_item",
					args: {
						product: frm.doc.name,
						price: frm.doc.price,
					},
					callback: (r) => {
						if (!r.message) {
							frappe.msgprint("Item Added to Cart");
						}
					},
				});
			});
			frm.add_custom_button("Cart", () => {
				frappe.db.get_value("User", frappe.session.user, "full_name").then((r) => {
					frappe.db.exists("Cart", r.message.full_name).then((exists) => {
						if (exists) {
							frappe.set_route("Form", "Cart", r.message.full_name);
						} else {
							frappe.msgprint(
								`Their is no cart for ${r.message.full_name}, Please create the cart`
							);
						}
					});
				});
			});
		}
		if (
			frm.doc.minimum_quantity >= frm.doc.quantity &&
			frappe.user.has_role("Stock Manager")
		) {
			frm.add_custom_button("Enter Stock", () => {
				frappe.new_doc("Stock Entry", {
					product: frm.doc.name,
				});
			});
		}
	},
});
