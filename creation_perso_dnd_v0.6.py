import tkinter as tk
from tkinter import messagebox

# Données statiques pour la création de personnage
races = {
    'Humain': {
        'description': 'Les humains sont polyvalents et adaptables, et se trouvent dans tous les coins du monde.',
        'details': [
            'Augmentation de caractéristiques. Force +1, Dextérité +1, Constitution +1, Intelligence +1, Sagesse +1, Charisme +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Langues. commun, une langue de votre choix'
        ],
        'bonus': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1}
    },
    'Elfe': {
        'description': 'Les elfes sont graciles, énigmatiques et souvent intrigants.',
        'details': [
            'Augmentation de caractéristiques. Dextérité +2, Intelligence +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. commun, elfique, une langue de votre choix',
            'Traits. Sens aiguisés *',
            'Ascendance féerique (AV aux JdS vs charme et la magie ne peut pas vous endormir)',
            'Transe (4h de méditation remplacent 8h de sommeil)',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        'bonus': {'Dextérité': 2, 'Intelligence': 1}
    },
    'Nain': {
        'description': 'Les nains sont robustes, fiables et souvent belliqueux.',
        'details': [
            'Augmentation de caractéristiques. Force +2, Constitution +2',
            'Taille. M',
            'Vitesse. 7.5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. commun, nain',
            'Traits. Résistance naine (AV aux JdS vs poison)',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre (bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre)',
            'Formation au port des armures naines'
        ],
        'bonus': {'Force': 2, 'Constitution': 2}
    }
}

classes = {
    'Guerrier': {
        'description': 'Des combattants experts avec une variété d’armures et d’armes.',
        'details': [
            'DV. 1d10',
            'Armures. Toutes les armures, boucliers',
            'Armes. Armes courantes, armes de guerre',
            'Jets de sauvegarde. Force, Constitution',
            'Choix de 2 compétences parmi Acrobaties, Athlétisme, Dressage, Histoire, Intimidation, Intuition, Perception, Survie'
        ],
    },
    'Mage': {
        'description': 'Des lanceurs de sorts étudient les arcanes magiques et lancent des sorts puissants.',
        'details': [
            'DV. 1d6',
            'Armes. Dague, fléchette, fronde, bâton, arbalète légère',
            'Jets de sauvegarde. Intelligence, Sagesse',
            'Choix de 2 compétences parmi Arcanes, Histoire, Intuition, Investigation, Médecine, Religion'
        ],
    },
    'Rogue': {
        'description': 'Des spécialistes des techniques furtives et des attaques sournoises.',
        'details': [
            'DV. 1d8',
            'Armures. Armures légères',
            'Armes. Armes courantes, arbalète de poing, épée courte, épée longue, rapière, arc court',
            'Outils. Outils de voleur',
            'Jets de sauvegarde. Dextérité, Intelligence',
            'Choix de 4 compétences parmi Acrobaties, Athlétisme, Discrétion, Escamotage, Intimidation, Intuition, Investigation, Perception, Persuasion, Représentation, Tromperie'
        ],
    }
}

historiques = {
    'Acolyte': {
        'description': 'Vous avez passé votre vie dans un temple à servir un dieu ou une cause religieuse.',
        'details': [
            'Compétences maîtrisées. Intuition, Religion',
            '2 Langues',
            'Capacité. Abri du fidèle'
        ],
    },
    'Criminel': {
        'description': 'Vous avez vécu une vie de crimes, soit en tant que voleur, contrebandier ou autre.',
        'details': [
            'Compétences maîtrisées. Discrétion, Tromperie',
            '0 Langues',
            'Outils maîtrisés. Jeu, outils de voleur',
            'Capacité. Accointances avec la pègre'
        ],
    },
    'Artisan': {
        'description': 'Vous avez appris votre métier en tant qu’artisan ou dans un métier de guilde.',
        'details': [
            'Compétences maîtrisées. Intuition, Persuasion',
            '1 Langue',
            'Outils maîtrisés. Outil d\'artisan',
            'Capacité. Membre de guilde (soutiens des compagnons de guilde)'
        ],
    }
}

# Liste des attributs du personnage
attributs_list = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']

# Coût de chaque valeur d'attribut
costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}

# Points disponibles pour acheter les attributs
points_disponibles = 27

# Attributs du personnage (initialement à 8)
attributs_personnage = {attr: 8 for attr in attributs_list}

