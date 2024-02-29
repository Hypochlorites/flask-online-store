import sqlite3
import hashlib 



def hash_password(raw_password):
  raw_password = raw_password.encode('utf-8')
  h = hashlib.sha256()
  h.update(raw_password)
  res = h.hexdigest()
  print(res)
  return res 



con = sqlite3.connect("ecommerce.db")
cur = con.cursor()


cur.execute("DROP TABLE IF EXISTS user")
cur.execute("""
CREATE TABLE user(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT,
  password TEXT,
  cash REAL,
  zip_code INTEGER
);""")



cur.execute( """
INSERT INTO user (name, cash, zip_code) VALUES
  ('Drone', 228, 00001),
  ('Drone1.1', 229, 00002),
  ('Drone1.2', 230, 00003),
  ('Drone1.3', 231, 00004);

""")
for i in range(1,5):
  cur.execute(""" 
  UPDATE user
  SET password = (?)
  WHERE id = (?);
  """, (hash_password('password'+str(i)),i))

cur.execute("DROP TABLE IF EXISTS product")
cur.execute("""
CREATE TABLE product(
  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  name TEXT,
  price REAL,
  shipping_cost REAL
);""")

cur.execute( """
INSERT INTO product (name, price, shipping_cost) VALUES
  ('World_Eater', 250000, 800),
  ('Placeholder', 12500, 5000),
  ('Lettuce', .05, 5),
  ('Angry_Lettuce', .075, 25000);

""")

cur.execute("DROP TABLE IF EXISTS orders")
cur.execute("""
CREATE TABLE orders(
  order_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  user_id INTEGER,
  product_id INTEGER,
  timestamp TEXT,
  FOREIGN KEY (user_id) REFERENCES user(id),
  FOREIGN KEY (product_id) REFERENCES product(id)

);""")

cur.execute("""
INSERT INTO orders(user_id, product_id, timestamp) VALUES
  (1, 3, datetime('now')),
  (1, 4, datetime('now')),
  (2, 3, datetime('now')),
  (3, 1, datetime('now'));
""")
#query orders and replace ids with names  
cur.execute("""
SELECT 
  order_id, user.name, product.name, product.price, orders.timestamp
FROM 
  orders
JOIN 
  user ON orders.user_id = user.id
JOIN
  product ON orders.product_id = product.id
;""")

joined_orders = cur.fetchall()

print('id username    product_name              price        timestamp  ')
for row in joined_orders:
  print(f"{row[0]} | {row[1].ljust(10, ' ')}  {row[2].ljust(20, ' ')} for ${row[3]} at {row[4]}")


con.commit()
