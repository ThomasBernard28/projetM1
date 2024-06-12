# Projet de Master 1 : Application de visualisation de résultats scolaires.

## Objectif de l'application : 

Le but de cette application est de visualiser dans une interface web développée à l'aide du module Python "Streamlit" les résultats scolaires d'élèves du cours d'anglais en secondaire.

## Fonctionnalités :

- Charger un bulletin standardisé au format Excel
- Extraire les résultats pour chaque élève dans les différentes compétences
- Comparer les élèves entre eux ou par rapport à la classe entière pour une, plusieurs ou toutes les compétences.
- Vision normalisée des résultats des étudiants en regard du reste de la classe.

## Pré-requis:

- Python 3.11
- Idéalement la création d'un _Python Virtual Environment (venv)_ pour l'installation desdépendances

## Comment exécuter le code:

1. Cloner le repository
2. Créer le venv et l'activer
   ```
   python -m venv .venv

   source .venv/bin/activate
   ```
4. Installer les dépendances à l'aide de pip avec la commande suivante :
   ```
   pip install -r requirements.txt
   ```
5. Exécuter l'application à l'aide de la commande suivante:
   ```
   streamlit run app/Hello.py
   ```
