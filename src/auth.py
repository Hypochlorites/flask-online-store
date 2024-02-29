import hashlib 
from . import queries as q 


def hash_password(raw_password):
  raw_password = raw_password.encode('utf-8')
  h = hashlib.sha256()
  h.update(raw_password)
  res = h.hexdigest()
  print(res)
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

