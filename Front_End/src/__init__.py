import pdb
from flask import Flask, render_template, url_for, request, redirect, session, flash
import gc
import hashlib
from functools import wraps
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

@app.route('/dashboard/', methods=["GET","POST","FRIEND"])
@login_required
def dashboard():
    try:
        if request.method == "POST":
            if "friend_request" in request.form:
                print(request)
                print("Friend SENT")
            if "Friend_Name" in request.form:
                print("Ok use name and id make sure its unique")
        return render_template("shift_cover.html",TOPIC_DICT = TOPIC_DICT)
    except Exception as e:
        return render_template("500.html", error = str(e))
@app.route('/register/', methods=["GET","POST"])
def register_page():
    error = ''
    try:
        if request.method == "POST":
            print(request.form['confirm'])
            #check if all fileds are filled
            for k, v in request.form.items():
                if v == "":
                    flash("{} must be filled in".format(k))
            #check if passwords match
            if request.form['password'] != request.form['confirm']:
                flash("Passwords Don't Match")
            #check if username is taken
            #place holder for api call
            elif request.form['username'] == "taken":
                flash("Username is Taken")
            #create account and send to dashboard
            if request.form['username'] == "admin":
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."
            gc.collect()

        return render_template("register.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("register.html", error = error)
    
@app.route('/login/', methods=["GET","POST"])
def login():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            #flash(attempted_username)
            #flash(attempted_password)
            user_entered_password = attempted_password
            salt = "5gz"
            db_password = user_entered_password+salt
            h = hashlib.md5(db_password.encode())
            if attempted_username == "admin" and attempted_password == "password":
                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
				
            else:
                error = "Invalid credentials. Try Again."


        return render_template("login.html", error = error)

    except Exception as e:
        #flash(e)
        return render_template("login.html", error = error)
    
@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    try:
        return render_template("404.html")
    except Exception as e:
        return render_template("500.html", error = str(e))

TOPIC_DICT = {"Profile":{"Username":"username",
                        "Profile Pic":"url for profile pic",
                         "Status":"My current Status",
                         "Posts":[{"title":"Good Boy","username":"ttravers","url":"url for image","comments":["comment","comment"]}]},
                  "Feed":[
	["Title of Post","url for S3 images","kevin",["comment 1","comment 2"]],
	["Good Boy","url for S3 images","kevin",[["ttravers","thats a good boy"],["ECuso","aww so handsome"]]],
	["Good Girl","url for S3 images","kevin",[["ttravers","thats a good girl"],["ECuso","aww so pretty"],["puppy","awwwwwwww"]]]
],
                  "Friends":[["Trinity Travers","/ttravers/"],
                             ["Ellie Cuso","ECuso"],
                             ["Puppy","Puppy"],
                             ["Kevin","ktravers"]]}


if __name__=="__main__":
    app.run()
