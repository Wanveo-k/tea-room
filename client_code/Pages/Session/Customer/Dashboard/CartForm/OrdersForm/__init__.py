from ._anvil_designer import OrdersFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

def format_datetime(dt):
    return dt.strftime("%d %B %Y at %H:%M")

class OrdersForm(OrdersFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_date_time.text = format_datetime(self.item['created_at'])
    self.label_price.text = f"€{self.item['total_price']:.2f}"
    self.label_done.text = "Yes" if self.item['is_done'] else "No"
    # Any code you write here will run before the form opens.

  def button_display_content_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.parent.load_one_order(self.item.get_id())
