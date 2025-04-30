import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime


@anvil.server.callable
def get_teas():
    return list(app_tables.teas.search())

@anvil.server.callable
def add_tea(name, description, is_available, price, image):
  if name is None or description is None or is_available is None or image is None or price is None:
    raise ValueError("Tous les champs doivent être remplis.")
  if not isinstance(name, str):
    raise TypeError("Le nom doit être une chaîne de caractères.")
  if not isinstance(description, str):
    raise TypeError("La description doit être une chaîne de caractères.")
  if not isinstance(is_available, bool):
    raise TypeError("La disponibilité doit être un booléen.")
  if not isinstance(price, (int, float)):
    raise TypeError("Le prix doit être un nombre.")

  now = datetime.now()
  row = app_tables.teas.add_row(name=name,
                                description=description,
                                is_available=is_available,
                                image=image,
                                price=price,
                                created_at=now,
                                updated_at=now)
  if row:
    return True
  else:
    return False

@anvil.server.callable
def update_tea(id, name, description, price, is_available):
  if name is None or description is None or is_available is None or price is None:
    raise ValueError("Tous les champs doivent être remplis.")
  if not isinstance(name, str):
    raise TypeError("Le nom doit être une chaîne de caractères.")
  if not isinstance(description, str):
    raise TypeError("La description doit être une chaîne de caractères.")
  if not isinstance(is_available, bool):
    raise TypeError("La disponibilité doit être un booléen.")
  if not isinstance(price, (int, float)):
    raise TypeError("Le prix doit être un nombre.")

  try:
    tea = app_tables.teas.get_by_id(id)
    tea.update(name=name,
                  description=description,
                  price=price,
                  is_available=is_available,
                  updated_at = datetime.now())
    return True
  except Exception as e:
    print(e)
    return False

@anvil.server.callable
def delete_tea(id):
  tea = app_tables.teas.get_by_id(id)
  try:
    tea.delete()
    return True
  except Exception as e:
    print(e)
    return None