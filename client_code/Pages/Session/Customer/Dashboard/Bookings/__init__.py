from ._anvil_designer import BookingsTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Bookings(BookingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_connection()
    anvil.server.call('mark_past_bookings')
    self.load_future_bookings()
    self.load_past_bookings()

  def check_connection(self):
    if not anvil.server.call("is_connected"):
      Notification("401: Authentication needed to access!", style="danger").show()
      open_form("Pages.NoSession.Auth.LogInForm")
    # Any code you write here will run before the form opens.

  def load_future_bookings(self, **event_args):
    bookings = anvil.server.call('get_user_bookings', False)

    if not bookings:
      self.label_future_message.text = "Vous n'avez aucune réservation future."
      self.label_future_message.visible = True

    self.repeating_panel_future.items = bookings
    
  def load_past_bookings(self, **event_args):
    bookings = anvil.server.call('get_user_bookings', True)

    if not bookings:
      self.label_past_message.text = "Vous n'avez aucune réservation passée."
      self.label_past_message.visible = True

    self.repeating_panel_past.items = bookings