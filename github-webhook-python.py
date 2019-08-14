# -*- coding: utf-8 -*-
import BaseHTTPServer
import json
import hmac
from hashlib import sha1
from collections import OrderedDict
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class my_web(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        primary_data = self.rfile.read(int(self.headers['Content-Length']))
        format_data = json.dumps(json.loads(primary_data,object_pairs_hook=OrderedDict),separators=(',',':'),ensure_ascii=False)
        secret_check = 'sha1=' + hmac.new('your_secret', msg=format_data, digestmod=sha1).hexdigest()
        if self.path == '/hook/push/' and  secret_check == self.headers['X-Hub-Signature']:
            self.send_response(200)
            message = json.dumps('Success Recive')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(message)
            run_command('xxxx','./xxxx/')
        else:
            self.send_response(403)
            message = json.dumps('Error Action')
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(message)
def run_command(remote_url, local_dir):
    import git
    import os
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    if len(os.listdir(local_dir)) <= 1:
        git.Repo.clone_from(url=remote_url, to_path=local_dir)
        print 'clone success'
    else:
        gp = git.cmd.Git(local_dir)
        gp.pull()
        print 'pull success'

if __name__ == '__main__':
    server_address = ('', 8000)
    my_app= BaseHTTPServer.HTTPServer(server_address=server_address,RequestHandlerClass=my_web,bind_and_activate=True)
    my_app.serve_forever()
