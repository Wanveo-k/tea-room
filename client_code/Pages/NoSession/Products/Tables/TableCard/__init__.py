from ._anvil_designer import TableCardTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class TableCard(TableCardTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.label_name.text = f"Name : {self.item['name']}"
    self.label_number_places.text = f"Number of chairs : {self.item['chairs_count']}"
    # Any code you write here will run before the form opens.

  def check_connection(self):
    if not anvil.server.call("is_connected"):
      Notification("You have to be connected to do this action!", style="danger").show()
      return False
    else: 
      return True
  
  def validate_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if not self.check_connection():
      return
    if anvil.server.call('needs_verify_identity'):
      password_box = TextBox(hide_text=True, placeholder="Enter your password")
      result = alert(
        content=password_box,
        title="You need to enter your password to confirm your identity",
        large=True,
        buttons=[("Confirm", True), ("Cancel", False)]
      )
      if not result:
        anvil.server.call('logout_user')
        return
      if not anvil.server.call('verify_identity', password_box.text):
        Notification('Error.', style="danger")
        return

    date = self.date_picker_1.date
    duration = self.drop_down_time_slots.selected_value
    table_id = self.item.get_id()
    
    if date is None or duration is None:
      Notification("Please select a date and a duration.", style="info").show()
      return

    try:
      status = anvil.server.call('add_booking', date, duration, table_id)
      if not status[0] and status[1] == "Unavailable time slots:\n":
        reserved_slots = anvil.server.call('get_reserved_slots_for_day', date, table_id)
        if reserved_slots:
          text = "The time slot you selected overlaps with an existing booking. Please choose a different time.\nUnavailable time slots for the day selected:\n"
          for start, end in reserved_slots:
            text += f"\t- {start.strftime('%H:%M')} - {end.strftime('%H:%M')}\n"
          self.label_message.text = text
          self.label_message.visible = True
      elif not status[0]:
        self.label_message.text = status[1]
        self.label_message.visible = True
        return
      else:
        self.label_message.visible = False
        Notification(status[1], style="success").show()
    except Exception as e:
      print(e)
      Notification("An error occurred. Please try again.", style="danger").show()

    