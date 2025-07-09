frappe.ui.form.on('Members', {
    refresh: function(frm) {
        frm.add_custom_button("Go to Product List", function () {
            
            localStorage.setItem('member_id', frm.doc.name);

            frappe.set_route('List', 'Product');
        });
    }
});

frappe.ui.form.on("Members", {
    refresh: function(frm) {
        if (frm.doc.cart_items && frm.doc.cart_items.length > 0) {
            frm.add_custom_button("Checkout Cart", () => {
                let total_price = 0;
                for (let item of frm.doc.cart_items) {
                    total_price += item.total;
                }
                frappe.new_doc('Transaction', {
                    member: frm.doc.name,
                    product_table: frm.doc.cart_items,
                    total_items: frm.doc.cart_items.length,
                    price: total_price
                });
            });
        }
    }
});

