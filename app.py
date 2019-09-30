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
MODULE_STORE.flask_app = app

app.config['ALLOWED_EXTENSIONS'] = {'py', 'csv', 'model'}
app.config['GLOBAL_DIR'] = '/tmp/global_dir'
app.config['DEF_DIR'] = '/tmp/def_dir'
app.config['TB_DIR'] = '/tmp/tb_dir'
app.config['PYTHON'] = 'python3'

socketio = SocketIO(app)
MODULE_STORE.socketio = socketio
sockets = {}
MODULE_STORE.sockets = sockets

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
    # app.config.from_pyfile('/Users/prathyushsp/Git/tensorflow-playground/instance/dev.py')
    # print(app.config)
    users_dict = {"admin":"admin@123", "nandu":"nandu"}#json.loads(open(app.config['USER_JSON']).read())
    MODULE_STORE.users_dict = users_dict
    users = [User(id).manager(item[0], item[1]) for id, item in enumerate(users_dict.items())]
    MODULE_STORE.users = users

    from tfplay.LoginManager import *
    from tfplay.AppBasics import *

    # os.system('nohup tensorboard --logdir=' + app.config['TB_DIR'] + ' --port ' + app.config[
        # 'TB_PORT'] + ' --host ' + app.config['TB_HOST'] + ' &')
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
