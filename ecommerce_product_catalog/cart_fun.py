import frappe


def has_permission_cart(user=None):
	if not user:
		user = frappe.session.user
	if "System Manager" in frappe.get_roles(user):
		return ""

	return f"`tabCart`.`user` = '{user}'"


def has_permission_transaction(user=None):
	if not user:
		user = frappe.session.user
	if "Stock Manager" in frappe.get_roles(user):
		return ""

	return f"`tabTransaction`.`user` = '{user}'"


def has_permission(doc, user=None):
	if not user:
		user = frappe.session.user
	if "Stock Manager" in frappe.get_roles(user):
		return True

	return doc.user == user


@frappe.whitelist()
def add_item(product, price):
	user = frappe.db.get_value("User", frappe.session.user, "full_name")
	cart = frappe.get_doc("Cart", user)
	for itm in cart.cart_items:
		if itm.product == product:
			itm.quantity += 1
			itm.amount = itm.quantity * int(price)
			break
	else:
		cart.append("cart_items", {"product": product, "quantity": 1, "amount": price})
	cart.save()


@frappe.whitelist()
def clear_cart(name):
	cart = frappe.get_doc("Cart", name)
	cart.cart_items = []
	cart.save()


def minimum_stock(product):
	message = f"""
        <h3>Minimum Stock Reached for {product.product_name}</h3>
        <p>Hello Stock Manager,</p>
        <p>Kindly please refill the {product.product_name} as soon as possible.<p>
    """
	frappe.sendmail(recipients=["lordk1612@gmail.com"], subject="Minimum Stock Reached", message=message)

	frappe.get_doc(
		{
			"doctype": "Notification Log",
			"subject": f"Minimum Stock Alert for {product.product_name}",
			"email_content": message,
			"for_user": "stockmanager@example.com",
			"type": "Alert",  # Info, Alert, or Warning
			"document_type": "Product",
			"document_name": product.name,
		}
	).insert(ignore_permissions=True)
