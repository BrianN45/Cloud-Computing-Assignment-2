from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)

# SQLite setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,    
    address TEXT NOT NULL,
	email TEXT NOT NULL
)''')
conn.commit()
conn.close()

@app.route('/')
def index():
	return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
		username = request.form['username']
		password = request.form['password']
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		email = request.form['email']
		address = request.form['address']

		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		c.execute("INSERT INTO users (username, password, firstname, lastname, email, address) VALUES (?, ?, ?, ?, ?, ?)",
						  (username, password, firstname, lastname, email, address))
		conn.commit()
		conn.close()

		return redirect(url_for('profile', username=username))

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
	username = request.form['username']
	password = request.form['password']
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
	user = c.fetchone()
	conn.close()

	if user:
		return redirect(url_for('profile', username=username))
	else:
	    return render_template('login.html', error='Incorrect username or password.')

@app.route('/upload-text', methods=['POST'])
def upload_text():
	uploaded_file = request.files.get('text_file')

	if not uploaded_file or not uploaded_file.filename:
		return render_template('login.html', upload_error='Please choose a text file.')

	if not uploaded_file.filename.lower().endswith('.txt'):
		return render_template('login.html', upload_error='Only .txt files are accepted.')

	text = uploaded_file.read().decode('utf-8', errors='replace')
	stored_filename = secure_filename(uploaded_file.filename)
	if not stored_filename:
		return render_template('login.html', upload_error='Please choose a valid file name.')

	stored_path = os.path.join(UPLOAD_FOLDER, stored_filename)

	with open(stored_path, 'w', encoding='utf-8') as text_file:
		text_file.write(text)

	return render_template(
		'login.html',
		word_count=len(text.split()),
		download_url=url_for('download_text', filename=stored_filename)
	)

@app.route('/download-text/<filename>')
def download_text(filename):
	return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/profile/<username>')
def profile(username):
		conn = sqlite3.connect(DB_PATH)
		c = conn.cursor()
		c.execute("SELECT * FROM users WHERE username=?", (username,))
		user = c.fetchone()
		conn.close()

		return render_template('profile.html', user=user)
	
if __name__ == '__main__':
	app.run(debug=True)