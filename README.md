# sql-visual-tool
## Install
In order to run this application on your machine, you need to install Flask and set it up in a virtual environment in the same folder as the application. Because these differ based on what OS you use, please refer to the [official Flask documentation](https://flask.palletsprojects.com/en/1.1.x/installation/) for how to install this. I'd also suggest including /venv/ in your .gitignore if you're going to make changes to this.

Once you have the virtual environment set up, make sure that you run `pip install flask` and `pip install pyodbc`. These are the required package installs for Flask and its dependents (the web server framework) and pyodbc, a python package used to access MSSQL servers.

Afterwards, configure your server credentials in the dbAccess.py file. The fields that need to be replaced come with `*` in place of the server, database, username, and password. After these have been saved in the file, you'll be good to go! 

If you continue getting errors at this point, you may have put in an invalid server credential, but can otherwise try switching the OBDC driver. You can find which drivers you have installed by running a python file within the virtual environment that shows the value of `pyodbc.drivers()`.

## Known Issues
This doesn't really work without a lot of poking and prodding on Mac, thanks to the pyodbc module which is responsible for making all the SQL queries; Macs don't typically come with the correct ODBC drivers to connect to the database. However, the author of the pyodbc module wrote [these instructions](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX) for anyone who would like to configure their machine with the correct Windows ODBC drivers.

If the table is too big, it pops off the page. In the meantime, exporting a file to a csv will let you see the resulting data in its entirety.

## Screenshots
Database Select page
![DB Page](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-4.PNG)

Query page
![Query Page](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-1.PNG)

Query page w/ results of query with one condition
![One Condition](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-2.PNG)

Query page w/ results of query with multiple conditions and sort preference
![Multiple Conditions and Sort](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-3.PNG)
