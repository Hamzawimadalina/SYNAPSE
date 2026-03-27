from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import os

from database import (
    creer_tables, inserer_donnees_test, ajouter_utilisateur, get_utilisateur, creer_session,
    get_chapitres, get_exercices_par_chapitre, get_progression_chapitre,
    get_statistiques_globales, get_moyenne_classe, get_moyenne_etablissement
)
from evaluation import afficher_exercice
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

utilisateur = None
root = None

# ------------------------- fonctions GUI -------------------------

def couleur_progression(valeur):
    if valeur >= 70: return "green"
    elif valeur >= 40: return "orange"
    else: return "red"

def emoji_frequence(frequence):
    if frequence == "forte":
        return "🔴"
    elif frequence == "moyenne":
        return "🟠"
    else:
        return "🟢"

def inscription():
    nom = simpledialog.askstring("Inscription", "Nom :")
    mdp = simpledialog.askstring("Inscription", "Mot de passe :", show="*")
    niveau = simpledialog.askstring("Inscription", "Niveau (1ère/Terminale) :")
    etablissement = simpledialog.askstring("Inscription", "Établissement :")
    if not (nom and mdp and niveau and etablissement):
        messagebox.showwarning("Attention", "Tous les champs sont obligatoires.")
        return
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

# -------------------- Liste des exercices d'un chapitre --------------------

def ouvrir_chapitre(chapitre_id, chapitre_nom):
    win = tk.Toplevel()
    win.title(f"Exercices - {chapitre_nom}")
    win.geometry("600x500")

    tk.Label(win, text=f"Chapitre : {chapitre_nom}", font=("Arial", 12, "bold")).pack(pady=10)

    exercices = get_exercices_par_chapitre(chapitre_id)

    if not exercices:
        tk.Label(win, text="Aucun exercice pour ce chapitre.").pack(pady=20)
    else:
        canvas = tk.Canvas(win)
        scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

        tk.Label(scrollable_frame, text="Liste des exercices", font=("Arial", 10, "underline")).grid(row=0, column=0, columnspan=2, pady=5)

        for i, exo in enumerate(exercices):
            exo_id = exo[0]
            exo_type = exo[2]
            exo_question = exo[3][:50] + "..." if len(exo[3]) > 50 else exo[3]

            tk.Label(scrollable_frame, text=f"{exo_type} : {exo_question}", anchor="w").grid(
                row=i+1, column=0, sticky="w", pady=2, padx=5)

            btn = tk.Button(scrollable_frame, text="Commencer",
                            command=lambda eid=exo_id: afficher_exercice(eid, utilisateur[0]))
            btn.grid(row=i+1, column=1, padx=10, pady=2)

    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=10)

# -------------------- Statistiques détaillées --------------------

def afficher_statistiques():
    if not utilisateur:
        return
    stats = get_statistiques_globales(utilisateur[0])

    win = tk.Toplevel()
    win.title("Mes statistiques")
    win.geometry("700x600")

    tk.Label(win, text="Statistiques globales", font=("Arial", 14, "bold")).pack(pady=10)

    frame_global = tk.Frame(win, relief=tk.GROOVE, bd=2)
    frame_global.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(frame_global, text=f"Exercices tentés : {stats['total_exercices']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(frame_global, text=f"Réussis : {stats['total_reussis']}").pack(anchor="w", padx=10, pady=2)
    tk.Label(frame_global, text=f"Taux de réussite : {stats['taux_reussite']}%").pack(anchor="w", padx=10, pady=2)

    tk.Label(win, text="Progression par chapitre", font=("Arial", 12, "bold")).pack(pady=10)

    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10)
    scrollbar.pack(side="right", fill="y")

    chapitres = get_chapitres("NSI")
    nom_vers_id = {chap[1]: chap[0] for chap in chapitres}

    for chap_nom, prog in stats['progression_par_chapitre']:
        chap_id = nom_vers_id.get(chap_nom)
        if chap_id:
            moyenne_classe = get_moyenne_classe(utilisateur[0], chap_id)
            moyenne_etablissement = get_moyenne_etablissement(utilisateur[0], chap_id)
        else:
            moyenne_classe = 50
            moyenne_etablissement = 50

        cadre = tk.Frame(scrollable_frame, relief=tk.GROOVE, bd=2)
        cadre.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(cadre, text=chap_nom, font=("Arial", 10, "bold")).pack(anchor="w", padx=5)

        pb = ttk.Progressbar(cadre, length=300, mode='determinate', value=prog)
        pb.pack(pady=2, padx=5)
        tk.Label(cadre, text=f"Vous : {prog}%", fg=couleur_progression(prog)).pack(anchor="w", padx=5)
        tk.Label(cadre, text=f"Moyenne de la classe : {moyenne_classe}%").pack(anchor="w", padx=5)
        tk.Label(cadre, text=f"Moyenne établissement : {moyenne_etablissement}%").pack(anchor="w", padx=5)

    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=10)

# -------------------- Graphique de progression --------------------

