import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


# Données statiques pour la création de personnage
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
        'capacite': [
            'Second souffle: Une fois par repos court ou long, vous pouvez utiliser une action bonus pour regagner un nombre de points de vie égal à 1d10 + votre niveau.',
            'Style de combat: Vous choisissez un style de combat qui vous accorde des avantages en combat.'
        ],
        'outils': [],
        'langues': []
    },
    'Mage': {
        'description': 'Des lanceurs de sorts étudient les arcanes magiques et lancent des sorts puissants.',
        'details': [
            'DV. 1d6',
            'Armes. Dague, fléchette, fronde, bâton, arbalète légère',
            'Jets de sauvegarde. Intelligence, Sagesse',
            'Choix de 2 compétences parmi Arcanes, Histoire, Intuition, Investigation, Médecine, Religion'
        ],
        'capacite': [
            'Incantation: Vous pouvez lancer des sorts de votre liste de sorts.',
            'Restauration arcanique (1/jour): Vous récupérez un nombre d’emplacements de sorts égal à [niv/2] (maximum niveau 5).'
        ],
        'outils': [],
        'langues': []
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
        'capacite': [
            'Expertise: Vous doublez votre bonus de compétence pour deux compétences ou outils de votre choix.',
            'Attaque sournoise: Une fois par tour, vous pouvez infliger des dégâts supplémentaires à une cible que vous attaquez avec une arme de finesse ou à distance si vous avez l’avantage à l’attaque ou si un allié est à portée de mêlée de la cible.',
            'Jargon des voleurs: Vous pouvez comprendre et parler le jargon des voleurs, un langage secret utilisé par les criminels.'
        ],
        'outils': ['Outils de voleur'],
        'langues': []
    }
}

races = {
    'Humain': {
        'description': 'Les Humains sont polyvalents et adaptables, avec une grande capacité à s’intégrer dans diverses cultures.',
        'details': [
    'Augmentation de caractéristiques. Force +1, Dextérité +1, Constitution +1, Intelligence +1, Sagesse +1, Charisme +1',
    'Taille. M',
    'Vitesse. 9 m/round',
    'Langues. commun, une langue de votre choix'
    ],
    'bonus': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1},
        'compétences': [],
        'outils': [],
        'langues': ['Commun', 'Une langue supplémentaire au choix']
    },
    'Elfe': {
        'description': 'Les Elfes sont des êtres agiles et gracieux, dotés d’une longue durée de vie et de sens aiguisés.',
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
        'bonus': {'Dextérité': 2, 'Intelligence': 1},
        'compétences': [],
        'outils': [],
        'langues': ['Commun', 'Elfique', 'Une langue supplémentaire au choix']
    },
    'Nain': {
        'description': 'Robustes et endurants, les Nains sont des artisans habiles avec une grande résistance.',
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
        'bonus': {'Force': 2, 'Constitution': 2},
        'compétences': [],
        'outils': ['Matériel de forgeron', 'Matériel de brasseur', 'Matériel de maçon'],
        'langues': ['Commun', 'Nain']
    }
}

