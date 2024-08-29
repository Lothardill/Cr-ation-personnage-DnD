import random
import tkinter as tk
from tkinter import messagebox
from pdfrw import PdfReader, PdfWriter, PageMerge

# Définition des races, classes, attributs et bonus raciaux

races = {
    'Humain': {
        'description': (
            "Les humains sont la race la plus adaptable et polyvalente de toutes.\n"
            "Traits:\n"
            "- Augmentation des valeurs de caractéristiques. Vos six valeurs de caractéristiques augmentent chacune de 1.\n"
            "- Âge: Les humains atteignent l'âge adulte à la fin de l'adolescence et vivent moins d'un siècle.\n"
            "- Alignement: Les humains ne tendent vers aucun alignement en particulier.\n"
            "- Taille: Les humains mesurent en moyenne entre 1,50 m et 1,90 m."
        ),
        'bonus': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1}
    },
    'Elfe': {
        'description': (
            "Les elfes sont des êtres élancés, gracieux, et mystérieux. Ils vivent dans des forêts luxurieuses et sont connus pour leur agilité et leur sagesse.\n"
            "Traits:\n"
            "- Dextérité augmentée de 2.\n"
            "- Vision nocturne: Peut voir dans l'obscurité jusqu'à 18 mètres.\n"
            "- Longévité: Les elfes vivent plusieurs siècles."
        ),
        'bonus': {'Dextérité': 2}
    },
    'Nain': {
        'description': (
            "Les nains sont robustes et fiables, souvent associés aux montagnes et aux mines. Ils sont connus pour leur courage et leur endurance.\n"
            "Traits:\n"
            "- Constitution augmentée de 2.\n"
            "- Vision dans le noir: Peut voir dans l'obscurité jusqu'à 18 mètres.\n"
            "- Résistance à la magie: Résistance aux sorts de type poison et sommeil."
        ),
        'bonus': {'Constitution': 2}
    },
    'Halfelin': {
        'description': (
            "Les halfelins sont petits, agiles et très sociables. Ils vivent souvent dans des communautés rurales et sont réputés pour leur discrétion.\n"
            "Traits:\n"
            "- Dextérité augmentée de 2.\n"
            "- Taille petite: Difficulté à utiliser des armes lourdes.\n"
            "- Chance: Avantage pour éviter les attaques."
        ),
        'bonus': {'Dextérité': 2}
    },
    'Orc': {
        'description': (
            "Les orcs sont des guerriers puissants et imposants. Ils sont souvent perçus comme des barbares, mais ils ont aussi une culture riche et complexe.\n"
            "Traits:\n"
            "- Force augmentée de 2.\n"
            "- Régénération: Récupère des points de vie supplémentaires chaque tour.\n"
            "- Sanguinaire: Avantage pour les attaques de mêlée."
        ),
        'bonus': {'Force': 2}
    },
    'Demi-elfe': {
        'description': (
            "Les demi-elfes sont le produit de l'union entre elfes et humains. Ils possèdent la beauté et l'agilité des elfes, ainsi que la résilience des humains.\n"
            "Traits:\n"
            "- Charisme augmentée de 2.\n"
            "- Vision nocturne: Peut voir dans l'obscurité jusqu'à 18 mètres.\n"
            "- Compétence: Peut choisir deux compétences supplémentaires."
        ),
        'bonus': {'Charisme': 2}
    },
    'Tieffelin': {
        'description': (
            "Les tieffelins sont des descendants de démons. Ils sont connus pour leurs traits démoniaques et leur puissance magique.\n"
            "Traits:\n"
            "- Intelligence augmentée de 1, Charisme augmentée de 2.\n"
            "- Résistance aux sorts de feu: Résistance à la magie du feu.\n"
            "- Vision nocturne: Peut voir dans l'obscurité jusqu'à 18 mètres."
        ),
        'bonus': {'Intelligence': 1, 'Charisme': 2}
    }
}

classes = {
    'Barbare': {
        'description': "Les barbares sont des combattants sauvages qui canalisent leur colère pour devenir des forces imparables en combat.",
        'traits': "Armure de peau : Peau dure. Rage : Augmente la force et la résistance mais diminue la défense.",
        'PV': 12,
        'avantages': "Proficience en force et constitution.",
        'compétences': "Athlétisme, Intimidation"
    },
    'Guerrier': {
        'description': "Les guerriers sont des maîtres du combat, utilisant une variété d'armes et d'armures pour protéger et attaquer.",
        'traits': "Maîtrise des armes et armures. Second souffle : Récupère des PV en combat.",
        'PV': 12,
        'avantages': "Proficience en force et constitution.",
        'compétences': "Athlétisme, Perception"
    },
    'Magicien': {
        'description': "Les magiciens sont des praticiens de la magie, étudiant des formules mystiques pour manipuler les forces de l'univers.",
        'traits': "Sorts : Utilise des sorts pour influencer la réalité. Étude : Peut apprendre de nouveaux sorts.",
        'PV': 6,
        'avantages': "Proficience en intelligence.",
        'compétences': "Arcanes, Histoire"
    },
    # Ajouter d'autres classes avec leurs détails ici
}

historiques = {
    'Artiste': {
        'description': "Artiste talentueux, maîtrisant l'art de la musique, de la peinture ou de la poésie. Voyage souvent pour partager leur art.",
        'équipements': ["Instrument de musique", "Outil artistique", "Tenue voyante"]
    },
    'Héros du peuple': {
        'description': "Héros légendaire, connu pour avoir sauvé son peuple d'une grande menace. Respecté et admiré à travers les terres.",
        'équipements': ["Arme symbolique", "Médaille d'honneur", "Trophée de victoire"]
    },
    # Ajouter d'autres historiques avec leurs détails ici
}