# Fonction pour augmenter une valeur d'attribut
def augmenter_attribut(attribut):
    global points_disponibles
    if points_disponibles > 0:
        current_value = attributs_personnage[attribut]
        next_value = current_value + 1
        if next_value in costs:
            cost = costs[next_value] - costs[current_value]
            if cost <= points_disponibles:
                attributs_personnage[attribut] = next_value
                points_disponibles -= cost
                update_display()
            else:
                messagebox.showwarning("Attention", "Vous n'avez pas suffisamment de points pour augmenter cet attribut.")
        else:
            messagebox.showwarning("Attention", "Cette valeur d'attribut est au maximum permis.")
    else:
        messagebox.showwarning("Attention", "Vous n'avez plus de points disponibles.")

# Fonction pour diminuer une valeur d'attribut
def diminuer_attribut(attribut):
    global points_disponibles
    current_value = attributs_personnage[attribut]
    previous_value = current_value - 1
    if previous_value in costs:
        cost = costs[current_value] - costs[previous_value]
        attributs_personnage[attribut] = previous_value
        points_disponibles += cost
        update_display()
    else:
        messagebox.showwarning("Attention", "Cette valeur d'attribut est au minimum permis.")

# Fonction pour calculer le modificateur d'attribut
def calculer_modificateur(valeur):
    if valeur <= 9:
        return -1
    elif valeur <= 11:
        return 0
    elif valeur <= 13:
        return 1
    elif valeur <= 15:
        return 2
    elif valeur <= 17:
        return 3

# Fonction pour mettre à jour l'affichage des attributs et points disponibles
def update_display():
    for i, attribut in enumerate(attributs_list):
        valeur = attributs_personnage[attribut]
        bonus = races[race_var.get()]['bonus'].get(attribut, 0)
        total = valeur + bonus
        modificateur = calculer_modificateur(total)
        attribut_labels[i].config(text=f"{attribut}")
        attribut_diminuer_buttons[i].config(state=tk.NORMAL)
        attribut_valeur_labels[i].config(text=f"{valeur}")
        attribut_augmenter_buttons[i].config(state=tk.NORMAL)
        attribut_bonus_labels[i].config(text=f"+{bonus}")
        attribut_valeur_finale_labels[i].config(text=f"{total} ({modificateur:+d})")
    points_label.config(text=f"Points restants: {points_disponibles}")

# Fonction pour valider la répartition des points d'attributs
def valider_repartition():
    global points_disponibles
    if points_disponibles == 0:
        messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
    else:
        messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Création de personnage")

