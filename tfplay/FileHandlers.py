"""
Created on 08 Oct 2016,
@author: Prathyush SP,
@version: 0.3.4

"""

import os
import json
from flask import request, Response, send_from_directory
from flask_login import current_user
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
from tfplay import MODULE_STORE

app = MODULE_STORE.rzt_flask_app


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['GLOBAL_DIR'] + '/' + current_user.username, filename))
    return Response('File Upload Successfull')


@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    print('In Download')
    uploads = app.config['GLOBAL_DIR'] + '/' + current_user.username
    return send_from_directory(directory=uploads, filename=filename, as_attachment=True)


@app.route('/save_file', methods=['POST'])
def save_file():
    open(app.config['GLOBAL_DIR'] + '/' + current_user.username + '/' + request.json['filename'], 'w').write(request.json['content'])
    return "File Saved"


@app.route('/load_file/<filename>')
def load_file(filename):
    print("Cookies ::  ", request.cookies)
    return send_from_directory(app.config['GLOBAL_DIR'] + '/' + current_user.username,
                               filename)


@app.route('/delete_file/<filename>')
def delete_file(filename):
    os.system("rm -rf " + app.config['GLOBAL_DIR'] + '/' + current_user.username + '/' + filename)
    return "File Deleted"


@app.route('/get_files')
def get_files():
    files = [f for f in listdir(app.config['GLOBAL_DIR'] + '/' + current_user.username + '/') if
             isfile(join(app.config['GLOBAL_DIR'] + '/' + current_user.username + '/', f))]
    data_files = [file for file in files if file.__contains__('.csv')]
    python_files = [file for file in files if file.__contains__('.py')]
    model_files = [file for file in files if file.__contains__('.model') and not file.__contains__('.meta')]
    return json.dumps({
        'data_files': data_files,
        'python_files': python_files,
        'model_files': model_files
    })
