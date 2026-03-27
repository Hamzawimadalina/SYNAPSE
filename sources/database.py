import sqlite3
from utils import hash_mdp

def connexion_db():
    return sqlite3.connect("synapse.db")

def creer_tables():
    conn = connexion_db()
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = OFF")
    tables = ['Erreur', 'Resultat', 'Exercice_Notion', 'Exercice', 'Notion', 'Chapitre', 'Session', 'Utilisateur']
    for table in tables:
        c.execute(f'DROP TABLE IF EXISTS {table}')
    c.execute("PRAGMA foreign_keys = ON")

    c.execute('''
        CREATE TABLE Utilisateur(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            mdp TEXT NOT NULL,
            niveau TEXT,
            etablissement TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE Session(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(utilisateur_id) REFERENCES Utilisateur(id)
        )
    ''')
    c.execute('''
        CREATE TABLE Chapitre (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matiere TEXT NOT NULL,
            nom TEXT NOT NULL,
            frequence_bac TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE Notion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE Exercice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_chapitre INTEGER NOT NULL,
            type TEXT NOT NULL,
            question TEXT NOT NULL,
            options TEXT,
            reponse_attendue TEXT,
            contraintes TEXT,
            nom_fonction TEXT,
            test_input TEXT,
            test_output TEXT,
            FOREIGN KEY (id_chapitre) REFERENCES Chapitre(id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE Exercice_Notion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercice_id INTEGER NOT NULL,
            notion_id INTEGER NOT NULL,
            FOREIGN KEY (exercice_id) REFERENCES Exercice(id) ON DELETE CASCADE,
            FOREIGN KEY (notion_id) REFERENCES Notion(id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE Resultat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            utilisateur_id INTEGER NOT NULL,
            exercice_id INTEGER NOT NULL,
            reussi INTEGER NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (utilisateur_id) REFERENCES Utilisateur(id) ON DELETE CASCADE,
            FOREIGN KEY (exercice_id) REFERENCES Exercice(id) ON DELETE CASCADE
        )
    ''')
    c.execute('''
        CREATE TABLE Erreur (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_resultat INTEGER NOT NULL,
            id_notion INTEGER NOT NULL,
            FOREIGN KEY (id_resultat) REFERENCES Resultat(id) ON DELETE CASCADE,
            FOREIGN KEY (id_notion) REFERENCES Notion(id) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Tables créées avec succès")

def inserer_donnees_test():
    conn = connexion_db()
    c = conn.cursor()
    # Vérifier si les chapitres existent déjà
    c.execute("SELECT COUNT(*) FROM Chapitre")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    chapitres = [
        ("NSI", "Algorithmes de tri", "forte"),
        ("NSI", "Structures de données", "moyenne"),
        ("NSI", "Bases de données SQL", "faible"),
        ("NSI", "Programmation orientée objet", "moyenne"),
        ("NSI", "Récursivité", "faible"),
    ]
    c.executemany(
        "INSERT INTO Chapitre (matiere, nom, frequence_bac) VALUES (?,?,?)",
        chapitres
    )
    print("✅ Chapitres insérés")

    notions = [
        ("Tri rapide",),
        ("Tri bulle",),
        ("Boucle for",),
        ("Requête SELECT",),
        ("Classe et objet",),
        ("Fonction récursive",),
    ]
    c.executemany("INSERT INTO Notion (nom) VALUES (?)", notions)
    print("✅ Notions insérées")

    exercices = [
        # Chapitre 1
        (1, "QCM", "Quel est le tri le plus rapide en moyenne ?",
         "Tri rapide;Tri bulle;Tri insertion", "0", "",
         "", "", ""),
        (1, "code", "Écris une fonction `tri_bulle(liste)` qui trie une liste.",
         "",
         "def tri_bulle(liste):\n    n = len(liste)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if liste[j] > liste[j+1]:\n                liste[j], liste[j+1] = liste[j+1], liste[j]\n    return liste",
         "print,max,min",
         "tri_bulle", "([3,1,2],)", "[1,2,3]"),
        (1, "trous", "Le tri par insertion a une complexité en moyenne de ______.",
         "", "O(n²)", "",
         "", "", ""),

        # Chapitre 2
        (2, "QCM", "Quelle structure utilise le principe LIFO ?",
         "Pile;File;Liste;Dictionnaire", "0", "",
         "", "", ""),
        (2, "code", "Écris une fonction `empiler(pile, element)` qui ajoute un élément à une pile (représentée par une liste).",
         "",
         "def empiler(pile, element):\n    pile.append(element)\n    return pile",
         "",
         "empiler", "([], 5)", "[5]"),

        # Chapitre 3
        (3, "QCM", "Quelle commande SQL permet de récupérer des données ?",
         "SELECT;INSERT;UPDATE;DELETE", "0", "",
         "", "", ""),
        (3, "code", "Écris une requête SQL pour sélectionner tous les élèves d'une table 'eleves'.",
         "", "SELECT * FROM eleves;", "",
         "", "", "SELECT * FROM eleves;"),

        # Chapitre 4
        (4, "QCM", "Quel mot-clé permet de définir une classe en Python ?",
         "class;def;struct;object", "0", "",
         "", "", ""),
        (4, "trous", "Une ______ est une instance d'une classe.",
         "", "objet", "",
         "", "", ""),

        # Chapitre 5
        (5, "code", "Écris une fonction récursive `factorielle(n)` qui calcule n!.",
         "",
         "def factorielle(n):\n    if n <= 1:\n        return 1\n    else:\n        return n * factorielle(n-1)",
         "",
         "factorielle", "(5,)", "120"),
        (5, "QCM", "Une fonction récursive doit contenir :",
         "Un cas de base;Une boucle;Une variable globale;Un return", "0", "",
         "", "", ""),
    ]

    for exo in exercices:
        c.execute('''
            INSERT INTO Exercice
            (id_chapitre, type, question, options, reponse_attendue, contraintes,
             nom_fonction, test_input, test_output)
            VALUES (?,?,?,?,?,?,?,?,?)
        ''', exo)
    print("✅ Exercices insérés")

    c.execute("SELECT id, nom FROM Notion")
    notion_map = {row[1]: row[0] for row in c.fetchall()}

    liaisons = [
        (1, notion_map["Tri rapide"]),
        (1, notion_map["Tri bulle"]),
        (2, notion_map["Tri bulle"]),
        (2, notion_map["Boucle for"]),
        (3, notion_map["Tri bulle"]),
        (4, notion_map["Boucle for"]),
        (5, notion_map["Boucle for"]),
        (6, notion_map["Requête SELECT"]),
        (7, notion_map["Requête SELECT"]),
        (8, notion_map["Classe et objet"]),
        (9, notion_map["Classe et objet"]),
        (10, notion_map["Fonction récursive"]),
        (11, notion_map["Fonction récursive"]),
    ]
    c.executemany("INSERT INTO Exercice_Notion (exercice_id, notion_id) VALUES (?,?)", liaisons)
    print("✅ Liaisons exercice-notion insérées")

    conn.commit()
    conn.close()
    print("✅ Toutes les données de test ont été insérées")

# --------------------------------------------------------------------
# Fonctions CRUD
# --------------------------------------------------------------------

def ajouter_utilisateur(nom, mdp, niveau, etablissement):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("INSERT INTO Utilisateur(nom, mdp, niveau, etablissement) VALUES (?, ?, ?, ?)",
              (nom, hash_mdp(mdp), niveau, etablissement))
    conn.commit()
    conn.close()
    print(f"✅ Utilisateur {nom} créé")

def get_utilisateur(nom, mdp):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT * FROM Utilisateur WHERE nom=?", (nom,))
    utilisateur = c.fetchone()
    conn.close()
    if utilisateur and utilisateur[2] == hash_mdp(mdp):
        return utilisateur
    return None

def creer_session(utilisateur_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("INSERT INTO Session(utilisateur_id) VALUES (?)", (utilisateur_id,))
    conn.commit()
    conn.close()

def get_chapitres(matiere):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT id, nom, frequence_bac FROM Chapitre WHERE matiere=?", (matiere,))
    chapitres = c.fetchall()
    conn.close()
    return chapitres

def get_exercices_par_chapitre(chapitre_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, id_chapitre, type, question, options, reponse_attendue, contraintes,
               nom_fonction, test_input, test_output
        FROM Exercice
        WHERE id_chapitre=?
    ''', (chapitre_id,))
    exercices = c.fetchall()
    conn.close()
    return exercices

