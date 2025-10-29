import frappe
from frappe.model.document import Document
from ecommerce_product_catalog.cart_fun import clear_cart, minimum_stock


class Transaction(Document):
	def before_save(self) :
		self.total_item = len(self.items)
		total_amount = 0
		for itm in self.items:
			total_amount += itm.amount
		
		self.total_amount = total_amount
	
	def on_submit(self):
		for itm in self.items:
			product = frappe.get_doc("Product", itm.product)
			if product.quantity < itm.quantity:
				frappe.throw(f"Sorry, The available quantity for {product.product_name} is {product.quantity}")
			else:
				frappe.db.set_value("Product", itm.product, "quantity", product.quantity - itm.quantity)
				if product.quantity - itm.quantity <= product.minimum_quantity:
					minimum_stock(product)

		clear_cart(self.user_name)
		frappe.db.commit()
		