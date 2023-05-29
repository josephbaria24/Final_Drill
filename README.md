# Installation Procedures for Flask REST API with MySQL Database


1. **Prerequisites**

   Before starting the installation, make sure you have the following prerequisites:
   
   - Python (version 3.6 or above) installed on your system.
   - pip (Python package installer) installed. It usually comes with Python installation.
   - MySQL server installed and running.
   
2. **Create a Virtual Environment** (optional but recommended)

   It's best practice to create a virtual environment to keep your project dependencies isolated. Open your terminal or command prompt and execute the following commands:
   
   ```bash
   # Install virtualenv if not already installed
   $ pip install virtualenv
   
   # Create a virtual environment
   $ virtualenv myenv
   
   # Change directory to virtual environment
   $ cd myenv
   
   # Activate the virtual environment
   $ /Scripts/activate
   ```
   
3. **Install Flask and Required Dependencies**

   In your terminal or command prompt, execute the following command to install Flask and required dependencies:
   
   ```bash
   $ pip install flask-mysqldb
   $ pip install flask
   ```

4. **Create a Flask Application**

   Create a new file, for example, `app.py`, and open it in a text editor. Add the following code to create a basic Flask application:
   
   ```python
   from flask import Flask
   
   app = Flask(__name__)
   
   @app.route('/')
   def hello_world():
       return '<h1>Hello, World!</h1>'
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```
   
5. **Connect to MySQL Database**

   In your Flask application code, import the `flask_mysqldb` module and establish a connection to your MySQL database. Modify your `app.py` file as follows:
   
   ```python
   from flask import Flask
   import flask_mysqldb
   
   app = Flask(__name__)
   
   # MySQL configuration
   app.config["MYSQL_HOST"] = "mysql_host"
   app.config["MYSQL_USER"] =  "mysql_name"
   app.config["MYSQL_PASSWORD"] =  "mysql_password"
   app.config["MYSQL_DB"] =  "mysql_database"
   app.config["MYSQL_CURSORCLASS"] =  "DictCursor"

   mysql = MySQL(app)
   
   # Establish MySQL connection
   def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

   )
   
   @app.route('/')
   def hello_world():
       return 'Hello, World!'
   
   if __name__ == '__main__':
       app.run(debug=True)
   ```

   Make sure to replace `'mysql_username'`, `'mysql_password'`, and `'mysql_database'` with your actual MySQL credentials.

6. **Start the Flask Development Server**

   In your terminal or command prompt, navigate to the directory containing your `app.py` file. Run the following command to start the Flask development server:
   
   ```bash
   $ python app.py
   ```
   
   You should see output similar to the following:
   
   ```
   * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
   ```

   This means your Flask application is running successfully.

7. **Test the API Endpoint**

   Open a web browser and visit `http://127.0.0.1:5000/`. You should see the "Hello, World!" message displayed.

   You have now successfully installed Flask REST API with a MySQL database.

Remember to update the MySQL configuration and adapt the code to fit your specific needs. This guide provides a basic setup to get you started.
