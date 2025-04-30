from ._anvil_designer import MFAFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class MFAForm(MFAFormTemplate):
  def __init__(self, image, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_qrcode.source = image
    # Any code you write here will run before the form opens.

  def button_validate_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().load_page("login")
