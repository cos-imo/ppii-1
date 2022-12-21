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
        msg="Les mots de passe ne correspondent pas"
    return render_template('inscription.html',message=msg)


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
            r = get_db().cursor()
            r.execute("SELECT id FROM utilisateurs WHERE nom=?",(nom,))
            tuple=r.fetchall()[0][0]
            session["id_utilisateur"]=tuple
            rsession=get_db().cursor()
            rsession.execute("SELECT statut FROM utilisateurs WHERE id={}".format(session["id_utilisateur"]))
            session_type=rsession.fetchall()[0][0]
            if session_type==1:
                return redirect(url_for("renvoyer_dashboard_util"))
            elif session_type==2:
                return redirect(url_for("renvoyer_prod"))
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
        liste_commandes_tuple=r.fetchall()
        lst_photo=[]
        a_payer=0
        for element in liste_commandes_tuple:
            lst_photo.append(element[1])
            a_payer+=element[4]
        rphoto=get_db().cursor()
        photos=[]
        for e in lst_photo:
            rphoto.execute("SELECT photo from produits where id={}".format(e))
            val=rphoto.fetchall()
            photos.append(val[0][0])
        r2=get_db().cursor()
        r2.execute("SELECT photo FROM produits WHERE id={}".format(id))
        rnom=get_db().cursor()
        rnom.execute("SELECT Prenom FROM utilisateurs WHERE id={}".format(id))
        nom=rnom.fetchall()[0][0]
        return render_template("dashboard_util.html", nom=nom, liste_commandes=liste_commandes_tuple, photo=photos, total=a_payer)
    else:
        return render_template("connexion.html")

@app.route("/producteur/dashboard")
def renvoyer_prod():
    if "id_utilisateur" in session:
        id=session["id_utilisateur"]
        r=get_db().cursor()
        r.execute("SELECT * FROM commande WHERE id={}".format(id))
        rnom=get_db().cursor()
        rnom.execute("SELECT Prenom FROM utilisateurs WHERE id={}".format(id))
        nom=rnom.fetchall()[0][0]
        rliste_produits=get_db().cursor()
        rliste_produits.execute("SELECT * FROM produits WHERE producteur={}".format(session["id_utilisateur"]))
        tuple=rliste_produits.fetchall()
        print(tuple)
        return render_template("dashboard_prod.html", nom=nom, commandes=r.fetchall(), liste_produits=tuple)
    else:
        return(redirect(url_for("connexion")))