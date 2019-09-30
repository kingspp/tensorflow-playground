"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

import threading
from tfplay.Utils import generate_json_status, regex_replace_code
from subprocess import PIPE
from eventlet.green.subprocess import Popen
from tfplay import MODULE_STORE

app = MODULE_STORE.flask_app


class KThread(threading.Thread):
    def __init__(self, code, sid, sockets):
        threading.Thread.__init__(self)
        self.process = None
        self.sid = sid
        self.code = code
        self.sockets = sockets

    def run(self):
        print("Request :: ", self.sockets[self.sid].user, " :: ")
        self.code = regex_replace_code(self.code, self.sid, self.sockets)
        print(self.code)
        with Popen([app.config['PYTHON'], '-u', '-c', self.code], stdout=PIPE, stderr=PIPE, bufsize=1,
                   universal_newlines=True) as p:
            self.process = p
            for line in p.stdout:
                self.sockets[self.sid].emit('response', generate_json_status('success', line))
            for line in p.stderr:
                if 'INFO' in line or 'DEBUG' in line:
                    self.sockets[self.sid].emit('response', generate_json_status('success', line))
                else:
                    self.sockets[self.sid].emit('response', generate_json_status('error', line))
        self.sockets[self.sid].emit('response', generate_json_status('terminated', 'Terminated'))

    def stop(self):
        print("Trying to stop thread ")
        self.sockets[self.sid].emit('response', generate_json_status('terminated', 'Terminated'))
        if self.process is not None:
            self.process.terminate()
            self.process = None
