from ._anvil_designer import OrderFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OrderForm(OrderFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_product.source = self.item['image']
    self.label_name.text = self.item['name']
    self.label_quantity.text = self.item['quantity']
    self.label_unit_price.text = self.item['price']
    total = self.item['price'] * self.item['quantity']
    self.label_total_price.text = f"Total: {total:.2f} €"
    # Any code you write here will run before the form opens.
