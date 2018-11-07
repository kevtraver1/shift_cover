import pdb
from flask import Flask, render_template, url_for, request, redirect, session, flash
import gc
import hashlib
from functools import wraps
import boto3
import urllib.request
import requests

app = Flask(__name__)
app.secret_key = b'A\x8by\xbdl\xbcpj>.EfWo,\xf2'
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap

@app.route('/register/', methods=["GET","POST"])
def register_page():
    error = ''
    try:
        if request.method == "POST":
            
            #check if all fileds are filled
            for k, v in request.form.items():
                if v == "":
                    flash("{} must be filled in".format(k))
            #check if passwords match
            if request.form['password'] != request.form['confirm']:
               flash("Passwords Don't Match")
            username = request.form['username']
            password = request.form['password']
            company = request.form['company']
            occupation = request.form['occupation']
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            salt = "5gz"
            db_password = password+salt
            hashed_password = hashlib.md5(db_password.encode())
            user_data = {"username":username,"password":password,"company":company,"occupation":occupation,"email":email,"first_name":first_name,"last_name":last_name}
            contents = requests.get("https://evzc9p1un8.execute-api.us-east-1.amazonaws.com/dev/create_account",user_data)
            response = contents.json()

            if response:
                #send email verifacation
                return redirect(url_for('login'))	
            else:
                error = "Invalid credentials. Try Again."
            gc.collect()

        return render_template("register.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("register.html", error = error) 

@app.route('/dashboard/', methods=["GET","POST"])
@login_required
def dashboard():
    try:
        
        print(request.form)
        #use decorator for validate forms

        if request.method == "POST":
            if request.form["post_id"] == "request_time":
                print("WOOOOOOOOO")
            if "friend_request" in request.form:
                print(request)
                print("Friend SENT")
            if "Friend_Name" in request.form:
                print("Ok use name and id make sure its unique")
        #use sessiion data as well to personalize veiwing
        return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)
    except Exception as e:
        return render_template("500.html", error = str(e))
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login'))

@app.route('/login/', methods=["GET","POST"])
def login():
    error = ''
    try:
        if request.method == "POST":
            username = request.form['username']
            password = request.form['password']
            #flash(attempted_username)
            #flash(attempted_password)
            salt = "5gz"
            db_password = password+salt
            hashed_password = hashlib.md5(db_password.encode())
            user_data = {"username":username,"password":password}
            contents = requests.get("https://evzc9p1un8.execute-api.us-east-1.amazonaws.com/dev/account_login",user_data)#account_login?username={}&password={}".format(username,password)).read()
            response_hash = contents.json()[0]
            if response_hash['username']:
                session['logged_in']    = True
                session['username']     = response_hash['username']
                session['password']     = response_hash['password']
                session['company']      = response_hash['company']
                session['occupation']   = response_hash['job_title']
                session['email']        = response_hash['email']
                session['first_name']   = response_hash['first_name']
                session['last_name']    = response_hash['last_name']
                session['account_id']   = response_hash['account_id']
                session['account_picture']= response_hash['account_picture']
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."


        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)  
		
@app.errorhandler(404)
def page_not_found(e):
    try:
        return render_template("404.html")
    except Exception as e:
        return render_template("500.html", error = str(e))		

@app.route('/post/', methods=["GET","POST"])
@login_required
def post():
    error = ''
    try:
        if request.method == "POST":
            print("post completed")

        return render_template("post.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("post.html", error = error)



TOPIC_DICT = {"Profile":{"Username":"username",
                        "Profile Pic":"url for profile pic",
                         "Status":"My current Status",
                         "Posts":[{"title":"Good Boy","username":"ttravers","url":"url for image","comments":["comment","comment"]}]},
                  "Feed":[
	["Title of Post","url for S3 images","kevin",["comment 1","comment 2"]],
	["Good Boy","url for S3 images","kevin",[["ttravers","thats a good boy"],["ECuso","aww so handsome"]]],
	["Good Girl","url for S3 images","kevin",[["ttravers","thats a good girl"],["ECuso","aww so pretty"],["puppy","awwwwwwww"]]]
],
"Requests":[
    ["11/7/2018","07:00:00","03:00:00","ME mum is having a birthday"],
    ["12/8/2018","08:15:00","04:15:00","IM DRINKING BOYS"],
    ["01/9/2019","09:30:00","05:30:00","I HAVE a job interview... i mean im sick cough cough"]
],
                  "Friends":[["Trinity Travers","/ttravers/"],
                             ["Ellie Cuso","ECuso"],
                             ["Puppy","Puppy"],
                             ["Kevin","ktravers"]]}


if __name__=="__main__":
    app.run()
    
