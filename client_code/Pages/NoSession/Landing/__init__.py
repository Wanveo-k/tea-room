from ._anvil_designer import LandingTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from ... import state
from anvil_extras import *

class Landing(LandingTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #state.register(self.on_state_change)
    #self.on_state_change()
    self.display_teas()
    self.display_goodies()
    self.display_tables()
    if anvil.server.call("is_connected"):
      self.button_sign_in.visible = False
      self.button_sign_up.visible = False
    else :
      self.button_sign_in.visible = True
      self.button_sign_up.visible = True

  def display_goodies(self):
    try:
      goodies = anvil.server.call('get_goodies')
      for goodie in goodies:
        self.landing_goodies_carousel_flow_panel.add_component(Image(source=goodie['image']))
    except Exception as e:
      alert(f"Erreur lors du chargement des images : {e}")

  def display_teas(self):
    try:
      teas = anvil.server.call('get_teas')
      for tea in teas:
        self.landing_teas_carousel_flow_panel.add_component(Image(source=tea['image']))
    except Exception as e:
      alert(f"Erreur lors du chargement des images : {e}")

  def display_tables(self):
    try:
      tables = anvil.server.call('get_tables')
      for table in tables:
        self.landing_tables_carousel_flow_panel.add_component(Image(source=table['picture']))
    except Exception as e:
      alert(f"Erreur lors du chargement des images : {e}")

  def button_sign_in_click(self, **event_args):
    get_open_form().load_page("login")

  def button_sign_up_click(self, **event_args):
    get_open_form().load_page("signup")

  def goodies_list_button_click(self, **event_args):
    get_open_form().load_page("goodies")
  
  def teas_list_button_click(self, **event_args):
    get_open_form().load_page("teas")  
    
  def tables_list_button_click(self, **event_args):
    get_open_form().load_page("tables")

  
   