def get_exercice(exercice_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, id_chapitre, type, question, options, reponse_attendue, contraintes,
               nom_fonction, test_input, test_output
        FROM Exercice
        WHERE id=?
    ''', (exercice_id,))
    exo = c.fetchone()
    conn.close()
    return exo

def get_notions_par_exercice(exercice_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT notion_id FROM Exercice_Notion WHERE exercice_id=?", (exercice_id,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def enregistrer_resultat(utilisateur_id, exercice_id, reussi):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("INSERT INTO Resultat (utilisateur_id, exercice_id, reussi) VALUES (?,?,?)",
              (utilisateur_id, exercice_id, 1 if reussi else 0))
    resultat_id = c.lastrowid
    conn.commit()
    conn.close()
    return resultat_id

def enregistrer_erreur(resultat_id, notion_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("INSERT INTO Erreur (id_resultat, id_notion) VALUES (?,?)",
              (resultat_id, notion_id))
    conn.commit()
    conn.close()

def get_resultats_utilisateur(utilisateur_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute('''
        SELECT r.id, r.exercice_id, r.reussi, r.date, e.id_chapitre
        FROM Resultat r
        JOIN Exercice e ON r.exercice_id = e.id
        WHERE r.utilisateur_id=?
    ''', (utilisateur_id,))
    resultats = c.fetchall()
    conn.close()
    return resultats

def get_progression_chapitre(utilisateur_id, chapitre_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute('''
        SELECT COUNT(*) FROM Resultat r
        JOIN Exercice e ON r.exercice_id = e.id
        WHERE r.utilisateur_id=? AND e.id_chapitre=? AND r.reussi=1
    ''', (utilisateur_id, chapitre_id))
    reussis = c.fetchone()[0]
    c.execute('''
        SELECT COUNT(*) FROM Resultat r
        JOIN Exercice e ON r.exercice_id = e.id
        WHERE r.utilisateur_id=? AND e.id_chapitre=?
    ''', (utilisateur_id, chapitre_id))
    total = c.fetchone()[0]
    conn.close()
    if total == 0:
        return 0
    return int((reussis / total) * 100)

def get_moyenne_classe(utilisateur_id, chapitre_id):
    """Moyenne des élèves du même niveau et même établissement que l'utilisateur"""
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT niveau, etablissement FROM Utilisateur WHERE id=?", (utilisateur_id,))
    user_info = c.fetchone()
    if not user_info:
        conn.close()
        return 50
    niveau, etablissement = user_info
    c.execute('''
        SELECT AVG(r.reussi) FROM Resultat r
        JOIN Exercice e ON r.exercice_id = e.id
        JOIN Utilisateur u ON r.utilisateur_id = u.id
        WHERE e.id_chapitre=? AND u.niveau=? AND u.etablissement=?
    ''', (chapitre_id, niveau, etablissement))
    moyenne = c.fetchone()[0]
    conn.close()
    if moyenne is None:
        return 50
    return int(moyenne * 100)

def get_moyenne_etablissement(utilisateur_id, chapitre_id):
    """Moyenne de tous les utilisateurs du même établissement (tous niveaux)"""
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT etablissement FROM Utilisateur WHERE id=?", (utilisateur_id,))
    user_info = c.fetchone()
    if not user_info:
        conn.close()
        return 50
    etablissement = user_info[0]
    c.execute('''
        SELECT AVG(r.reussi) FROM Resultat r
        JOIN Exercice e ON r.exercice_id = e.id
        JOIN Utilisateur u ON r.utilisateur_id = u.id
        WHERE e.id_chapitre=? AND u.etablissement=?
    ''', (chapitre_id, etablissement))
    moyenne = c.fetchone()[0]
    conn.close()
    if moyenne is None:
        return 50
    return int(moyenne * 100)

def get_notion_id(nom_notion):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT id FROM Notion WHERE nom=?", (nom_notion,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_statistiques_globales(utilisateur_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM Resultat WHERE utilisateur_id=?", (utilisateur_id,))
    total_exercices = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM Resultat WHERE utilisateur_id=? AND reussi=1", (utilisateur_id,))
    total_reussis = c.fetchone()[0]
    c.execute("SELECT id, nom FROM Chapitre")
    chapitres = c.fetchall()
    progression_par_chapitre = []
    for chap_id, chap_nom in chapitres:
        prog = get_progression_chapitre(utilisateur_id, chap_id)
        progression_par_chapitre.append((chap_nom, prog))
    conn.close()
    return {
        "total_exercices": total_exercices,
        "total_reussis": total_reussis,
        "taux_reussite": int((total_reussis / total_exercices * 100)) if total_exercices > 0 else 0,
        "progression_par_chapitre": progression_par_chapitre
    }

if __name__ == "__main__":
    print("🔧 Création des tables...")
    creer_tables()
    print("\n📦 Insertion des données de test...")
    inserer_donnees_test()
    print("\n✅ Base de données initialisée.")
