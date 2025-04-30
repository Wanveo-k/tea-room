from ._anvil_designer import RowTemplateGoodieTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplateGoodie(RowTemplateGoodieTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_name.text = self.item['name']
    self.text_description.text = self.item['description']
    self.text_price.text = self.item['price']
    self.image_goodie.source = self.item['image']
    self.check_box_availability.checked = self.item['is_available']
    self.text_quantity.text = self.item['quantity']
    # Any code you write here will run before the form opens.

  def button_update_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.text_name.text
    descritpion = self.text_description.text
    is_available = self.check_box_availability.checked

    try:
      price = float(self.text_price.text)
      quantity = int(self.text_quantity.text)
    except ValueError:
      alert("Veuillez entrer un prix et une quantité valides.")
      return

    password_box = TextBox(hide_text=True, placeholder="Enter admin password")
    result = alert(
        content=password_box,
        title="Administrator Confirmation",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
    )
    try:
      user_id = anvil.server.call('get_user_info')['user_id']
      is_good_password = anvil.server.call('verify_password', user_id, password_box.text)
    except Exception as e:
      print(e)
      Notification("Invalid password. Please try again.", style="danger").show()
      return
    if result and is_good_password:
        try:
          if anvil.server.call("update_goodie", self.item['id'], name, descritpion, price, quantity, is_available):
            Notification("Goodie updated successfully!", style="success").show()
          else:
            Notification("Something went wrong. The product could not be updated.", style="danger").show()
        except Exception as e:
          alert(str(e))
          return 
    else:
      return

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    password_box = TextBox(hide_text=True, placeholder="Enter admin password")
    result = alert(
        content=password_box,
        title="Administrator Confirmation",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
    )
    try:
      user_id = anvil.server.call('get_user_info')['user_id']
      is_good_password = anvil.server.call('verify_password', user_id, password_box.text)
    except Exception as e:
      print(e)
      Notification("Invalid password. Please try again.", style="danger").show()
      return
    if result and is_good_password:
      try:
        if anvil.server.call('delete_goodie', self.item['id']):
          Notification("Goodie deleted successfully!", style="success").show()
        else:
          Notification("Something went wrong. The product could not be deleted.", style="danger").show()
      except Exception as e:
        alert(str(e))
        return 
    else:
      return
