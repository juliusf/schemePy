#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request
import schemepy
import schemepy.reader as rd
import schemepy.evaluator as ev
import imp

DEBUG = True
SECRET_KEY = '$(secret_key)'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/_interpret')
def evaluate():
    statement = request.args.get('statement')
    ev = imp.reload(schemepy.evaluator)
    try:
        expression = rd.parse(statement)
        res = ev.evaluate(expression)
    except Exception as e:
        res = e
    return jsonify(result= str(res))

@app.route('/_interpretDirect')
def direct():
    statement = request.args.get('statement')
    try:
        expression = rd.parse(statement)
        res = ev.evaluate(expression)
    except Exception as e:
        res = e
    return jsonify(result= str(res))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')
if __name__ == '__main__':
    app.run()