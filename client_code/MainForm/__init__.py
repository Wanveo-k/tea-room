from ._anvil_designer import MainFormTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.js

# Ces imports sont corrects
from ..Pages.NoSession.Landing import Landing
from ..Pages.NoSession.Legal.TermsOfService import TermsOfService
from ..Pages.NoSession.Legal.CookiesPolicy import CookiesPolicy
from ..Pages.NoSession.Legal.PrivatePolicy import PrivatePolicy
from ..Pages.NoSession.Legal.LegalInformation import LegalInformation
from ..Pages.NoSession.Products.Teas import Teas
from ..Pages.NoSession.Products.Goodies import Goodies
from ..Pages.NoSession.Products.Tables import Tables
from ..Pages.NoSession.Auth.SignUpForm import SignUpForm
from ..Pages.NoSession.Auth.LogInForm import LogInForm
from ..Pages.Session.Customer.Dashboard import Dashboard  


class MainForm(MainFormTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_page("landing")
    if anvil.server.call("is_connected"):
      self.login_link.text = "LOGOUT"
      self.link_profile.visible = True
      self.link_signup.visible = False
    else :
      self.link_profile.visible = False

  def load_page(self, page_name):
    self.content_panel.clear()
    if page_name == "landing":
      self.content_panel.add_component(Landing()) 
    elif page_name == "legal":
      self.content_panel.add_component(LegalInformation())
    elif page_name == "terms":
      self.content_panel.add_component(TermsOfService())
    elif page_name == "private":
      self.content_panel.add_component(PrivatePolicy())
    elif page_name == "cookies":
      self.content_panel.add_component(CookiesPolicy())
    elif page_name == "teas":
      self.content_panel.add_component(Teas())
    elif page_name == "goodies":
      self.content_panel.add_component(Goodies())
    elif page_name == "signup":
      signup_form = SignUpForm()
      signup_form.role = "custom-wide"
      self.content_panel.add_component(signup_form)
    elif page_name == "login":
      login_form = LogInForm()
      login_form.role = "custom-wide"
      self.content_panel.add_component(login_form)
    elif page_name == "dashboard": 
      self.content_panel.add_component(Dashboard())
    elif page_name == "tables":
      self.content_panel.add_component(Tables())

  def terms_of_service_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().load_page("terms")

  def legal_information_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().load_page("legal")

  def private_policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().load_page("private")

  def cookies_policy_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    get_open_form().load_page("cookies")

  def landing_link_click(self, **event_args):
    get_open_form().load_page("landing")

  def goodies_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().load_page("goodies")

  def teas_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().load_page("teas")

  def tables_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    get_open_form().load_page("tables")

  def login_link_click(self, **event_args):
    if not anvil.server.call("is_connected"):
      get_open_form().load_page("login")
    else:
      anvil.server.call("logout_user")
      anvil.js.window.location.reload()

  def link_profile_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Pages.Session.Customer.Dashboard")

  def link_signup_click(self, **event_args):
    """This method is called when the link is clicked"""
    if not anvil.server.call("is_connected"):
      get_open_form().load_page("signup")

    


