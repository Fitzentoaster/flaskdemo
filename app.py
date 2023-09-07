from flask import Flask, flash, jsonify, redirect, render_template, request, session, after_this_request
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functools import wraps

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '42'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    return render_template("error.html", top=code, bottom=message), code

@app.route('/')
def index():
    return render_template("homepage.html")

@app.route('/products')
def products():
    return render_template("products.html")

@app.route('/cart')
@login_required
def cart():
    return render_template("cart.html")

@app.route('/checkout')
@login_required
def checkout_page():
    return render_template("checkout.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not (request.form.get("username") == "boopty"):
            flash("Invalid Username or Password", "danger")
            return redirect("/login")    
        
        if not request.form.get("password") == "123":
            flash("Invalid Username or Password", "danger")
            return redirect("/login")  

        session["user_id"] = "boopty"
        flash('Login Successful', 'primary')
        return redirect("/")
    else:
        return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("Logged Out Successfully", 'primary')
    return redirect("/")

if __name__ == "__main__":
    app.run()