historiques = {
    'Criminel': {
        'description': 'Les criminels possèdent des compétences spécifiques pour les activités illicites.',
        'details': [
            'Compétences. Choix de 2 compétences parmi Acrobaties, Discrétion, Escamotage, Intimidation, Tromperie'
        ],
        'compétences': ['Acrobaties', 'Discrétion', 'Escamotage', 'Intimidation', 'Tromperie'],
        'outils': ['Dés', 'Jeu d’échecs draconiques', 'Jeu de cartes', 'Jeu des Dragons'],
        'langues': []
    },
    'Artisan': {
        'description': 'Les artisans possèdent une expertise particulière dans divers outils et matériaux.',
        'details': [
            'Langues. Une langue supplémentaire au choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Artisanat, Histoire, Investigation, Médecine, Nature',
            'Outils. choix d\'un outil spécifique à une profession'
        ],
        'compétences': ['Arcanes', 'Artisanat', 'Histoire', 'Investigation', 'Médecine', 'Nature'],
        'outils': ['Matériel d’alchimie', 'Matériel de brasseur', 'Matériel de calligraphe', 'Matériel de peintre', 'Matériel de bijoutier', 'Matériel de bricoleur', 'Matériel de cartographe', 'Matériel de charpentier', 'Matériel de cordonnier', 'Matériel de forgeron', 'Matériel de maçon', 'Matériel de menuisier', 'Matériel de potier', 'Matériel de souffleur de verre', 'Matériel de Tanneur', 'Matériel de tisserand', 'Matériel de cuisinier'],
        'langues': ['Une langue supplémentaire au choix']
    },
    'Acolyte': {
        'description': 'Les acolytes ont une formation religieuse approfondie et des compétences dans les rituels et le culte.',
        'details': [
            'Langues. Deux langues supplémentaires aux choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Histoire, Médecine, Religion'
        ],
        'compétences': ['Arcanes', 'Histoire', 'Médecine', 'Religion'],
        'outils': [],
        'langues': ['Deux langues supplémentaires au choix']
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
        
        attribut_valeur_labels[i].config(text=f"{valeur}", anchor="center")
        attribut_bonus_labels[i].config(text=f"{bonus:+d}", anchor="center")
        attribut_valeur_finale_labels[i].config(text=f"{total} ({modificateur:+d})", anchor="center")
    
    points_label.config(text=f"Points restants: {points_disponibles}")

# Fonction pour valider la répartition des points d'attributs
def valider_repartition():
    global points_disponibles
    if points_disponibles == 0:
        messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
    else:
        messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

# Fonction pour mettre à jour les capacités de classe
def update_capacites_classe(*args):
    classe = classes[classe_var.get()]
    capacites_classe_label.config(text="\n".join(classe['capacite']))
    
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

# Création de la fenêtre principale
root = tk.Tk()
root.title("Création de personnage")

# Création du widget Notebook
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, sticky='nsew')

# Onglet Race
race_tab = ttk.Frame(notebook)
notebook.add(race_tab, text='Race')

tk.Label(race_tab, text="Race", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
tk.Label(race_tab, text="Choisissez une race:").grid(row=1, column=0)
race_var = tk.StringVar(value=list(races.keys())[0])
race_menu = tk.OptionMenu(race_tab, race_var, *races.keys())
race_menu.grid(row=2, column=0)

race_description_label = tk.Label(race_tab, text="", wraplength=400, justify="left")
race_description_label.grid(row=3, column=0, pady=10)
race_details_label = tk.Label(root, text="", wraplength=400, justify="left")
race_details_label.grid(row=6, column=0, columnspan=2, pady=10)

# Onglet Classe
classe_tab = ttk.Frame(notebook)
notebook.add(classe_tab, text='Classe')

tk.Label(classe_tab, text="Classe", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
tk.Label(classe_tab, text="Choisissez une classe:").grid(row=1, column=0)
classe_var = tk.StringVar(value=list(classes.keys())[0])
classe_menu = tk.OptionMenu(classe_tab, classe_var, *classes.keys())
classe_menu.grid(row=2, column=0)

classe_description_label = tk.Label(classe_tab, text="", wraplength=400, justify="left")
classe_description_label.grid(row=3, column=0, pady=10)
classe_details_label = tk.Label(classe_tab, text="", wraplength=400, justify="left")
classe_details_label.grid(row=4, column=0, pady=10)
capacites_classe_label = tk.Label(classe_tab, text="", wraplength=400, justify="left")
capacites_classe_label.grid(row=5, column=0, pady=10)

# Onglet Historique
historique_tab = ttk.Frame(notebook)
notebook.add(historique_tab, text='Historique')

tk.Label(historique_tab, text="Historique", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
tk.Label(historique_tab, text="Choisissez un historique:").grid(row=1, column=0)
historique_var = tk.StringVar(value=list(historiques.keys())[0])
historique_menu = tk.OptionMenu(historique_tab, historique_var, *historiques.keys())
historique_menu.grid(row=2, column=0)

historique_description_label = tk.Label(historique_tab, text="", wraplength=400, justify="left")
historique_description_label.grid(row=3, column=0, pady=10)
historique_details_label = tk.Label(historique_tab, text="", wraplength=400, justify="left")
historique_details_label.grid(row=4, column=0, pady=10)

# Onglet Caractéristiques
caracteristiques_tab = ttk.Frame(notebook)
notebook.add(caracteristiques_tab, text='Caractéristiques')

tk.Label(caracteristiques_tab, text="Répartition des caractéristiques", font=('Arial', 12, 'bold')).grid(row=0, column=0, columnspan=6, pady=4)

tk.Label(caracteristiques_tab, text="Caractéristique", anchor="center").grid(row=1, column=0, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="Bonus racial", anchor="center").grid(row=1, column=3, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="", anchor="center").grid(row=1, column=1, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="Valeur brute", anchor="center").grid(row=1, column=2, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="Valeur finale", anchor="center").grid(row=1, column=4, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="Modificateur", anchor="center").grid(row=1, column=5, padx=5, sticky="ew")
tk.Label(caracteristiques_tab, text="", anchor="center").grid(row=13, column=3, padx=5, sticky="ew")

# Créer les widgets pour chaque attribut
attribut_valeur_labels = []
attribut_bonus_labels = []
attribut_valeur_finale_labels = []

for i, attribut in enumerate(attributs_list):
    tk.Label(caracteristiques_tab, text=attribut).grid(row=i+2, column=0, padx=5, sticky="w")
    tk.Button(caracteristiques_tab, text="-", command=lambda attr=attribut: diminuer_attribut(attr)).grid(row=i+2, column=1, padx=5, sticky="ew")
    attribut_valeur_labels.append(tk.Label(caracteristiques_tab, text="8", anchor="center"))
    attribut_valeur_labels[-1].grid(row=i+2, column=2, padx=5, sticky="ew")
    tk.Button(caracteristiques_tab, text="+", command=lambda attr=attribut: augmenter_attribut(attr)).grid(row=i+2, column=4, padx=5, sticky="ew")
    attribut_bonus_labels.append(tk.Label(caracteristiques_tab, text="0", anchor="center"))
    attribut_bonus_labels[-1].grid(row=i+2, column=3, padx=5, sticky="ew")
    attribut_valeur_finale_labels.append(tk.Label(caracteristiques_tab, text="8 (0)", anchor="center"))
    attribut_valeur_finale_labels[-1].grid(row=i+2, column=5, padx=5, sticky="ew")

points_label = tk.Label(caracteristiques_tab, text=f"Points restants: {points_disponibles}")
points_label.grid(row=len(attributs_list)+2, column=0, columnspan=6, pady=10)

tk.Button(caracteristiques_tab, text="Valider la répartition", command=valider_repartition).grid(row=len(attributs_list)+3, column=0, columnspan=6, pady=10)



# Mettre à jour l'affichage au démarrage
update_display()

# Événements de mise à jour pour les menus déroulants
race_var.trace("w", update_race_details)
classe_var.trace("w", update_capacites_classe)
historique_var.trace("w", lambda *args: update_display())

# Démarrer l'application
root.mainloop()