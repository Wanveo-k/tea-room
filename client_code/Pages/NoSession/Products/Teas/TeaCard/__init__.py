from ._anvil_designer import TeaCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..... import state

class TeaCard(TeaCardTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    
  def form_show(self, **event_args):
    tea = self.item
    print(">>> item reçu dans TeaCard :", self.item)

    self.tea_name.text = tea["name"]
    img = tea.get("image")
    if isinstance(img, Media) or isinstance(img, str):
      self.tea_image.source = img
    else:
      self.tea_image.source = "https://placehold.co/200x150?text=Image+manquante"

    self.tea_price.text = f"{tea['price']} €"
    self.tea_description.text = tea["description"] 

  def check_connection(self):
    if not anvil.server.call("is_connected"):
      Notification("You have to be connected to do this action!", style="danger").show()
      return False
    else: 
      return True
      
  def add_to_cart_button_click(self, **event_args):
    if not self.check_connection():
      return
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

    product_id = self.item.get_id()
    anvil.server.call("add_cart", product_id)
    Notification("Ajouté au panier 🛒").show()