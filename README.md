# Projet Pluridisciplinaire d'Informatique Intégrative - Semestre 1

![Static Badge](https://img.shields.io/badge/Télécom-Projet_scolaire-purple)
![Static Badge](https://img.shields.io/badge/Backend-Python(Flask)-yellow)
![Static Badge](https://img.shields.io/badge/Frontend-HTML-orange)
![Static Badge](https://img.shields.io/badge/Frontend-CSS-purple)
![Static Badge](https://img.shields.io/badge/Base_de_donn%C3%A9es-sqlite3-blue)

**Note**: This readme is also available in [english](https://github.com/cos-imo/ppii-1/blob/main/README-EN.md)

## Présentation

Projet développé dans le cadre de ma scolarité à [Télécom Nancy](https://telecomnancy.univ-lorraine.fr) (1ère année - 1er semestre)
Extrait du sujet:
> Votre objectif est, [...] de concevoir et d’implémenter une application innovante dédiées à l’optimisation des ressources dans les vergers et potagers du territoire.

La présente application est ainsi une **plateforme permettant d'organiser la vente en circuits-courts et/ou de particulier à particulier.**

**Membres du groupe** :
- VESSE Léo       (Chef de projet)
- AING Olivia
- LERUEZ Thomas
- UNGARO Cosimo

## Installation
##### Téléchargement
###### Par SSH
```
git clone git@github.com:cos-imo/ppii-1.git
```
###### Par HTTP
```
git clone https://github.com/cos-imo/ppii-1.git
```

##### Activation de l'environnement virtuel
**ATTENTION**: Le dépôt sur lequel vous vous trouvez est une copie d'un dépôt de travail GitLab. Ainsi de nombreux documents (ex. Gestion de Projet) se trouvent dans le dépôt. Le code se trouve dans le dossier **PROJET**. Les commandes données ci-dessous supposent que vous vous trouvez à la racine du projet (dossier ppii-1)

```
python3 -m venv PROJET/.venv
source PROJET/.venv/bin/activate
```

##### Installation des dépendances (optionnel)
```
pip install -r PROJET/requirements.txt
```

##### Lancement
Depuis la dossier contenant le code (dossier PROJET) exécuter:
```
flask run
```
Pour activer le débogueur:
```
flask run --debug
```
