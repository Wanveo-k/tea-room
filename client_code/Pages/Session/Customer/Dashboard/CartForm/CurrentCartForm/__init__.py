from ._anvil_designer import CurrentCartFormTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class CurrentCartForm(CurrentCartFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.form_show()
    # Any code you write here will run before the form opens.
  def delete_link_click(self, **event_args):
    if anvil.server.call('needs_verify_identity'):
      password_box = TextBox(hide_text=True, placeholder="Enter your password")
      result = alert(
        content=password_box,
        title="You need to enter your password to confirm your identity",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
      )
      if not result:
        anvil.server.call('logout_user')
        return
      if not anvil.server.call('verify_identity', password_box.text):
        Notification('Error.', style="danger")
        return

    if confirm(f"Supprimer {self.item['name']} du panier ?"):
      anvil.server.call('remove_cart_item', self.item['id'])
      self.parent.raise_event("x-refresh")
      
  def form_show(self, **event_args):
    self.image_1.source = self.item['image'] if 'image' in self.item else None
    self.rich_text_name.content = self.item['name']
    self.label_1.text = str(self.item['quantity'])
    self.rich_text_price.content = f"{self.item['price']:.2f} €"

  def button_plus_click(self, **event_args):
    if anvil.server.call('needs_verify_identity'):
      password_box = TextBox(hide_text=True, placeholder="Enter your password")
      result = alert(
        content=password_box,
        title="You need to enter your password to confirm your identity",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
      )
      if not result:
        anvil.server.call('logout_user')
        return
      if not anvil.server.call('verify_identity', password_box.text):
        Notification('Error.', style="danger")
        return

    if  int(self.label_1.text) < 9 :
      self.label_1.text = int(self.label_1.text) + 1 
      product_id=self.item["id"]
      try:
        anvil.server.call('add_cart', product_id)
      except Exception:
        Notification("An error occurred, please try again.").show()

  def button_moins_click(self, **event_args):
    if anvil.server.call('needs_verify_identity'):
      password_box = TextBox(hide_text=True, placeholder="Enter your password")
      result = alert(
        content=password_box,
        title="You need to enter your password to confirm your identity",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
      )
      if not result:
        anvil.server.call('logout_user')
        return
      if not anvil.server.call('verify_identity', password_box.text):
        Notification('Error.', style="danger")
        return

    if int(self.label_1.text) > 0 :
      self.label_1.text = int(self.label_1.text) - 1 
      product_id=self.item["id"]
      try:
        anvil.server.call('remove_cart_item', product_id)
      except Exception:
        Notification("An error occurred, please try again.").show()
