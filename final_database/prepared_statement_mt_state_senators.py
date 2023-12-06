#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rep-list.html', methods=['GET'])
def showReps():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    mycursor = connection.cursor()
    newFirstName = request.args.get('fname')
    newLastName = request.args.get('lname')
    newDistrict = request.args.get('district')
    newParty = request.args.get('party')
    if newFirstName is not None and newLastName is not None and newDistrict is not None:
        mycursor.execute("INSERT INTO senators (firstname, lastname, district, party) values (%s, %s, %s, %s)", (newFirstName, newLastName, newDistrict, newParty ))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        mycursor.execute("DELETE FROM senators WHERE repID=%s", (deleteID,))
        connection.commit()

    mycursor.execute("SELECT repID, firstname, lastname, district, party FROM senators")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('rep-list.html', collection=myresult)

@app.route("/updateRep")
def updateRep():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    id = request.args.get('id')
    newFirstName = request.args.get('fname')
    newLastName = request.args.get('lname')
    newDistrict = request.args.get('district')
    newParty = request.args.get('party')
    if id is None:
        return "Error, ID not specified"
    elif newFirstName is not None and newLastName is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE senators SET firstname=%s, lastname=%s, district=%s, party=%s WHERE repID=%s", (newFirstName, newLastName, newDistrict, newParty, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showReps'))

    mycursor = connection.cursor()
    mycursor.execute("SELECT repID, firstname, lastname, district, party FROM senators WHERE repID=%s", (id,))
    id, existingFName, existingLName, existingDistrict, existingParty = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('rep-update.html', id=id, existingFName=existingFName, existingLName=existingLName, existingDistrict=existingDistrict, existingParty=existingParty)


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")