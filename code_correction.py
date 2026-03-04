from database import enregistrer_resultat
import ast

def detecter_contournements(code_saisi, contraintes):
    """
    Vérifie si le code saisi contient des mots interdits (contournements).
    Retourne (True, mot) si un mot interdit est trouvé, sinon (False, None).
    """
    if not contraintes:
        return False, None
    for mot in contraintes:
        if mot in code_saisi:
            return True, mot
    return False, None

def verifier_fonction(nom_fonction, code_saisi, test_entre, resultat_attendu, contraintes=None):
    """
    Vérifie l'exécution d'une fonction saisie par l'élève.
    
    Paramètres:
        nom_fonction (str): nom de la fonction attendue
        code_saisi (str): code Python écrit par l'élève
        test_entre (any): argument(s) à passer à la fonction (peut être une valeur unique, un tuple ou une liste)
        resultat_attendu (any): résultat que la fonction doit retourner
        contraintes (list): liste de mots interdits (ex: ["print", "max", "min"])
    
    Retourne:
        (bool, str): (réussite, message)
    """
    if contraintes is None:
        contraintes = []

    # 1. Détection des contournements
    contournement, mot = detecter_contournements(code_saisi, contraintes)
    if contournement:
        return False, f"❌ Contournement interdit détecté : utilisation de '{mot}'"

    # 2. Exécution du code dans un espace de noms sécurisé
    try:
        namespace = {}
        exec(code_saisi, {}, namespace)
    except Exception as e:
        return False, f"❌ Erreur de syntaxe ou d'exécution dans votre code : {e}"

    # 3. Vérification que la fonction est bien définie
    if nom_fonction not in namespace:
        return False, f"❌ Fonction '{nom_fonction}' non définie dans votre code"
    
    fonction = namespace[nom_fonction]
    if not callable(fonction):
        return False, f"❌ '{nom_fonction}' n'est pas une fonction appelable"

    # 4. Préparation des arguments
    # Si test_entre est un tuple ou une liste, on le décompose, sinon on le met dans un tuple
    if isinstance(test_entre, (tuple, list)):
        args = test_entre
    else:
        args = (test_entre,)

    # 5. Exécution de la fonction avec les arguments
    try:
        resultat = fonction(*args)
    except Exception as e:
        return False, f"❌ Erreur lors de l'exécution de votre fonction : {e}"

    # 6. Comparaison du résultat
    if resultat == resultat_attendu:
        return True, "✅ Correct ! Votre fonction a produit le résultat attendu."
    else:
        return False, f"❌ Résultat incorrect. Attendu : {resultat_attendu}, obtenu : {resultat}"

# Exemple d'utilisation (pour test)
if __name__ == "__main__":
    code_test = """
def somme(a, b):
    return a + b
"""
    ok, msg = verifier_fonction("somme", code_test, (2, 3), 5, contraintes=["print"])
    print(msg)