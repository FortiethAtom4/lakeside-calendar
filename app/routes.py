
from time import strftime

from flask import render_template, request, redirect, flash, get_flashed_messages
from flask_login import current_user, login_user, logout_user
from datetime import datetime, timedelta
import logging

from app import app, login
import service
from models import User

logger = logging.getLogger(__name__)

@login.user_loader
def get_user(id: str) -> User:
    return service.get_user(int(id))

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        flash("Already logged in, restoring saved session")
        return redirect("/")

    if request.method == "POST":
        body: dict = request.form

        logged_in_user = service.login(body.get("email","LLL"),body.get("password","L"))

        if logged_in_user != None:
            if login_user(logged_in_user,remember=False,duration=timedelta(hours=6)):
                app.logger.info("Successful login for \"" + logged_in_user.first_name + " " + logged_in_user.last_name + "\"")
                return redirect("/")
            else:
                flash("Your account has been deactivated.")
                return redirect("/login")
        else:
            flash("Invalid email and/or password.")

    return render_template  ("login.html")

@app.route("/logout")
def logout():
    logout_user()
    get_flashed_messages()
    flash("Logout successful.")
    return redirect('/login')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        flash("You are already registered. Please log out to register a new account.")
        return redirect('/')
    
    if request.method == "POST":
        body: dict = request.form
        if service.new_user(body.get("email",""),body.get("password",""),body.get("first_name",""),body.get("last_name",""), 1):
            app.logger.info("Successfully registered new account at " + body.get("email"))
            flash('Registered successfully. Please use your new account to login.')
            return redirect('/login')
        else:
            flash("Unable to register your account. Please try again later.")
            app.logger.warning("Failed to register new account")

            
    return render_template('register.html')

@app.route("/", methods=['GET','POST'])
def home_page():
    if not current_user.is_authenticated:
        flash("Welcome to the Lion House Calendar. Please log in to continue.")
        return redirect("/login")

    today = datetime.today()

    body_data: dict = service.prepare_index_page(int(request.form.get("year",today.year)),int(request.form.get("month",today.month)))

    return render_template("index.html",data=body_data)


@app.route("/select",methods=['POST'])
def select_day():
    return "yes"



    

    
