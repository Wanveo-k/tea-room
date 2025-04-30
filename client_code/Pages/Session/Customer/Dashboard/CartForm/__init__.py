from ._anvil_designer import CartFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

def format_datetime(dt):
    return dt.strftime("%d %B %Y at %H:%M")

class CartForm(CartFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_cart()
    self.load_orders()
    self.repeating_panel_1.set_event_handler("x-refresh", self.load_cart())
    # Any code you write here will run before the form opens.
    
  def load_cart(self, **event_args):
    carts = anvil.server.call('get_cart_items')

    if not carts:
      self.label_total.text = "Votre panier est vide. 🛒"
      self.button_validate_cart.enabled = False
    else:
      total = sum(item['price'] * item['quantity'] for item in carts)
      self.label_total.text = f"Total: {total:.2f} €"

    cart_items = []
    for cart in carts:
      cart_items.append({'id' : cart['id'],
                           'image' : cart['image'],
                           'name' : cart['name'],
                           'quantity' : cart['quantity'],
                           'price' : cart['price']})
    self.repeating_panel_1.items = cart_items

  def button_validate_cart_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      carts = anvil.server.call('get_cart')
      anvil.server.call('add_order', 
                        content=carts['content'],
                        price=carts['total_amount'],
                        user_id=carts['user_id'])
      anvil.server.call('delete_cart', carts['user_id'])
      Notification("Your order has been successfully confirmed!", style='success').show()
      self.load_cart()
    except Exception as e:
      print(e)
      Notification("An error occurred. Please try again or contact an administrator.", style='danger').show()

  def load_orders(self, **event_args):
    orders = anvil.server.call('get_orders')

    if orders == []:
      self.order_message.text = "Vous n'avez aucune commande passée."
      self.column_panel_2.visible = True
    self.repeating_panel_2.items = orders

  def load_one_order(self, order_id, **event_args):
    self.label_order.visible = True
    self.grid_order.visible = True
    order = anvil.server.call('get_order', order_id)

    self.label_order.text = "Order made on {}".format(format_datetime(order['created_at']))
    content = order["content"] or {}
    cart_content = []
    for product_id, quantity in content.items():
      product = anvil.server.call('get_product', product_id)
      if product:
        cart_content.append({
        "id": product_id,
        "name": product["name"],
        "price": product["price"],
        "image": product["image"],
        "quantity": quantity})
    self.repeating_panel_order.items = cart_content
    self.total_order_price.text = f"Total: {order['total_price']:.2f} €"