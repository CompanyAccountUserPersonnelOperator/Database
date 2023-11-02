#! /usr/bin/python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/form-get.html')
def renderFormGet():
    output = render_template('form-get.html')
    return output 

@app.route('/submitformGet.html', methods=['GET'])
def renderTableGet():
    firstname = request.args.get('fname')
    print(firstname)
    lastname = request.args.get('lname')
    output = render_template('table.html', firstname=firstname, lastname=lastname)
    return output 

@app.route('/form-post.html')
def renderFormPost():
    output = render_template('form-post.html')
    return output 

@app.route('/submitformPost.html', methods=['POST'])
def renderTablePost():
    firstname = request.form.get('fname')
    lastname = request.form.get('lname')
    output = render_template('table.html', firstname=firstname, lastname=lastname)
    return output 


@app.route('/table-list.html')
def renderMultiple():
    exampleCollection = [{'firstname':'test1', 'lastname':'test2'},
                         {'firstname':'test3', 'lastname':'test4'}]
    output = render_template('table-list.html', collection=exampleCollection)
    return output 


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")