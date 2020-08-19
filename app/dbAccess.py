from app import app
#used to pass requests back to routes
from flask import json, make_response
#used to write csv
from io import StringIO
import csv
#used to connect to MSSQL DB
import pyodbc

#default db connection
conn = ""
userConn = ""
#used to store data for csv
curData = []
curTable = ""
curColumns = []

#get list of dbs for db page
#safety: safe from injection, as the function will throw an exception if an sql statement is inserted
#params: none
#returns: a json object with the html string containing options for all databases in the server.
def loadDBList():
    #connect to db to fetch master list
    global conn
    conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                      'SERVER=*;'
                      'DATABASE=*;'
                      'uid=*;'
                      'pwd=*;')
    #create db query object
    print("Received DB list load request")
    db = conn.cursor()
    #query for list of dbs
    #add something like "WHERE name LIKE "%naming convention%" if you want to limit which servers are visible
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

#change db for query tool.
#safety: safe from injection, as the function will throw an exception if an sql statement is inserted
#param: name of database, username, and password for login
#returns: nothing specifically but changes the instance of conn
def newDB(dbName, user, pwd):
    global userConn
    #close existing db connection
    if(userConn != ""):
        userConn.close()
        
    try:
        userConn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                                  'SERVER=*;'
                                  'DATABASE=' + str(dbName) + ';'
                                  'uid=' + str(user) + ';'
                                  'pwd=' + str(pwd) + ';')

    except:
        return "INVALID CREDENTIAL"

#used to check for keywords that indicate actions of an sql injection. there's no need for any of these keywords, as the tool is intended to be read-only
#param: a string containing a query or table
#return: true if the statement passed in contains a flagged word, false otherwise
#example: i try and enter a value into the value section that drops the current table. this is called before the query is executed, and will prevent it from executing
def injectionAlert(tableString):
    if("INSERT" in tableString):
        return True
    elif("DROP" in tableString):
        return True
    elif("DELETE" in tableString):
        return True
    elif("UPDATE" in tableString):
        return True
    elif("ALTER" in tableString):
        return True
    elif("CREATE" in tableString):
        return True
    else:
        return False

#used to load list of tables from current db for visual query tool
#safety: safe from injection, does not take any input from the user.
#param: none
#returns: a json object with a string containing the html code for every table's name, where each name is in an <option> tag
def loadTableList():
    #create db query object
    print("Received table list load request")
    db = conn.cursor()
    #execute query that fetches all tables from db
    sqlLoadTableList = "SELECT Distinct TABLE_NAME FROM information_schema.TABLES"
    db.execute(sqlLoadTableList)
    val = db.fetchall()
    #put table list into html format for dropdown menu
    tableList = [x[0] for x in val]
    tableListString = ""
    for x in tableList:
        tableListString = tableListString + "<option value='" + x + "'>" + x + "</option>"
    db.close()
    print("Sending response with tables")
    return json.dumps(tableListString)

#used to fetch a list of columns for the currently selected table in the visual query tool
#safety: safe from injection, does not rely on user text input for feedback from the server, explicit checking
#param: a table
#returns: a json object with a string containing the html code for every column's name, where each column is in an <option> tag
def loadColumnList(table):
    db = conn.cursor()
    tablePar = str(table)
    #sql injection protection
    if(injectionAlert(tablePar) or ("SELECT" in table)):
        return json.dumps("<option>SQL Injection Detected</option>")
    sqlLoadColumnList = "SELECT * FROM ["+tablePar+"]"
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
#safety: safe at this level, explicit query checking
#param: query, an object holding the result of a query
#returns: a string with the html code for a table holding the results
def buildResultTableHTML(query):
    global curData, curColumns
    print("Received request to build result table")
    #sql injection protection
    if(injectionAlert(query)):
        result = "<tr><td>Query denied - contains keywords that signal an SQL Injection</tr></tr>"
        return json.dumps(result)
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
#safety: does not execute sql.
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
