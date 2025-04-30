from ._anvil_designer import DashboardTemplate
from anvil import *
import anvil.server
import anvil.js
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .CartForm import CartForm
from .ProfileForm import ProfileForm
from ...Admin.ListClients import ListClients
from ...Admin.ListProducts import ListProducts
from ...Admin.AddProduct import AddProduct
from .Bookings import Bookings


class Dashboard(DashboardTemplate):
  def __init__(self, **properties):
    self.content_panel.add_component( ProfileForm())# Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.check_connection()
    self.profile_link()

    user = anvil.server.call('get_current_user_profile')
    if user and user['is_admin']:
      self.linear_panel_admin.visible = True

  def check_connection(self):
    if not anvil.server.call("is_connected"):
      Notification("401: Authentication needed to access!", style="danger").show()
      open_form("Pages.NoSession.Auth.LogInForm")
    # Any code you write here will run before the form opens.
    
  def logout_link(self, **event_args):
     """This method is called when the button is clicked"""
     anvil.users.logout()
     anvil.server.session.cleanup()  # (optionnel, mais propre)
     anvil.open_form('Pages.NoSession.Landing') 
    
  def profile_link(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(ProfileForm()) # Profile()
    
  def cart_link(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(CartForm()) # Cart()

  def list_client_link(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(ListClients())

  def list_product_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(ListProducts())

  def add_product_link(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(AddProduct())
    
  def logout_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.server.call("logout_user")
    anvil.open_form('MainForm') 

  def main_page_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.open_form("MainForm")

  def link_booking_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(Bookings())
