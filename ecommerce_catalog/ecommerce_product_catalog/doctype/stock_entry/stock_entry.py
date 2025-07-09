import frappe
from frappe.model.document import Document


class StockEntry(Document):
	def before_save(self) :
		if self.type == "New Stock" and (not self.price or self.price == 0):
			frappe.throw("Price cannot be zero for new stock entry.")
		pass

	def on_submit(self) :
		product=frappe.get_doc("Product", self.product)
		product.quantity += self.quantity
		if self.price != 0 or self.price is None:
			product.price = self.price
		product.save()
		frappe.db.commit()
		frappe.msgprint(f"Stock updated for {product.name}.")