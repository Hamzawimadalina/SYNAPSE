NOTIONS_TEST = {
    1: "Algorithmes de tri",
    2: "Structures de données",
    3: "Fonctions",
    4: "Bases SQL",
    5: "Fonctions Maths",
    6: "Probabilités",
    7: "Statistiques"
}

def analyser_erreurs(utilisateur_id, chapitre_id, reussi):
    if not reussi:
        notion = NOTIONS_TEST.get(chapitre_id, "Général")
        print(f"❗ Vous devez retravailler la notion : {notion}")
        return notion
    return None

def generer_fiche(notion):
    fiches = {
        "Algorithmes de tri": "Revoyez tris par insertion, bulle, rapide et complexité.",
        "Structures de données": "Revoyez listes, dictionnaires, piles et files.",
        "Fonctions": "Revoyez définition, paramètres, retour et portée.",
        "Bases SQL": "Revoyez SELECT, JOIN, INSERT, UPDATE.",
        "Fonctions Maths": "Revoyez dérivées et intégrales simples.",
        "Probabilités": "Revoyez événements, probas conditionnelles et indépendance.",
        "Statistiques": "Revoyez moyennes, médianes, écarts types."
    }
    contenu = fiches.get(notion, "Révision générale à faire.")
    print(f"📄 Fiche de révision : {contenu}")

def proposer_reessai():
    print("🔄 Essayez à nouveau cet exercice pour renforcer vos compétences !")
