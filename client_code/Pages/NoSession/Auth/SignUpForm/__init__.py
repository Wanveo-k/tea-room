from ._anvil_designer import SignUpFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .ErrorMessageEntropy import ErrorMessageEntropy
from .MFAForm import MFAForm

class SignUpForm(SignUpFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.credentials_fields.password_field.hide_text = True
    self.confirmed_password_field.hide_text = True
    
    self.entropy_message.add_component(ErrorMessageEntropy())
    
    self.sign_up_form_buttons.submit_button.add_event_handler('click', self.submit_click)
    self.sign_up_form_buttons.reset_button.add_event_handler('click', self.reset_click)

  def submit_click(self, **event_args):
    firstname = self.name_fields.firstname_field.text 
    lastname = self.name_fields.lastname_field.text
    email = self.credentials_fields.email_field.text
    password = self.credentials_fields.password_field.text
    confirmed_password = self.confirmed_password_field.text 

    if not firstname or not lastname or not email or not password or not confirmed_password:
      Notification("Every field must be filled", style="danger").show()
      return

    if anvil.server.call("in_database", email):
      Notification("Email already used", style="danger").show()
      return

    if anvil.server.call("calculate_entropy", password) < 50:
      self.entropy_message.visible = True
      return
      
    if password != confirmed_password:
      Notification("The passwords are not identical", style="danger").show()
      return  
    
    try:
      response = anvil.server.call('add_user', firstname, lastname, email, anvil.server.call("hash_password", password))
      Notification(response, style="success").show()
      
      uri = anvil.server.call('generate_totp_secret', email)
      buffer = anvil.server.call('generate_qrcode', uri)
      self.mfa_form.add_component(MFAForm(buffer))
      self.mfa_form.visible = True
      
      self.sign_up_form_buttons.visible = False
      self.name_fields.firstname_field.enabled = False 
      self.name_fields.lastname_field.enabled = False 
      self.credentials_fields.email_field.enabled = False
      self.credentials_fields.password_field.enabled = False 
      self.confirmed_password_field.enabled = False

    except Exception as e:
      print(e)
      Notification("Error while communicating with the server", style="danger").show()

  def reset_click (self, **event_args):
    self.name_fields.firstname_field.text = "" 
    self.name_fields.lastname_field.text = ""
    self.credentials_fields.email_field.text = ""
    self.credentials_fields.password_field.text = ""
    self.confirmed_password_field.text = ""
    Notification("All data was reset").show()