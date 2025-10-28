import frappe

def create_cart(doc, method) :
    if not frappe.db.exists("Cart", doc.full_name):
        cart = frappe.new_doc("Cart")
        cart.user = doc.email
        cart.insert()
        frappe.msgprint("Cart for the user is created sucessfully")


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
            itm.amount = itm.quantity * price
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
