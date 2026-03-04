from database import ajouter_utilisateur, get_utilisateur, creer_session

def inscription():
    print("=== INSCRIPTION ===")
    nom = input("Nom : ")
    mdp = input("Mot de passe : ")
    niveau = input("Niveau (1ère/Terminale) : ")
    etablissement = input("Établissement : ")
    ajouter_utilisateur(nom, mdp, niveau, etablissement)
    print(f"Utilisateur {nom} créé avec succès !\n")

def connexion():
    print("=== CONNEXION ===")
    nom = input("Nom : ")
    mdp = input("Mot de passe : ")
    utilisateur = get_utilisateur(nom, mdp)
    if utilisateur:
        print(f"Connexion réussie. Bienvenue {utilisateur[1]} !\n")
        creer_session(utilisateur[0])
        return utilisateur
    else:
        print("Nom ou mot de passe incorrect.\n")
        return None
