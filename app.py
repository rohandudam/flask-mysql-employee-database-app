from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = '6a79be6c56edb4fe2b946b5f'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'employee_data'

mysql = MySQL(app)

"""
@app.route('/', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
		name = request.form['name']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE name = % s AND password = % s', (name, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['name'] = account['name']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect name / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('name', None)
	return redirect(url_for('login'))
"""

@app.route('/', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'name' in request.form and 'department' in request.form and 'email' in request.form :
		name = request.form['name']
		department = request.form['department']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM employee WHERE email = % s', (email, ))
		employee_email = cursor.fetchone()
		if employee_email:
			msg = 'Employee already exists !'
		elif not name or not department or not email:
			msg = 'Please fill out the form !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', name):
			msg = 'name must contain only characters and numbers !'
		elif (department!='HR' and department!='ENG'):
			msg = "Department must be 'HR' or 'ENG' for now"
		else:
			cursor.execute('SELECT id FROM department WHERE name LIKE %s', [department])
			department_id = cursor.fetchone()
			cursor.execute('INSERT INTO employee (email, name , department_id) VALUES (%s, %s, %s)', (email, name, department_id["id"]))
			mysql.connection.commit()
			msg = 'You have successfully added employee details !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

if __name__ == "__main__":
    app.run(debug=True)
