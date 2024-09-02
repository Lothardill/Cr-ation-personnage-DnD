import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Données statiques pour la création de personnage
# Les options supplémentaire
description_style_de_combat = {
    'Archerie': '+2 aux jets d\'attaque avec une arme à distance.',
    'Arme à deux mains': 'Relance les 1 et 2 d\'un dé de dégâts avec une arme de corps à corps à deux mains ou polyvalente.',
    'Combat à deux armes': 'Si on combat avec deux armes, ajoute le modificateur de caractéristique aux dégâts de la seconde attaque.',
    'Défense': 'Si on porte une armure, +1 à la CA.',
    'Duel': 'Si on tient seulement une arme de corps à corps dans une main, +2 aux dégâts.',
    'Protection': 'Si on porte un bouclier, impose un désavantage au jet d\'attaque d\'une créature à 1,50 mètre.',
    'Armes de lancer': 'Dégaine une arme de lancer dans la même action que l\'attaque et +2 aux dégâts avec une arme de lancer.',
    'Combat à mains nues': 'Inflige 1d4/1d6/1d8 + mod.For dégâts contondants à mains nues.',
    'Combat en aveugle': 'Voit dans un rayon de 3 m tout ce qui n\'a pas un abri total, et les créatures invisibles non cachées.',
    'Interception': 'Si on porte un bouclier ou une arme, réduit les dégâts infligés à une créature dans un rayon de 1,50 m de 1d10 + bonus de maîtrise.',
    'Technique supérieure': 'Apprend 1 manœuvre, DD de sauvegarde vs manœuvre égal à 8 + bonus de maîtrise + mod. Force ou Dextérité, et gagne un d6 de supériorité.'
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
        'capacite': [
            'Second souffle: Une fois par repos court ou long, vous pouvez utiliser une action bonus pour regagner un nombre de points de vie égal à 1d10 + votre niveau.',
            'Style de combat: Vous choisissez un style de combat qui vous accorde des avantages en combat.'
        ],
        'outils': ['Matériel de forgeron', 'Matériel de brasseur'],
        'nombre_de_competence': 2,
        'competences': 'Acrobaties, Athlétisme, Dressage, Histoire, Intimidation, Intuition, Perception, Survie',
        'style_de_combat': 'Archerie, Arme à deux mains, Combat à deux armes, Défense, Duel, Protection, Armes de lancer, combat à mains nues, combat en aveugle, Interception, Technique supérieur',
        'description_style_de_combat': description_style_de_combat,
        'pack':'Pack (a), Pack (b)',
        'pack_(a)': [
            'Cotte de mailles',
            'Bouclier',
            '1 arme de guerre',
            'Arbalète légère',
            'Sac d\'exploration souterraine'
        ],
        'pack_(b)':[
            'Armure de cuir',
            '2 armes de guerre',
            '2 hachettes',
            'Arc long',
            'Sac d\'explorateur'
        ]
    },
    'Magicien': {
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
        'nombre_de_competence': 2,
        'competences': 'Arcanes, Histoire, Intuition, Investigation, Médecine, Religion',
        'pack':'Pack (a), Pack (b)',
        'pack_(a)': [
            'Bâton',
            'Grimoire',
            'Sacoche à composantes',
            'Sac d\'érudit'
        ],
        'pack_(b)':[
            'Dague',
            'Grimoire',
            'Focalisateur arcanique',
            'Sac d\'explorateur'
        ]
    },
    'Roublard': {
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
            'Attaque sournoise: Une fois par tour, vous pouvez infliger des dégâts supplémentaires à une cible que vous attaquez avec une arme de finesse ou à distance si vous avez l’avantage à l\'attaque ou si un allié est à portée de mêlée de la cible.',
            'Jargon des voleurs: Vous pouvez comprendre et parler le jargon des voleurs, un langage secret utilisé par les criminels.'
        ],
        'outils': ['Outils de voleur'],
        'nombre_de_competence': 4,
        'competences': 'Acrobaties, Athlétisme, Discrétion, Escamotage, Intimidation, Intuition, Investigation, Perception, Persuasion, Représentation, Tromperie',
        'pack':'Pack (a), Pack (b)',
        'pack_(a)': [
            'Armure de cuir',
            'Rapière',
            'Arc court',
            '2 dagues',
            'Outils de voleur',
            'Sac de cambrioleur'
        ],
        'pack_(b)':[
            'Armure de cuir',
            '2 épées courtes',
            '2 dagues',
            'Outils de voleur',
            'Sac d\'exploration souterraine'
        ]
    }
}

