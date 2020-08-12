from app import app
from flask import render_template, request, redirect, make_response
import pyodbc
import csv
from io import StringIO

conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                      'SERVER=*;'
                      'DATABASE=*;'
                      'uid=*;'
                      'pwd=*;')

curData = ""

#used to load list of tables from current db for visual query tool
#param: none
#returns: a string with the html code for every table's name, where each name is in an <option> tag
def loadTableList():
    #create db query object
    db = conn.cursor()
    #load table list
    sqlLoadTableList = "SELECT Distinct TABLE_NAME FROM information_schema.TABLES"
    db.execute(sqlLoadTableList)
    val = db.fetchall()
    tableList = [x[0] for x in val]
    #put table list into html for dropdown menu
    tableListString = ""
    for x in tableList:
        tableListString = tableListString + "<option value='" + x + "'>" + x + "</option>"
    db.close()
    return tableListString

#create html for jinja based on query results
#param: db, an object holding the result of a query
#returns: a string with the html code for a table holding the results
def buildResultTableHTML(query):
    global curData
    if "SELECT" not in query:
        return "<tr>Query could not be completed</tr>"

    db = conn.cursor()
    try:
        db.execute(query)
        result = ""
        data = db.fetchall()
        curData = data
        #get column names
        columns = [column[0] for column in db.description]
        result = result + "<tr>"
        for col in columns:
            result = result + "<th>" + str(col) + "</th>"
        result = result + "</tr>"
        #put results of query into html table
        for row in data:
            result = result + "<tr>"
            for col in row:
                result = result + "<td>" + str(col) + "</td>"
            result = result + "</tr>"

    except:
        result = "<tr>Query could not be completed</tr>"

    db.close()
    return result

#index
@app.route('/')
def index():
    return render_template("public/index.html")

#query landing page
@app.route('/query', methods=["GET"])
def query():
    tableListString = loadTableList()
    return render_template("public/query.html", tableListString=tableListString)

#loads sql query
@app.route('/query/load-sql-query', methods=["POST"])
def sqlLoadQuery():
    #list of tables in case of new query
    tableListString = loadTableList()
    #store query from sql line if possible
    query = request.form["sql-query"]
    result = buildResultTableHTML(query)
    return render_template("public/query.html", result=result, tableListString=tableListString)

#loads query from using tool
@app.route('/query/load-tool-query', methods=["POST"])
def loadToolQuery():
    tableListString = loadTableList()
    query = "FROM " + request.form["table-select"] + " "
    query = "SELECT " + request.form["attr1-select"] + " " + query
    result = buildResultTableHTML(query)
    return render_template("public/query.html", result=result, tableListString=tableListString)

#exports current table to csv
@app.route('/query/download-csv')
def post():
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(curData)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
