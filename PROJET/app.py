"""
AVANT DE CODER:
-> Obligatoire, tout le monde doit utiliser vscode pour que les json de formattage de code fonctionnent
-> installer l'extension autopep8 pour pas avoir un git diff lisible
-> installer l'exentsion prettier pour avoir un code lisible
-> mettre des rangée de # pour séparer les root
-> commentez votre code pour le rendre lisisble par les autres
-> utilisez des noms de variables explicites éventuellement réutiliser le même nom si celà désigne la même chose
-> ne vous inquiétez pas à la sauvegarde le code doit s'auto formater
-> aérez votre code
MERCI DE RESPECTER CES CONSIGNES
"""


# Imports

from flask import *
from flask import session
import sqlite3
import hashlib


# Initialisation de l'application

app = Flask(__name__)


# DB gestion

# Connexion à la DB

DATABASE = 'project.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = "anystringhere"


def get_db():

    db = getattr(g, DATABASE, None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Fermeture de la DB


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, DATABASE, None)
    if db is not None:
        db.close()


#####################################################################################################################
#                                             Code de l'application                                                 #
#####################################################################################################################


# Renders main page


@app.route('/')
def main():
    r = get_db().cursor()
    r.execute("SELECT body FROM messages")
    return render_template('main.html', liste=r.fetchall())


#####################################################################################################################


# Renders inscription page

@app.route("/inscription", methods=['GET', 'POST'])
def insc():
    msg = ''
    if request.method == 'POST' and request.form.get('first_name') and request.form.get('name') and request.form.get('password') and request.form.get('password') == request.form.get('password2'):
        rid = get_db().cursor()  # Curseur de l'id
        # On récupère le plus grand id disponible
        rid.execute("SELECT MAX(id) FROM utilisateurs")
        # On l'augmente de 1 pour bien avoir le plus grand indice
        new_id = rid.fetchall()[0][0]+1
        # On récupère, dans les prochaines lignes, les données du formumlaire
        nom = request.form.get('first_name')
        prenom = request.form.get('name')
        pseudo = prenom = request.form.get('pseudo')
        adresse_mail = request.form.get('email')
        num_de_tel = request.form.get('phone_number')
        mdp = bytes(request.form.get('password'), 'utf-8')
        conn = get_db()  # On créé une connexion pour l'insertion
        cur = conn.cursor()
        # On calcule le hash du mot de passe
        mass = hashlib.sha256(mdp).hexdigest()
        if request.form.get('prod'):
            cur.execute('INSERT INTO utilisateurs VALUES(?,?,?,?,?,?,?,?)', (new_id,
                        prenom, nom, adresse_mail, num_de_tel, mass, 2, pseudo))  # On insère ensuite le tout dans la base de données
        else:
            cur.execute('INSERT INTO utilisateurs VALUES(?,?,?,?,?,?,?,?)', (new_id,
                        prenom, nom, adresse_mail, num_de_tel, mass, 1, pseudo))
        conn.commit()
        conn.close()  # On ferme la connection
        # On enregistre dans session l'id actif
        session["id_utilisateur"] = new_id
        return redirect(url_for("renvoyer_dashboard_util"))
    elif request.method == 'POST' and request.form.get('first_name') and request.form.get('name') and request.form.get('password'):
        # Si les mots de passe ne correspondent pas, on l'affiche  à l'écran
        msg = "Les mots de passe ne correspondent pas"
    return render_template('inscription.html', message=msg)


#####################################################################################################################


# Renders connection page


@app.route("/connexion", methods=['GET', 'POST'])
def connexion_page():
    # Si le formulaire est bien rempli...
    if request.method == 'POST' and request.form.get('name') and request.form.get('password'):
        r = get_db().cursor()  # On créé un curseur
        nom = request.form.get('name')  # On récupère les données du formulaire
        mdp = bytes(request.form.get('password'), 'utf-8')
        # On calcule le hash du mot de passe entré
        mass = hashlib.sha256(mdp).hexdigest()
        # On récupère le hash de l'identifiant entré
        r.execute("SELECT motdepasse FROM utilisateurs WHERE pseudo=?", (nom,))
        tuple = r.fetchall()
        if tuple[0][0] == mass:  # Si les deux correspondent...
            r = get_db().cursor()
            r.execute("SELECT id FROM utilisateurs WHERE pseudo=?",
                      (nom,))  # On récupère l'id
            tuple = r.fetchall()[0][0]
            session["id_utilisateur"] = tuple  # Et on le stocke dans session
            rsession = get_db().cursor()
            rsession.execute("SELECT statut FROM utilisateurs WHERE id={}".format(  # On récupère le statut (utilisateur ou producteur)
                session["id_utilisateur"]))
            session_type = rsession.fetchall()[0][0]
            if session_type == 1:
                # On renvoie ensuite la page correspondante
                return redirect(url_for("renvoyer_dashboard_util"))
            elif session_type == 2:
                # On renvoie ensuite la page correspondante
                return redirect(url_for("renvoyer_prod"))
            print("connected")

            return redirect(url_for("renvoyer_dashboard_util"))
        else:
            print("Connection failed")
    # Si rien ne se passe (ou erreur) on recharge la même page
    return render_template("connexion.html")


