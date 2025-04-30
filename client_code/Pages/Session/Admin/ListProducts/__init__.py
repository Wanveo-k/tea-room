from ._anvil_designer import ListProductsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class ListProducts(ListProductsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    self.load_teas()
    self.load_goodies()
    # Any code you write here will run before the form opens.

  def load_teas(self):
    teas = anvil.server.call('get_teas')
    if teas is None:
      return

    teas_items = []
    for tea in teas:
      teas_items.append({'id' : tea.get_id(),
                        'name' : tea['name'],
                        'description' : tea['description'],
                        'price' : tea['price'],
                        'is_available' : tea['is_available'],
                        'image' : tea['image']})
    self.table_teas.items = teas_items

  def load_goodies(self):
    goodies = anvil.server.call('get_goodies')
    if goodies is None:
      return

    goodies_items = []
    for goodie in goodies:
      goodies_items.append({'id' : goodie.get_id(),
                        'name' : goodie['name'],
                        'description' : goodie['description'],
                        'price' : goodie['price'],
                        'is_available' : goodie['is_available'],
                        'image' : goodie['image'],
                        'quantity' : goodie['quantity']})
    self.table_goodies.items = goodies_items