#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request, current_app
import schemepy
import schemepy.reader as rd
import schemepy.evaluator as ev
import imp
import time
import sys
sys.setrecursionlimit(100000)

DEBUG = True
SECRET_KEY = '$(secret_key)'

app = Flask(__name__)
app.config.from_object(__name__)

env = ev.get_root_environment()


@app.route('/_interpret')
def evaluate():
    global env
    statement = request.args.get('statement')
    ev = imp.reload(schemepy.evaluator)
    env = ev.get_root_environment()
    try:
        start = time.time()
        expression = rd.parse(statement)
        current_app.logger.info(expression)
        res = ev.evaluate(expression, env)
        end = time.time() - start
        current_app.logger.info(end)
        res=  str(res)
    except Exception as e:
        expression = rd.parse(statement)
        res = e
        res=  str(res)
    return jsonify(result=res)

@app.route('/_interpretDirect')
def direct():
    statement = request.args.get('statement')
    try:
        expression = rd.parse(statement)
        res = ev.evaluate(expression, env)
        res = str(res)
        current_app.logger.info(res)
    except Exception as e:
        res = e
    return jsonify(result=res)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run(debug=True)
