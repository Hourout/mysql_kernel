import pandas as pd
import sqlalchemy as sa
from ipykernel.kernelbase import Kernel


__version__ = '0.3.0'

class MysqlKernel(Kernel):
    implementation = 'mysql_kernel'
    implementation_version = __version__
    language = 'sql'
    language_version = 'latest'
    language_info = {'name': 'sql',
                     'mimetype': 'text/x-sh',
                     'file_extension': '.sql'}
    banner = 'mysql kernel'

    def __init__(self, **kwargs):
        Kernel.__init__(self, **kwargs)
        self.engine = False
        
    def output(self, output):
        if not self.silent:
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
        output = ''
        if not code.strip():
            return self.ok()
        sql = code.rstrip()+('' if code.rstrip().endswith(";") else ';')
        try:
            for v in sql.split(";"):
                v = v.rstrip()
                l = v.lower()
                if len(l)>0:
                    if l.startswith('mysql://'):
                        if l.count('@')>1:
                            self.output("Connection failed, The Mysql address cannot have two '@'.")
                        else:
                            self.engine = sa.create_engine(f'mysql+py{v}')
                    elif l.startswith('create database '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('drop database '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('create table '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('drop table '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('delete '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('alter table '):
                        pd.io.sql.execute(l, con=self.engine)
                    elif l.startswith('insert into '):
                        pd.io.sql.execute(l, con=self.engine)
                    else:
                        if self.engine:
                            if l.startswith('select ') and ' limit ' not in l:
                                output = pd.read_sql(l+' limit 1000', self.engine).to_html()
                            else:
                                output = pd.read_sql(l, self.engine).to_html()
                        else:
                            output = 'Unable to connect to Mysql server. Check that the server is running.'
            self.output(output)
            return self.ok()
        except Exception as msg:
            self.output(str(msg))
            return self.err('Error executing code ' + sql)
