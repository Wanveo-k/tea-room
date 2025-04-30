from ._anvil_designer import OTPFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OTPForm(OTPFormTemplate):
  def __init__(self, user_email, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.user_email = user_email
    # Any code you write here will run before the form opens.

  def button_validate_click(self, **event_args):
    """This method is called when the button is clicked"""
    otp_code = self.text_box_totp.text

    valid = anvil.server.call('verify_totp', self.user_email, otp_code)
    if valid:
      Notification("Login successful! 🎉", style='success').show()
      open_form("Pages.Session.Customer.Dashboard")
    else:
      Notification("Invalid MFA code.", style="danger").show()
