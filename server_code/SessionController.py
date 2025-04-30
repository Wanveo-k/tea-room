import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from argon2 import PasswordHasher
from datetime import datetime, timedelta, timezone
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
import math
import pyotp
import qrcode
import io

ph = PasswordHasher(
        time_cost=3,
        memory_cost=65536,
        parallelism=2,
        hash_len=32,
        salt_len=16)

############ SignUp functions
@anvil.server.callable
def hash_password(password):
  return ph.hash(password)

@anvil.server.callable
def in_database(email):
  if app_tables.users.get(email=email): 
    return True
  else:
    return False

@anvil.server.callable
def calculate_entropy(password):
  lenght_alphabet = 0

  if any(c.isupper() for c in password):
      lenght_alphabet += 26
  if any(c.islower() for c in password):
      lenght_alphabet += 26
  if any(c.isdigit() for c in password):
      lenght_alphabet += 10
  if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?/ " for c in password):
      lenght_alphabet += 28
  
  return math.log2(lenght_alphabet)*len(password)

############ MFA functions
@anvil.server.callable
def generate_totp_secret(email):
    totp = pyotp.TOTP(pyotp.random_base32())
    app_tables.users.get(email=email)['totp_secret'] = totp.secret
    return totp.provisioning_uri(name=email, issuer_name="TeaRoom")

@anvil.server.callable
def verify_totp(email, code):
    user = app_tables.users.get(email=email)
    totp = pyotp.TOTP(user['totp_secret'])
    return totp.verify(code)

@anvil.server.callable
def generate_qrcode(uri):
  buffer = io.BytesIO()
  img = qrcode.make(uri)
  img.save(buffer, format="PNG")
  buffer.seek(0)
  return anvil.BlobMedia('image/png', buffer.read())

############ LogIn functions
@anvil.server.callable
def verify_password(user_id, password):
  user = app_tables.users.get_by_id(user_id)
  ph.verify(user['password'], password)
  return True

@anvil.server.callable
def login_user(email, password):
  user = app_tables.users.get(email=email)
  if user is None:
    return "Invalid Data"

  if user['password'][0] != "$":
    user['password'] = hash_password(user['password'])
    
  if ph.check_needs_rehash(user['password']):
    user['password'] = hash_password(user['password'])
    
  try:
    user_id = user.get_id()
    verify_password(user_id, password)
    
    if user['soft_delete']:
      anvil.server.call('restore_soft_delte_user', user_id)
      
    user['last_login'] = datetime.now()
    set_user_info(user['email'], user_id, user['is_admin'], user['totp_secret'] is not None)

    if user['is_admin']:
      anvil.server.call('delete_expired_users')
      
    print("Is connected:", is_connected())
    return f"Welcome back {user['firstname']} {user['lastname']}! 🎉"
  except Exception as e:
    print(e)
    return "Invalid Password"

@anvil.server.callable
def needs_verify_identity():
  last_auth_time = anvil.server.session.get('last_auth_time')
  if not last_auth_time or datetime.now(timezone.utc) - last_auth_time > timedelta(hours=1):
    return True
  else:
    return False
  
@anvil.server.callable
def verify_identity(password):
    if password:
      if verify_password(anvil.server.session['user_id'], password):
        anvil.server.session['last_auth_time'] = datetime.now()
        return True
      else:
        anvil.Notification("Mot de passe incorrect").show()
        return False
    else:
      return False

@anvil.server.callable
def logout_user():
  for key in list(anvil.server.session):
    del anvil.server.session[key]

@anvil.server.callable
def set_user_info(email, id, is_admin, has_totp):
  anvil.server.session['user_email'] = email
  anvil.server.session['user_id'] = id
  anvil.server.session['user_is_admin'] = is_admin
  anvil.server.session['authenticated'] = True
  anvil.server.session['last_auth_time'] = datetime.now()
  anvil.server.session['has_totp'] = has_totp
  print("SESSION SET:")
  print(get_user_info())

@anvil.server.callable
def get_user_info():
    return {"user_email":anvil.server.session.get('user_email'), "user_id":anvil.server.session.get('user_id'), "has_totp": anvil.server.session.get('has_totp')}

@anvil.server.callable
def is_connected():
  try:
    return anvil.server.session['user_id'] is not None
  except Exception as e:
    print(e)
    return False


############ Token Functions
# L'idée de mettre un token en place a été abandonnée car Anvil lie déjà les sessions stockées sur le serveur avec les clients grâce à des tokens en HttpOnly.
# Les fonctions ci-dessous sont donc inutiles, mais elles montrent les étapes à suivre si un système de tokens aurait dû être mis en place

secret_key_clear = "[~v{vh/==hHhHnaXlgwUc1z-<q#0%s4Pz/JcO7_%B()6kEI#5+4d'_qMyNm%Jl+"
secret_key = URLSafeTimedSerializer(secret_key_clear)

token_lifetime = 3600

@anvil.server.callable
def generate_token(user_id, user_email):
  try:
    return secret_key.dumps(user_id)
  except Exception as e:
    print(e)
    return None

@anvil.server.callable
def verify_token(token, token_lifetime):
  try:
    info = secret_key.loads(token, token_lifetime)
    return info
  except BadSignature or SignatureExpired:
    return False
  except Exception as e:
    print(e)
    return None