races = {
    'Humain': {
        'description': 'Les Humains sont polyvalents et adaptables, avec une grande capacité à s’intégrer dans diverses cultures.',
        'details': [
            'Augmentation de caractéristiques. Force +1, Dextérité +1, Constitution +1, Intelligence +1, Sagesse +1, Charisme +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Langues. Commun, une langue de votre choix'
        ],
        'bonus': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1},
        'compétences': [],
        'outils': [],
        'langues': ['Commun', 'Une langue supplémentaire au choix'],
        'nombre_de_langue': 1,
        'langue_parlee_race': 'Commun'
    },
    'Elfe': {
        'description': 'Les Elfes sont des êtres agiles et gracieux, dotés d’une longue durée de vie et de sens aiguisés.',
        'details': [
            'Augmentation de caractéristiques. Dextérité +2, Intelligence +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique, une langue de votre choix',
            'Traits. Sens aiguisés *',
            'Ascendance féerique (AV aux JdS vs charme et la magie ne peut pas vous endormir)',
            'Transe (4h de méditation remplacent 8h de sommeil)',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        'bonus': {'Dextérité': 2, 'Intelligence': 1},
        'compétences': [],
        'outils': [],
        'langues': ['Commun', 'Elfique', 'Une langue supplémentaire au choix'],
        'nombre_de_langue': 1,
        'langue_parlee_race': 'Commun, Elfique'
    },
    'Nain': {
        'description': 'Robustes et endurants, les Nains sont des artisans habiles avec une grande résistance.',
        'details': [
            'Augmentation de caractéristiques. Force +2, Constitution +2',
            'Taille. M',
            'Vitesse. 7.5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Nain',
            'Traits. Résistance naine (AV aux JdS vs poison)',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre (bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre)',
            'Formation au port des armures naines'
        ],
        'bonus': {'Force': 2, 'Constitution': 2},
        'compétences': [],
        'outils': ['Matériel de forgeron', 'Matériel de brasseur', 'Matériel de maçon'],
        'langues': ['Commun', 'Nain'],
        'nombre_de_langue': 0,
        'langue_parlee_race': 'Commun, Nain'
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
        'choix_outils': ['Kit d\'empoisonneur','Kit d\'herboriste','Kit de contrefaçon','Kit de déguisement','Kit de navigateur','Outils de voleur'],
        'langues': [],
        'nombre_de_competence': 2,
        'nombre_de_langue_historique': 0
    },
    'Artisan': {
        'description': 'Les artisans possèdent une expertise particulière dans divers outils et matériaux.',
        'details': [
            'Langues. Une langue supplémentaire au choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Artisanat, Histoire, Investigation, Médecine, Nature',
            'Outils. choix d\'un outil spécifique à une profession'
        ],
        'compétences': ['Arcanes', 'Artisanat', 'Histoire', 'Investigation', 'Médecine', 'Nature'],
        'outils': ['Matériel d’alchimie', 'Matériel de brasseur', 'Matériel de calligraphe', 'Matériel de peintre', 'Matériel de bijoutier', 'Matériel de bricoleur', 'Matériel de cartographe', 'Matériel de charpentier', 'Matériel de cordonnier', 'Matériel de forgeron', 'Matériel de maçon', 'Matériel de menuisier', 'Matériel de potier', 'Matériel de souffleur de verre', 'Matériel de tanneur', 'Matériel de tisserand', 'Matériel de cuisinier'],
        'langues': ['Une langue supplémentaire au choix'],
        'nombre_de_competence': 2,
        'nombre_de_langue_historique': 1
    },
    'Acolyte': {
        'description': 'Les acolytes ont une formation religieuse approfondie et des compétences dans les rituels et le culte.',
        'details': [
            'Langues. Deux langues supplémentaires aux choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Histoire, Médecine, Religion'
        ],
        'compétences': ['Arcanes', 'Histoire', 'Médecine', 'Religion'],
        'outils': [],
        'langues': ['Deux langues supplémentaires au choix'],
        'nombre_de_competence': 2,
        'nombre_de_langue_historique': 2
    }
}

