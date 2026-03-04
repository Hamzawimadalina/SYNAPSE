chapitres_test = {
    1: {"matiere": "NSI", "nom": "Algorithmes de tri", "progress": 20},
    2: {"matiere": "NSI", "nom": "Structures de données", "progress": 50},
    3: {"matiere": "NSI", "nom": "Fonctions", "progress": 40},
    4: {"matiere": "NSI", "nom": "Bases SQL", "progress": 30},
    5: {"matiere": "Maths", "nom": "Fonctions", "progress": 70},
    6: {"matiere": "Maths", "nom": "Probabilités", "progress": 90},
    7: {"matiere": "Maths", "nom": "Statistiques", "progress": 50}
}

def selection_chapitre(chapitre_id):
    return chapitres_test.get(chapitre_id, None)