@app.route("/images/verger_1.png")
def renvoyer_bg():
    return send_file("ressources/images/verger_1.png")


@app.route("/images/<produit>")
def renvoyer_produit(produit):
    return send_file("ressources/icons/{}.png".format(produit))


@app.route("/images/about")
def renvoyer_about():
    return send_file("ressources/images/about_logo")


@app.route("/utilisateur/dashboard")
def renvoyer_dashboard_util():
    if "id_utilisateur" in session:
        id = session["id_utilisateur"]
        r = get_db().cursor()
        r.execute("SELECT * FROM commande WHERE id_util={}".format(id))
        liste_commandes_tuple = r.fetchall()
        lst_photo = []
        a_payer = 0
        for element in liste_commandes_tuple:
            lst_photo.append(element[1])
            a_payer += element[4]
        rphoto = get_db().cursor()
        photos = []
        for e in lst_photo:
            rphoto.execute("SELECT photo from produits where id={}".format(e))
            val = rphoto.fetchall()
            photos.append(val[0][0])
        r2 = get_db().cursor()
        r2.execute("SELECT photo FROM produits WHERE id={}".format(id))
        rnom = get_db().cursor()
        rnom.execute("SELECT Prenom FROM utilisateurs WHERE id={}".format(id))
        nom = rnom.fetchall()[0][0]
        return render_template("dashboard_util.html", nom=nom, liste_commandes=liste_commandes_tuple, photo=photos, total=a_payer)
    else:
        return render_template("connexion.html")


@app.route("/producteur/dashboard")
def renvoyer_prod():
    if "id_utilisateur" in session:
        id = session["id_utilisateur"]
        r = get_db().cursor()
        r.execute("SELECT * FROM commande WHERE id={}".format(id))
        rnom = get_db().cursor()
        rnom.execute("SELECT Prenom FROM utilisateurs WHERE id={}".format(id))
        nom = rnom.fetchall()[0][0]
        rliste_produits = get_db().cursor()
        rliste_produits.execute(
            "SELECT * FROM produits WHERE producteur={}".format(session["id_utilisateur"]))
        tuple = rliste_produits.fetchall()
        print(tuple)
        return render_template("dashboard_prod.html", nom=nom, commandes=r.fetchall(), liste_produits=tuple)
    else:
        return (redirect(url_for("connexion")))


@app.route('/publications', methods=["GET", "POST"])
def publications():
    # Si l'utilisateur n'est pas connecté, il ne peut pas accéder à cette page : on le redirige vers l'accueil.
    if "id_utilisateur" not in session:
        return redirect("/")
    userid = session["id_utilisateur"]
    conn = get_db()
    cur = conn.cursor()
    if request.method == "POST":
        # Si l'utilisateur a posté une publication, on l'insère dans la bd
        if request.form.get('submessage') != None:
            cur.execute("INSERT INTO publications (posterid, date, message) VALUES (?, datetime('now','localtime'), ?)",
                        (userid, request.form['message']))
            conn.commit()
        # Si l'utilisateur a posté un commentaire, on l'insère dans la bd
        elif request.form.get('subcomm') != None:
            cur.execute("INSERT INTO commentaires (postid, userid, commentaire, date) VALUES (?, ?, ?, datetime('now','localtime'))",
                        (request.form['postid'], userid, request.form['messagecomm']))
            conn.commit()
    cur.execute("SELECT publications.id, posterid, strftime('%d/%m/%Y à %H:%M', date), message, pseudo FROM publications JOIN utilisateurs ON utilisateurs.id = posterid WHERE posterid IN (SELECT ? UNION SELECT following FROM follow WHERE follower = ?) ORDER BY publications.id DESC LIMIT 15", (userid, userid))
    # On récupère les publications qui doivent s'afficher sur le fil d'actualité de l'utilisateur
    publis = cur.fetchall()
    Lpublis = []  # Initialisation de la liste des publications avec ses commentaires
    for p in publis:
        cur.execute(
            "SELECT commentaires.id, userid, commentaire, strftime('%d/%m/%Y à %H:%M', date), pseudo FROM commentaires JOIN utilisateurs ON utilisateurs.id = userid WHERE postid = ? ORDER BY commentaires.id DESC", (p[0],))
        # On ajoute à la liste la publication p avec ses commentaires
        Lpublis.append(p + (cur.fetchall(),))
    return render_template('publications.html', publis=Lpublis)


