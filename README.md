# SQL Query Tool
## Install
In order to run this application on your machine, you need to install Flask and set it up in a virtual environment in the same folder as the application. Because installing the virtual environment differs based on what OS you use, please refer to the [official Flask documentation](https://flask.palletsprojects.com/en/1.1.x/installation/) for how to install it. I'd also suggest including /venv/ in your .gitignore if you're going to clone/make changes to this.

Once you have the virtual environment set up, make sure that you run `pip install flask` and `pip install pyodbc`. These are the required package installs for Flask (the web server framework) and its dependents and pyodbc (a python package used to access MSSQL servers).

Afterwards, configure your server credentials in the dbAccess.py file. The fields that need to be replaced come with `*` in place of the server, database, username, and password. After these have been saved in the file, you'll be good to go! 

If you continue getting errors at this point, you may have put in an invalid server credential, but can otherwise try switching the OBDC driver. You can find which drivers you have installed by running a python file within the virtual environment that shows the value of `pyodbc.drivers()`.

## Known Issues
This doesn't really work without a lot of poking and prodding on Mac, thanks to the pyodbc module which is responsible for making all the SQL queries; Macs don't typically come with the correct ODBC drivers to connect to the database. However, the author of the pyodbc module wrote [these instructions](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX) for anyone who would like to configure their machine with the correct Windows ODBC drivers.

If the table is too big, it pops off the page. In the meantime, exporting a file to a csv will let you see the resulting data in its entirety.

## Intended Use
This is a web application that is designed to allow users who are not familiar with SQL to make queries of a database. If you plan on utilizing this application for many people to use at once, it's important to make sure that users all have logins to the targeted SQL server, as too many people trying to access queries at once may create issues if they are all coming from one account. If you plan on using this program on your local to access a server on your network, your biggest bottleneck will likely be how quickly your server can execute queries.

## Screenshots
Database Select page
![DB Page](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-4.PNG)

Query page
![Query Page](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-1.PNG)

Query page w/ results of SQL query
![SQL Query](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-6.PNG)

Query page w/ results of visual query with no conditions
![No Condition](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-2.PNG)

Query page w/ results of visual query with one condition
![One Condition](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-3.PNG)

Query page w/ results of visual query with multiple conditions and sort
![Multiple Conditions](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-5.PNG)


## Use Notice & Agreement
This is open source software. I choose to publish this tool for my own personal use, and at no cost to users. I have no problem with any users modifying the source code for their own use; however, the work published in this repository is my intellectual property, and should not be claimed otherwise. I am not liable for any loss that is incurred in any fashion as a result of using this tool. As always, please be responsible when handling sensitive and/or valuable data.
