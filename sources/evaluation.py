import tkinter as tk
from tkinter import messagebox, scrolledtext
import ast

from database import (
    get_exercice,
    get_notions_par_exercice,
    enregistrer_resultat,
    enregistrer_erreur
)
from code_correction import verifier_fonction
from remediation import afficher_remediation


def afficher_exercice(exercice_id, utilisateur_id):
    """
    Affiche un exercice dans une nouvelle fenêtre et évalue la réponse.
    """
    exo = get_exercice(exercice_id)
    if not exo:
        messagebox.showerror("Erreur", "Exercice introuvable.")
        return

    (_, id_chapitre, type_exo, question, options, reponse_attendue,
     contraintes, nom_fonction, test_input, test_output) = exo

    notions_ids = get_notions_par_exercice(exercice_id)

    fenetre = tk.Toplevel()
    fenetre.title(f"Exercice {exercice_id}")
    fenetre.geometry("600x500")
    fenetre.resizable(False, False)

    tk.Label(fenetre, text=question, font=("Arial", 12, "bold"),
             wraplength=550, justify="left").pack(pady=10, padx=20)

    input_frame = tk.Frame(fenetre)
    input_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

    reponse_var = tk.StringVar()
    reponse_text = None

    if type_exo == "QCM":
        options_list = options.split(";")
        for i, opt in enumerate(options_list):
            rb = tk.Radiobutton(input_frame, text=opt, variable=reponse_var,
                                value=str(i), font=("Arial", 10))
            rb.pack(anchor="w", pady=2)

    elif type_exo == "trous":
        entry = tk.Entry(input_frame, textvariable=reponse_var, width=50)
        entry.pack(pady=10)

    elif type_exo == "code":
        reponse_text = scrolledtext.ScrolledText(input_frame, height=15, width=70,
                                                  wrap=tk.NONE, font=("Courier", 10))
        reponse_text.pack(fill=tk.BOTH, expand=True)

    elif type_exo == "texte":
        reponse_text = scrolledtext.ScrolledText(input_frame, height=10, width=70,
                                                  wrap=tk.WORD, font=("Arial", 10))
        reponse_text.pack(fill=tk.BOTH, expand=True)

    else:
        messagebox.showerror("Erreur", f"Type d'exercice inconnu : {type_exo}")
        fenetre.destroy()
        return

    def soumettre():
        if type_exo in ("QCM", "trous"):
            reponse = reponse_var.get().strip()
            if not reponse:
                messagebox.showwarning("Attention", "Veuillez saisir une réponse.")
                return
        elif type_exo in ("code", "texte"):
            reponse = reponse_text.get("1.0", tk.END).strip()
            if not reponse:
                messagebox.showwarning("Attention", "Veuillez écrire quelque chose.")
                return

        reussi = False
        message = ""

        if type_exo == "QCM":
            try:
                choix = int(reponse)
                reussi = (choix == int(reponse_attendue))
            except ValueError:
                reussi = False
            if reussi:
                message = "✅ Correct !"
            else:
                options_list = options.split(";")
                bonne = options_list[int(reponse_attendue)] if options_list else "inconnue"
                message = f"❌ Incorrect. La bonne réponse était : {bonne}"

        elif type_exo == "trous":
            reussi = (reponse == reponse_attendue)
            if reussi:
                message = "✅ Correct !"
            else:
                message = f"❌ Incorrect. La bonne réponse était : {reponse_attendue}"

        elif type_exo == "code":
            try:
                input_val = ast.literal_eval(test_input) if test_input else None
                output_val = ast.literal_eval(test_output) if test_output else None
                reussi, msg = verifier_fonction(
                    nom_fonction=nom_fonction,
                    code_saisi=reponse,
                    test_entre=input_val,
                    resultat_attendu=output_val,
                    contraintes=contraintes.split(",") if contraintes else []
                )
                message = msg
            except Exception as e:
                message = f"❌ Erreur lors de l'évaluation : {e}"
                reussi = False

        elif type_exo == "texte":
            reussi = True
            message = "Réponse enregistrée (non évaluée automatiquement)."

        resultat_id = enregistrer_resultat(utilisateur_id, exercice_id, reussi)

        if not reussi and notions_ids:
            for notion_id in notions_ids:
                enregistrer_erreur(resultat_id, notion_id)

        messagebox.showinfo("Résultat", message)
        fenetre.destroy()

        if not reussi:
            afficher_remediation(notions_ids, exercice_id, utilisateur_id)

    bouton_frame = tk.Frame(fenetre)
    bouton_frame.pack(pady=10)

    tk.Button(bouton_frame, text="Soumettre", command=soumettre,
              bg="lightblue", width=15).pack(side=tk.LEFT, padx=5)
    tk.Button(bouton_frame, text="Annuler", command=fenetre.destroy,
              width=15).pack(side=tk.LEFT, padx=5)

    fenetre.mainloop()