# Liste des attributs du personnage
attributs_list = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']

# Liste complète des compétences
competences_completes = ['Acrobaties', 'Arcanes', 'Athlétisme', 'Discrétion', 'Dressage', 'Escamotage', 'Histoire', 'Intimidation', 'Investigation', 'Médecine', 'Nature', 'Perception', 'Perspicacité', 'Persuasion', 'Religion', 'Représentation', 'Survie', 'Tromperie']

# Liste complète des langues
langues_standard = ['Commun', 'Elfique', 'Géant', 'Gnome', 'Gobelin', 'Halfelin', 'Nain', 'Orc']
langues_exotiques = ['Abyssal', 'Céleste', 'Commun des profondeurs', 'Draconique', 'Infernal', 'Primordial', 'Profond', 'Sylvestre']

# Variable globale pour stocker les valeurs sélectionnées
selected_values = []
comboboxes = []  # Ajout de l'initialisation ici
competences_classe_selectionnees = []

# Fonction pour formater les valeurs avec "(déjà sélectionné)"
def format_value(value):
    if value in selected_values:
        return f"{value} (déjà sélectionné)"
    return value

# Fonction pour nettoyer les valeurs sélectionnées
def clean_value(value):
    return value.replace(" (déjà sélectionné)", "")

# Fonction pour extraire les compétences et langues disponibles
def extraire_competences_et_langues():
    competences_disponibles_classe = set()
    competences_disponibles_historique = set()
    langues_disponibles = set(langues_standard + langues_exotiques)
    outils_disponibles = set()
    
    classe_selectionnee = classe_combobox.get()
    race_selectionnee = race_combobox.get()
    historique_selectionne = historique_combobox.get()
    
    if classe_selectionnee:
        competences_disponibles_classe.update(classes[classe_selectionnee].get('competences', '').split(', '))
        outils_disponibles.update(classes[classe_selectionnee].get('outils', []))
    
    if race_selectionnee:
        competences_disponibles_classe.update(races[race_selectionnee].get('compétences', []))
        outils_disponibles.update(races[race_selectionnee].get('outils', []))
        langues_parlees_race = races[race_selectionnee].get('langue_parlee_race', '').split(', ')
        for langue in langues_parlees_race:
            selected_values.append(langue)
    
    if historique_selectionne:
        competences_disponibles_historique.update(historiques[historique_selectionne].get('compétences', []))
        outils_disponibles.update(historiques[historique_selectionne].get('outils', []))
        outils_disponibles.update(historiques[historique_selectionne].get('choix_outils', []))
    
    return competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles

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
        bonus = races[race_combobox.get()]['bonus'].get(attribut, 0) if race_combobox.get() else 0
        total = valeur + bonus
        modificateur = calculer_modificateur(total)
        
        attribut_valeur_labels[i].config(text=f"{valeur}")
        attribut_bonus_labels[i].config(text=f"{bonus:+d}")
        attribut_valeur_finale_labels[i].config(text=f"{total} ({modificateur:+d})")
    
    points_label.config(text=f"Points restants: {points_disponibles}")

