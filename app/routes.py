from flask import request, redirect, flash
from flask_login import current_user, login_user, logout_user
from datetime import timedelta
import json

from app import app, login
import service
from models import User


@login.user_loader
def get_user(id: str) -> User:
    return service.get_user(int(id))

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        print("already authenticated")
        return redirect("index.html")

    body: dict = json.loads(request.data)

    logged_in_user = service.login(body.get("email","LLL"),body.get("password","L"))

    if logged_in_user != None:
        login_user(logged_in_user,remember=True,duration=timedelta(hours=6))
        print("logged in")
        return redirect("index.html")

    return redirect("login.html")

@app.route("/logout")
def logout():
    logout_user()
    print("logged out")
    return redirect('index.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated():
        return redirect('index.html')
    
    body: dict = json.loads(request.data)
    if service.new_user(body.get("email",""),body.get("password",""),body.get("first_name",""),body.get("last_name","")):
        flash('Registered successfully. Please use your new account to login.')
        return redirect('login.html')

    return redirect('register.html')

# TODO move somewhere better
app.run()
    

    
