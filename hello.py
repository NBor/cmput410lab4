#!/usr/bin/env python
from flask import Flask
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, Flask!'

@app.route('/second')
@app.route('/second/<name>')
def hello_two(name='Flask'):
    return "<h1>Hello %s (second test)!</h1>" % name

if __name__ == '__main__':
    app.debug = True
    app.run()
