from ._anvil_designer import LogInFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from .... import state
from .OTPForm import OTPForm

class LogInForm(LogInFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.credentials_fields_1.password_field.hide_text = True
    self.form_buttons_1.submit_button.add_event_handler('click', self.submit_click)
    self.form_buttons_1.reset_button.add_event_handler('click', self.reset_click)

  def submit_click(self, **event_args):
    email = self.credentials_fields_1.email_field.text
    password = self.credentials_fields_1.password_field.text
    
    session = anvil.server.call("login_user", email, password)
    
    if session[0] != "W":
      Notification(session, style="danger").show()
      return

    if anvil.server.call('get_user_info')['has_totp']:
      self.form_buttons_1.visible = False
      self.credentials_fields_1.email_field.enabled = False 
      self.credentials_fields_1.password_field.enable = False 
      self.flow_panel_otp.add_component(OTPForm(self.credentials_fields_1.email_field.text))
      self.flow_panel_otp.visible = True
    else:
      Notification(session, style='success').show()
      open_form("Pages.Session.Customer.Dashboard")

  def reset_click (self, **event_args):
    self.credentials_fields_1.email_field.text = ""
    self.credentials_fields_1.password_field.text = ""
    Notification("All data was reset", style="success").show()
    
    
    