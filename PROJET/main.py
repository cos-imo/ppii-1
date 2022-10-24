from flask import *
import sqlite3

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
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO test VALUES(?,?)', (nom,prenom))
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
         r.execute("select pass from test where nom=(?)",request.form.get('name'))
         print(liste=r.fetchall())

    return render_template("connexion.html")

app.run(host='localhost', port=5000)
