"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

from flask import request, redirect, render_template, url_for, flash, abort, make_response, session
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
from tfplay.User import User
import os
import json

app = rzt_flask_app
users = rzt_users
users_dict = rzt_users_dict

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        if request.form['ltype'] == "login":
            username, password = request.form['username'], request.form['password']
            for id, user in enumerate(users):
                if user.username == username and user.password == password:
                    users[id].active = True
                    login_user(user)
                    if not os.path.isdir(app.config['GLOBAL_DIR'] + '/' + 'username'):
                        os.system("mkdir -p " + app.config['GLOBAL_DIR'] + '/' + current_user.username + '/')
                        os.system("cp -r " + app.config['DEF_DIR'] + '/* ' + app.config[
                            'GLOBAL_DIR'] + '/' + current_user.username + '/')
                    return redirect('/')
            else:
                return abort(401)
        elif request.form['ltype'] == "register":
            username, password, key = request.form['username'], request.form['password'], request.form['key']
            if key == app.config['KEY']:
                if username not in users_dict:
                    users_dict[username] = password
                    users.append(User(len(users)).manager(username, password))
                    open(app.config['USER_JSON'], 'w').write(json.dumps(users_dict))
                    flash('Registration Successful')
                    return redirect(url_for('home'))
                flash('Username Exists!!')
                return redirect(url_for('home'))
            flash('Invalid KEY')
            return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route("/logout")
@login_required
def logout():
    print('Request Cookies :: ')
    print(request.cookies)
    resp = make_response(redirect('/login'))
    session.clear()
    resp.set_cookie('session', expires=0)
    for id, user in enumerate(users):
        if user.id == current_user.id:
            users[id].active = False
    logout_user()
    return resp


@app.route("/logout/all")
def logout_all():
    for user in users:
        load_user(user.id)
        logout_user()
    session.clear()
    return redirect('/login')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return users[int(userid)]
