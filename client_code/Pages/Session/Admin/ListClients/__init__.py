from ._anvil_designer import ListClientsTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


class ListClients(ListClientsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.table.set_event_handler('x-refresh-table', self.load_clients)

    self.load_clients()
    # Any code you write here will run before the form opens.

  def load_clients(self):
    clients = anvil.server.call('get_users_list')
    if clients is None:
      return

    clients_items = []
    for client in clients:
      clients_items.append({'id' : client.get_id(),
                           'firstname' : client['firstname'],
                           'lastname' : client['lastname'],
                           'email' : client['email'],
                           'is_admin' : client['is_admin'],
                           'photo' : client['photo'],
                           'created_at' : client['created_at'],
                           'updated_at' : client['updated_at'],
                           'last_login' : client['last_login'],
                           'soft_delete': client['soft_delete']})
    self.table.items = clients_items