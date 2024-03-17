import os
from flask import Flask, request, render_template, redirect, url_for, session 

from src.auth import login, signup 
from src.queries import get_products

from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/')
def home():
  print(session)
  try:
    products = get_products()
    context = {
        'user': "Temporary",
        'products': products,
        'session' : session,
        'error': None
    } 
  except Exception as e:
    context = {
        'user': "temporary",
        'products': None,
        'error': e
    }
  
  
  return render_template('index.html', context=context)


@app.route('/signin', methods=["GET", "POST"])
def signin_route():
  error = None
  if request.method == "POST":
    email = request.form.get("username")
    password = request.form.get("password")
    authenticated = login(email,password)
    if authenticated:
      session['email'] = email
      return redirect(url_for('home'))
    else:
      error = "Incorrect email or password"
  return render_template('signin.html', error=error)


@app.route('/signup', methods=["GET", "POST"])
def signup_route():
  error = None
  if request.method == "POST":
    email = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    print(password)
    print(confirm_password)
    
    if password != confirm_password:
      error = "Passwords do not match"
      return render_template('signup.html', error=error)

    try: 
      signup(email, password)
    except Exception as e:
      error = e
      return render_template('signup.html', error=error)

    return redirect(url_for('signin_route'))
    
      
  
  return render_template('signup.html', error=error)




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
