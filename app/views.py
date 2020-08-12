from app import app
from flask import render_template, request, redirect, json
from app import dbAccess
import csv

curData = []
curTable = ""
curColumns = []

#index
@app.route('/')
def index():
    return render_template("public/index.html")

#query landing page
@app.route('/query', methods=["GET"])
def query():
    tableListString = json.loads(dbAccess.loadTableList())
    return render_template("public/query.html", tableListString=tableListString)

@app.route('/query/fetch-columns', methods=["POST"])
def fetchC():
    table = request.form['table']
    tableListString = json.loads(dbAccess.loadTableList())
    columnListString = dbAccess.loadColumnList(table)
    columnListString = json.loads(columnListString)
    return render_template("public/query.html", columnListString=columnListString, tableListString=tableListString)

#loads sql query
@app.route('/query/load-sql-query', methods=["POST"])
def sqlLoadQuery():
    global curTable
    #list of tables in case of new query
    tableListString = json.loads(dbAccess.loadTableList())
    #store query from sql line if possible
    query = request.form["sql-query"]
    #get table name from query
    curTable = query
    tableEndInd = curTable.index(' FROM')
    curTable = curTable[tableEndInd + 6:]
    try:
        curTable = curTable[:curTable.index(' WHERE')]
    except:
        print("No conditions specified")

    result = json.loads(dbAccess.buildResultTableHTML(query))
    return render_template("public/query.html", result=result, tableListString=tableListString, curTable=curTable)

#loads query from using tool
@app.route('/query/load-tool-query', methods=["POST"])
def loadToolQuery():
    global curTable
    tableListString = json.loads(dbAccess.loadTableList())
    query = "SELECT " + request.form["attr1-select"] + " FROM " + request.form["table-select"]
    result = json.loads(dbAccess.buildResultTableHTML(query))
    curTable = request.form["table-select"]
    return render_template("public/query.html", result=result, tableListString=tableListString, curTable=curTable)

#exports current table to csv
@app.route('/query/download-csv')
def post():
    return dbAccess.exportCSV()
