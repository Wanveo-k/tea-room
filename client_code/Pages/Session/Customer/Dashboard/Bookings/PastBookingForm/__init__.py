from ._anvil_designer import PastBookingFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class PastBookingForm(PastBookingFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    table = anvil.server.call('get_table', self.item['table_id'])
    self.image.source = table['picture']
    self.label_name.text = table['name']
    self.label_start_datetime.text = self.item['booking_start'].strftime("%Y-%m-%d %H:%M")
    self.label_end_datetime.text = self.item['booking_end'].strftime("%Y-%m-%d %H:%M")
    # Any code you write here will run before the form opens.
