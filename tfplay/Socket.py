"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

from tfplay.KThread import KThread
from flask import request
from tfplay.Utils import generate_json_status
from flask_login import current_user, login_required
from tfplay import MODULE_STORE

socketio = MODULE_STORE.rzt_socketio
sockets = MODULE_STORE.rzt_sockets


class Socket:
    def __init__(self, sid, user):
        self.sid = sid
        self.connected = True
        self.user = user

    def emit(self, event, data):
        socketio.emit(event, data, room=self.sid)


@socketio.on('event')
@login_required
def run_p_code(message):
    if 'code' in message:
        t = KThread(message['code'], request.sid, sockets)
        t.daemon = True
        t.start()
        sockets[request.sid].emit('response', generate_json_status('running', 'Running'))
        current_user.thread = t
        current_user.busy = True
        current_user.script = message['code']


@socketio.on('connect')
@login_required
def connect():
    sockets[request.sid] = Socket(request.sid, current_user.username)
    print('Current user :: ', (current_user.username))


@socketio.on('disconnect')
@login_required
def disconnect():
    sockets.pop(request.sid)