# Titre pour la sélection de la race
tk.Label(root, text="Race", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

# Sélection de la race
race_var = tk.StringVar(value=list(races.keys())[0])
tk.Label(root, text="Choisissez une race:").grid(row=1, column=0)
race_menu = tk.OptionMenu(root, race_var, *races.keys())
race_menu.grid(row=1, column=1)

# Description de la race
race_description_label = tk.Label(root, text="", wraplength=400, justify="left")
race_description_label.grid(row=2, column=0, columnspan=2, pady=10)

# Détails de la race
race_details_label = tk.Label(root, text="", wraplength=400, justify="left")
race_details_label.grid(row=3, column=0, columnspan=2, pady=10)

# Titre pour la sélection de la classe
tk.Label(root, text="Classe", font=('Arial', 12, 'bold')).grid(row=4, column=0, columnspan=2, pady=10)

# Sélection de la classe
classe_var = tk.StringVar(value=list(classes.keys())[0])
tk.Label(root, text="Choisissez une classe:").grid(row=5, column=0)
classe_menu = tk.OptionMenu(root, classe_var, *classes.keys())
classe_menu.grid(row=5, column=1)

# Description de la classe
classe_description_label = tk.Label(root, text="", wraplength=400, justify="left")
classe_description_label.grid(row=6, column=0, columnspan=2, pady=10)

# Détails de la classe
classe_details_label = tk.Label(root, text="", wraplength=400, justify="left")
classe_details_label.grid(row=7, column=0, columnspan=2, pady=10)

# Titre pour la sélection de l'historique
tk.Label(root, text="Historique", font=('Arial', 12, 'bold')).grid(row=8, column=0, columnspan=2, pady=10)

# Sélection de l'historique
historique_var = tk.StringVar(value=list(historiques.keys())[0])
tk.Label(root, text="Choisissez un historique:").grid(row=9, column=0)
historique_menu = tk.OptionMenu(root, historique_var, *historiques.keys())
historique_menu.grid(row=9, column=1)

# Description de l'historique
historique_description_label = tk.Label(root, text="", wraplength=400, justify="left")
historique_description_label.grid(row=10, column=0, columnspan=2, pady=10)

# Détails de l'historique
historique_details_label = tk.Label(root, text="", wraplength=400, justify="left")
historique_details_label.grid(row=11, column=0, columnspan=2, pady=10)

# Titre pour la répartition des caractéristiques
tk.Label(root, text="Répartition des caractéristiques", font=('Arial', 12, 'bold')).grid(row=12, column=0, columnspan=6, pady=10)

# Création des labels pour les colonnes
tk.Label(root, text="Caractéristique").grid(row=13, column=0, padx=5, sticky="w")
tk.Label(root, text="").grid(row=13, column=1, padx=5, sticky="w")
tk.Label(root, text="Valeur brute").grid(row=13, column=2, padx=5, sticky="w")
tk.Label(root, text="").grid(row=13, column=3, padx=5, sticky="w")
tk.Label(root, text="Bonus racial").grid(row=13, column=4, padx=5, sticky="w")
tk.Label(root, text="Valeur finale").grid(row=13, column=5, padx=5, sticky="w")

# Configurer les poids des colonnes et fixer la largeur des colonnes
root.grid_columnconfigure(0, weight=2)  # Caractéristique
root.grid_columnconfigure(1, weight=0)  # Diminuer
root.grid_columnconfigure(2, weight=2)  # Valeur brute
root.grid_columnconfigure(3, weight=0)  # Augmenter
root.grid_columnconfigure(4, weight=1)  # Bonus racial
root.grid_columnconfigure(5, weight=2)  # Valeur finale

# Fixer la largeur minimale des colonnes contenant les boutons
root.grid_columnconfigure(1, minsize=20)  # Diminuer
root.grid_columnconfigure(3, minsize=20)  # Augmenter

attribut_labels = []
attribut_valeur_labels = []
attribut_augmenter_buttons = []
attribut_diminuer_buttons = []
attribut_bonus_labels = []
attribut_valeur_finale_labels = []

for i, attribut in enumerate(attributs_list):
    tk.Label(root, text=attribut).grid(row=14+i, column=0, padx=5, sticky="w")
    tk.Button(root, text="-", command=lambda a=attribut: diminuer_attribut(a)).grid(row=14+i, column=1, padx=0, sticky="ew")
    attribut_valeur_label = tk.Label(root, text="")
    attribut_valeur_label.grid(row=14+i, column=2, padx=5, sticky="w")
    tk.Button(root, text="+", command=lambda a=attribut: augmenter_attribut(a)).grid(row=14+i, column=3, padx=0, sticky="ew")
    attribut_bonus_label = tk.Label(root, text="")
    attribut_bonus_label.grid(row=14+i, column=4, padx=5, sticky="w")
    attribut_valeur_finale_label = tk.Label(root, text="")
    attribut_valeur_finale_label.grid(row=14+i, column=5, padx=5, sticky="w")
    
    attribut_labels.append(tk.Label(root, text=attribut))
    attribut_diminuer_buttons.append(tk.Button(root, text="-", command=lambda a=attribut: diminuer_attribut(a)))
    attribut_valeur_labels.append(attribut_valeur_label)
    attribut_augmenter_buttons.append(tk.Button(root, text="+", command=lambda a=attribut: augmenter_attribut(a)))
    attribut_bonus_labels.append(attribut_bonus_label)
    attribut_valeur_finale_labels.append(attribut_valeur_finale_label)


# Points restants
points_label = tk.Label(root, text=f"Points restants: {points_disponibles}")
points_label.grid(row=20, column=0, columnspan=2, pady=10)

# Bouton de validation
tk.Button(root, text="Valider répartition", command=valider_repartition).grid(row=20, column=2, columnspan=2, pady=10)

# Fonction pour mettre à jour la description et les détails de la race sélectionnée
def update_race_details(*args):
    race = races[race_var.get()]
    race_description_label.config(text=race['description'])
    race_details_label.config(text="\n".join(race['details']))
    update_display()

# Fonction pour mettre à jour la description et les détails de la classe sélectionnée
def update_classe_details(*args):
    classe = classes[classe_var.get()]
    classe_description_label.config(text=classe['description'])
    classe_details_label.config(text="\n".join(classe['details']))

# Fonction pour mettre à jour la description et les détails de l'historique sélectionné
def update_historique_details(*args):
    historique = historiques[historique_var.get()]
    historique_description_label.config(text=historique['description'])
    historique_details_label.config(text="\n".join(historique['details']))

# Lier les fonctions de mise à jour aux modifications des menus déroulants
race_var.trace('w', update_race_details)
classe_var.trace('w', update_classe_details)
historique_var.trace('w', update_historique_details)

# Initialiser l'affichage
update_race_details()
update_classe_details()
update_historique_details()
update_display()

# Lancer l'application
root.mainloop()