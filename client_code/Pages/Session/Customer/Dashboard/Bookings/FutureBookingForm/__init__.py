from ._anvil_designer import FutureBookingFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class FutureBookingForm(FutureBookingFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    table = anvil.server.call('get_table', self.item['table_id'])
    self.image.source = table['picture']
    self.label_name.text = table['name']
    self.label_start_datetime.text = self.item['booking_start'].strftime("%Y-%m-%d %H:%M")
    self.label_end_datetime.text = self.item['booking_end'].strftime("%Y-%m-%d %H:%M")
    # Any code you write here will run before the form opens.

  def button_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
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

    if confirm("Cancel booking?"):
      try:
        anvil.server.call('cancel_booking', self.item.get_id())
        Notification("Booking successfully canceled.", style="success").show()
      except Exception as e:
        print(e)
        Notification("An error occurred.", style="danger").show()