equipements = {
    'Artiste': {
        'A': ["Instrument de musique", "Outil artistique", "Tenue voyante"],
        'B': ["Arc", "Flèches", "Dague", "Capuche de camouflage"]
    },
    'Héros du peuple': {
        'A': ["Arme symbolique", "Médaille d'honneur", "Trophée de victoire"],
        'B': ["Arcane focus", "Bâton", "Robe d'enchanteur", "Potion de soins"]
    },
    # Ajouter d'autres options d'équipements pour chaque historique ici
}

# Liste des attributs pour la génération aléatoire
attributs = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']

# Génération aléatoire des attributs en utilisant 4d6, garder les 3 meilleurs
def generer_attributs():
    return {attr: sum(sorted([random.randint(1, 6) for _ in range(4)])[1:]) for attr in attributs}

# Génération du personnage complet
def generer_personnage(race, classe, historique, choix_equipement):
    attributs = generer_attributs()
    attributs = appliquer_bonus_racial(attributs, race)
    
    personnage = {
        'Race': race,
        'Classe': classe,
        'Attributs': attributs,
        'Historique': historique,
        'Équipement': equipements[historique][choix_equipement]
    }
    return personnage

# Fonction pour appliquer les bonus raciaux aux attributs
def appliquer_bonus_racial(attributs, race):
    bonus_racial = races[race]['bonus']
    for attr in attributs:
        attributs[attr] += bonus_racial.get(attr, 0)
    return attributs

# Fonction pour remplir et exporter la fiche de personnage PDF
def export_pdf_interface():
    global current_personnage
    
    if not current_personnage:
        messagebox.showerror("Erreur", "Aucun personnage généré. Veuillez générer un personnage avant d'exporter en PDF.")
        return
    
    pdf_template_path = 'fiche_personnage_template.pdf'
    output_pdf_path = 'fiche_personnage.pdf'
    
    template_pdf = PdfReader(pdf_template_path)
    page = template_pdf.pages[0]
    
    # Remplir les champs de la fiche de personnage
    page.TextBoxRace = current_personnage['Race']
    page.TextBoxClasse = current_personnage['Classe']
    
    # Attributs
    for attr in attributs:
        setattr(page, f'TextBox{attr}', str(current_personnage['Attributs'][attr]))
    
    # Historique
    historique_description = historiques[current_personnage['Historique']]['description']
    historique_equipements = ', '.join(equipements[current_personnage['Historique']][current_personnage['Équipement']])
    
    page.TextBoxHistorique = f"{current_personnage['Historique']}: {historique_description}"
    page.TextBoxEquipement = f"Équipements: {historique_equipements}"
    
    # Sauvegarder la fiche de personnage remplie
    PdfWriter().addpage(page).write(output_pdf_path)
    
    messagebox.showinfo("PDF Exporté", f"La fiche de personnage a été exportée avec succès en PDF: {output_pdf_path}")

# Interface utilisateur avec Tkinter
root = tk.Tk()
root.title("Générateur de Personnages DnD")

# Variables pour les choix de l'utilisateur
race_var = tk.StringVar(value='Humain')
classe_var = tk.StringVar(value='Guerrier')
historique_var = tk.StringVar(value='Artiste')
equipement_var = tk.StringVar(value='A')

# Fonction pour mettre à jour les descriptions lors de la sélection d'une option
def update_descriptions(*args):
    race = race_var.get()
    classe = classe_var.get()
    historique = historique_var.get()
    
    race_description.config(text=races[race]['description'])
    classe_description.config(text=classes[classe]['description'])
    historique_description.config(text=historiques[historique]['description'])

# Menus déroulants pour sélectionner la race, la classe et l'historique
tk.Label(root, text="Choisissez une race:").pack()
race_menu = tk.OptionMenu(root, race_var, *races.keys(), command=update_descriptions)
race_menu.pack()

tk.Label(root, text="Choisissez une classe:").pack()
classe_menu = tk.OptionMenu(root, classe_var, *classes.keys(), command=update_descriptions)
classe_menu.pack()

tk.Label(root, text="Choisissez un historique:").pack()
historique_menu = tk.OptionMenu(root, historique_var, *historiques.keys(), command=update_descriptions)
historique_menu.pack()

# Descriptions dynamiques pour les options sélectionnées
tk.Label(root, text="Description de la race:").pack()
race_description = tk.Label(root, wraplength=400, justify='left')
race_description.pack()

tk.Label(root, text="Description de la classe:").pack()
classe_description = tk.Label(root, wraplength=400, justify='left')
classe_description.pack()

tk.Label(root, text="Description de l'historique:").pack()
historique_description = tk.Label(root, wraplength=400, justify='left')
historique_description.pack()

# Choix d'équipement pour l'historique
historique_equipement_label = tk.Label(root, text="Choisissez un set d'équipement:")
historique_equipement_label.pack()

historique_equipement_menu = tk.OptionMenu(root, equipement_var, *['A', 'B'])
historique_equipement_menu.pack()

# Boutons
generate_button = tk.Button(root, text="Générer Personnage", command=lambda: generer_personnage_interface(race_var.get(), classe_var.get(), historique_var.get(), equipement_var.get()))
generate_button.pack(pady=10)

export_button = tk.Button(root, text="Exporter en PDF", command=export_pdf_interface)
export_button.pack(pady=10)

# Lancer la fenêtre principale
root.mainloop()