@app.route('/messagerie/<int:readid>', methods=["GET", "POST"])
@app.route('/messagerie/', methods=["GET", "POST"])
def messagerie(readid=0):
    # Si l'utilisateur n'est pas connecté, il ne peut pas accéder à cette page : on le redirige vers l'accueil.
    if "id_utilisateur" not in session:
        return redirect("/")
    userid = session["id_utilisateur"]
    msgread = None  # Initialisation des paramètres du message lu, va être modifié s'il y en a effectivement un
    conn = get_db()
    cur = conn.cursor()
    # Si l'utilisateur a souhaité supprimer des messages de sa boîte de réception
    if request.form.get('suppmsg') != None:
        Lsuppr = []  # Initialisation de la liste des suppressions
        for k in list(request.form.keys()):
            if k.isdigit():  # Si la clé est un entier naturel (le "name" des checkboxes)
                Lsuppr.append(int(k))  # On ajoute à la liste des suppressions
        Lsupprstr = "(" + str(Lsuppr)[1:-1] + ")"
        # Moche, mais pas trouvé d'autre moyen avec le IN, et normalement pas de faille SQL car uniquement des chiffres
        cur.execute("UPDATE messages SET suppr = 1 WHERE id IN " + Lsupprstr)
        conn.commit()
    # Si l'utilisateur veut supprimer le message qu'il était en train de lire
    if request.form.get('suppmsglecture') != None:
        cur.execute("UPDATE messages SET suppr = 1 WHERE id = ?",
                    (request.form['readid'],))
        conn.commit()
    if readid > 0:  # Si l'utilisateur a cliqué sur un message à lire
        # On met le message qui va être lu par l'utilisateur dans l'état "lu"
        cur.execute(
            "UPDATE messages SET read = 1 WHERE id = ? AND receiver = ?", (readid, userid))
        conn.commit()
        cur.execute("SELECT messages.id, sender, subject, strftime('%d/%m/%Y à %H:%M', date), pseudo, body FROM messages JOIN utilisateurs ON utilisateurs.id = sender WHERE receiver = ? AND suppr = 0 AND messages.id = ? ORDER BY messages.id DESC", (userid, readid))
        # On récupère les données du message que l'utilisateur veut lire
        msgread = cur.fetchone()
    cur.execute("SELECT messages.id, sender, read, subject, strftime('%d/%m/%Y à %H:%M', date), pseudo FROM messages JOIN utilisateurs ON utilisateurs.id = sender WHERE receiver = ? AND suppr = 0 ORDER BY messages.id DESC LIMIT 15", (userid,))
    messages = cur.fetchall()  # On récupère la boîte de réception de l'utilisateur
    return render_template('messagerie.html', messages=messages, msgread=msgread)


@app.route('/ecrire', methods=["GET", "POST"])
def ecrire():
    # Si l'utilisateur n'est pas connecté, il ne peut pas accéder à cette page : on le redirige vers l'accueil.
    if "id_utilisateur" not in session:
        return redirect("/")
    userid = session["id_utilisateur"]
    if request.form.get('objet') != None:
        objet = request.form['objet']
    else:
        objet = "Pas d'objet"  # Objet par défaut
    if request.form.get('dest') != None:
        dest = request.form['dest']
    else:
        dest = ""  # Destinateur par défaut
    if request.form.get('corps') != None:
        corps = request.form['corps']
    else:
        corps = ""  # Corps nul par défaut
    # Initialisation d'un éventuel message d'erreur. S'il n'y en a pas, on restera sur None.
    erreur = None
    tentenvoi = None  # Si l'utilisateur vient d'envoyer un message

    if request.form.get('envoyer') != None:
        conn = get_db()
        cur = conn.cursor()
        tentenvoi = True
        cur.execute("SELECT id FROM utilisateurs WHERE pseudo = ?", (request.form.get(
            'dest'),))  # On récupère l'id de l'utilisateur qui correspond au pseudo entré
        iddesttuple = cur.fetchone()
        if iddesttuple != None:  # Si on a effectivement un utilisateur dont le pseudo correspond
            iddest = iddesttuple[0]
            cur.execute("INSERT INTO messages (sender, receiver, subject, body, date) VALUES (?, ?, ?, ?, datetime('now','localtime'))",
                        (userid, iddest, objet, corps))  # On insère le message dans la base de données (correspond donc à l'envoi)
            conn.commit()
        else:
            # Erreur si le pseudo entré ne correspond à aucun pseudo dans la base de données.
            erreur = "Le pseudo spécifié n'existe pas."
    return render_template('ecrire.html', objet=objet, dest=dest, corps=corps, erreur=erreur, tentenvoi=tentenvoi)


app.run(host='localhost', port=5000)
