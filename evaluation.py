import tkinter as tk
from tkinter import messagebox, scrolledtext
from database import (
    get_exercice,
    get_notions_par_exercice,
    enregistrer_resultat,
    enregistrer_erreur
)
from code_correction import verifier_fonction
import ast

# Import de la remédiation (à implémenter par Nada)
# from remediation import afficher_remediation

def afficher_exercice(exercice_id, utilisateur_id):
    """
     afficher un exercice et évaluer la réponse.
    """
    # Récupérer les données de l'exercice
    exo = get_exercice(exercice_id)
    if not exo:
        messagebox.showerror("Erreur", "Exercice introuvable.")
        return

    # Structure de l'exercice (selon database.py)
    # id, id_chapitre, type, question, options, reponse_attendue, contraintes, nom_fonction, test_input, test_output
    # Indices : 0:id, 1:id_chapitre, 2:type, 3:question, 4:options, 5:reponse_attendue, 6:contraintes,
    #           7:nom_fonction, 8:test_input, 9:test_output
    type_exo = exo[2]
    question = exo[3]
    options = exo[4]          # pour QCM
    reponse_attendue = exo[5] # pour QCM et trous
    contraintes = exo[6]      # pour code
    nom_fonction = exo[7]     # pour code
    test_input = exo[8]       # pour code
    test_output = exo[9]      # pour code

    # Récupérer les notions liées à cet exercice
    notions_ids = get_notions_par_exercice(exercice_id)

    # Créer une nouvelle fenêtre
    fenetre = tk.Toplevel()
    fenetre.title(f"Exercice {exercice_id}")
    fenetre.geometry("600x500")

    # Afficher la question
    tk.Label(fenetre, text=question, font=("Arial", 12, "bold"), wraplength=550).pack(pady=10)

    # Variable pour stocker la réponse de l'utilisateur
    reponse_var = tk.StringVar()
    resultat_id = None  # sera défini après enregistrement

    # Fonction appelée lors de la soumission
    def soumettre():
        nonlocal resultat_id
        reussi = False
        message = ""

        # Évaluation selon le type
        if type_exo == "QCM":
            choix = reponse_var.get()
            if not choix:
                messagebox.showwarning("Attention", "Veuillez sélectionner une réponse.")
                return
            # comparer avec l'indice de la bonne réponse (stocké dans reponse_attendue)
            try:
                reussi = (int(choix) == int(reponse_attendue))
            except:
                reussi = False
            if reussi:
                message = "✅ Correct !"
            else:
                # Récupérer la bonne réponse textuelle
                options_list = options.split(";")
                bonne_option = options_list[int(reponse_attendue)] if options_list else "inconnue"
                message = f"❌ Incorrect. La bonne réponse était : {bonne_option}"

        elif type_exo == "trous":
            reponse = reponse_var.get().strip()
            reussi = (reponse == reponse_attendue)
            if reussi:
                message = "✅ Correct !"
            else:
                message = f"❌ Incorrect. La bonne réponse était : {reponse_attendue}"

        elif type_exo == "code":
            code = reponse_var.get()  # zone de texte multiligne
            # Évaluer le code avec la fonction de vérification
            try:
                # Convertir test_input et test_output en objets Python
                input_val = ast.literal_eval(test_input) if test_input else None
                output_val = ast.literal_eval(test_output) if test_output else None
                # Appeler verifier_fonction
                reussi, msg = verifier_fonction(
                    nom_fonction=nom_fonction,
                    code_saisi=code,
                    test_entre=input_val,
                    resultat_attendu=output_val,
                    contraintes=contraintes.split(",") if contraintes else []
                )
                message = msg
            except Exception as e:
                message = f"Erreur lors de l'évaluation : {e}"
                reussi = False

        elif type_exo == "texte":
            # Pas de correction automatique, on considère que c'est toujours réussi ? À discuter.
            reponse = reponse_var.get()
            # Pour l'instant, on considère que l'utilisateur a réussi s'il a écrit quelque chose
            reussi = bool(reponse.strip())
            message = "Réponse enregistrée (non évaluée automatiquement)."
        else:
            messagebox.showerror("Erreur", f"Type d'exercice inconnu : {type_exo}")
            return

        # Enregistrer le résultat dans la base
        resultat_id = enregistrer_resultat(utilisateur_id, exercice_id, reussi)

        # Si échec, enregistrer les erreurs pour chaque notion
        if not reussi and notions_ids:
            for notion_id in notions_ids:
                enregistrer_erreur(resultat_id, notion_id)

        # Afficher le message de résultat
        messagebox.showinfo("Résultat", message)

        # Si échec, appeler la remédiation
        if not reussi:
            # Fermer la fenêtre actuelle ? Optionnel.
            fenetre.destroy()
            # Appeler la fonction de remédiation (à implémenter par Nada)
            # from remediation import afficher_remediation
            # afficher_remediation(notions_ids, exercice_id, utilisateur_id)
        else:
            # Si réussi, on peut simplement fermer ou proposer de continuer
            if messagebox.askyesno("Succès", "Bravo ! Voulez-vous continuer ?"):
                fenetre.destroy()
            else:
                fenetre.destroy()

    # Interface selon le type
    if type_exo == "QCM":
        # Afficher les options sous forme de boutons radio
        options_list = options.split(";")
        for i, opt in enumerate(options_list):
            tk.Radiobutton(fenetre, text=opt, variable=reponse_var, value=str(i)).pack(anchor="w", padx=20)

    elif type_exo == "trous":
        tk.Entry(fenetre, textvariable=reponse_var, width=50).pack(pady=10)

    elif type_exo == "code":
        # Zone de texte multiligne
        text_area = scrolledtext.ScrolledText(fenetre, height=15, width=70)
        text_area.pack(pady=10)
        # Lier la variable au contenu (on peut récupérer avec text_area.get("1.0", tk.END))
        # On utilisera une fonction pour extraire le texte au moment de la soumission
        def get_code():
            return text_area.get("1.0", tk.END).strip()
        # On redéfinit soumettre pour utiliser get_code
        def soumettre_code():
            nonlocal resultat_id
            code = get_code()
            reponse_var.set(code)  # on stocke dans la variable pour y accéder dans soumettre
            soumettre()
        # On remplace le bouton de soumission par un appel à soumettre_code
        tk.Button(fenetre, text="Soumettre", command=soumettre_code).pack(pady=10)
        # Pour éviter d'avoir deux boutons, on ne crée pas le bouton général tout de suite
        # On sort de la structure classique
        # On va plutôt gérer le cas code à part
        # On met un bouton ici et on retourne pour éviter le bouton général
        return  # On sort car on a déjà créé le bouton spécifique

    elif type_exo == "texte":
        # Zone de texte libre
        text_area = scrolledtext.ScrolledText(fenetre, height=10, width=70)
        text_area.pack(pady=10)
        def get_texte():
            return text_area.get("1.0", tk.END).strip()
        def soumettre_texte():
            nonlocal resultat_id
            texte = get_texte()
            reponse_var.set(texte)
            soumettre()
        tk.Button(fenetre, text="Soumettre", command=soumettre_texte).pack(pady=10)
        return

    # Bouton de soumission pour les types QCM et trous
    if type_exo in ("QCM", "trous"):
        tk.Button(fenetre, text="Soumettre", command=soumettre).pack(pady=10)

    # Bouton annuler
    tk.Button(fenetre, text="Annuler", command=fenetre.destroy).pack(pady=5)

    # Pour les types code et texte, on a déjà géré le bouton et on est sorti,
    # donc on ne doit pas exécuter la suite.
    # On peut structurer autrement, mais pour simplifier on laisse comme ça.

    fenetre.mainloop()