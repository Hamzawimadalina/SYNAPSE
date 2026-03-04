import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from database import (
    creer_tables, ajouter_utilisateur, get_utilisateur, creer_session,
    get_chapitres, get_exercices_par_chapitre, get_progression_chapitre,
    get_statistiques_globales, get_moyenne_classe
)
# Import des fonctions d'évaluation (seront implémentées par Hamza)
from evaluation import afficher_exercice
from stats import afficher_progression  # pourra être utilisé plus tard
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

utilisateur = None
root = None

# ------------------------- fonctions GUI -------------------------

def couleur_progression(valeur):
    if valeur >= 70: return "green"
    elif valeur >= 40: return "orange"
    else: return "red"

def inscription():
    nom = simpledialog.askstring("Inscription", "Nom :")
    mdp = simpledialog.askstring("Inscription", "Mot de passe :", show="*")
    niveau = simpledialog.askstring("Inscription", "Niveau (1ère/Terminale) :")
    etablissement = simpledialog.askstring("Inscription", "Établissement :")
    ajouter_utilisateur(nom, mdp, niveau, etablissement)
    messagebox.showinfo("Succès", f"Utilisateur {nom} créé !")

def connexion():
    global utilisateur
    nom = simpledialog.askstring("Connexion", "Nom :")
    mdp = simpledialog.askstring("Connexion", "Mot de passe :", show="*")
    user = get_utilisateur(nom, mdp)
    if user:
        creer_session(user[0])
        messagebox.showinfo("Connexion", f"Bienvenue {user[1]} !")
        utilisateur = user
        menu_principal()
    else:
        messagebox.showerror("Erreur", "Nom ou mot de passe incorrect.")

def deconnexion():
    global utilisateur
    utilisateur = None
    messagebox.showinfo("Déconnexion", "Vous êtes déconnecté.")
    root.destroy()
    main_window()

# -------------------- Nouvelle fonction : afficher les exercices d'un chapitre --------------------

def ouvrir_chapitre(chapitre_id, chapitre_nom):
    """Ouvre une nouvelle fenêtre listant les exercices du chapitre."""
    win = tk.Toplevel()
    win.title(f"Exercices - {chapitre_nom}")
    win.geometry("500x400")

    tk.Label(win, text=f"Chapitre : {chapitre_nom}", font=("Arial", 12, "bold")).pack(pady=10)

    # Récupérer les exercices depuis la base
    exercices = get_exercices_par_chapitre(chapitre_id)

    if not exercices:
        tk.Label(win, text="Aucun exercice pour ce chapitre.").pack(pady=20)
    else:
        # Cadre pour la liste des exercices
        frame = tk.Frame(win)
        frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        # En-tête
        tk.Label(frame, text="Liste des exercices", font=("Arial", 10, "underline")).grid(row=0, column=0, columnspan=2, pady=5)

        # Afficher chaque exercice avec un bouton
        for i, exo in enumerate(exercices):
            # exo : (id, type, question, options, reponse_attendue, contraintes)
            exo_id = exo[0]
            exo_type = exo[1]
            exo_question = exo[2][:50] + "..." if len(exo[2]) > 50 else exo[2]

            # Libellé
            tk.Label(frame, text=f"{exo_type} : {exo_question}", anchor="w").grid(row=i+1, column=0, sticky="w", pady=2, padx=5)

            # Bouton "Commencer"
            btn = tk.Button(frame, text="Commencer",
                            command=lambda eid=exo_id: afficher_exercice(eid, utilisateur[0], win))
            btn.grid(row=i+1, column=1, padx=10, pady=2)

    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=10)

# -------------------- barres de progression (simplifiée) -----------------------

