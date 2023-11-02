#! /usr/bin/python3

from flask import Flask, render_template, url_for

app = Flask(__name__)

navbar = """<a href="/">Index</a> <a href="/page1">Page 1</a> <a href="/page2">Page 2</a>"""

@app.route('/')
def index():
    return render_template("index.html", navbar=navbar)

@app.route('/page1')
def renderPage1():
    output = render_template('page1.html', navbar=navbar)
    return output 

@app.route('/page2')
def renderPage2():
    output = render_template('page2.html', navbar=navbar)
    return output 

if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")