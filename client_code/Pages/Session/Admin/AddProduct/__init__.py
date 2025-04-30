from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class AddProduct(AddProductTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_tea_add_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.text_tea_name.text
    descritpion = self.text_tea_description.text
    is_available = self.check_box_tea.checked
    image = self.file_loader_tea.file

    try:
      price = float(self.text_tea_price.text)
    except ValueError:
      alert("Veuillez entrer un prix valide.")
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
        if anvil.server.call("add_tea", name, descritpion, is_available, price, image):
          Notification("Tea added successfully!", style="success").show()
        else:
          Notification("Something went wrong. The product could not be added.", style="danger").show()
      except Exception as e:
        alert(str(e))
        return
    else:
      return

  def button_goodie_add_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.text_goodie_name.text
    descritpion = self.text_goodie_description.text
    is_available = self.check_box_goodie.checked
    image = self.file_loader_goodie.file

    try:
      price = float(self.text_goodie_price.text)
      quantity = int(self.text_goodie_quantity.text)
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
        if anvil.server.call("add_goodie", name, descritpion, is_available, quantity, price, image):
          Notification("Goodie added successfully!", style="success").show()
        else:
          Notification("Something went wrong. The product could not be added.", style="danger").show()
      except Exception as e:
        alert(str(e))
        return     
    else:
      return

  def button_tea_clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_tea_name.text = ""
    self.text_tea_description.text = ""
    self.check_box_tea.checked = True
    self.file_loader_tea.clear()
    self.text_tea_price.text = ""
    Notification("All data was reset", style="success").show()

  def button_goodie_clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.text_goodie_name.text = ""
    self.text_goodie_description.text = ""
    self.check_box_goodie.checked = True
    self.file_loader_goodie.clear()
    self.text_goodie_price.text = ""
    self.text_goodie_quantity.text = ""
    Notification("All data was reset", style="success").show()
