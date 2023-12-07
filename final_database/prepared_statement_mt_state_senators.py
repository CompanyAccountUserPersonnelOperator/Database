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


@app.route('/bill-list.html', methods=['GET'])
def showBills():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    mycursor = connection.cursor()
    newName = request.args.get('name')
    newCategory = request.args.get('category')
    newDate = request.args.get('date')
    if newName is not None and newCategory is not None and newDate is not None:
        mycursor.execute("INSERT INTO bills (billname, category, date) values (%s, %s, %s)", (newName, newCategory, newDate))
        connection.commit()
    elif request.args.get('delete') == 'true':
        deleteID = request.args.get('id')
        mycursor.execute("DELETE FROM bills WHERE billID=%s", (deleteID,))
        connection.commit()

    mycursor.execute("SELECT billID, billname, category, date FROM bills")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('bill-list.html', collection=myresult)


@app.route('/bill-vote-list.html', methods=['GET'])
def showVote():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    mycursor = connection.cursor()
    Bid = request.args.get('bID')
    mycursor.execute("""SELECT bills.billname, senate_votes.vote, bills.date FROM bills
    JOIN senate_votes ON bills.billID = senate_votes.billID
    JOIN senators ON senators.repID = senate_votes.repID
    WHERE senators.repID = %s""", (Bid,))
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('bill-vote-list.html',
    collection=myresult)


@app.route('/sen-vote-list.html', methods=['GET'])
def showSen():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    mycursor = connection.cursor()
    senID = request.args.get('SenID')
    mycursor.execute("""SELECT senators.firstname, senators.lastname, senators.party, bills.billname, senate_votes.vote
    FROM senators
    JOIN senate_votes ON senators.repID = senate_votes.repID
    JOIN bills ON bills.billID = senate_votes.billID
    WHERE bills.billID = %s""", (senID,))
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('sen-vote-list.html',
    collection=myresult)


@app.route("/vote-list.html", methods=['GET'])
def addVote():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    mycursor = connection.cursor()
    senateid = request.args.get('senator')
    billid = request.args.get('bill')
    vote = request.args.get('vote')
    if senateid is not None and billid is not None:
        mycursor.execute("UPDATE senate_votes SET vote=%s WHERE repID=%s AND billID=%s", (vote, senateid, billid))
        mycursor.close()
        connection.commit()
        connection.close()
    return render_template("vote-list.html")


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


@app.route("/updateBill")
def updateBill():
    with open('secrets.json', 'r') as secretsFile:
        creds = json.load(secretsFile)['mysqlCredentials']
    connection = mysql.connector.connect(**creds)

    id = request.args.get('id')
    newName = request.args.get('name')
    newCategory = request.args.get('category')
    newDate = request.args.get('date')
    if id is None:
        return "Error, ID not specified"
    elif newName is not None and newCategory is not None:
        mycursor = connection.cursor()
        mycursor.execute("UPDATE bills SET billname=%s, category=%s, date=%s WHERE billID=%s", (newName, newCategory, newDate, id))
        mycursor.close()
        connection.commit()
        connection.close()
        return redirect(url_for('showBills'))

    mycursor = connection.cursor()
    mycursor.execute("SELECT billID, billname, category, date, FROM bills WHERE billID=%s", (id,))
    id, existingName, existingCategory, existingDate = mycursor.fetchone()
    mycursor.close()
    connection.close()
    return render_template('bill-update.html', id=id, existingName=existingName, existingCategory=existingCategory, existingDate=existingDate)

 
if __name__ == '__main__':
    app.run(port=8000, host="0.0.0.0")