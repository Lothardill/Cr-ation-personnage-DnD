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

# Fonctions pour gérer l'affichage des détails
def afficher_details_classe(event):
    classe_selectionnee = classe_combobox.get()
    description = classes[classe_selectionnee]['description']
    details = classes[classe_selectionnee]['details']
    capacites = classes[classe_selectionnee]['capacite']
    details_str = '\n'.join(details)
    capacites_str = '\n'.join(capacites)
    classe_details_label.config(text=f'Description:\n{description}\n\nDétails de la Classe:\n{details_str}\n\nCapacités de la Classe:\n{capacites_str}')

def afficher_details_race(event):
    race_selectionnee = race_combobox.get()
    description = races[race_selectionnee]['description']
    details = races[race_selectionnee]['details']
    details_str = '\n'.join(details)
    race_details_label.config(text=f'Description:\n{description}\n\nDétails de la Race:\n{details_str}')

def afficher_details_historique(event):
    historique_selectionne = historique_combobox.get()
    description = historiques[historique_selectionne]['description']
    details = historiques[historique_selectionne]['details']
    details_str = '\n'.join(details)
    historique_details_label.config(text=f'Description:\n{description}\n\nDétails de l\'Historique:\n{details_str}')

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Création de Personnage")
fenetre.geometry("600x600")

# Ajout des onglets
tabControl = ttk.Notebook(fenetre)

onglet_classe = ttk.Frame(tabControl)
onglet_race = ttk.Frame(tabControl)
onglet_historique = ttk.Frame(tabControl)
onglet_caracteristiques = ttk.Frame(tabControl)
onglet_competences = ttk.Frame(tabControl)

tabControl.add(onglet_classe, text='Classe')
tabControl.add(onglet_race, text='Race')
tabControl.add(onglet_historique, text='Historique')
tabControl.add(onglet_caracteristiques, text='Caractéristiques')
tabControl.add(onglet_competences, text='Compétences')

tabControl.pack(expand=1, fill="both")

# Widgets pour l'onglet Classe
classe_label = tk.Label(onglet_classe, text="Choisissez une classe:")
classe_label.pack(pady=10)
classe_combobox = ttk.Combobox(onglet_classe, values=list(classes.keys()))
classe_combobox.pack(pady=10)
classe_combobox.bind("<<ComboboxSelected>>", afficher_details_classe)

classe_details_label = tk.Label(onglet_classe, text="", justify=tk.LEFT, wraplength=500)
classe_details_label.pack(pady=10)

# Widgets pour l'onglet Race
race_label = tk.Label(onglet_race, text="Choisissez une race:")
race_label.pack(pady=10)
race_combobox = ttk.Combobox(onglet_race, values=list(races.keys()))
race_combobox.pack(pady=10)
race_combobox.bind("<<ComboboxSelected>>", afficher_details_race)

race_details_label = tk.Label(onglet_race, text="", justify=tk.LEFT, wraplength=500)
race_details_label.pack(pady=10)

# Widgets pour l'onglet Historique
historique_label = tk.Label(onglet_historique, text="Choisissez un historique:")
historique_label.pack(pady=10)
historique_combobox = ttk.Combobox(onglet_historique, values=list(historiques.keys()))
historique_combobox.pack(pady=10)
historique_combobox.bind("<<ComboboxSelected>>", afficher_details_historique)

historique_details_label = tk.Label(onglet_historique, text="", justify=tk.LEFT, wraplength=500)
historique_details_label.pack(pady=10)

# Widgets pour l'onglet Caractéristiques
caracteristiques_labels = []
caracteristiques_spinboxes = []

for attribut in attributs_list:
    frame = tk.Frame(onglet_caracteristiques)
    frame.pack(pady=5)
    label = tk.Label(frame, text=attribut + ":")
    label.pack(side=tk.LEFT)
    spinbox = tk.Spinbox(frame, from_=3, to=18)
    spinbox.pack(side=tk.LEFT)
    caracteristiques_labels.append(label)
    caracteristiques_spinboxes.append(spinbox)

# Widgets pour l'onglet Compétences
competences_label = tk.Label(onglet_competences, text="Compétences sélectionnées:")
competences_label.pack(pady=10)
competences_text = tk.Text(onglet_competences, height=15, width=50)
competences_text.pack(pady=10)

# Bouton pour enregistrer le personnage
def enregistrer_personnage():
    messagebox.showinfo("Enregistrement", "Personnage enregistré avec succès!")

enregistrer_button = tk.Button(fenetre, text="Enregistrer le personnage", command=enregistrer_personnage)
enregistrer_button.pack(pady=10)

# Lancement de la boucle principale
fenetre.mainloop()
