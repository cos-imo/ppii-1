from flask import *
import sqlite3
import hashlib

app = Flask(__name__)


DATABASE = 'project.db'

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

@app.route('/style.css')
def return_css():
    return render_template('static/css/style.css')


@app.route('/')
def main():
    r=get_db().cursor()
    r.execute("SELECT body FROM messages")
    return render_template('main.html',liste=r.fetchall())

@app.route("/inscription", methods=['GET','POST'])
def insc():
    msg = ''
    if request.method == 'POST' and request.form.get('first_name') and request.form.get('name'):
        print("ok")
        nom = request.form.get('first_name')
        prenom = request.form.get('name')
        mdp=bytes(request.form.get('password'),'utf-8')
        conn = get_db()
        cur = conn.cursor()
        mass=hashlib.sha256(mdp).hexdigest()
        cur.execute('INSERT INTO test VALUES(?,?)', (nom,mass))
        conn.commit()
        conn.close()
    else:
        print('please fill out the form')
    return render_template('inscription.html')
    
@app.route("/connexion", methods=['GET','POST'])
def connexion_page():
    msg=''
    if request.method == 'POST' and request.form.get('name') and request.form.get('password'):
         r = get_db().cursor()
         nom=request.form.get('name')
         r.execute("select pass from test where nom=?",(nom,))
         print(r.fetchall())

    return render_template("connexion.html")

app.run(host='localhost', port=5000)
