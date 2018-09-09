import json
from subprocess import CalledProcessError, check_output, STDOUT
import re
import os
from tfplay import MODULE_STORE

app = MODULE_STORE.rzt_flask_app


def generate_json_status(status, data):
    return json.dumps({
        'status': status,
        'data': data
    })


def get_ram_usage():
    try:
        total_ram = int(
            str(check_output("cat /proc/meminfo | grep MemTotal |  grep -o '[0-9]*'", stderr=STDOUT, shell=True),
                encoding="utf-8")) / 1000
        free_ram = int(
            str(check_output("cat /proc/meminfo | grep MemFree |  grep -o '[0-9]*'", stderr=STDOUT, shell=True),
                encoding="utf-8")) / 1000
        ram_usage = {
            'total': "{0:.2f}".format(total_ram),
            'used': "{0:.2f}".format(total_ram - free_ram),
            'free': "{0:.2f}".format(free_ram),
            'used_p': "{0:.2f}".format((total_ram - free_ram) / total_ram * 100)
        }
        return ram_usage
    except CalledProcessError:
        return {
            'total': 'Proc Not Supported',
            'used': 'Proc Not Supported',
            'free': 'Proc Not Supported',
            'used_p': 'Proc Not Supported',
        }


def get_disk_usage():
    try:
        disk_usage = str(check_output("df -h | grep "+app.config['DISK_DRIVE'], stderr=STDOUT, shell=True), encoding="utf-8")
        disk_usage = [i for i in disk_usage.split(" ") if i != ""]
        disk_usage = {
            'total': disk_usage[1],
            'used': disk_usage[2],
            'free': disk_usage[3],
            'used_p': disk_usage[4]
        }
        return disk_usage
    except CalledProcessError:
        return {
            'total': 'Proc Not Supported',
            'used': 'Proc Not Supported',
            'free': 'Proc Not Supported',
            'used_p': 'Proc Not Supported'
        }


def get_cpu_usage():
    try:
        cpu_usage = float(str(
            check_output("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'",
                         stderr=STDOUT, shell=True), encoding="utf-8"))
        cpu_usage = {
            'used': "{0:.2f}".format(cpu_usage),
            'free': "{0:.2f}".format(100.0 - cpu_usage)
        }
        return cpu_usage
    except (CalledProcessError, ValueError):
        return {
            'used': 'Proc Not Supported',
            'free': 'Proc Not Supported'
        }


def regex_replace_code(code, sid, sockets):
    file_name = re.search(r"(?<='|\").*.csv", code)
    saved_file_name = re.search(r"(?<='|\").*.model", code)
    if not isinstance(file_name, type(None)):
        file_name = file_name.group(0)
        code = re.sub("(?<='|\").*.csv",
                      app.config['GLOBAL_DIR'] + '/' + sockets[sid].user + '/' + file_name,
                      code)
    if not isinstance(saved_file_name, type(None)):
        saved_file_name = saved_file_name.group(0)
        code = re.sub("(?<='|\").*.model",
                      app.config['GLOBAL_DIR'] + '/' + sockets[sid].user + '/' + saved_file_name,
                      code)
    code = re.sub(".*(from|import).*(os|system|subprocess).*", "", code)
    code = re.sub("tf.train.SummaryWriter\('logs', graph=sess.graph\)",
                  "tf.train.SummaryWriter('" + app.config['TB_DIR'] + '/' + sockets[
                      sid].user + "', graph=sess.graph)", code)
    os.system('rm -rf ' + app.config['TB_DIR'] + '/' + sockets[sid].user + '/*' )
    print(sockets[sid].user+'\n'+code)
    return code
