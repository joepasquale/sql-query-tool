from app import app, dbAccess
from flask import json, redirect, render_template, url_for, request, make_response

curData = []
curTable = ""
curColumns = []
tables = json.loads(dbAccess.loadTableList())
dbList = json.loads(dbAccess.loadDBList())

#landing page
@app.route('/')
def dbSelect():
    return render_template("public/dbSelect.html", dbListString=dbList)

#
@app.route('/loadDB', methods=["POST"])
def loadDb():
    global tables
    database = request.form["dbSelect"]
    dbAccess.newDB(database)
    tables = json.loads(dbAccess.loadTableList())
    return redirect(url_for('query'), tables)

#index
@app.route('/query')
def query():
    return render_template("public/query.html", tableListString=tables)

#load columns for specific table
@app.route('/query/cols', methods=["POST"])
def queryLoad():
    return dbAccess.loadColumnList(request.form['table'])

#loads result onto page
@app.route('/query/result', methods=["POST"])
def result():
    query = request.form["query"]
    print("Query: "+ str(query))
    output = json.loads(dbAccess.buildResultTableHTML(query))
    print("Received output from dbAccess: " + output[:32])
    return output


#exports current table to csv
@app.route('/query/download-csv')
def post():
    return dbAccess.exportCSV()
