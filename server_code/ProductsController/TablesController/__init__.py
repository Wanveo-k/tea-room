import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta, time, timezone
import anvil.tz

# This is a server package. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_user_bookings(is_past):
  user_id = anvil.server.call('get_user_info')['user_id']
  return list(app_tables.bookings.search(user_id=user_id, is_past=is_past))

@anvil.server.callable
def get_futur_table_bookings(table_id):
  return list(app_tables.bookings.search(table_id=table_id, is_past=False))

@anvil.server.callable
def get_table(table_id):
  return app_tables.tables.get_by_id(table_id)

def is_in_opening_hours(start_date, end_date):
  opening_time = time(9, 0)   # 09:00
  closing_time = time(19, 0)  # 19:00

  if start_date.date() != end_date.date():
    return True

  if opening_time <= start_date.time() and end_date.time() <= closing_time:
    return False
  else:
    return True

def has_conflicting_booking(start, end, table_id):
  bookings = get_futur_table_bookings(table_id)
  
  for booking in bookings:
    existing_start = booking['booking_start']
    existing_end = booking['booking_end']
    
    if (start < existing_end) and (end > existing_start):
      return True 
  return False

@anvil.server.callable
def add_booking(start_date, duration_str, table_id):
  user_id = anvil.server.call('get_user_info')['user_id']
  now = datetime.now(anvil.tz.tzlocal())
  
  if not now < start_date:
    return False, "The selected date and time must be in the future. Please try again."
  durations = {
    "30 minutes": 30,
    "1 hour": 60,
    "1 hour 30 minutes": 90,
    "2 hours": 120
  }

  if duration_str in durations:
    minutes = durations[duration_str]
    end_date = start_date + timedelta(minutes=minutes)

  if is_in_opening_hours(start_date, end_date):
    return False, "Our booking hours are from 9:00 AM to 7:00 PM. Please choose a time within this range."

  if has_conflicting_booking(start_date, end_date, table_id):
    return False, "Unavailable time slots:\n"
    
  app_tables.bookings.add_row(created_at=now,
                             updated_at=now,
                             table_id=table_id,
                             user_id=user_id,
                             booking_start=start_date,
                             booking_end=end_date,
                             is_confirmed=False, 
                             is_past=False)
  return True, "Your reservation has been successfully made."

@anvil.server.callable
def get_reserved_slots_for_day(booking_datetime, table_id):
  bookings = get_futur_table_bookings(table_id)
  reserved_slots = []
  for booking in bookings:
    if booking['booking_start'].date() == booking_datetime.date():
      reserved_slots.append((booking['booking_start'], booking['booking_end']))
  return reserved_slots

@anvil.server.callable
def cancel_booking(booking_id):
  row = app_tables.bookings.get_by_id(booking_id)
  row.delete()

@anvil.server.callable
def mark_past_bookings():
    now = datetime.now(timezone.utc)

    for booking in app_tables.bookings.search(is_past=False):
        if booking['booking_end'] < now:
            booking['is_past'] = True