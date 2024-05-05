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
  context = {
      'products': None,
      'session' : session,
      'error': None
  } 
  try:
    products = get_products()
    context['products'] = products
  except Exception as e:
    context['error'] = e
    
  
  
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

@app.route("/cart/add", methods=["GET", "POST"])
def add_to_cart():

 
  product_id = request.form.get("product_id")

  
  # print(f"product: {product_id}")
  # print(f"intial: {session.get('cart')}")
  
  cart = session.get('cart',{})
  cart[product_id] = cart.get(product_id, 0) + 1
  session['cart'] = cart
  print(f"after: {session['cart']}")
  flash("Added to Cart", "success")
  return redirect(url_for('home'))

@app.route("/cart", methods=["GET", "POST"])
def cart():
  if request.method == "POST":
      pass

  context = {
      'products': None, 
      'session': session,
      'error': None,
  }

  try:
      products = get_products()
      cart = session.get('cart')
      if cart is None:
          context['products'] = []
      else:
          product_ids_in_cart = cart.keys()
          # print(f"product_ids_in_cart: {product_ids_in_cart} ")
          # print(f"before filter: {products}")
          products = list(filter(lambda x: str(x[0]) in product_ids_in_cart, products))
          products = [ (*product, cart[str(product[0])] ) for product in products ]
          context['products'] = products 
          
  except Exception as e:
      context['error'] = e

  
  return render_template('cart.html', context=context)

@app.route("/cart/update-quantity", methods=["POST"])
def update_quantity():
    product_id = request.form.get("product_id")
    quantity = request.form.get("quantity")
    cart = session.get('cart', {})

    try: 
      if quantity == "0":
          cart.pop(product_id)
      else:
          cart[product_id] = quantity
    except Exception as e:
        print(e)
  
    session['cart'] = cart
    return redirect(url_for('cart'))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
