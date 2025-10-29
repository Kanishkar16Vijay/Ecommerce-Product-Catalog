import frappe
from frappe.model.document import Document


class StockEntry(Document):
	def on_submit(self):
		product = frappe.get_doc("Product", self.product)
		if self.price:
			product.price = self.price

		product.quantity += self.quantity
		self.amount = (self.price or product.price) * self.quantity
		product.save()
