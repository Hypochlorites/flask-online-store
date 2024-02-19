import sqlite3
from typing import List, Union


def create_connection():
  return sqlite3.connect("ecommerce.db")


def run_query(query, values=None):
  conn = create_connection()
  cur = conn.cursor()
  if values:
    cur.execute(query, values)
  else:
    cur.execute(query)

  if query.strip().upper().startswith("SELECT"):
    return cur.fetchall()
  else:
    conn.commit()
  conn.close()


def add_user(username: str, hashed_password: str):
  query = """
  INSERT INTO user(name, password, cash)
  VALUES(?, ?, ?)
  """
  values = (username, hashed_password, 0)
  run_query(query, values)


def get_user_by_username(username: str) -> Union[List, None]:
  query = """
  SELECT 
    *
  FROM 
    user
  WHERE name = (?)
  """
  values = (username, )
  users = run_query(query, values)
  if users is None: return None
  if len(users) == 0: return None
  return users[0]


def get_user_by_id(id: int) -> Union[List, None]:
  query = """
  SELECT 
    *
  FROM 
    user
  WHERE id = (?)
  """
  values = (id, )
  users = run_query(query, values)

  if users is None: return None
  if len(users) == 0: return None
  return users[0]


def update_cash(id: int, cash: float):

  query = """
  UPDATE user
  SET cash = (?)
  WHERE id = (?)
  """
  values = (round(cash, 2), id)
  run_query(query, values)


def get_orders() -> list:

  query = """
  SELECT 
    order_id, user.name, product.name, product.price, orders.timestamp
  FROM 
    orders
  JOIN 
    user ON orders.user_id = user.id
  JOIN
    product ON orders.product_id = product.id
  ;"""

  joined_orders = run_query(query)
  print('id username    product_name              price        timestamp  ')

  if joined_orders is not None:
    for row in joined_orders:
      print(
          f"{row[0]} | {row[1].ljust(10, ' ')}  {row[2].ljust(20, ' ')} for ${row[3]} at {row[4]}"
      )

    return joined_orders
  else:
    return []


def select_orders(id: int) -> list:
  query = """
  SELECT 
    order_id, product.name, product.price, orders.timestamp
  FROM
    orders
  JOIN 
    product ON orders.product_id = product.id
  WHERE user_id = (?)
  """
  values = (id, )
  orders = run_query(query, values)
  if orders is not None:
    return (orders)
  else:
    return []


def get_products() -> list:
  query = """
  SELECT * FROM product; 
  """
  products = run_query(query)
  if products is None:
    raise Exception("Products are none... why...")
  return products


def place_order(user_id, product_id, timestamp):
  query = """
  INSERT INTO orders(user_id, product_id, timestamp) 
  VALUES(?, ?, ?)
  """
  values = (user_id, product_id, timestamp)
  run_query(query, values)


def remove_order(order_id: int):
  query = """
  DELETE FROM orders
  WHERE order_id = (?)
  """
  values = (order_id,)
  run_query(query, values)

