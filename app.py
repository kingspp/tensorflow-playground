"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

import eventlet
eventlet.monkey_patch()

import argparse
import os
import logging
# noinspection PyUnresolvedReferences
from tfplay.User import User

from flask import Flask
# noinspection PyUnresolvedReferencesl
import json
from flask_socketio import SocketIO
from tfplay import MODULE_STORE


'''
{"admin": "admin@123", "vinay": "vinay", "nandu": "nandu", "prathyush": "prathyush"}
'''

# PyLogger Initialization
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask Configuration
app = Flask(__name__, static_folder=str(os.getcwd() + '/static'), instance_relative_config=True)
app.secret_key = os.urandom(32)
MODULE_STORE.rzt_flask_app = app
app.config['ALLOWED_EXTENSIONS'] = {'py', 'csv', 'model'}

socketio = SocketIO(app)
MODULE_STORE.rzt_socketio = socketio
sockets = {}
MODULE_STORE.rzt_sockets = sockets

# noinspection PyUnresolvedReferences
from tfplay.FileHandlers import *
# noinspection PyUnresolvedReferences
from tfplay.Socket import *
# noinspection PyUnresolvedReferences
from tfplay.KThread import *


# Main Function - Start Here
if __name__ == '__main__':
    eventlet.monkey_patch()
    # parser = argparse.ArgumentParser(description='PyFlow: Debugger')
    # parser.add_argument('-f', '--file', help='Input File for debugging', required=False)
    # parser.add_argument('-r', help="Run Flask", required=True)
    # args = vars(parser.parse_args())
    # if args['r']:
        # app.config.from_pyfile(args['r'])
    app.config.from_pyfile('/Users/prathyushsp/Git/tensorflow-playground/instance/dev.py')
    print(app.config)
    users_dict = json.loads(open(app.config['USER_JSON']).read())
    __builtins__.rzt_users_dict = users_dict
    users = [User(id).manager(item[0], item[1]) for id, item in enumerate(users_dict.items())]
    __builtins__.rzt_users = users

    from tfplay.LoginManager import *
    from tfplay.AppBasics import *

    os.system('nohup tensorboard --logdir=' + app.config['TB_DIR'] + ' --port ' + app.config[
        'TB_PORT'] + ' --host ' + app.config['TB_HOST'] + ' &')
    app.run(app, host=app.config['FLASK_HOST'], port=app.config['FLASK_PORT'], debug=app.config['FLASK_DEBUG'])
