from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, send, emit
from uuid import uuid4
from random import choice, randint
import string, sqlite3

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SECRET_KEY"] = uuid4().hex
app.config["DEBUG"] = True;
sio = SocketIO(app)
cswitch = True;

def getcode():
	return ''.join(choice(string.ascii_lowercase) for x in range(5)) + str(randint(10, 90))

def getconn():
	return sqlite3.connect('rooms.db')

def orderdb(query, update):
	inst = getconn()
	res = inst.execute(query)
	if (update):	
		inst.commit();
	inst.close()
	return res

@app.route('/', methods = ['GET', 'POST'])
def main():
	global cswitch;
	if (session.get('username')):
		return redirect('/home')
	cswitch = True;
	return render_template("index.html", go = False)

@app.route('/go', methods = ['POST'])
def go():
	session['username'] = request.form['uname']
	return render_template("index.html", go = True, username = session['username'])

@app.route('/home', methods = ['GET'])
def home():
	if (not session.get('username')):
		return redirect('/')
	global cswitch; cswitch = True;
	return render_template('index.html', go = True, username = session['username'])

@app.route('/changename', methods = ['GET', 'POST'])
def changename():
	return render_template("index.html", go = False)

@app.route('/join', methods = ['POST'])
def join():
	global cswitch; cswitch = False;
	attempt = request.form['rcode']
	inst = getconn()
	res = inst.execute('SELECT * FROM rooms WHERE code = "%s"' % attempt)
	for row in res:
		if (row[0] == attempt):
			inst.close();
			session['code'] = attempt
			return redirect('/chat')
	inst.close();
	return render_template("errors.html", err = "No such room exists.")

@app.route('/chat')
def chat():
	global cswitch
	if (not session.get('username')):
		return redirect('/')
	if (cswitch):
		session['code'] = getcode(); cswitch = False
		orderdb("INSERT INTO rooms values('" + session['code'] + "')", True)
	return render_template("msgpage.html", code = session['code'])

@sio.on('msg')
def handlemsg(msg):
	if (session.get('code')):
		print("Received: " + str(msg));
		if ('id = "status"' in msg):
			sep = " "
		else:
			sep = ": "
		emit('declarecode', session['code'])
		emit('msg', session['username'] + sep + msg + "<a hidden>" + session['code'] 
			+ "</a>", broadcast = True)

@sio.on('disc')
def showdisc():
	print("Disconnect found.")
	if (session.get('code')):
		emit('msg', session['username'] + " disconnected. <a hidden>" 
			+ session['code'] + "</a>", broadcast = True)

if __name__ == "__main__":
	orderdb('CREATE TABLE IF NOT EXISTS "rooms" (code)', True)
	sio.run(app)
