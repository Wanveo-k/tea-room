import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta, timezone

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
def add_user(firstname, lastname, email, password):
  now = datetime.now()
  app_tables.users.add_row(
    firstname=firstname,
    lastname=lastname,
    email=email,
    password=password,
    created_at=now,
    updated_at=now,
    is_admin=False
  )
  return "user added with success"

@anvil.server.callable
def get_current_user_profile():
    if 'user_id' not in anvil.server.session:
      return None 
    user = app_tables.users.get_by_id(anvil.server.session['user_id'])
    if user:
        return user
    else:
        return None

@anvil.server.callable
def get_users_list():
  return list(app_tables.users.search())

@anvil.server.callable
def update_basic_info(id, firstname, lastname, email, is_admin):
  user = app_tables.users.get_by_id(id)
  user.update(email = email,
             lastname= lastname,
             firstname = firstname,
             is_admin = is_admin,
             updated_at = datetime.now())

@anvil.server.callable
def update_password(id, password):
  hash_password = anvil.server.call("hash_password", password)
  user = app_tables.users.get_by_id(id)
  user['password'] = hash_password

@anvil.server.callable
def soft_delete_user(user_id):
  row = app_tables.users.get_by_id(user_id)
  row.update(soft_delete=True, deletion_date=datetime.now())
  anvil.server.call("logout_user")

@anvil.server.callable
def restore_soft_delte_user(user_id):
  user = app_tables.users.get_by_id(user_id)
  user['soft_delete'] = None
  user['deletion_date'] = None

@anvil.server.callable
def delete_expired_users():
  soft_deleted_users = app_tables.users.search(soft_delete=True)
  
  for user in soft_deleted_users:
    if user['deletion_date'] is not None:
      if datetime.now(timezone.utc) > user['deletion_date'] + timedelta(days=30):
        user_email = user['email']
        user_id = user.get_id()
        user.delete()
        print("The user (email: '{}', id: '{}') has been deleted.".format(user_email, user_id))

@anvil.server.callable
def delete_user(user_id, is_admin_command = False):
  try:
    if not is_admin_command: 
      soft_delete_user(user_id)
    else:
      user = app_tables.users.get_by_id(user_id)
      user.delete()
    return True
  except Exception as e:
    print(e)
    return None
  