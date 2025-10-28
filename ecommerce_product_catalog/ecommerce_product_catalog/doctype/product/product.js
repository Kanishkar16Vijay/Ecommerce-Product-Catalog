frappe.ui.form.on("Product", {
	refresh(frm) {
        if(frappe.session.user != "Administrator" && frappe.session.user != "Guest"){
            frm.add_custom_button("Add to Cart", () => {
                frappe.call({
                    method:"ecommerce_product_catalog.cart_fun.add_item",
                    args: {
                        product: frm.doc.name,
                        price: frm.doc.price
                    },
                    callback : (r) => {
                        if(! r.message){
                            frappe.msgprint("Item Added to Cart");
                        }
                    }
                });
            });
        }
        if(frm.doc.minimum_quantity >= frm.doc.quantity && frappe.session.user === "Administrator"){
            frm.add_custom_button("Enter Stock", () => {
                frappe.new_doc("Stock Entry", {
                    product: frm.doc.name
                })
            });
        }
	},
});