# Fonction pour valider la répartition des points d'attributs
def valider_repartition():
    global points_disponibles
    if points_disponibles == 0:
        messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
    else:
        messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

# Fonction pour gérer l'affichage des détails
def afficher_details_classe(event):
    reset_selected_values()
    reset_comboboxes()
    classe_selectionnee = classe_combobox.get()
    description = classes[classe_selectionnee]['description']
    details = classes[classe_selectionnee]['details']
    capacites = classes[classe_selectionnee]['capacite']
    details_str = '\n'.join(details)
    capacites_str = '\n'.join(capacites)
    classe_details_label.config(text=f'Description:\n{description}\n\nDétails de la Classe:\n{details_str}\n\nCapacités de la Classe:\n{capacites_str}')
    update_maitrise()

def afficher_details_race(event):
    reset_selected_values()
    reset_comboboxes()
    race_selectionnee = race_combobox.get()
    description = races[race_selectionnee]['description']
    details = races[race_selectionnee]['details']
    details_str = '\n'.join(details)
    race_details_label.config(text=f'Description:\n{description}\n\nDétails de la Race:\n{details_str}')
    update_display()
    update_maitrise()

def afficher_details_historique(event):
    reset_selected_values()
    reset_comboboxes()
    historique_selectionne = historique_combobox.get()
    description = historiques[historique_selectionne]['description']
    details = historiques[historique_selectionne]['details']
    details_str = '\n'.join(details)
    historique_details_label.config(text=f'Description:\n{description}\n\nDétails de l\'Historique:\n{details_str}')
    update_maitrise()

def update_combobox_options(combobox, values, label_text):
    current_value = combobox.get()
    formatted_values = []
    for value in values:
        if value in selected_values and value != current_value:
            formatted_values.append(f"{value} (déjà sélectionné)")
        else:
            formatted_values.append(value)
    
    combobox['values'] = formatted_values
    if current_value not in formatted_values:
        combobox.set('')
    combobox.label_text = label_text

def update_comboboxes():
    classe_selectionnee = classe_combobox.get()
    race_selectionnee = race_combobox.get()
    historique_selectionne = historique_combobox.get()
    
    competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles = extraire_competences_et_langues()
    langues_parlees_race = set()

    if race_selectionnee:
        langues_parlees_race.update(races[race_selectionnee].get('langue_parlee_race', '').split(', '))

    for combobox, label_text in comboboxes:
        if "compétences de la classe" in label_text.lower():
            values = competences_disponibles_classe
        elif "compétences de la race" in label_text.lower():
            values = races[race_selectionnee].get('compétences', [])
        elif "compétences de l'historique" in label_text.lower():
            values = competences_disponibles_historique
        elif "langues de la race" in label_text.lower():
            values = langues_disponibles
        elif "langues de l'historique" in label_text.lower():
            values = langues_disponibles
        elif "outils de la race" in label_text.lower():
            values = races[race_selectionnee].get('outils', [])
        elif "outils de la classe" in label_text.lower():
            values = classes[classe_selectionnee].get('outils', [])
        elif "outils de l'historique" in label_text.lower():
            if label_text == "Outils de l'historique":
                values = historiques[historique_selectionne].get('outils', [])
            elif label_text == "Choix d'outils de l'historique":
                values = historiques[historique_selectionne].get('choix_outils', [])
        
        update_combobox_options(combobox, values, label_text)

def update_selected_values():
    global selected_values
    selected_values = [clean_value(combobox.get()) for combobox, label_text in comboboxes if combobox.get()]
    update_comboboxes()

