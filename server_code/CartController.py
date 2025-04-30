import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#

@anvil.server.callable
def add_order(content, price, user_id):
  app_tables.orders.add_row(content=content,
                            created_at=datetime.now(),
                            total_price=price,
                            user_id=user_id,
                           is_done=False)

@anvil.server.callable
def get_orders():
  user_id=anvil.server.call("get_user_info")["user_id"]
  return list(app_tables.orders.search(user_id=user_id))

@anvil.server.callable
def get_order(order_id):
  return app_tables.orders.get_by_id(order_id)

@anvil.server.callable
def add_cart(product_id):
  user_id=anvil.server.call("get_user_info")["user_id"]
  row=app_tables.carts.get(user_id=user_id)
  try:
    product = app_tables.goodies.get_by_id(product_id)
    if product is None:
      product = app_tables.teas.get_by_id(product_id)
    product_price = product['price']
  except Exception as e:
    print(e)
    raise Exception
  
  if not row :
    app_tables.carts.add_row(user_id=user_id, total_amount=product_price, content={product_id: 1})
  else :
    row["total_amount"] = row["total_amount"]+product_price
    content= row["content"]
    if product_id in content:
      content[product_id]+=1
    else :
      content[product_id]= 1
    row["content"] = content 
    row['update_at'] = datetime.now() 

@anvil.server.callable
def get_cart():
  user_id=anvil.server.call("get_user_info")["user_id"]
  return app_tables.carts.get(user_id=user_id)

@anvil.server.callable
def get_product(product_id):
  product = app_tables.goodies.get_by_id(product_id)
  if product is None:
    product = app_tables.teas.get_by_id(product_id)
  if product:
    return product
  
@anvil.server.callable
def get_cart_items():
  user_id=anvil.server.call("get_user_info")["user_id"]
  row=app_tables.carts.get(user_id=user_id)
  if not row:
    return []  # Aucun panier pour cet utilisateur
    
  content = row["content"] or {}
  cart_content = []
  for product_id, quantity in content.items():
    product = get_product(product_id)
    if product:
      cart_content.append({
      "id": product_id,
      "name": product["name"],
      "price": product["price"],
      "image": product["image"],
      "quantity": quantity})
  return cart_content

@anvil.server.callable
def remove_cart_item(product_id):
  user_id = anvil.server.call("get_user_info")["user_id"]
  row = app_tables.carts.get(user_id=user_id)
  if row:
    try:
      product = app_tables.goodies.get_by_id(product_id)
      if product is None:
        product = app_tables.teas.get_by_id(product_id)
      product_price = product['price']
    except Exception as e:
      print(e)
      raise Exception
    row["total_amount"] = row["total_amount"]-product_price
    
    content = row["content"]
    if product_id in content:
      content[product_id] -= 1
      if content[product_id] == 0:
        content.pop(product_id, None)
    row["content"] = content 
    row['update_at'] = datetime.now()

@anvil.server.callable
def delete_cart(user_id):
  row = app_tables.carts.get(user_id=user_id)
  row.delete()
    



  
  
