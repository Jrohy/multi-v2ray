#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPBasicAuth

from .app import func_router
from .util_core.config import Config

config = Config()
app = Flask(__name__, static_url_path='/static')
app.register_blueprint(func_router)

auth = HTTPBasicAuth()

@auth.get_password
def get_pw(username):
    return config.get_web('pass')

@app.route('/')
@auth.login_required
def index():
    return render_template(config.get_web('index_page'))

if __name__ == '__main__':
    app.run(debug=True, port=config.get_web('port'))