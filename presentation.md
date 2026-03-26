# SYNAPSE – L’apprentissage qui s’adapte à tes erreurs

## Présentation globale du projet
**SYNAPSE** est une application d’entraînement destinée aux lycéens de première et terminale suivant la spécialité NSI.  
Inspirée des mécanismes naturels d’apprentissage (plasticité cérébrale), elle analyse chaque erreur pour adapter le parcours de l’élève en temps réel. Plutôt que de simplement sanctionner, elle transforme l’erreur en signal de progression : l’élève reçoit une fiche de révision ciblée et peut réessayer l’exercice.

Le projet répond au thème **« Nature & Informatique »** en modélisant un système vivant :
- Détection des lacunes (comme un cerveau identifie ses faiblesses),
- Adaptation personnalisée (renforcement des acquis),
- Croissance organique (progression sous forme de chemin non linéaire).

### Public cible
- Élèves de première et terminale (spécialité NSI),
- Établissements scolaires souhaitant suivre la progression des élèves,
- Réseaux éducatifs (type AEFE) pour des analyses globales.

## Organisation du travail
L’équipe est composée de trois élèves :

- **Malek Hassen** – Responsable de l’interface et de la présentation  
  Développement du point d’entrée (`main.py`), gestion des sessions (connexion/inscription), création du module parcours et des statistiques, conception de l’interface graphique Tkinter, rédaction des fiches de révision (contenu pédagogique).

- **Hamza** – Chef d’équipe, responsable technique  
  Coordination du groupe, conception de la base de données (`database.py` – tables SQLite, opérations CRUD, calcul des moyennes), développement du module de correction automatique (`code_correction.py` – détection de contournements, exécution sécurisée), création des utilitaires (`utils.py` – hachage des mots de passe), rédaction de la documentation (README, licence, requirements.txt).

- **Nada** – Responsable de l’évaluation et de la remédiation  
  Implémentation du moteur d’évaluation (`evaluation.py` – QCM, trous, code, texte), intégration de la remédiation (`remediation.py` – affichage des fiches, bouton « Réessayer »), enregistrement des résultats et des erreurs en base de données.

## Étapes de réalisation
1. **Réflexion initiale** : définir une approche basée sur l’analyse des erreurs et l’adaptation.
2. **Architecture modulaire** : séparer les responsabilités (base, interface, évaluation, remédiation).
3. **Développement progressif** :
   - Gestion des comptes et sessions (console, puis Tkinter),
   - Affichage des parcours et des exercices,
   - Moteur d’évaluation pour les différents types d’exercices,
   - Remédiation et statistiques,
   - Tests et améliorations itératives.
4. **Documentation** : préparation du dossier de candidature (dossier technique, vidéo, résumé).

## Difficultés rencontrées et solutions
- **Structuration du code en modules** : nous avons utilisé des imports bien définis et une séparation claire des responsabilités pour éviter les dépendances circulaires.
- **Correction automatique du code Python** : nécessité d’exécuter le code élève dans un espace de noms isolé (`exec` avec dictionnaire vide) et de détecter les contournements (mots interdits).
- **Interface graphique** : nous avons dû apprendre Tkinter en autonomie, ce qui a demandé des recherches et des tests approfondis.
- **Gestion des données et statistiques** : nous avons ajusté les requêtes SQL pour garantir des résultats cohérents (moyennes par classe et par établissement).

## Ouverture et améliorations futures
- **Moteur d’exercices enrichi** : intégrer davantage de chapitres de NSI et de mathématiques (étude de fonctions, géométrie dans l’espace, intégration…).
- **Analyse des erreurs plus fine** : proposer des fiches encore plus personnalisées en fonction des notions réellement mal comprises.
- **Version web** : transformer le prototype en application web pour une accessibilité plus large.
- **Version mobile** : développer une application mobile pour un usage nomade.

SYNAPSE constitue une base solide, et nous savons exactement dans quelle direction l’emmener.