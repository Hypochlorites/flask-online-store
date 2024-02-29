from flask import Flask, request, render_template, redirect, url_for
from src.auth import login#, signup 


app = Flask(__name__)


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/signin', methods=["GET", "POST"])
def signin():
  error = None
  if request.method == "POST":
    email = request.form.get("username")
    password = request.form.get("password")
    authenticated = login(email,password)
    if authenticated:
      return redirect(url_for('home'))
    else:
      error = "Incorrect email or password"
  return render_template('signin.html', error=error)


# @app.route('signup')
# def signup():
#   return render_template('signup.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=80)
