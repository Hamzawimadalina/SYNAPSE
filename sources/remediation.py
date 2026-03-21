import tkinter as tk
from database import connexion_db

FICHES = {
    "Tri rapide": "Le tri rapide a une complexité moyenne de O(n log n). Il choisit un pivot et partitionne.",
    "Tri bulle": "Le tri bulle compare les éléments adjacents et les échange si nécessaire. Complexité O(n²).",
    "Boucle for": "La boucle for permet d'itérer sur les éléments d'une séquence (liste, tuple, etc.).",
    "Requête SELECT": "SELECT colonnes FROM table WHERE condition ; permet de récupérer des données.",
    "Classe et objet": "Une classe est un modèle, un objet en est une instance. Utilisez le mot-clé 'class'.",
    "Fonction récursive": "Une fonction récursive s'appelle elle-même. Elle doit avoir un cas de base.",
}

def get_nom_notion(notion_id):
    conn = connexion_db()
    c = conn.cursor()
    c.execute("SELECT nom FROM Notion WHERE id=?", (notion_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def afficher_remediation(notions_ids, exercice_id, utilisateur_id):
    noms_notions = []
    for nid in notions_ids:
        nom = get_nom_notion(nid)
        if nom:
            noms_notions.append(nom)

    win = tk.Toplevel()
    win.title("Remédiation")
    win.geometry("500x400")

    tk.Label(win, text="Notions à retravailler :", font=("Arial", 12, "bold")).pack(pady=10)

    for nom in noms_notions:
        cadre = tk.Frame(win, relief=tk.GROOVE, bd=2)
        cadre.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(cadre, text=nom, font=("Arial", 10, "bold"), fg="red").pack(anchor="w", padx=5)
        texte_fiche = FICHES.get(nom, "Pas de fiche disponible pour cette notion.")
        tk.Label(cadre, text=texte_fiche, wraplength=450, justify="left").pack(anchor="w", padx=5, pady=2)

    def reessayer():
        win.destroy()
        from evaluation import afficher_exercice
        afficher_exercice(exercice_id, utilisateur_id)

    tk.Button(win, text="Réessayer l'exercice", command=reessayer, bg="lightblue").pack(pady=20)
    tk.Button(win, text="Fermer", command=win.destroy).pack(pady=5)

if __name__ == "__main__":
    # Test
    afficher_remediation([1, 2], 1, 1)