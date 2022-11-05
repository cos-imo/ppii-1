from flask import *
import sqlite3
import hashlib

app = Flask(__name__)

#####################################################################################################################
# DB gestion

DATABASE = 'project.db'

def get_db():
            
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Cut the connection to the database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#####################################################################################################################

#what's its use?

@app.route('/style.css')
def return_css():
    return render_template('static/css/style.css')

#####################################################################################################################

# Renders main page

@app.route('/')
def main():
    r=get_db().cursor()
    r.execute("SELECT body FROM messages")
    return render_template('main.html',liste=r.fetchall())


#####################################################################################################################

<<<<<<< HEAD
<<<<<<< HEAD
app.run(host='localhost', port=5000)


#test 12
=======
=======
>>>>>>> origin/cosimo
#Renders insciption page

@app.route("/inscription", methods=['GET','POST'])
def insc():
    msg = '' #why?
    if request.method == 'POST' and request.form.get('first_name') and request.form.get('name'):
        print("ok")
        nom = request.form.get('first_name')
        prenom = request.form.get('name')
        mdp=bytes(request.form.get('password'),'utf-8')
        conn = get_db()
        cur = conn.cursor()
        mass=hashlib.sha256(mdp).hexdigest() #does that mean that we somehow get the password unprotected? security problems?
        cur.execute('INSERT INTO test VALUES(?,?)', (nom,mass))
        conn.commit()
        conn.close()
    else:
        print('please fill out the form')
    return render_template('inscription.html')


#####################################################################################################################

#Renders connection page


@app.route("/connexion", methods=['GET','POST'])
def connexion_page():
    msg='' #again why?
    if request.method == 'POST' and request.form.get('name') and request.form.get('password'):  #to avoid getting None values I suppose?
         r = get_db().cursor()
         nom=request.form.get('name')
         r.execute("SELECT pass FROM test WHERE nom=?",(nom,))
         print(r.fetchall())

    return render_template("connexion.html")

app.run(host='localhost', port=5000)
<<<<<<< HEAD
>>>>>>> origin/cosimo
=======
>>>>>>> origin/cosimo
