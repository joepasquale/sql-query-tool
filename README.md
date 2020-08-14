# sql-visual-tool
## Install
In order to run this application on your machine, you need to install Flask and set it up in a virtual environment in the same folder as the application. Because these differ based on what OS you use, please refer to the [official Flask documentation](https://flask.palletsprojects.com/en/1.1.x/installation/) for how to install this. I'd also suggest including /venv/ in your .gitignore if you're going to make changes to this.

Once you have the virtual environment set up, make sure that you run `pip install flask` and `pip install pyodbc`.

Afterwards, configure your server credentials in the dbAccess.py file, and you'll be good to go!

## Known Issues
This doesn't really work without a lot of poking and prodding on Mac, thanks to the pyodbc module which is responsible for making all the SQL queries; Macs don't typically come with the correct ODBC drivers to connect to the database. However, the author of the pyodbc module wrote [these instructions](https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Mac-OSX) for anyone who would like to configure it. 

## Screenshots

Query page
![Query Page](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-1.PNG)

Query page w/ results of query with one condition
![One Condition](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-2.PNG)

Query page w/ results of query with multiple conditions and sort preference
![Multiple Conditions and Sort](https://github.com/joepasquale/sql-query-tool/blob/master/app/static/img/sql-q-tool-3.PNG)
