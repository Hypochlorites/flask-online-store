import os
from flask import Flask, request, render_template, redirect, url_for, session, flash 

from src.auth import login, signup 
from src.queries import get_products

from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

@app.route('/')
def home():
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
    username = request.form.get("username")
    password = request.form.get("password")
    authenticated = login(username,password)
    if authenticated:
      session['username'] = username
      return redirect(url_for('home'))
    else:
      error = "Incorrect username or password"
  return render_template('signin.html', error=error)


@app.route('/signup', methods=["GET", "POST"])
def signup_route():
  error = None
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm-password")
    
    if password != confirm_password:
      error = "Passwords do not match"
      return render_template('signup.html', error=error)

    try: 
      signup(username, password)
    except Exception as e:
      error = e
      return render_template('signup.html', error=error)

    return redirect(url_for('signin_route'))
    
      
  
  return render_template('signup.html', error=error)

@app.route("/signout")
def signout():
  session.clear()

  return redirect(url_for('home'))

@app.route("/add-to-cart", methods=["GET", "POST"])
def add_to_cart():
  product_id = request.form.get("product_id")

  cart = session.get('cart',{})
  cart[product_id] = cart.get(product_id, 0) + 1
  session['cart'] = cart
  flash("Added to Cart", "success")
  print(f"flash: {flash}")
  return redirect(url_for('home'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
