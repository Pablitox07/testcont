import os
import requests
import socket

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import (Flask, redirect, render_template, request, send_from_directory, url_for)

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


@app.route('/dnsres')  # New route
def default():
    user_ip = request.remote_addr
    return f"Your IP address is {user_ip}"

@app.route('/getyourip')
def getip():
    ip_address = request.headers.get('X-Forwarded-For')
    x_forwarded_for = request.headers.get('X-Forwarded-For', '').split(',')[0].strip()
    return f'Your IP address is {x_forwarded_for}'

    

if __name__ == '__main__':
   app.run()
