# Projet Pluridisciplinaire d'Informatique Intégrative - Semestre 1

![Static Badge](https://img.shields.io/badge/Télécom-School_project-purple)
![Static Badge](https://img.shields.io/badge/Backend-Python(Flask)-yellow)
![Static Badge](https://img.shields.io/badge/Frontend-HTML-orange)
![Static Badge](https://img.shields.io/badge/Frontend-CSS-purple)
![Static Badge](https://img.shields.io/badge/Database-sqlite3-blue)



## Presentation

This project was developped during my scholarship at [Télécom Nancy](https://telecomnancy.univ-lorraine.fr) (1st year - 1st semester).  
Subject excerpt:
> Your goal is [...] to conceive and implement an innovative application dedicated to resource's optimization within territory's orchard and gardens

The current application is a **platform facilitating local food circuits and and/or vegetable's person to person sales**

**Group members**:
- VESSE Léo       (Project's chief)
- AING Olivia
- LERUEZ Thomas
- UNGARO Cosimo

## Installation
##### Download
###### Via SSH
```
git clone git@github.com:cos-imo/ppii-1.git
```
###### Via HTTP
```
git clone https://github.com/cos-imo/ppii-1.git
```

##### Activation de l'environnement virtuel
**WARNING**: The current repository is a copy of the original working repository (that was hosted in my school's gitlab). That's why a lot of documents (such as Project Managemnt's one) are into the repository. The code is contained within **PROJET**'s folder. The command given below suppose that you are at the project's root (directory ppii-1)

```
python3 -m venv PROJET/.venv
source PROJET/.venv/bin/activate
```

##### Installing dependencies (optional)
```
pip install -r PROJET/requirements.txt
```

##### Launching
From the folder containing the code (folder PROJET) execute:
```
flask run
```
If you want to activate the debugger:
```
flask run --debug
```
