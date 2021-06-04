from flask import Flask, render_template, request, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# app secret
app.secret_key = '6a79be6c56edb4fe2b946b5f'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'employee_data'
mysql = MySQL(app)

@app.route('/', methods =['GET', 'POST'])
def register():
	"Employee Register Form"
	msg = ''
	if request.method == 'POST' and 'name' in request.form and 'department' in request.form and 'email' in request.form :
		# Get values from form
		name = request.form['name']
		department = request.form['department']
		email = request.form['email']
		# Connect to MySQL db and execute queries to get and update data
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM employee WHERE email = % s', (email, ))
		employee_email = cursor.fetchone()
		# logic to verify form entries
		if not name or not department or not email:
			msg = 'Please fill out the complete form !'
		elif employee_email:
			msg = 'Employee already exists !'
		elif not re.match(r'^[A-Za-z ]+$', name):
			msg = 'name must contain only characters!'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif (department.upper()!='HR' and department.upper()!='ENG'):
			msg = "Department must be 'HR' or 'ENG' for now"
		else:
			cursor.execute('SELECT id FROM department WHERE name LIKE %s', [department.upper()])
			department_id = cursor.fetchone()
			cursor.execute('INSERT INTO employee (email, name , department_id) VALUES (%s, %s, %s)', (email, name, department_id["id"]))
			mysql.connection.commit()
			msg = 'You have successfully added employee details !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

if __name__ == "__main__":
    app.run(debug=True)
