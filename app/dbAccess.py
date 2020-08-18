from app import app
#used to pass requests back to routes
from flask import json, make_response
#used to write csv
from io import StringIO
import csv
#used to connect to MSSQL DB
import pyodbc

#default db connection
conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                      'SERVER=*;'
                      'DATABASE=*;'
                      'uid=*;'
                      'pwd=*;')

#used to store data for csv
curData = []
curTable = ""
curColumns = []

#get list of dbs for db page
#params: none
#returns: a json object with the html string containing options for all databases in the server.
def loadDBList():
    #create db query object
    print("Received DB list load request")
    db = conn.cursor()
    #query for list of dbs
    #can add something like "WHERE name LIKE "%naming convention%" if you want to limit which servers are visible
    sqlLoadDBList = "SELECT name FROM master.sys.databases"
    db.execute(sqlLoadDBList)
    val = db.fetchall()
    dbList = [x[0] for x in val]
    #put db list into html for dropdown menu
    dbListString = ""
    for x in dbList:
        dbListString = dbListString + "<option value='" + x + "'>" + x + "</option>"
    db.close()
    print("Sending response with DBs")
    return json.dumps(dbListString)

#change db for query tool
#param: name of database, username, and password for login
#returns: nothing specifically but changes the instance of conn
def newDB(dbName, user, pwd):
    global conn
    conn.close()
    try:
        conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                              'SERVER=*;'
                              'DATABASE=' + str(dbName) + ';'
                              'uid=' + str(user) + ';'
                              'pwd=' + str(pwd) + ';')

    except:
        return "INVALID CREDENTIAL"

#used to find what table a query is searching
#param: query
#returns: table from query
def truncateQuery(query):
    global curTable
    curTable = query
    tableEndInd = query.index(' FROM')
    curTable = curTable[tableEndInd + 6:]
    try:
        curTable = curTable[:curTable.index(' WHERE')]
    except:
        print("No conditions specified")

    return curTable

#used to load list of tables from current db for visual query tool
#param: none
#returns: a json object with a string containing the html code for every table's name, where each name is in an <option> tag
def loadTableList():
    #create db query object
    print("Received table list load request")
    db = conn.cursor()
    sqlLoadTableList = "SELECT Distinct TABLE_NAME FROM information_schema.TABLES"
    db.execute(sqlLoadTableList)
    val = db.fetchall()
    tableList = [x[0] for x in val]
    #put table list into html for dropdown menu
    tableListString = ""
    for x in tableList:
        tableListString = tableListString + "<option value='" + x + "'>" + x + "</option>"
    db.close()
    print("Sending response with tables")
    return json.dumps(tableListString)

#used to fetch a list of columns for the currently selected table in the visual query tool
#param: a table
#returns: a json object with a string containing the html code for every column's name, where each column is in an <option> tag
def loadColumnList(table):
    db = conn.cursor()
    print("Received column load request")
    sqlLoadColumnList = "SELECT * FROM [" + str(table) + "]"
    db.execute(sqlLoadColumnList)
    columnList = [str(column[0]) for column in db.description]
    #put table list into html for dropdown menu
    columnListString = ""
    for x in columnList:
        columnListString = columnListString + \
            "<option value='" + x + "'>" + x + "</option>"
    db.close()
    print("Sending response with columns")
    return json.dumps(columnListString)


#create html for jinja based on query results
#param: db, an object holding the result of a query
#returns: a string with the html code for a table holding the results
def buildResultTableHTML(query):
    global curData, curColumns
    print("Received request to build result table")
    #db cursor tool
    db = conn.cursor()
    #try/catch is in place to catch an exception from the db executing the query
    try:
        result = ""
        db.execute(query)
        data = db.fetchall()
        curData = data
        #get column names
        columns = [str(column[0]) for column in db.description]
        curColumns = columns
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
        result = "<tr><td>Query failed</tr></tr>"

    db.close()
    print("Sending response with query result")
    return json.dumps(result)

#a function to export the currently viewed table to a csv file
#params: none explicitly, but it needs to be used after searching a table, or else the file will be empty
#returns: a flask response containing the csv table
def exportCSV():
    print("Request received to export CSV of results")
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(curColumns)
    cw.writerows(curData)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    print("Sending response with CSV export")
    return output