def barre_progression(valeur, nom_chapitre):
    """Affiche une petite fenêtre avec la progression (utilisée depuis le menu)."""
    win = tk.Toplevel()
    win.title(f"Progression - {nom_chapitre}")
    tk.Label(win, text=f"Maîtrise du chapitre {nom_chapitre}").pack(pady=10)
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("green.Horizontal.TProgressbar", foreground=couleur_progression(valeur),
                    background=couleur_progression(valeur))
    pb = ttk.Progressbar(win, length=250, mode='determinate', style="green.Horizontal.TProgressbar")
    pb['value'] = valeur
    pb.pack(pady=10)
    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=5)

# -------------------- graphiques matplotlib (provisoire) -----------------------

def afficher_graphique_progression():
    """Affiche un graphique des progressions par chapitre (basé sur les vraies données)."""
    if not utilisateur:
        return
    stats = get_statistiques_globales(utilisateur[0])
    progression_par_chapitre = stats["progression_par_chapitre"]  # liste de (chap_nom, prog)

    fig, ax = plt.subplots(figsize=(6,4))
    noms = [p[0] for p in progression_par_chapitre]
    valeurs = [p[1] for p in progression_par_chapitre]
    couleurs = [couleur_progression(v) for v in valeurs]
    ax.barh(noms, valeurs, color=couleurs)
    ax.set_xlabel("Maîtrise (%)")
    ax.set_title("Progression par chapitre")
    ax.set_xlim(0,100)
    plt.tight_layout()

    win = tk.Toplevel()
    win.title("Graphique de progression")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()
    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=5)

# -------------------- menu principal ------------------------------

def menu_principal():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("SYNAPSE - Menu Principal")
    root.geometry("600x500")

    tk.Label(root, text=f"Bienvenue {utilisateur[1]} !", font=("Arial", 14)).pack(pady=10)

    # Récupérer les chapitres depuis la base (seulement NSI pour l'instant)
    chapitres = get_chapitres("NSI")  # retourne une liste de (id, nom, frequence)

    # Cadre pour les chapitres
    frame_chapitres = tk.Frame(root)
    frame_chapitres.pack(pady=10)

    for chap in chapitres:
        chap_id, chap_nom, chap_freq = chap

        # Sous-cadre pour un chapitre
        sub = tk.Frame(frame_chapitres, relief=tk.GROOVE, bd=2)
        sub.pack(fill=tk.X, padx=20, pady=5)

        # Ligne du haut : nom et bouton "Voir exercices"
        ligne1 = tk.Frame(sub)
        ligne1.pack(fill=tk.X, padx=5, pady=2)
        tk.Label(ligne1, text=chap_nom, font=("Arial", 11, "bold")).pack(side=tk.LEFT)
        tk.Button(ligne1, text="Voir exercices",
                  command=lambda cid=chap_id, cn=chap_nom: ouvrir_chapitre(cid, cn)).pack(side=tk.RIGHT)

        # Barre de progression
        prog = get_progression_chapitre(utilisateur[0], chap_id)
        pb = ttk.Progressbar(sub, length=400, mode='determinate', value=prog)
        pb.pack(pady=5, padx=5)
        # Étiquette avec le pourcentage
        tk.Label(sub, text=f"{prog}% maîtrisé", fg=couleur_progression(prog)).pack()

    # Boutons supplémentaires
    tk.Button(root, text="Afficher graphique progression", command=afficher_graphique_progression).pack(pady=5)
    tk.Button(root, text="Déconnexion", command=deconnexion).pack(pady=10)

    root.mainloop()

# -------------------- fenêtre principale --------------------------

def main_window():
    global root
    root = tk.Tk()
    root.title("SYNAPSE - Connexion/Inscription")
    tk.Label(root, text="Bienvenue sur SYNAPSE !", font=("Arial", 14)).pack(pady=10)
    tk.Button(root, text="Inscription", width=20, command=inscription).pack(pady=5)
    tk.Button(root, text="Connexion", width=20, command=connexion).pack(pady=5)
    tk.Button(root, text="Quitter", width=20, command=root.destroy).pack(pady=10)
    root.mainloop()

# -------------------- lancement --------------------------
if __name__ == "__main__":
    creer_tables()
    main_window()
    