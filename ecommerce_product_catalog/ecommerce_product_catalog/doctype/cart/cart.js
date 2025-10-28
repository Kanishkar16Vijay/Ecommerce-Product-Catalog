frappe.ui.form.on("Cart", {
	refresh(frm) {
        if(frappe.session.user != "Administrator" && frappe.session.user != "Guest" && frm.doc.cart_items.length){
            frm.add_custom_button("Clear Cart", () => {
                frappe.call({
                    method:"ecommerce_product_catalog.cart_fun.clear_cart",
                    args: {
                        name : frm.doc.name
                    },
                    callback : (r) => {
                        if(! r.message){
                            frappe.msgprint("Cart Cleared");
                        }
                    }
                })
            })
        }
	},
});
