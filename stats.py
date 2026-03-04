from database import get_resultats_utilisateur

def afficher_progression(utilisateur_id):
    resultats = get_resultats_utilisateur(utilisateur_id)
    if not resultats:
        print("Pas de résultats encore.")
        return
    total = len(resultats)
    reussis = sum([r[4] for r in resultats])
    progression = int((reussis/total)*100)
    print(f"📊 Progression globale : {progression}% ({reussis}/{total} réussis)")

def comparer_reseau(utilisateur_id, niveau="classe"):
    # Valeurs fictives pour test
    valeurs = {"classe": 60, "etablissement": 55, "reseau": 50}
    print(f"📈 Comparaison {niveau} : votre score = 50%, moyenne {niveau} = {valeurs.get(niveau, '?')}%")
