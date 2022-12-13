from flask import *
from flask import session
import sqlite3
import hashlib

app = Flask(__name__)

#####################################################################################################################
# DB gestion

DATABASE = 'project.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key="anystringhere"

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
    if request.method == 'POST' and request.form.get('first_name') and request.form.get('name') and request.form.get('password') and request.form.get('password')==request.form.get('password2'):
        rid=get_db().cursor()
        rid.execute("SELECT MAX(id) FROM utilisateurs")
        new_id=rid.fetchall()[0][0]+1
        nom = request.form.get('first_name')
        prenom = request.form.get('name')
        adresse_mail=request.form.get('email')
        num_de_tel=request.form.get('phone_number')
        mdp=bytes(request.form.get('password'),'utf-8')
        conn = get_db()
        cur = conn.cursor()
        mass=hashlib.sha256(mdp).hexdigest()
        if request.form.get('prod'):
            cur.execute('INSERT INTO utilisateurs VALUES(?,?,?,?,?,?,?)', (new_id,prenom,nom,adresse_mail,num_de_tel,mass,2))
        else:
            cur.execute('INSERT INTO utilisateurs VALUES(?,?,?,?,?,?,?)', (new_id,prenom,nom,adresse_mail,num_de_tel,mass,1))
        conn.commit()
        conn.close()
        session["id_utilisateur"]=new_id
        return redirect(url_for("renvoyer_dashboard_util"))
    elif request.method == 'POST' and request.form.get('first_name') and request.form.get('name') and request.form.get('password'):
        print("Passwords not matching")
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
         mdp=bytes(request.form.get('password'),'utf-8')
         mass=hashlib.sha256(mdp).hexdigest()
         r.execute("SELECT motdepasse FROM utilisateurs WHERE nom=?",(nom,))
         tuple=r.fetchall()
         if tuple[0][0]==mass:
            print("connected")
            return redirect(url_for("renvoyer_dashboard_util"))
         else:
            print("Connection failed")


    return render_template("connexion.html")

@app.route("/images/verger_1.jpg")
def renvoyer_bg():
    return send_file("ressources/images/verger_1.jpg")

@app.route("/images/<produit>")
def renvoyer_produit(produit):
    return send_file("ressources/icons/{}.png".format(produit))

@app.route("/images/about")
def renvoyer_about():
    return send_file("ressources/images/about_logo")

@app.route("/utilisateur/dashboard")
def renvoyer_dashboard_util():
    if "id_utilisateur" in session:
        id=session["id_utilisateur"]
        r=get_db().cursor()
        r.execute("SELECT * FROM commande WHERE id_util={}".format(id))
        print(r.fetchall())
        r2=get_db().cursor()
        r2.execute("SELECT photo FROM produits WHERE id={}".format(id))
        return render_template("dashboard_util.html", liste_commandes=r.fetchall(), photo=r2.fetchall())
    else:
        return render_template("connexion.html")

@app.route("/producteur/dashboard")
def renvoyer_prod(nom="Monsieur/Madame", id=3):
    r=get_db().cursor()
    r.execute("SELECT * FROM commande WHERE id={}".format(id))
    return render_template("dashboard_prod.html", nom=nom, commandes=r.fetchall())