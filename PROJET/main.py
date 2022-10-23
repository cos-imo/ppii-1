from flask import *
import sqlite3

app = Flask(__name__)


from flask import Flask, render_template, g, request
import sqlite3
app = Flask(__name__)

DATABASE = 'project.db'

app = Flask(__name__)

def get_db():
            
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/students', methods=['GET','POST'])
def all_students():
    r = get_db().cursor()
    r.execute("select lien,nom,nb_utilisation from liens")
    return render_template('page_test.html',liste=r.fetchall())

@app.route('/style.css')
def return_css():
    return render_template('static/css/style.css')


@app.route('/')
def main():
    r=get_db().cursor()
    r.execute("SELECT body FROM messages")
    return render_template('main.html',liste=r.fetchall())



app.run(host='localhost', port=5000)
