from flask import Flask

import MySQLdb
import gc
#Garbage collector
app = Flask(__name__)

app.debug = True

# database connection method
def connection():
	conn = MySQLdb.connect(
		host = "localhost",
		user = "flaskdb",
		passwd = "flaskdb",
		db = "flask_db"
		)

	c = conn.cursor()
	return c, conn

c, con = connection()

# default routing provies reference to all routes
@app.route("/")
def hello():
	return 'Please follow links to make use of MySQL Database: <br>' \
		'1. /get/ - get all users <br>' \
		'2. /username/ - get particular user <br>' \
		'3. /delete/username/ - delete user with username <br>' \
		'4. /insert/username/firstname/lastname/ - insert user <br>' \
		'5. /lastname/lastname/ - list the users with lastname <br>' \

# getting all registered user data
# e.g. http://localhost:5000/get/
@app.route("/get/")
def get_data():
	c.execute("SELECT * FROM users")
	users = c.fetchall()
	data = 'Name of Users: <br>'
	for user in users:
		data = data + user[1] + ': ' \
		+ user[2] + ' ' + user[3] + '<br>'

	gc.collect()
	return data

# insert user with username, firstname and password
# e.g. http://localhost:5000/insert/jeevan/Jeevan/Pant/
@app.route("/insert/")
@app.route("/insert/<username>/<firstname>/<lastname>/")
def insert_data(username=None, firstname=None, lastname=None):
	if username != None and firstname != None and lastname != None:
		c.execute('INSERT INTO users (username, firstname, lastname) VALUES(%s, %s, %s)',[
			username,
			firstname, 
			lastname
			])
        	
		con.commit()
		gc.collect()
		return 'Data inserted successfully: ' +  username + ', ' \
			+ firstname + ' ' + lastname
	else:
		return 'Data insufficient. Please try again!'

# delete user
# e.g. http://localhost:5000/delete/jeevan/
@app.route("/delete/")
@app.route("/delete/<username>/")
def delete_data(username=None):
	if username != None:
		try:
			c.execute("SELECT * FROM users WHERE username=%s", [username,])
			user = c.fetchone()

			c.execute("DELETE FROM users WHERE username=%s", [
			username
			])
			con.commit()
			gc.collect()
			return 'Data delected successfully with useraname: ' +  username
		except:
			return "User couldn't be found"
		else:
			return 'Provide data to delete. Please try again!'

# get specific user
# e.g. http://localhost:5000/jeevan/
@app.route("/<username>/")
def users(username):
	try:
		c.execute("SELECT * FROM users WHERE username=%s", [username])
		user = c.fetchone()
		gc.collect()
		return user[2] + ' ' + user[3]
	except:
		return "User couldn't be found"

# getting all registered user by lastname
# e.g. http://localhost:5000/lastname/
@app.route("/lastname")
@app.route("/lastname/<lastname>/")
def list_data(lastname=None):
	if lastname != None:
		try:
			c.execute("SELECT * FROM users WHERE lastname=%s", [lastname])
			users = c.fetchall()

			data = 'Name of Users: <br>'
			for user in users:
				data = data + user[1] + ': ' \
				+ user[2] + ' ' + user[3] + '<br>'

			gc.collect()
			return 'List lastname user: ' + data

		except:
        	        return "User couldn't be found"
        		#else:
        	       	#return 'Provide lastname. Please try again!'

if __name__ == "__main__":
	app.run()
