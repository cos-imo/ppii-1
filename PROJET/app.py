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
import sqlite3
import hashlib


# Initialisation de l'application

app = Flask(__name__)


# DB gestion

# Connexion à la DB

DATABASE = 'project.db'


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


# Renders insciption page

@app.route("/inscription", methods=['GET', 'POST'])
def insc():
    if request.method == 'POST' and request.form.get('first_name') and request.form.get('name'):
        print("ok")
        nom = request.form.get('first_name')
        prenom = request.form.get('name')
        mdp = bytes(request.form.get('password'), 'utf-8')
        conn = get_db()
        cur = conn.cursor()
        mass = hashlib.sha256(mdp).hexdigest()
        cur.execute('INSERT INTO test VALUES(?,?)', (nom, mass))
        conn.commit()
        conn.close()
    else:
        print('please fill out the form')
    return render_template('inscription.html')


#####################################################################################################################


# Renders connection page


@app.route("/connexion", methods=['GET', 'POST'])
def connexion_page():
    if request.method == 'POST' and request.form.get('name') and request.form.get('password'):
        r = get_db().cursor()
        nom = request.form.get('name')
        r.execute("SELECT pass FROM test WHERE nom=?", (nom,))
        print(r.fetchall())

    return render_template("connexion.html")


app.run(host='localhost', port=5000)


#####################################################################################################################
#                                  Merci de mettre ici vos routes de test éventuelles                               #
#####################################################################################################################


#####################################################################################################################

# Justifiez la fonction, fonction de test ou je sais pas quoi

# @app.route('/style.css')
# def return_css():
#     return render_template('static/css/style.css')

#####################################################################################################################


# @app.route("/images/verger_1.jpg")
# def renvoyer_bg():
#     return send_file("ressources/images/verger_1.jpg")


#####################################################################################################################

# @app.route("/images/about")
# def renvoyer_about():
#     return send_file("ressources/images/about_logo")

#####################################################################################################################
