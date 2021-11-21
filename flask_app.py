from flask import Flask, request
from algo import main as main_algo

app = Flask(__name__)

with open('main.html', encoding='utf-8') as f:
    mainhtml = f.read()


@app.route('/')
def main():
    return mainhtml


@app.route('/cards/')
def cards():
    r = request.args
    return main_algo([x.strip() for x in r['words'].split(',')],
        int(r['nwords']), int(r['rows']), int(r['columns']), int(r['empty']), r['color'])
