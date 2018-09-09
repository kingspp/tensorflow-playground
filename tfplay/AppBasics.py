"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

import threading
from tfplay.Utils import generate_json_status, get_ram_usage, get_disk_usage, get_cpu_usage
from flask import Response, redirect, flash, render_template, url_for, request
from flask_login import current_user, login_required
import os
import json

app = rzt_flask_app
users = rzt_users
socketio = rzt_socketio
sockets = rzt_sockets


def tfstatus():
    return {
        'ram_usage': get_ram_usage(),
        'disk_usage': get_disk_usage(),
        'cpu_usage': get_cpu_usage(),
        'thread_usage': threading.active_count()
    }


def tf_users():
    active_user_count, busy_user_count = 0,0
    user_list = []
    for user in users:
        state = 'offline'
        if not isinstance(user.thread, type(None)) and not user.thread.isAlive():
            user.busy = False
            state = 'available'
        else:
            if user.active:
                active_user_count += 1
                state = 'available'
                if user.busy:
                    busy_user_count += 1
                    state = 'busy'
        user_list.append({
            'username': user.username,
            'script': user.script,
            'state': state
        })
    return {
        'user_status': {
            'total': len(users),
            'busy': busy_user_count,
            'active': active_user_count,
            'offline': len(users) - active_user_count - busy_user_count
        },
        'users': user_list
    }


@socketio.on('status')
def tf_status_socket():
    sockets[request.sid].emit('status_response', tfstatus())


@socketio.on('user')
def user_status_socket():
    sockets[request.sid].emit('user_response', tf_users())


@app.route('/tfstatus')
def tf_status_response():
    return Response(json.dumps(tfstatus()))


@app.route('/userstatus')
def user_status_response():
    return Response(json.dumps(tf_users()))


@app.route('/restart/<config>')
def restart(config):
    os.system('ls')
    os.system('sudo ./build.sh ' + config)
    return "Restarting . . Please wait ..."


@app.route('/stop')
def stop():
    current_user.thread.stop()
    return Response(generate_json_status('terminated', 'Terminated'))


@app.route('/users')
@login_required
def user_template():
    if current_user.username == 'admin':
        return render_template('user.html')
    else:
        return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard_template():
    if current_user.username == 'admin':
        return render_template('admin.html')
    else:
        return redirect(url_for('home'))


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    flash("Invalid Username / Password")
    return redirect(url_for('home'))


@app.route('/current_user')
def get_current_user():
    return json.dumps({'username': current_user.username})


@app.route('/')
@login_required
def home():
    if current_user.username == "admin":
        return render_template("admin.html")
    else:
        return render_template('index.html')
