import tkinter as tk
from tkinter import messagebox

# Données statiques pour la création de personnage
races = {
    'Humain': {'description': 'Les humains sont polyvalents et adaptables, et se trouvent dans tous les coins du monde.', 'bonus': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1}},
    'Elfe': {'description': 'Les elfes sont graciles, énigmatiques et souvent intrigants.', 'bonus': {'Dextérité': 2, 'Sagesse': 1}},
    'Nain': {'description': 'Les nains sont robustes, fiables et souvent belliqueux.', 'bonus': {'Constitution': 2, 'Sagesse': 1}},
}

classes = {
    'Guerrier': {'description': 'Des combattants experts avec une variété d’armures et d’armes.', 'bonus': {'Force': 2}},
    'Mage': {'description': 'Des lanceurs de sorts étudient les arcanes magiques et lancent des sorts puissants.', 'bonus': {'Intelligence': 2}},
    'Rogue': {'description': 'Des spécialistes des techniques furtives et des attaques sournoises.', 'bonus': {'Dextérité': 2}},
}

historiques = {
    'Acolyte': {'description': 'Vous avez passé votre vie dans un temple à servir un dieu ou une cause religieuse.', 'bonus': {'Sagesse': 1}},
    'Criminel': {'description': 'Vous avez vécu une vie de crimes, soit en tant que voleur, contrebandier ou autre.', 'bonus': {'Dextérité': 1, 'Charisme': 1}},
    'Artisan': {'description': 'Vous avez appris votre métier en tant qu’artisan ou dans un métier de guilde.', 'bonus': {'Force': 1, 'Intelligence': 1}},
}

equipements = {
    'Acolyte': {
        'Bâton de prière': ['Bâton de prière', 'Bâton'],
        'Encens': ['Encens', 'Parfum'],
    },
    'Criminel': {
        'Arme de poing': ['Arme de poing', 'Fronde'],
        'Poignard': ['Poignard', 'Couteau'],
    },
    'Artisan': {
        'Outils d’artisanat': ['Outils d’artisanat', 'Outils'],
        'Tablier de cuir': ['Tablier de cuir', 'Tablier'],
    },
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

# Fonction pour mettre à jour l'affichage des attributs et points disponibles
def update_display():
    for i, attribut in enumerate(attributs_list):
        attribut_labels[i].config(text=f"{attribut}: {attributs_personnage[attribut]}")
    points_label.config(text=f"Points restants: {points_disponibles}")

# Fonction pour valider la répartition des points d'attributs
def valider_repartition():
    global points_disponibles
    if points_disponibles == 0:
        messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
    else:
        messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

# Fonction pour mettre à jour les descriptions en fonction des choix de l'utilisateur
def update_descriptions(*args):
    race_description.config(text=races[race_var.get()]['description'])
    classe_description.config(text=classes[classe_var.get()]['description'])
    historique_description.config(text=historiques[historique_var.get()]['description'])
    equipement_menu['menu'].delete(0, 'end')
    for equip in equipements[historique_var.get()].keys():
        equipement_menu['menu'].add_command(label=equip, command=tk._setit(equipement_var, equip))

# Interface utilisateur avec Tkinter
root = tk.Tk()
root.title("Générateur de Personnages DnD")

# Cadre pour les menus déroulants de sélection
frame_menus = tk.Frame(root)
frame_menus.pack(padx=20, pady=10)

# Menus déroulants pour sélectionner la race, la classe, l'historique et l'équipement
race_var = tk.StringVar(root)
race_var.set('Humain')  # Valeur par défaut
race_label = tk.Label(frame_menus, text="Race:")
race_label.grid(row=0, column=0, sticky='w')
race_menu = tk.OptionMenu(frame_menus, race_var, *races.keys())
race_menu.grid(row=0, column=1, padx=10)
race_var.trace_add('write', update_descriptions)

classe_var = tk.StringVar(root)
classe_var.set('Guerrier')  # Valeur par défaut
classe_label = tk.Label(frame_menus, text="Classe:")
classe_label.grid(row=1, column=0, sticky='w')
classe_menu = tk.OptionMenu(frame_menus, classe_var, *classes.keys())
classe_menu.grid(row=1, column=1, padx=10)
classe_var.trace_add('write', update_descriptions)

historique_var = tk.StringVar(root)
historique_var.set('Acolyte')  # Valeur par défaut
historique_label = tk.Label(frame_menus, text="Historique:")
historique_label.grid(row=2, column=0, sticky='w')
historique_menu = tk.OptionMenu(frame_menus, historique_var, *historiques.keys())
historique_menu.grid(row=2, column=1, padx=10)
historique_var.trace_add('write', update_descriptions)

equipement_var = tk.StringVar(root)
equipement_var.set('Bâton de prière')  # Valeur par défaut
equipement_label = tk.Label(frame_menus, text="Équipement:")
equipement_label.grid(row=3, column=0, sticky='w')
equipement_menu = tk.OptionMenu(frame_menus, equipement_var, *equipements[historique_var.get()].keys())
equipement_menu.grid(row=3, column=1, padx=10)
equipement_var.trace_add('write', update_descriptions)

# Descriptions des choix sélectionnés
race_description_label = tk.Label(frame_menus, text="Description de la Race:")
race_description_label.grid(row=4, column=0, sticky='w', pady=(10, 0))
race_description = tk.Label(frame_menus, text=races[race_var.get()]['description'], wraplength=300, justify='left')
race_description.grid(row=5, column=0, columnspan=2, pady=(0, 10))

classe_description_label = tk.Label(frame_menus, text="Description de la Classe:")
classe_description_label.grid(row=6, column=0, sticky='w', pady=(10, 0))
classe_description = tk.Label(frame_menus, text=classes[classe_var.get()]['description'], wraplength=300, justify='left')
classe_description.grid(row=7, column=0, columnspan=2, pady=(0, 10))

historique_description_label = tk.Label(frame_menus, text="Description de l'Historique:")
historique_description_label.grid(row=8, column=0, sticky='w', pady=(10, 0))
historique_description = tk.Label(frame_menus, text=historiques[historique_var.get()]['description'], wraplength=300, justify='left')
historique_description.grid(row=9, column=0, columnspan=2, pady=(0, 10))

# Bouton pour générer le personnage
generate_button = tk.Button(frame_menus, text="Générer Personnage", command=update_descriptions)
generate_button.grid(row=10, column=0, columnspan=2, pady=(10, 0))

# Cadre pour les attributs du personnage
frame_attributs = tk.Frame(root)
frame_attributs.pack(padx=20, pady=10)

# Affichage des attributs et boutons +/-
attribut_labels = []
for i, attribut in enumerate(attributs_list):
    label = tk.Label(frame_attributs, text=f"{attribut}: {attributs_personnage[attribut]}")
    label.grid(row=i, column=0, sticky='w')
    attribut_labels.append(label)

    button_frame = tk.Frame(frame_attributs)
    button_frame.grid(row=i, column=1)

    plus_button = tk.Button(button_frame, text="-", command=lambda attr=attribut: diminuer_attribut(attr))
    plus_button.pack(side=tk.LEFT)

    minus_button = tk.Button(button_frame, text="+", command=lambda attr=attribut: augmenter_attribut(attr))
    minus_button.pack(side=tk.RIGHT)

# Affichage des points restants
points_label = tk.Label(root, text=f"Points restants: {points_disponibles}")
points_label.pack()

# Bouton pour valider la répartition des points
valider_button = tk.Button(root, text="Valider Répartition", command=valider_repartition)
valider_button.pack(pady=10)

# Lancer l'interface principale
root.mainloop()
