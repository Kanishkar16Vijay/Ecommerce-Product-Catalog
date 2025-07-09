# Copyright (c) 2025, Kanishkar and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Transaction(Document):
    def before_save(self) :
        for item in self.product_table:
            product=frappe.get_doc("Product", item.product)
            if item.quantity <= product.quantity :
                product.quantity -= item.quantity
                product.save()
                if product.quantity < (product.minimum_stock or 0):
                    # Set the email parameters
                    subject = f"Low Stock Alert: {product.name1}"
                    message = f"""
                    Hello,

                    The stock for <b>{product.name1}</b> has fallen below the minimum threshold.
                    <br><br>
                    <b>Available Quantity:</b> {product.quantity}<br>
                    <b>Minimum Threshold:</b> {product.minimum_stock}
                    <br><br>
                    Please take action accordingly.

                    <br><br>
                    Regards,<br>
                    Inventory System
                    """

                    recipients = ["lordk1612@gmail.com"]

                    frappe.sendmail(
                        recipients=recipients,
                        subject=subject,
                        message=message
                    )
            else:
                frappe.throw(f"Insufficient stock for product {item.product}. Available quantity: {product.quantity}, Requested quantity: {item.quantity}")
            
    def on_submit(self):
        member = frappe.get_doc("Members", self.member)
        member.set("cart_items",[])
        member.save()