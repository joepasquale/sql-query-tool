# sql-visual-tool
## Install
In order to run this application on your machine, you need to install Flask and set it up in a virtual environment in the same folder as the application. Because these differ based on what OS you use, please refer to the [official Flask documentation](https://flask.palletsprojects.com/en/1.1.x/installation/) for how to install this. I'd also suggest including /venv/ in your .gitignore if you're going to make changes to this.

Once you have the virtual environment set up, make sure that you run `pip install flask` and `pip install pyodbc`.

Afterwards, configure your server credentials in the dbAccess.py file, and you'll be good to go!
