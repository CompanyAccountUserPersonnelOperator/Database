#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showReps():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    newFirstName = request.args.get('fname')
    newLastName = request.args.get('lname')
    newEmail = request.args.get('email')
    if newFirstName is not None and newLastName is not None and newEmail is not None:
        mycursor.execute("INSERT into reps (lastname, firstname, email) values (%s, %s, %s)", (newLastName, newFirstName, newEmail))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        mycursor.execute("DELETE FROM reps WHERE repID=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the reps table
    mycursor.execute("SELECT repID, lastname, firstname, email FROM reps")
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
    newEmail = request.args.get('email')
    if id is None:
        return "Error, id not specified"
    elif newFirstName is not None and newLastName is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE reps SET lastname=%s, firstname=%s, email=%s WHERE repID=%s", (newLastName, newFirstName, newEmail, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('rep-list.html'))

    mycursor = connection.cursor()
    mycursor.execute("SELECT * FROM reps WHERE repID=%s", (id,))
    _, existingLName, existingFName, existingEmail = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('rep-update.html', id=id, existingFName=existingFName, existingLName=existingLName,existingEmail=existingEmail)


if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")