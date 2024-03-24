import hashlib 
from . import queries as q 


def hash_password(raw_password):
  raw_password = raw_password.encode('utf-8')
  h = hashlib.sha256()
  h.update(raw_password)
  res = h.hexdigest()
  return res 
  
def login(username, password):
  user = q.get_user_by_username(username)
  if user is None:
    print("user is none")
    return False 
  hashed_password = hash_password(password) 
  if hashed_password != user[2]:
    print("hashed password doesn't match")
    return False 
  return True 

def signup(username, password):
  user = q.get_user_by_username(username)
  if user is not None:
    raise Exception("Username taken")
  
  if len(password) < 3:
    raise Exception("Password must be at least 3 characters")

  hashed_password = hash_password(password)
  q.add_user(username, hashed_password)
  
  return True 
  