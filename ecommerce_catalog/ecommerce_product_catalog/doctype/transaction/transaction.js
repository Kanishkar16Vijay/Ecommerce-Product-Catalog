frappe.ui.form.on("Transaction", {
    after_save: function(frm) {
        localStorage.removeItem("member_id");
    }
});

frappe.ui.form.on("Transaction", {
    member: async function(frm) {
        if (!frm.doc.member) return;

        try {
            const member = await frappe.db.get_doc("Members", frm.doc.member);

            if (member.cart_items && member.cart_items.length > 0) {

                frm.clear_table("product_table");

                // Add cart items to transaction
                member.cart_items.forEach(item => {
                    let row = frm.add_child("product_table", {
                        product: item.product,
                        quantity: item.quantity,
                        price: item.price,
                        total: item.quantity * item.price
                    });
                });

                frm.refresh_field("product_table");

                frm.set_value("total_items", member.cart_items.length);
                const total_price = member.cart_items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
                frm.set_value("price", total_price);

            } else {
                frappe.msgprint("⚠️ No cart items found for this member.");
            }
        } catch (err) {
            console.error(err);
            frappe.msgprint("Something went wrong fetching the member data.");
        }
    }
});
