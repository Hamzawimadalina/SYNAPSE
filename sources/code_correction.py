import ast

def detecter_contournements(code_saisi, contraintes):
    if not contraintes:
        return False, None
    for mot in contraintes:
        if mot in code_saisi:
            return True, mot
    return False, None

def verifier_fonction(nom_fonction, code_saisi, test_entre, resultat_attendu, contraintes=None):
    if contraintes is None:
        contraintes = []

    contournement, mot = detecter_contournements(code_saisi, contraintes)
    if contournement:
        return False, f"❌ Contournement interdit détecté : utilisation de '{mot}'"

    try:
        namespace = {}
        exec(code_saisi, {}, namespace)
    except Exception as e:
        return False, f"❌ Erreur de syntaxe ou d'exécution dans votre code : {e}"

    if nom_fonction not in namespace:
        return False, f"❌ Fonction '{nom_fonction}' non définie dans votre code"

    fonction = namespace[nom_fonction]
    if not callable(fonction):
        return False, f"❌ '{nom_fonction}' n'est pas une fonction appelable"

    if isinstance(test_entre, (tuple, list)):
        args = test_entre
    else:
        args = (test_entre,)

    try:
        resultat = fonction(*args)
    except Exception as e:
        return False, f"❌ Erreur lors de l'exécution de votre fonction : {e}"

    if resultat == resultat_attendu:
        return True, "✅ Correct ! Votre fonction a produit le résultat attendu."
    else:
        return False, f"❌ Résultat incorrect. Attendu : {resultat_attendu}, obtenu : {resultat}"

if __name__ == "__main__":
    code_test = """
def somme(a, b):
    return a + b
"""
    ok, msg = verifier_fonction("somme", code_test, (2, 3), 5, contraintes=["print"])
    print(msg)