def afficher_graphique_progression():
    if not utilisateur:
        return
    stats = get_statistiques_globales(utilisateur[0])
    progression_par_chapitre = stats["progression_par_chapitre"]

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

# -------------------- Cours et ressources --------------------

def afficher_cours():
    dossier_cours = "cours_images"
    
    # Créer le dossier s'il n'existe pas
    if not os.path.exists(dossier_cours):
        os.makedirs(dossier_cours)
        messagebox.showinfo("Initialisation", "Le dossier 'cours_images' a été créé. Ajoutez vos images (PNG, JPG, GIF) et réessayez.")
        return

    extensions = (".png", ".jpg", ".jpeg", ".gif")
    images = [f for f in os.listdir(dossier_cours) if f.lower().endswith(extensions)]
    
    if not images:
        messagebox.showinfo("Info", "Aucune image trouvée dans 'cours_images'.")
        return

    win = tk.Toplevel()
    win.title("Cours et ressources")
    win.geometry("800x600")
    
    canvas = tk.Canvas(win)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)
    
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Garder une référence des images pour éviter le garbage collector
    win.image_refs = []

    for img_file in images:
        path = os.path.join(dossier_cours, img_file)
        try:
            img = Image.open(path)
            # Redimensionner pour une largeur max de 700 pixels (hauteur proportionnelle)
            ratio = 700 / img.size[0]
            new_height = int(img.size[1] * ratio)
            img = img.resize((700, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            win.image_refs.append(photo)  # Stocker la référence

            # Afficher l'image dans un cadre avec son nom
            frame = tk.Frame(scrollable_frame, bd=2, relief=tk.GROOVE)
            frame.pack(pady=10, padx=10, fill=tk.X)
            tk.Label(frame, text=img_file, font=("Arial", 10, "bold")).pack()
            lbl = tk.Label(frame, image=photo)
            lbl.image = photo  # Référence supplémentaire
            lbl.pack()
        except Exception as e:
            print(f"Erreur chargement {img_file} : {e}")
    
    tk.Button(win, text="Fermer la bibliothèque", command=win.destroy, bg="indianred", fg="white").pack(pady=10)

# -------------------- Menu principal ------------------------------

def menu_principal():
    global root
    root.destroy()
    root = tk.Tk()
    root.title("SYNAPSE - Menu Principal")
    root.geometry("700x600")

    tk.Label(root, text=f"Bienvenue {utilisateur[1]} !", font=("Arial", 14)).pack(pady=10)

    chapitres = get_chapitres("NSI")
    if not chapitres:
        tk.Label(root, text="Aucun chapitre trouvé. Vérifiez que la base est initialisée.", fg="red").pack()
        tk.Button(root, text="Retour", command=deconnexion).pack()
        return

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    scrollbar.pack(side="right", fill="y")

    for chap in chapitres:
        chap_id, chap_nom, chap_freq = chap
        sub = tk.Frame(scrollable_frame, relief=tk.GROOVE, bd=2)
        sub.pack(fill=tk.X, padx=10, pady=5)

        ligne1 = tk.Frame(sub)
        ligne1.pack(fill=tk.X, padx=5, pady=2)

        emoji = emoji_frequence(chap_freq)
        tk.Label(ligne1, text=f"{emoji} {chap_nom}", font=("Arial", 11, "bold")).pack(side=tk.LEFT)

        tk.Button(ligne1, text="Voir exercices",
                  command=lambda cid=chap_id, cn=chap_nom: ouvrir_chapitre(cid, cn)).pack(side=tk.RIGHT)

        prog = get_progression_chapitre(utilisateur[0], chap_id)
        pb = ttk.Progressbar(sub, length=400, mode='determinate', value=prog)
        pb.pack(pady=5, padx=5)
        tk.Label(sub, text=f"{prog}% maîtrisé", fg=couleur_progression(prog)).pack()

    frame_boutons = tk.Frame(root)
    frame_boutons.pack(pady=10)

    tk.Button(frame_boutons, text="Graphique progression",
              command=afficher_graphique_progression, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_boutons, text="Statistiques détaillées",
              command=afficher_statistiques, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_boutons, text="Cours (fiches)",
              command=afficher_cours, width=20).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_boutons, text="Déconnexion",
              command=deconnexion, width=20).pack(side=tk.LEFT, padx=5)

    root.mainloop()

# -------------------- Fenêtre principale (connexion/inscription) ---

def main_window():
    global root
    root = tk.Tk()
    root.title("SYNAPSE - Connexion/Inscription")
    root.geometry("400x300")

    tk.Label(root, text="Bienvenue sur SYNAPSE !", font=("Arial", 14)).pack(pady=20)

    tk.Button(root, text="Inscription", width=20, command=inscription).pack(pady=5)
    tk.Button(root, text="Connexion", width=20, command=connexion).pack(pady=5)
    tk.Button(root, text="Quitter", width=20, command=root.destroy).pack(pady=10)

    root.mainloop()

# -------------------- Lancement --------------------------

if __name__ == "__main__":
    creer_tables()
    inserer_donnees_test()
    main_window()
