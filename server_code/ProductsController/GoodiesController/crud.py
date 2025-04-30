import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

@anvil.server.callable
def get_goodies():
    return list(app_tables.goodies.search())

@anvil.server.callable
def add_goodie(name, description, is_available, quantity, price, image):
  if name is None or description is None or is_available is None or quantity is None or image is None or price is None:
    raise ValueError("Tous les champs doivent être remplis.")
  if not isinstance(name, str):
    raise TypeError("Le nom doit être une chaîne de caractères.")
  if not isinstance(description, str):
    raise TypeError("La description doit être une chaîne de caractères.")
  if not isinstance(is_available, bool):
    raise TypeError("La disponibilité doit être un booléen.")
  if not isinstance(quantity, int):
    raise TypeError("La quantité doit être un entier.")
  if not isinstance(price, (int, float)):
    raise TypeError("Le prix doit être un nombre.")

  now = datetime.now()
  row = app_tables.goodies.add_row(name=name,
                                  description=description,
                                  is_available=is_available,
                                  quantity=quantity,
                                  image=image,
                                  price=price,
                                  created_at=now,
                                  updated_at=now)
  if row:
    return True
  else:
    return False

@anvil.server.callable
def update_goodie(id, name, description, price, quantity, is_available):
  if name is None or description is None or is_available is None or quantity is None or price is None:
    raise ValueError("Tous les champs doivent être remplis.")
  if not isinstance(name, str):
    raise TypeError("Le nom doit être une chaîne de caractères.")
  if not isinstance(description, str):
    raise TypeError("La description doit être une chaîne de caractères.")
  if not isinstance(is_available, bool):
    raise TypeError("La disponibilité doit être un booléen.")
  if not isinstance(quantity, int):
    raise TypeError("La quantité doit être un entier.")
  if not isinstance(price, (int, float)):
    raise TypeError("Le prix doit être un nombre.")

  try:
    goodie = app_tables.goodies.get_by_id(id)
    goodie.update(name=name,
                  description=description,
                  price=price,
                  quantity=quantity,
                  is_available=is_available,
                  updated_at = datetime.now())
    return True
  except Exception as e:
    print(e)
    return False

@anvil.server.callable
def delete_goodie(id):
  goodie = app_tables.goodies.get_by_id(id)
  try:
    goodie.delete()
    return True
  except Exception as e:
    print(e)
    return False