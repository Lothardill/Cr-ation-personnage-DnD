import random

# Étape 1: Nom du personnage
character_name = input("Entrez le nom de votre personnage: ")

# Étape 2: Choix de la race
races = {
    "Nain": ["Nain des montagnes", "Nain des collines"],
    "Demi-orc": None,
    "Drakéide": None,
    "Humain": None,
    "Elfe": ["Elfe des bois", "Haut elfe", "Elfe noir"],
    "Halfelin": ["Halfelin pied-léger", "Halfelin robuste"],
    "Gnome": ["Gnome des forêts", "Gnome des roches"],
    "Tieffelin": None,
    "Demi-elfe": None
}

print("Choisissez une race parmi les suivantes:")
for i, race in enumerate(races.keys()):
    print(f"{i+1}. {race}")

race_choice = int(input("Entrez le numéro de la race: ")) - 1
race = list(races.keys())[race_choice]

if races[race]:
    print(f"Choisissez un type de {race} parmi les suivants:")
    for i, subrace in enumerate(races[race]):
        print(f"{i+1}. {subrace}")
    subrace_choice = int(input("Entrez le numéro du type: ")) - 1
    subrace = races[race][subrace_choice]
else:
    subrace = None

# Étape 3: Choix de la classe
classes = [
    "Barbare", "Barde", "Clerc", "Druide", "Ensorceleur", "Guerrier",
    "Magicien", "Moine", "Occultiste", "Paladin", "Rôdeur", "Roublard"
]

print("Choisissez une classe parmi les suivantes:")
for i, cls in enumerate(classes):
    print(f"{i+1}. {cls}")

class_choice = int(input("Entrez le numéro de la classe: ")) - 1
character_class = classes[class_choice]

# Étape 4: Choix de l'historique
backgrounds = [
    "Acolyte", "Artisan de guilde", "Artiste", "Charlatan", "Criminel",
    "Enfant des rues", "Ermite", "Héros du peuple", "Marin", "Noble",
    "Sage", "Sauvageon", "Soldat"
]

print("Choisissez un historique parmi les suivants:")
for i, background in enumerate(backgrounds):
    print(f"{i+1}. {background}")

background_choice = int(input("Entrez le numéro de l'historique: ")) - 1
character_background = backgrounds[background_choice]

# Étape 5: Génération des caractéristiques
def roll_dice():
    rolls = [random.randint(1, 6) for _ in range(4)]
    return sum(sorted(rolls)[1:])

stats = [roll_dice() for _ in range(6)]
print("Vos caractéristiques générées sont:", stats)

# Étape 6: Calcul des modificateurs de caractéristiques
def calculate_modifier(stat):
    return (stat - 10) // 2

modifiers = [calculate_modifier(stat) for stat in stats]
print("Vos modificateurs de caractéristiques sont:", modifiers)

# Étape 7: Détermination de l'équipement et des compétences
# (Cette étape nécessitera des informations supplémentaires sur les classes et les historiques)

# Étape 8: Remplir la feuille de personnage PDF
# Nous utiliserons une bibliothèque comme reportlab ou pdfrw pour cette partie

# Pour l'instant, nous allons juste imprimer les informations collectées
print("\n--- Fiche de Personnage ---")
print(f"Nom: {character_name}")
print(f"Race: {race} {subrace if subrace else ''}")
print(f"Classe: {character_class}")
print(f"Historique: {character_background}")
print(f"Caractéristiques: {stats}")
print(f"Modificateurs: {modifiers}")