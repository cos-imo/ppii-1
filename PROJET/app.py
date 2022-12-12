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




#Renders insciption page

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


#####################################################################################################################

#Renders connection page


@app.route("/connexion", methods=['GET','POST'])
def connexion_page():
    msg=''
    if request.method == 'POST' and request.form.get('name') and request.form.get('password'):
         r = get_db().cursor()
         nom=request.form.get('name')
         r.execute("SELECT pass FROM test WHERE nom=?",(nom,))
         print(r.fetchall())

    return render_template("connexion.html")

@app.route("/images/verger_1.jpg")
def renvoyer_bg():
    return send_file("ressources/images/verger_1.jpg")

@app.route("/images/about")
def renvoyer_about():
    return send_file("ressources/images/about_logo")

@app.route("/utilisateur/dashboard")
def renvoyer_dashboard_util(id =3):
    r=get_db().cursor()
    r.execute("SELECT * FROM commande WHERE id={}".format(id))
    r2=get_db().cursor()
    r2.execute("SELECT photo FROM produits WHERE id={}".format(id))
    print(r2.fetchall())
    return render_template("dashboard_util.html", liste_commandes=r.fetchall(), photo=r2.fetchall())

@app.route("/producteur/dashboard")
def renvoyer_prod(nom="Monsieur/Madame", id=3):
    r=get_db().cursor()
    r.execute("SELECT * FROM commande WHERE id={}".format(id))
    return render_template("dashboard_prod.html", nom=nom, commandes=r.fetchall())