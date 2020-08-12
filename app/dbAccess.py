from app import app
from flask import json, make_response
import pyodbc, csv
from io import StringIO

conn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
                      'SERVER=*;'
                      'DATABASE=*;'
                      'uid=*;'
                      'pwd=*;')
curData = []
curTable = ""
curColumns = []


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
    db=conn.cursor()
    print("Received column load request")
    sqlLoadColumnList = "SELECT * FROM [" + str(table) + "]"
    db.execute(sqlLoadColumnList)
    columnList = [str(column[0]) for column in db.description]
    #put table list into html for dropdown menu
    columnListString = ""
    for x in columnList:
        columnListString = columnListString + "<option value='" + x + "'>" + x + "</option>"
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
    try:
        result = ""
        db.execute(query)
        print(query)
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
