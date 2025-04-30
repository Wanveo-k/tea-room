from ._anvil_designer import ProfileFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ProfileForm(ProfileFormTemplate):
  def __init__(self, **properties):
      self.init_components(**properties)
      self.populate_fields()
    
  def populate_fields(self):
    try:
      self.user = anvil.server.call("get_current_user_profile")
    except Exception as e:
      print(e)
      return
    self.text_box_first_name.text = self.user['firstname']
    self.text_box_last_name.text = self.user['lastname']
    self.text_box_email.text = self.user['email']
    #if user['photo']:
      #self.image_profile.source = user['photo'] 
        
  def update_information_click(self, **event_args):
    """This method is called when the button is clicked"""
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

    anvil.server.call(
      "update_basic_info",
      self.user.get_id(),
      self.text_box_first_name.text,
      self.text_box_last_name.text,
      self.text_box_email.text,
      self.user['is_admin']
    )
    
    alert("Infos mises à jour !")  
    
  def update_password_click(self, **event_args):
    """This method is called when the button is clicked"""
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

    new_pass = self.text_box_4.text
    confirm = self.text_box_5.text
    if new_pass == confirm and new_pass != "":
      anvil.server.call("update_password", self.user.get_id(), new_pass)
      alert("Mot de passe mis à jour ✅")
    else:
      alert("Les mots de passe ne correspondent pas ❌")
      
  def update_picture_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.user['photo'] = file
    self.user.update()
    self.image_profile.source = file  # Met à jour l'affichage directement 

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

  def update_picture_change_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

  def button_delete_click(self, **event_args):
    """This method is called when the button is clicked"""
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

      user_id = anvil.server.call('get_user_info')['user_id']
      if anvil.server.call('delete_user', user_id):
        alert("You have a 30-day period to restore your account before it is permanently deleted. To recover your data, simply log in again during this time.")
        anvil.open_form("MainForm")
      else:
        alert("An error occurred. Please contact an administrator at contact@tearoom.com.")

      

 
  