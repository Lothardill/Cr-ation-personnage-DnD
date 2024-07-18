import random
import tkinter as tk
from tkinter import messagebox
from faker import Faker
from pdfrw import PdfReader, PdfWriter, PageMerge

# Initialisation
fake = Faker()

# Définition des races, classes, attributs et bonus raciaux
races = {
    'Humain': {'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1},
    'Elfe': {'Dextérité': 2},
    'Nain': {'Constitution': 2},
    'Halfelin': {'Dextérité': 2},
    'Orc': {'Force': 2},
    'Demi-elfe': {'Charisme': 2},
    'Tieffelin': {'Intelligence': 1, 'Charisme': 2}
}

classes = ['Barbare', 'Guerrier', 'Paladin', 'Moine', 'Rôdeur', 'Roublard', 'Magicien', 'Clerc', 'Druide', 'Barde', 'Ensorceleur', 'Occultiste']

attributs = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']

equipements = {
    'Historique1': ['Épée', 'Bouclier'],
    'Historique2': ['Arc', 'Flèches'],
    'Historique3': ['Bâton magique', 'Potion']
}

historiques = list(equipements.keys())

# Génération aléatoire des attributs en utilisant 4d6, garder les 3 meilleurs
def generer_attributs():
    return {attr: sum(sorted([random.randint(1, 6) for _ in range(4)])[1:]) for attr in attributs}

# Appliquer les modificateurs raciaux
def appliquer_bonus_racial(attributs, race):
    bonus = races[race]
    for attr, value in bonus.items():
        attributs[attr] += value
    return attributs

# Génération d'un historique et d'une personnalité
def generer_historique():
    return fake.paragraph(nb_sentences=5)

def generer_personnalite():
    traits = [fake.word() for _ in range(3)]
    return ', '.join(traits)

# Génération du personnage complet
def generer_personnage(race, classe, historique):
    attributs = generer_attributs()
    attributs = appliquer_bonus_racial(attributs, race)
    
    personnage = {
        'Race': race,
        'Classe': classe,
        'Attributs': attributs,
        'Historique': generer_historique(),
        'Personnalité': generer_personnalite(),
        'Équipement': equipements[historique]
    }
    return personnage

# Remplir et exporter la fiche de personnage PDF
def remplir_pdf(personnage, template_path='5E_CharacterSheet_Fillable.pdf', output_path='personnage_dnd.pdf'):
    # Lire le template PDF
    template = PdfReader(template_path)
    annotations = template.pages[0]['/Annots']
    
    # Dictionnaire de mapping pour les champs
    field_map = {
        'CharacterName': personnage['Race'],
        'ClassLevel': personnage['Classe'],
        'Background': personnage['Historique'],
        'PlayerName': 'Generated',
        'Race ': personnage['Race'],
        'Alignment': 'Neutral',
        'STR': personnage['Attributs']['Force'],
        'DEX': personnage['Attributs']['Dextérité'],
        'CON': personnage['Attributs']['Constitution'],
        'INT': personnage['Attributs']['Intelligence'],
        'WIS': personnage['Attributs']['Sagesse'],
        'CHA': personnage['Attributs']['Charisme'],
    }

    # Remplir les champs du PDF
    for annotation in annotations:
        if annotation['/T']:
            key = annotation['/T'][1:-1]
            if key in field_map:
                annotation.update(
                    pdfrw.PdfDict(V='{}'.format(field_map[key]))
                )
    
    # Ecrire le fichier PDF de sortie
    PdfWriter().write(output_path, template)
    messagebox.showinfo("Exportation réussie", f"Personnage exporté en PDF: {output_path}")

# Interface utilisateur
def generer_personnage_interface():
    race = race_var.get()
    classe = classe_var.get()
    historique = historique_var.get()
    personnage = generer_personnage(race, classe, historique)
    afficher_personnage(personnage)
    global current_personnage
    current_personnage = personnage

def afficher_personnage(personnage):
    race_label.config(text=f"Race: {personnage['Race']}")
    classe_label.config(text=f"Classe: {personnage['Classe']}")
    
    attributs_text = "\n".join([f"{attr}: {value}" for attr, value in personnage['Attributs'].items()])
    attributs_label.config(text=f"Attributs:\n{attributs_text}")
    
    historique_text.delete(1.0, tk.END)
    historique_text.insert(tk.END, personnage['Historique'])
    
    personnalite_label.config(text=f"Personnalité: {personnage['Personnalité']}")
    equipement_label.config(text=f"Équipement: {', '.join(personnage['Équipement'])}")

def export_pdf_interface():
    if current_personnage:
        remplir_pdf(current_personnage)
    else:
        messagebox.showwarning("Avertissement", "Veuillez générer un personnage avant d'exporter.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Générateur de Personnages DnD")

# Variables pour les choix de l'utilisateur
race_var = tk.StringVar(value='Humain')
classe_var = tk.StringVar(value='Guerrier')
historique_var = tk.StringVar(value='Historique1')

# Menus déroulants pour sélectionner la race, la classe et l'historique
tk.Label(root, text="Choisissez une race:").pack()
tk.OptionMenu(root, race_var, *races.keys()).pack()

tk.Label(root, text="Choisissez une classe:").pack()
tk.OptionMenu(root, classe_var, *classes).pack()

tk.Label(root, text="Choisissez un historique:").pack()
tk.OptionMenu(root, historique_var, *historiques).pack()

# Boutons
generate_button = tk.Button(root, text="Générer Personnage", command=generer_personnage_interface)
generate_button.pack(pady=10)

export_button = tk.Button(root, text="Exporter en PDF", command=export_pdf_interface)
export_button.pack(pady=10)

# Labels pour afficher les informations du personnage
race_label = tk.Label(root, text="Race:")
race_label.pack()

classe_label = tk.Label(root, text="Classe:")
classe_label.pack()

attributs_label = tk.Label(root, text="Attributs:")
attributs_label.pack()

historique_label = tk.Label(root, text="Historique:")
historique_label.pack()

historique_text = tk.Text(root, height=10, width=50)
historique_text.pack()

personnalite_label = tk.Label(root, text="Personnalité:")
personnalite_label.pack()

equipement_label = tk.Label(root, text="Équipement:")
equipement_label.pack()

current_personnage = None

# Lancer la fenêtre principale
root.mainloop()