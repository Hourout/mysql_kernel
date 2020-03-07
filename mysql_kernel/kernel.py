import os
import json

import pymysql
from ipykernel.kernelbase import Kernel


__version__ = '0.1.0'


class MysqlParser():
    def __init__(self, display, **kwargs):
        if display=='prettytable':
            self.load = __import__('prettytable')
            self.type = 'prettytable'
        else:
            try:
                self.load = __import__('pandas')
                self.type = 'pandas'
            except ImportError as msg:
                self.load = __import__('prettytable')
                self.type = 'prettytable'
        self.pandas = True if self.type=='pandas' else False

    def format(self, content):
        if self.type=='pandas':
            content = self.load.DataFrame(content).to_html()
        else:
            content = self.load.from_db_cursor(content).get_html_string()
        return content

class MysqlKernel(Kernel):
    implementation = 'jupyter-mysql-kernel'
    implementation_version = __version__
    language = 'mysql'
    language_version = 'latest'
    language_info = {'name': 'mysql',
                     'mimetype': 'text/x-sh',
                     'file_extension': '.sql'}
    banner = 'mysql kernel'

    mysql_setting_file = os.path.join(os.path.expanduser('~'), '.local/config/mysql_config.json')
    mysql_config = {'user': 'root',
                    'host': '127.0.0.1',
                    'port': '3306',
                    'charset': 'utf8',
                    'password': '',
                    'display': 'pandas'}

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        if os.path.exists(self.mysql_setting_file):
            with open(self.mysql_setting_file, "r") as f:
                self.mysql_config.update(json.load(f))
        self.parser = MysqlParser(self.mysql_config['display'])
        self.connect()

    def connect(self):
        cursorclass = pymysql.cursors.DictCursor if self.parser.pandas else pymysql.cursors.Cursor
        try:
            self.connect = pymysql.connect(host=self.mysql_config['host'],
                                           port=int(self.mysql_config['port']),
                                           user=self.mysql_config['user'],
                                           charset=self.mysql_config['charset'],
                                           passwd=self.mysql_config['password'],
                                           cursorclass=cursorclass)
            self.cursor = self.connect.cursor()
        except Exception:
            self.connect = False

    def execute(self, sql):
        if not self.connect:
            self.connect()
        if self.connect:
            self.cursor.execute(sql)

    def fetchall(self):
        if not self.connect:
            self.connect()
        if self.connect:
            return self.cursor.fetchall() if self.parser.pandas else self.cursor
        return False

    def commit(self):
        if not self.connect:
            self.connect()
        if self.connect:
            self.connect.commit()

    def output(self, output):
        if not self.silent:
            if not isinstance(output, str):
                output = self.parser.format(output)
            display_content = {'source': 'kernel',
                               'data': {'text/html': output},
                               'metadata': {}}
            self.send_response(self.iopub_socket, 'display_data', display_content)
    
    def ok(self):
        return {'status':'ok', 'execution_count':self.execution_count, 'payload':[], 'user_expressions':{}}

    def err(self, msg):
        return {'status':'error',
                'error':msg,
                'traceback':[msg],
                'execution_count':self.execution_count,
                'payload':[],
                'user_expressions':{}}

    def do_execute(self, code, silent, store_history=True, user_expressions=None, allow_stdin=False):
        self.silent = silent
        if not code.strip():
            return self.ok()
        if not self.connect:
            msg = 'Unable to connect to Mysql server. Check that the server is running.'
            self.output(msg)
            return self.err(msg)
        sql = code.rstrip()
        output = ''
        try:
            splitString = ";\n" if ";\n" in sql or sql.endswith(";") else "\n"
            for v in sql.split(splitString):
                v = v.rstrip()
                l = v.lower()
                if len(v) > 0:
                    if v[0] == "#":
                        continue
                    self.execute(v)
                    if l.startswith('select')|l.startswith('show')|l.startswith('explain')|l.startswith('desc'):
                        output = self.fetchall()
                    else:
                        self.commit()
                        output = 'yes'
            self.output(output)
            return self.ok()
        except Exception as msg:
            self.output(format(msg))
            return self.err('Error executing code ' + sql)

    
