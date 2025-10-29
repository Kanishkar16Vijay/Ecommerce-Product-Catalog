import frappe


def has_permission_cart(user=None):
    if not user:
        user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return ""
    
    return f"`tabCart`.`user` = '{user}'"


def has_permission(doc, user=None):
    if not user:
        user = frappe.session.user
    if "System Manager" in frappe.get_roles(user):
        return ""
    
    return doc.user == user


@frappe.whitelist()
def add_item(product, price):
    user = frappe.db.get_value("User", frappe.session.user, "full_name")
    cart = frappe.get_doc("Cart", user)
    for itm in cart.cart_items:
        if itm.product == product:
            itm.quantity+=1
            itm.amount = itm.quantity * int(price)
            break
    else :
        cart.append("cart_items", {
            "product":product,
            "quantity":1,
            "amount":price
        })
    cart.save()


@frappe.whitelist()
def clear_cart(name):
    cart = frappe.get_doc("Cart", name)
    cart.cart_items = []
    cart.save()


def minimum_stock(product):
    message = f'''
        <h3>Minimum Stock Reached for {product.product_name}</h3>
        <p>Hello Stock Manager,</p>
        <p>Kindly please refill the {product.product_name} as soon as possible.<p>
    '''
    frappe.sendmail(
        recipients=['lordk1612@gmail.com'],
        subject="Minimum Stock Reached",
        message=message
    )