from ._anvil_designer import RowTemplateUserTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplateUser(RowTemplateUserTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_firstname.text = self.item['firstname']
    self.text_lastname.text = self.item['lastname']
    self.text_email.text = self.item['email']
    self.check_box_admin.checked = self.item['is_admin']
    self.image.source = self.item['photo']
    
    if self.item['soft_delete']:
      self.text_firstname.enabled = False
      self.text_lastname.enabled = False
      self.text_email.enabled = False
      self.check_box_admin.enabled = False
      self.update_button.text = "Restore"
    # Any code you write here will run before the form opens.

  def update_button_click(self, **event_args):
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
      if self.update_button.text == "Restore":
        anvil.server.call('restore_soft_delte_user', self.item['id'])
      else:
        anvil.server.call(
          "update_basic_info",
          self.item['id'],
          self.text_firstname.text,
          self.text_lastname.text,
          self.text_email.text,
          self.check_box_admin.checked)
      self.raise_event('x-refresh-table')
    else:
      return

  def delete_button_click(self, **event_args):
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
      if anvil.server.call("delete_user", self.item['id'], is_admin_command=True):
        Notification("User deleted with success", style="success").show()
        self.raise_event('x-refresh-table')
      else:
        Notification("Error", style="danger").show()
    else:
      return
