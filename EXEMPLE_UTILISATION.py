from code_correction import verifier_fonction

# Exemple simple : fonction somme_deux
code_etudiant = """
def somme_deux(a, b):
    return a + b
"""

nom_fonction = "somme_deux"
entrees_test = (2, 3)
resultat_attendu = 5
contraintes = ["print", "max", "min"]

ok, message = verifier_fonction(nom_fonction, code_etudiant, entrees_test, resultat_attendu, contraintes)
print(message)