def creer_menu_deroulant(options, label_text, parent_frame, nombre=None):
    if not options:
        return  # Ne rien faire si les options sont vides
    tk.Label(parent_frame, text=label_text, font=('Arial', 10, 'bold')).pack(anchor="w")
    frame = tk.Frame(parent_frame)
    frame.pack(anchor="w", pady=5)
    if nombre is None:
        nombre = len(options)
    for _ in range(nombre):
        if len(options) == 1:
            label = tk.Label(frame, text=options[0], font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=5)
        else:
            formatted_options = [format_value(opt) for opt in sorted(options)]
            combobox = ttk.Combobox(frame, values=formatted_options, state="readonly")
            combobox.pack(side=tk.LEFT, padx=5)
            combobox.bind("<<ComboboxSelected>>", lambda event: [update_selected_values()])
            comboboxes.append((combobox, label_text))

def update_maitrise():
    competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles = extraire_competences_et_langues()
    
    # Clear previous widgets
    for widget in maitrise_frame.winfo_children():
        widget.destroy()
    
    global comboboxes
    comboboxes = []

    # Compétences de la race
    race_selectionnee = race_combobox.get()
    if race_selectionnee:
        competences_race = races[race_selectionnee].get('compétences', [])
        creer_menu_deroulant(competences_race, "Compétences de la race", maitrise_frame)

    # Compétences de la classe
    classe_selectionnee = classe_combobox.get()
    if classe_selectionnee:
        nombre_de_competence = classes[classe_selectionnee]['nombre_de_competence']
        competences_classe = list(competences_disponibles_classe)
        creer_menu_deroulant(competences_classe, "Compétences de la classe", maitrise_frame, nombre=nombre_de_competence)

    # Compétences de l'historique
    historique_selectionne = historique_combobox.get()
    if historique_selectionne:
        nombre_de_competence_historique = historiques[historique_selectionne]['nombre_de_competence']
        competences_historique = list(competences_disponibles_historique)
        creer_menu_deroulant(competences_historique, "Compétences de l'historique", maitrise_frame, nombre=nombre_de_competence_historique)

    # Outils de la race
    if race_selectionnee:
        outils_race = races[race_selectionnee].get('outils', [])
        creer_menu_deroulant(outils_race, "Outils de la race", maitrise_frame, 1)

    # Outils de la classe
    creer_menu_deroulant(classes[classe_selectionnee].get('outils', []), "Outils de la classe", maitrise_frame, nombre=1)

    # Outils de l'historique
    if historique_selectionne:
        outils_historiques = historiques[historique_selectionne]['outils']
        choix_outils_historiques = historiques[historique_selectionne].get('choix_outils', [])
        if outils_historiques or choix_outils_historiques:
            tk.Label(maitrise_frame, text="Outils de l'historique", font=('Arial', 10, 'bold')).pack(anchor="w")
            outils_historiques_frame = tk.Frame(maitrise_frame)
            outils_historiques_frame.pack(anchor="w", pady=5)
            if outils_historiques:
                formatted_outils_historiques = [format_value(opt) for opt in sorted(outils_historiques)]
                combobox_outils_historique = ttk.Combobox(outils_historiques_frame, values=formatted_outils_historiques, state="readonly")
                combobox_outils_historique.pack(side=tk.LEFT, padx=5)
                combobox_outils_historique.bind("<<ComboboxSelected>>", lambda event: [update_selected_values()])
                comboboxes.append((combobox_outils_historique, "Outils de l'historique"))
            if choix_outils_historiques:
                formatted_choix_outils_historiques = [format_value(opt) for opt in sorted(choix_outils_historiques)]
                combobox_choix_outils_historiques = ttk.Combobox(outils_historiques_frame, values=formatted_choix_outils_historiques, state="readonly")
                combobox_choix_outils_historiques.pack(side=tk.LEFT, padx=5)
                combobox_choix_outils_historiques.bind("<<ComboboxSelected>>", lambda event: [update_selected_values()])
                comboboxes.append((combobox_choix_outils_historiques, "Choix d'outils de l'historique"))

    # Langues de la race
    if race_selectionnee:
        langues_parlees_race = races[race_selectionnee].get('langue_parlee_race', '').split(', ')
        if langues_parlees_race or races[race_selectionnee].get('nombre_de_langue', 0) > 0:
            tk.Label(maitrise_frame, text="Langues de la race", font=('Arial', 10, 'bold')).pack(anchor="w")
            langues_race_frame = tk.Frame(maitrise_frame)
            langues_race_frame.pack(anchor="w", pady=5)
            for langue in langues_parlees_race:
                tk.Label(langues_race_frame, text=langue, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
            all_langues = sorted(langues_standard + langues_exotiques)
            formatted_all_langues = [format_value(opt) for opt in all_langues]
            for _ in range(races[race_selectionnee].get('nombre_de_langue', 0)):
                combobox_langues_supplementaires_race = ttk.Combobox(langues_race_frame, values=formatted_all_langues, state="readonly")
                combobox_langues_supplementaires_race.pack(side=tk.LEFT, padx=5)
                combobox_langues_supplementaires_race.bind("<<ComboboxSelected>>", lambda event: [update_selected_values()])
                comboboxes.append((combobox_langues_supplementaires_race, "Langues de la race"))

    # Langues de l'historique
    if historique_selectionne:
        nombre_de_langue_historique = historiques[historique_selectionne].get('nombre_de_langue_historique', 0)
        if nombre_de_langue_historique > 0:
            creer_menu_deroulant(langues_standard + langues_exotiques, "Langues de l'historique", maitrise_frame, nombre=nombre_de_langue_historique)

def reset_selected_values():
    global selected_values
    selected_values = []
    
def reset_comboboxes():
    for combobox, label_text in comboboxes:
        combobox.set('')

def extraire_competences_historique_selectionnees():
    competences_classe_selectionnees = []
    for combobox, label_text in comboboxes:
        if "Compétences de la classe" in label_text:
            valeur = combobox.get()
            if ' (déjà sélectionné)' in valeur:
                competences_classe_selectionnees.append(clean_value(valeur))
    return competences_classe_selectionnees

# Fonction pour mettre à jour les options
def update_options():
    for widget in options_frame.winfo_children():
        widget.destroy()

    classe_selectionnee = classe_combobox.get()

    if classe_selectionnee == 'Roublard':
        tk.Label(options_frame, text="Expertise (Roublard)", font=('Arial', 12, 'bold')).pack(anchor="w")
        expertise_frame = tk.Frame(options_frame)
        expertise_frame.pack(anchor="w", pady=5)
        for i in range(2):  # Deux menus déroulants pour l'expertise
            expertise_combobox = ttk.Combobox(expertise_frame, values=extraire_competences_historique_selectionnees(), state="readonly")
            expertise_combobox.pack(side=tk.LEFT, padx=5)
            comboboxes.append((expertise_combobox, "Expertise (Roublard)"))


    if 'style_de_combat' in classes[classe_selectionnee]:
        style_frame = tk.Frame(options_frame)
        style_frame.pack(anchor="w", pady=5)
        
        tk.Label(options_frame, text="Style de combat", font=('Arial', 12, 'bold')).pack(anchor="w")
        styles_disponibles = classes[classe_selectionnee]['style_de_combat'].split(', ')
        style_combobox = ttk.Combobox(options_frame, values=styles_disponibles, state="readonly")
        style_combobox.pack(anchor="w", pady=5)


        def show_style_description(event):
            style = style_combobox.get()
            description = description_style_de_combat.get(style, '')
            description_label.config(text=description, fg="#802040", font=('Arial', 12, 'bold'))

        style_combobox.bind("<<ComboboxSelected>>", show_style_description)
        description_label = tk.Label(options_frame, text="", wraplength=500)
        description_label.pack(anchor="e", padx=20)

    if 'pack' in classes[classe_selectionnee]:
        tk.Label(options_frame, text="Pack de départ", font=('Arial', 12, 'bold')).pack(anchor="w")
        packs_disponibles = classes[classe_selectionnee]['pack'].split(', ')
        pack_combobox = ttk.Combobox(options_frame, values=packs_disponibles, state="readonly")
        pack_combobox.pack(anchor="w", pady=5)

        def show_pack_content(event):
            pack = pack_combobox.get()
            content = '\n'.join(classes[classe_selectionnee][f'pack_({pack[-2]})'])
            pack_content_label.config(text=content)

        pack_combobox.bind("<<ComboboxSelected>>", show_pack_content)
        pack_content_label = tk.Label(options_frame, text="", justify=tk.LEFT, anchor="w", wraplength=500)
        pack_content_label.pack(anchor="w", pady=5)



# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Création de Personnage")
fenetre.geometry("800x800")

# Ajout des onglets
tabControl = ttk.Notebook(fenetre)

onglet_classe = ttk.Frame(tabControl)
onglet_race = ttk.Frame(tabControl)
onglet_historique = ttk.Frame(tabControl)
onglet_caracteristiques = ttk.Frame(tabControl)
onglet_maitrise = ttk.Frame(tabControl)
onglet_options = ttk.Frame(tabControl)

tabControl.add(onglet_classe, text='Classe')
tabControl.add(onglet_race, text='Race')
tabControl.add(onglet_historique, text='Historique')
tabControl.add(onglet_caracteristiques, text='Caractéristiques')
tabControl.add(onglet_maitrise, text='Maîtrise')
tabControl.add(onglet_options, text='Options')

tabControl.pack(expand=1, fill="both")

# Déplacer la création des comboboxes avant les widgets et les fonctions qui les utilisent
classe_combobox = ttk.Combobox(onglet_classe, values=list(classes.keys()), state="readonly")
classe_combobox.pack(pady=10)

race_combobox = ttk.Combobox(onglet_race, values=list(races.keys()), state="readonly")
race_combobox.pack(pady=10)

historique_combobox = ttk.Combobox(onglet_historique, values=list(historiques.keys()), state="readonly")
historique_combobox.pack(pady=10)

classe_combobox.bind("<<ComboboxSelected>>", lambda event: [afficher_details_classe(event), update_maitrise(), update_options()])
race_combobox.bind("<<ComboboxSelected>>", lambda event: [afficher_details_race(event), update_display(), update_maitrise()])
historique_combobox.bind("<<ComboboxSelected>>", lambda event: [afficher_details_historique(event), update_maitrise()])

# Widgets pour l'onglet Classe
classe_label = tk.Label(onglet_classe, text="Choisissez une classe:")
classe_label.pack(pady=10)

classe_details_label = tk.Label(onglet_classe, text="", justify=tk.LEFT, wraplength=500)
classe_details_label.pack(pady=10)

# Widgets pour l'onglet Race
race_label = tk.Label(onglet_race, text="Choisissez une race:")
race_label.pack(pady=10)

race_details_label = tk.Label(onglet_race, text="", justify=tk.LEFT, wraplength=500)
race_details_label.pack(pady=10)

# Widgets pour l'onglet Historique
historique_label = tk.Label(onglet_historique, text="Choisissez un historique:")
historique_label.pack(pady=10)

historique_details_label = tk.Label(onglet_historique, text="", justify=tk.LEFT, wraplength=500)
historique_details_label.pack(pady=10)

# Widgets pour l'onglet Caractéristiques
caracteristiques_labels = []
attribut_valeur_labels = []
attribut_augmenter_buttons = []
attribut_diminuer_buttons = []
attribut_bonus_labels = []
attribut_valeur_finale_labels = []

titre_label = tk.Label(onglet_caracteristiques, text="Répartition des caractéristiques", font=('Arial', 12, 'bold'))
titre_label.grid(row=0, column=0, columnspan=6, pady=4)

# Création des labels pour les colonnes
tk.Label(onglet_caracteristiques, text="Caractéristique").grid(row=1, column=0, padx=5, sticky="w")
tk.Label(onglet_caracteristiques, text="Bonus racial", anchor="center").grid(row=1, column=1, padx=5, sticky="ew")
tk.Label(onglet_caracteristiques, text="").grid(row=1, column=2, padx=5, sticky="ew")
tk.Label(onglet_caracteristiques, text="Valeur brute", anchor="center").grid(row=1, column=3, padx=5, sticky="ew")
tk.Label(onglet_caracteristiques, text="").grid(row=1, column=4, padx=5, sticky="ew")
tk.Label(onglet_caracteristiques, text="Valeur finale", anchor="center").grid(row=1, column=5, padx=5, sticky="ew")

# Configurer les poids des colonnes et fixer la largeur des colonnes
onglet_caracteristiques.grid_columnconfigure(0, weight=2)  # Caractéristique
onglet_caracteristiques.grid_columnconfigure(2, weight=1)  # Diminuer
onglet_caracteristiques.grid_columnconfigure(3, weight=2)  # Valeur brute
onglet_caracteristiques.grid_columnconfigure(4, weight=1)  # Augmenter
onglet_caracteristiques.grid_columnconfigure(1, weight=2)  # Bonus racial
onglet_caracteristiques.grid_columnconfigure(5, weight=2)  # Valeur finale

# Fixer la largeur minimale des colonnes contenant les boutons
onglet_caracteristiques.grid_columnconfigure(2, minsize=10)  # Diminuer
onglet_caracteristiques.grid_columnconfigure(4, minsize=10)  # Augmenter

for i, attribut in enumerate(attributs_list):
    tk.Label(onglet_caracteristiques, text=attribut).grid(row=2+i, column=0, padx=5, sticky="w")
    tk.Button(onglet_caracteristiques, text="-", command=lambda a=attribut: diminuer_attribut(a)).grid(row=2+i, column=2, padx=0, sticky="ew")
    attribut_valeur_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_valeur_label.grid(row=2+i, column=3, padx=5, sticky="ew")
    tk.Button(onglet_caracteristiques, text="+", command=lambda a=attribut: augmenter_attribut(a)).grid(row=2+i, column=4, padx=0, sticky="ew")
    attribut_bonus_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_bonus_label.grid(row=2+i, column=1, padx=5, sticky="ew")
    attribut_valeur_finale_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_valeur_finale_label.grid(row=2+i, column=5, padx=5, sticky="ew")
    
    attribut_valeur_labels.append(attribut_valeur_label)
    attribut_bonus_labels.append(attribut_bonus_label)
    attribut_valeur_finale_labels.append(attribut_valeur_finale_label)

# Points restants
points_label = tk.Label(onglet_caracteristiques, text=f"Points restants: {points_disponibles}")
points_label.grid(row=20, column=0, columnspan=2, pady=10)

# Bouton de validation
tk.Button(onglet_caracteristiques, text="Valider répartition", command=valider_repartition).grid(row=20, column=2, columnspan=2, pady=10)

# Widgets pour l'onglet Maîtrise
maitrise_frame = tk.Frame(onglet_maitrise)
maitrise_frame.pack(pady=10, fill="x")

# Widgets pour l'onglet Options
options_frame = tk.Frame(onglet_options)
options_frame.pack(pady=10, fill="x")

# Bouton pour enregistrer le personnage
def enregistrer_personnage():
    selected_values_print = "\n".join(selected_values)
    messagebox.showinfo("Enregistrement", f"Personnage enregistré avec succès!\nCompétences sélectionnées:\n{selected_values_print}")

enregistrer_button = tk.Button(fenetre, text="Enregistrer le personnage", command=enregistrer_personnage)
enregistrer_button.pack(pady=10)

# Lancement de la boucle principale
fenetre.mainloop()
