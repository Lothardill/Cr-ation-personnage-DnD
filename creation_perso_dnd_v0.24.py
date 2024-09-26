import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import textwrap

# Classes de données pour encapsuler les caractéristiques du jeu
class StyleDeCombat:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

class Classe:
    def __init__(self, nom, description, details, capacites, nombre_outils, outils, nombre_de_competence, competences,
                 sort_mineur_classe, nombre_sort_mineur_classe, sort_niveau_un_classe, nombre_sort_niveau_un_classe,
                 styles_de_combat, argent_classe, packs, dd_sauvegarde_sorts=None, modificateur_attaque_sort=None,
                 ca=None, jets_de_sauvegarde=None, pv=None):
        self.nom = nom
        self.description = description
        self.details = details
        self.capacites = capacites
        self.nombre_outils = nombre_outils
        self.outils = outils
        self.nombre_de_competence = nombre_de_competence
        self.competences = competences
        self.sort_mineur_classe = sort_mineur_classe
        self.nombre_sort_mineur_classe = nombre_sort_mineur_classe
        self.sort_niveau_un_classe = sort_niveau_un_classe
        self.nombre_sort_niveau_un_classe = nombre_sort_niveau_un_classe
        self.styles_de_combat = styles_de_combat
        self.argent_classe = argent_classe
        self.packs = packs
        self.dd_sauvegarde_sorts = dd_sauvegarde_sorts if dd_sauvegarde_sorts is not None else "Pas de DD"
        self.modificateur_attaque_sort = modificateur_attaque_sort
        self.ca = ca if ca is not None else "10 + modificateur de Dextérité"
        self.jets_de_sauvegarde = jets_de_sauvegarde if jets_de_sauvegarde is not None else "Aucun"
        self.pv = pv if pv is not None else 8
        
    def calculer_argent(self):
        des, multiplicateur = map(int, self.argent_classe.split('d4 x '))
        somme = sum(random.randint(1, 4) for _ in range(des))
        return somme * multiplicateur

class Race:
    def __init__(self, nom, description, details, bonus, choix_bonus, competences, nombre_competences_race, outils, sort_race, nombre_sort_race, langues, nombre_de_langue, langue_parlee_race, armes_maitrisees_race, armures_maitrisees_race):
        self.nom = nom
        self.description = description
        self.details = details
        self.bonus = bonus
        self.choix_bonus=choix_bonus
        self.competences = competences
        self.nombre_competences_race = nombre_competences_race
        self.outils = outils
        self.sort_race = sort_race
        self.nombre_sort_race = nombre_sort_race
        self.langues = langues
        self.nombre_de_langue = nombre_de_langue
        self.langue_parlee_race = langue_parlee_race
        self.armes_maitrisees_race=armes_maitrisees_race
        self.armures_maitrisees_race=armures_maitrisees_race

class Historique:
    def __init__(self, nom, description, details, competences, outils, choix_outils, langues, nombre_de_competence, nombre_de_langue_historique, equipement, argent_historique, capacite):
        self.nom = nom
        self.description = description
        self.details = details
        self.competences = competences
        self.outils = outils
        self.choix_outils = choix_outils
        self.langues = langues
        self.nombre_de_competence = nombre_de_competence
        self.nombre_de_langue_historique = nombre_de_langue_historique
        self.equipement = equipement
        self.argent_historique = argent_historique
        self.capacite = capacite

class Personnage:
    def __init__(self, classes, races, historiques):
        self.classes = classes
        self.races = races
        self.historiques = historiques
        self.selected_values = []
        self.comboboxes = []
        self.points_disponibles = 27
        self.attributs_personnage = {attr: 8 for attr in attributs_list}
        self.expertise_selections = ["", ""]  # Pour stocker les choix d'expertise des deux menus
        

    def format_value(self, value):
        if value in self.selected_values:
            return f"{value} (déjà sélectionné)"
        return value

    def clean_value(self, value):
        return value.replace(" (déjà sélectionné)", "")

    def extraire_competences_et_langues(self, classe_selectionnee, race_selectionnee, historique_selectionne):
        competences_disponibles_classe = set()
        competences_disponibles_historique = set()
        langues_disponibles = set(langues_standard + langues_exotiques)
        outils_disponibles = set()

        if classe_selectionnee:
            competences_disponibles_classe.update(self.classes[classe_selectionnee].competences.split(', '))
            outils_disponibles.update(self.classes[classe_selectionnee].outils)

        if race_selectionnee:
            # Ensure class and race competencies are separate
            competences_disponibles_race = set()
            competences_disponibles_race.update(self.races[race_selectionnee].competences)

            outils_disponibles.update(self.races[race_selectionnee].outils)
            langues_parlees_race = self.races[race_selectionnee].langue_parlee_race.split(', ')
            for langue in langues_parlees_race:
                self.selected_values.append(langue)

        if historique_selectionne:
            competences_disponibles_historique.update(self.historiques[historique_selectionne].competences)
            outils_disponibles.update(self.historiques[historique_selectionne].outils)
            outils_disponibles.update(self.historiques[historique_selectionne].choix_outils)

        return competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles
    
    def augmenter_attribut(self, attribut):
        if self.points_disponibles > 0:
            current_value = self.attributs_personnage[attribut]
            next_value = current_value + 1
            if next_value in costs:
                cost = costs[next_value] - costs[current_value]
                if cost <= self.points_disponibles:
                    self.attributs_personnage[attribut] = next_value
                    self.points_disponibles -= cost
                    self.update_display()
                else:
                    messagebox.showwarning("Attention", "Vous n'avez pas suffisamment de points pour augmenter cet attribut.")
            else:
                messagebox.showwarning("Attention", "Cette valeur d'attribut est au maximum permis.")
        else:
            messagebox.showwarning("Attention", "Vous n'avez plus de points disponibles.")

    def diminuer_attribut(self, attribut):
        current_value = self.attributs_personnage[attribut]
        previous_value = current_value - 1
        if previous_value in costs:
            cost = costs[current_value] - costs[previous_value]
            self.attributs_personnage[attribut] = previous_value
            self.points_disponibles += cost
            self.update_display()
        else:
            messagebox.showwarning("Attention", "Cette valeur d'attribut est au minimum permis.")

    def calculer_modificateur(self, valeur):
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

    def update_display(self):
        # Initialiser une variable pour stocker les modificateurs pour chaque caractéristique
        self.modificateurs_pour_la_fiche_perso = {}  # Remise à zéro à chaque appel de update_display

        race_selectionnee = race_combobox.get()  # Récupérer la race sélectionnée
        if race_selectionnee == "Demi-elfe":  # Si la race est Demi-elfe
            # Récupérer les choix personnalisés des combobox pour le Demi-elfe
            custom_bonus_1 = choix_bonus_1_combobox.get()
            custom_bonus_2 = choix_bonus_2_combobox.get()
        else:
            custom_bonus_1 = None
            custom_bonus_2 = None

        for i, attribut in enumerate(attributs_list):
            valeur = self.attributs_personnage[attribut]

            # Récupérer le bonus racial
            bonus = self.races[race_selectionnee].bonus.get(attribut, 0) if race_selectionnee else 0

            # Ajouter les bonus personnalisés (spécifique au Demi-elfe)
            if race_selectionnee == "Demi-elfe":
                if attribut == custom_bonus_1:
                    bonus += 1
                if attribut == custom_bonus_2:
                    bonus += 1

            total = valeur + bonus  # Calculer la valeur totale avec le bonus
            modificateur = self.calculer_modificateur(total)  # Calcul du modificateur

            # Stocker le modificateur dans la variable self.modifiers
            self.modificateurs_pour_la_fiche_perso[attribut] = modificateur

            # Debugging output
            print(f"{attribut} : ({modificateur})")
            print(self.modificateurs_pour_la_fiche_perso)

            # Mettre à jour les labels avec les nouvelles valeurs
            attribut_valeur_labels[i].config(text=f"{valeur}")
            attribut_bonus_labels[i].config(text=f"{bonus:+d}")
            attribut_valeur_finale_labels[i].config(text=f"{total} ({modificateur:+d})")

        # Mettre à jour les points restants
        points_label.config(text=f"Points restants: {self.points_disponibles}")


    def valider_repartition(self):
        if self.points_disponibles == 0:
            messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
        else:
            messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

    def update_combobox_options(self, combobox, values, label_text):
        current_value = combobox.get()
        formatted_values = []
        for value in values:
            if value in self.selected_values and value != current_value:
                formatted_values.append(f"{value} (déjà sélectionné)")
            else:
                formatted_values.append(value)

        combobox['values'] = formatted_values
        if current_value not in formatted_values:
            combobox.set('')
        combobox.label_text = label_text

    def extraire_competences_selectionnees(self):
        competences_selectionnees = []
        for combobox, label_text in self.comboboxes:
            if combobox.winfo_exists():  # Vérifier si la combobox existe toujours
                value = combobox.get()
                if value and "(déjà sélectionné)" not in value:
                    competences_selectionnees.append(value)
        print(f"Compétences extraites: {competences_selectionnees}")  # Debugging
        return competences_selectionnees


          
    def update_comboboxes(self):
    # Supprimer les comboboxes détruites de la liste
        self.comboboxes = [(combobox, label_text) for combobox, label_text in self.comboboxes if combobox.winfo_exists()]

        classe_selectionnee = classe_combobox.get()
        race_selectionnee = race_combobox.get()
        historique_selectionne = historique_combobox.get()

        competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles = self.extraire_competences_et_langues(classe_selectionnee, race_selectionnee, historique_selectionne)
        langues_parlees_race = set()

        if race_selectionnee:
            langues_parlees_race.update(self.races[race_selectionnee].langue_parlee_race.split(', '))

        for combobox, label_text in self.comboboxes:
            if "compétences de la classe" in label_text.lower():
                values = competences_disponibles_classe
            elif "compétences de la race" in label_text.lower():
                values = self.races[race_selectionnee].competences
            elif "compétences de l'historique" in label_text.lower():
                values = competences_disponibles_historique
            elif "langues de la race" in label_text.lower():
                values = langues_disponibles
            elif "langues de l'historique" in label_text.lower():
                values = langues_disponibles
            elif "outils de la race" in label_text.lower():
                values = self.races[race_selectionnee].outils
            elif "outils de la classe" in label_text.lower():
                values = self.classes[classe_selectionnee].outils
            elif "outils de l'historique" in label_text.lower():
                if label_text == "Outils de l'historique":
                    values = self.historiques[historique_selectionne].outils
                elif label_text == "Choix d'outils de l'historique":
                    values = self.historiques[historique_selectionne].choix_outils

            self.update_combobox_options(combobox, values, label_text)


    def update_selected_values(self):
        self.selected_values = []
        for combobox, label_text in self.comboboxes:
            try:
                value = combobox.get()
                if value:
                    self.selected_values.append(self.clean_value(value))
            except tk.TclError:
            # La combobox a été détruite, passer
                continue
        print(f"Valeurs sélectionnées mises à jour: {self.selected_values}")  # Debugging
        self.update_comboboxes()

    def creer_menu_deroulant(self, options, label_text, parent_frame, nombre=None):
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
                formatted_options = [self.format_value(opt) for opt in sorted(options)]
                combobox = ttk.Combobox(frame, values=formatted_options, state="readonly")
                combobox.pack(side=tk.LEFT, padx=5)
                combobox.bind("<<ComboboxSelected>>", lambda event: [self.update_selected_values(), update_options()])
                self.comboboxes.append((combobox, label_text))
            
    def reset_selected_values(self):
        self.selected_values = []

    def reset_comboboxes(self):
        for combobox, label_text in self.comboboxes:
            combobox.set('')

    def update_maitrise(self):
        # Réinitialiser le cadre de maîtrise pour tout effacer
        for widget in maitrise_frame.winfo_children():
            widget.destroy()

        # Reset comboboxes 
        self.comboboxes = []

        # Récupérer les compétences et outils disponibles en fonction de la classe, de la race et de l'historique
        competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles = self.extraire_competences_et_langues(
            classe_combobox.get(), race_combobox.get(), historique_combobox.get()
            )

        # Logique spécifique aux races
        race_selectionnee = race_combobox.get()
        if race_selectionnee: 
            competences_race = self.races[race_selectionnee].competences
            nombre_competences_race = self.races[race_selectionnee].nombre_competences_race

            # S'il y a des compétences spécifique aux races, créer des nouveaux menus
            if nombre_competences_race > 0:
                self.creer_menu_deroulant(competences_race, "Compétences de la race", maitrise_frame, nombre=nombre_competences_race)

        # Logique des compétences de classes
        classe_selectionnee = classe_combobox.get()
        if classe_selectionnee:
            nombre_de_competence = self.classes[classe_selectionnee].nombre_de_competence
            competences_classe = list(self.classes[classe_selectionnee].competences.split(', '))  # Utiliser uniquement les compétences de la classe
            self.creer_menu_deroulant(competences_classe, "Compétences de la classe", maitrise_frame, nombre=nombre_de_competence)

        # Logique des compétences d'historique
        historique_selectionne = historique_combobox.get()
        if historique_selectionne:
            nombre_de_competence_historique = self.historiques[historique_selectionne].nombre_de_competence
            competences_historique = list(competences_disponibles_historique)
            self.creer_menu_deroulant(competences_historique, "Compétences de l'historique", maitrise_frame, nombre=nombre_de_competence_historique)

        # Logiques de maîtrise d'outils (Race, Classe, Historique)
        if race_selectionnee:
            outils_race = self.races[race_selectionnee].outils
            self.creer_menu_deroulant(outils_race, "Outils de la race", maitrise_frame, 1)
        
        classe_selectionnee = classe_combobox.get()
        if classe_selectionnee:
            nombre_outils_classe = self.classes[classe_selectionnee].nombre_outils
            if nombre_outils_classe == 1:
                self.creer_menu_deroulant(self.classes[classe_selectionnee].outils, "Outils de la classe", maitrise_frame, 1)
                
            # Créer un menu déroulant pour chaque outil (en fonction de nombre_outils)
            if nombre_outils_classe > 1:
                outils_classe = list(self.classes[classe_selectionnee].outils.split(', '))
                self.creer_menu_deroulant(outils_classe, "Outils de la classe", maitrise_frame, nombre=nombre_outils_classe)

        if historique_selectionne:
            outils_historiques = self.historiques[historique_selectionne].outils
            choix_outils_historiques = self.historiques[historique_selectionne].choix_outils
            if outils_historiques or choix_outils_historiques:
                tk.Label(maitrise_frame, text="Outils de l'historique", font=('Arial', 10, 'bold')).pack(anchor="w")
                outils_historiques_frame = tk.Frame(maitrise_frame)
                outils_historiques_frame.pack(anchor="w", pady=5)
                if outils_historiques:
                    formatted_outils_historiques = [self.format_value(opt) for opt in sorted(outils_historiques)]
                    combobox_outils_historique = ttk.Combobox(outils_historiques_frame, values=formatted_outils_historiques, state="readonly")
                    combobox_outils_historique.pack(side=tk.LEFT, padx=5)
                    self.comboboxes.append((combobox_outils_historique, "Outils de l'historique"))

                if choix_outils_historiques:
                    formatted_choix_outils_historiques = [self.format_value(opt) for opt in sorted(choix_outils_historiques)]
                    combobox_choix_outils_historiques = ttk.Combobox(outils_historiques_frame, values=formatted_choix_outils_historiques, state="readonly")
                    combobox_choix_outils_historiques.pack(side=tk.LEFT, padx=5)
                    self.comboboxes.append((combobox_choix_outils_historiques, "Choix d'outils de l'historique"))
        
        race_combobox.bind("<<ComboboxSelected>>", lambda event: on_race_selected())
        
# Données de jeu
attributs_list = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']
competences_completes = ['Acrobaties', 'Arcanes', 'Athlétisme', 'Discrétion', 'Dressage', 'Escamotage', 'Histoire', 'Intimidation', 'Investigation', 'Médecine', 'Nature', 'Perception', 'Perspicacité', 'Persuasion', 'Religion', 'Représentation', 'Survie', 'Tromperie']
langues_standard = ['Commun', 'Elfique', 'Géant', 'Gnome', 'Gobelin', 'Halfelin', 'Nain', 'Orc']
langues_exotiques = ['Abyssal', 'Céleste', 'Commun des profondeurs', 'Draconique', 'Infernal', 'Primordial', 'Profond', 'Sylvestre']
dragons_info = [
    ("Blanc", "Froid", "cône de 4,50 m (JdS de Con.)", "Froid"),
    ("Bleu", "Foudre", "ligne de 1,50 x 9 m (JdS de Dex.)", "Foudre"),
    ("Noir", "Acide", "ligne de 1,50 x 9 m (JdS de Dex.)", "Acide"),
    ("Rouge", "Feu", "cône de 4,50 m (JdS de Dex.)", "Feu"),
    ("Vert", "Poison", "cône de 4,50 m (JdS de Con.)", "Poison"),
    ("Airain", "Feu", "ligne de 1,50 x 9 m (JdS de Dex.)", "Feu"),
    ("Argent", "Froid", "cône de 4,50 m (JdS de Con.)", "Froid"),
    ("Bronze", "Foudre", "ligne de 1,50 x 9 m (JdS de Dex.)", "Foudre"),
    ("Cuivre", "Acide", "ligne de 1,50 x 9 m (JdS de Dex.)", "Acide"),
    ("Or", "Feu", "cône de 4,50 m (JdS de Dex.)", "Feu")
]
sort_mineur = [
    {"nom": "Amis", "type": "enchantement", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "S, M (une petite quantité de maquillage appliquée sur le visage durant l'incantation)", "durée": "concentration, jusqu'à 1 minute", "description": "Pour la durée du sort, vous avez un avantage à tous vos jets de Charisme effectués contre une créature de votre choix qui n'a pas une attitude hostile envers vous. Lorsque le sort prend fin, la créature réalise que vous avez utilisé la magie pour l'influencer et devient hostile à votre égard. Une créature plutôt violente risque de vous attaquer. D'autres créatures peuvent vous demander de l'argent ou un service (à la discrétion du MD), cela dépend de la nature de l'échange que vous avez eu avec la créature."},
    {"nom": "Aspersion d'acide", "type": "invocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous propulsez une bulle d'acide. Choisissez une ou deux créatures que vous pouvez voir, à 1,50 mètre ou moins l'une de l'autre, dans la portée du sort. La cible doit réussir un jet de sauvegarde de Dextérité ou subir 1d6 dégâts d'acide. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Assistance", "type": "divination", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "concentration, jusqu'à 1 minute", "description": "Vous touchez une créature consentante. Une fois avant la fin du sort, la cible peut lancer un d4 et ajouter le résultat du dé à un jet de caractéristique de son choix. Elle peut lancer le dé avant ou après avoir effectué son jet de caractéristique. Le sort prend alors fin."},
    {"nom": "Bouffée de poison", "type": "invocation", "temps_incantation": "1 action", "portée": "3 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous tendez votre paume vers une créature visible dans la portée du sort et vous projetez une bouffée de gaz nocif de votre main. La créature doit réussir un jet de sauvegarde de Constitution ou subir 1d12 dégâts de poison. Les dégâts de ce sort augmentent de 1d12 lorsque vous atteignez le niveau 5 (2d12), le niveau 11 (3d12) et le niveau 17 (4d12)."},
    {"nom": "Contact glacial", "type": "nécromancie", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "1 round", "description": "Vous créez une main squelettique fantomatique dans l'espace d'une créature à portée. Faites une attaque à distance avec un sort contre la créature pour l'étreindre d'une froideur sépulcrale. Si le coup touche, la cible subit 1d8 dégâts nécrotiques, et elle ne peut récupérer ses points de vie avant le début de votre prochain tour. Jusque-là, la main fantomatique s'accroche à la cible. Si vous ciblez un mort-vivant, il aura également un désavantage à ses jets d'attaque contre vous jusqu'à la fin de votre prochain tour. Les dégâts de ce sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8) et le niveau 17 (4d8)."},
    {"nom": "Contrôle des flammes", "type": "transmutation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "S", "durée": "instantanée ou 1 heure (voir ci-dessous)", "description": "Vous choisissez un feu non magique visible dans la portée du sort de 1,50 mètre d'arête maximum. Vous pouvez l'affecter de l'une des façons suivantes : Vous pouvez faire grossir instantanément le feu de 1,50 mètre dans une direction, à condition que du bois ou un autre combustible soit présent dans cette nouvelle zone. Vous pouvez éteindre instantanément les flammes à l'intérieur du cube. Vous pouvez doubler ou diminuer de moitié l'aire de lumière vive ou de lumière faible projetée par le feu et/ou en changer la couleur. La modification dure 1 heure. Vous pouvez faire apparaître des formes simples (comme une vague silhouette de créature, un objet inanimé ou une localisation) dans les flammes et les animer comme bon vous semble. Les silhouettes persistent pendant 1 heure. Si vous lancez ce sort plusieurs fois, vous pouvez avoir jusqu'à trois de ses effets non-instantanés actifs à la fois, et vous pouvez en dissiper un en une action."},
    {"nom": "Coup au but", "type": "divination", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "S", "durée": "concentration, jusqu'à 1 round", "description": "Vous tendez votre main et pointez un doigt en direction d'une cible à portée. Votre magie vous aide à trouver une petite faille dans les défenses de votre cible. Lors de votre prochain tour, vous obtenez un avantage pour votre premier jet d'attaque contre la cible, à condition que le sort ne soit pas déjà terminé."},
    {"nom": "Coup de tonnerre", "type": "évocation", "temps_incantation": "1 action", "portée": "1,50 mètre", "composantes": "S", "durée": "instantanée", "description": "Vous créez un bruit de tonnerre qui peut être entendu jusqu'à 30 mètres. Hormis vous-même, toute créature à portée doit réussir un jet de sauvegarde de Constitution ou subir 1d6 dégâts de tonnerre. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Décharge occulte", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Un rayon d'énergie crépitante zigzague jusqu'à une créature à portée. Effectuez une attaque à distance avec un sort contre la cible. En cas de réussite, la cible subit 1d10 dégâts de force. Ce sort crée plus d'un rayon lorsque vous montez en niveau : deux rayons au niveau 5, trois rayons au niveau 11, et quatre rayons au niveau 17. Vous pouvez diriger les rayons sur une cible unique et les répartir entre différentes créatures. Effectuez un jet d'attaque séparé pour chaque rayon."},
    {"nom": "Druidisme", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S", "durée": "instantanée", "description": "En murmurant aux esprits de la nature, vous créez l'un des effets suivants, dans la portée du sort : Vous créez un minuscule et inoffensif effet sensoriel qui permet de prédire les conditions météorologiques pour les 24 prochaines heures, à l'endroit où vous êtes. L'effet pourrait se manifester comme un orbe doré pour indiquer un ciel dégagé, un nuage pour annoncer la pluie, un flocon de neige pour une chute de neige et ainsi de suite. L'effet persiste pour 1 round. Vous provoquez immédiatement la floraison d'une fleur, l'ouverture d'une gousse ou le débourrement d'un bourgeon de feuille. Vous créez un inoffensif effet sensoriel instantané comme une chute de feuilles, une légère brise, le son d'un petit animal ou une subtile odeur de putois. L'effet doit se limiter à un cube de 1,50 mètre d'arête. Vous éteignez ou allumez instantanément une bougie, une torche ou un petit feu de camp."},
    {"nom": "Embrasement", "type": "invocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "concentration, jusqu'à 1 minute", "description": "Vous créez un feu de joie sur un sol visible dans la portée du sort. Jusqu'à ce que le sort finisse, le feu de joie magique occupe un cube de 1,50 mètre d'arête. Toute créature située à la place du feu de joie lorsque vous lancez le sort doit réussir un jet de sauvegarde de Dextérité ou subir 1d8 dégâts de feu. Une créature doit aussi faire un jet de sauvegarde lorsqu'elle se déplace dans l'espace occupé par le feu de joie pour la première fois dans un tour ou si elle termine son tour dans cet espace. Le feu de joie met le feu aux objets inflammables dans sa zone qui ne sont ni tenus ni portés. Les dégâts de ce sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8) et le niveau 17 (4d8)."},
    {"nom": "Éruption de lames", "type": "invocation", "temps_incantation": "1 action", "portée": "personnelle (rayon de 1,50 mètre)", "composantes": "V", "durée": "instantanée", "description": "Vous créez temporairement un cercle de lames spectrales autour de vous. Toutes les autres créatures dans un rayon de 1,50 mètre autour de vous doivent réussir un jet de sauvegarde de Dextérité ou subir 1d6 dégâts de force. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez les niveaux 5 (2d6), 11 (3d6) et 17 (4d6)."},
    {"nom": "Façonnage de l'eau", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "S", "durée": "instantanée ou 1 heure (voir ci-dessous)", "description": "Choisissez un cube d'eau visible de 1,50 mètre d'arête dans la portée du sort. Vous pouvez alors le manipuler d'une des façons suivantes : Vous déplacez instantanément ou modifiez le sens du courant selon vos directives jusqu'à 1,50 mètre dans n'importe quelle direction. Ce mouvement n'a pas assez de force pour causer des dégâts. Vous pouvez faire apparaître des formes simples dans l'eau et les animer selon vos instructions. Ce changement dure 1 heure. Vous modifiez la couleur ou l'opacité de l'eau. L'eau doit être transformée de façon homogène. Ce changement dure 1 heure. Vous gelez l'eau, à condition qu'elle ne contienne aucune créature. L'eau dégèle au bout de 1 heure. Si vous lancez ce sort plusieurs fois, vous ne pouvez avoir que deux de ces effets non-instantanés actifs à la fois, et vous pouvez en dissiper un en une action."},
    {"nom": "Façonnage de la terre", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "S", "durée": "instantanée ou 1 heure (voir ci-dessous)", "description": "Vous choisissez une section de terre ou de pierre qui ne dépasse pas un cube de 1,50 mètre d'arête et visible dans la portée du sort. Vous pouvez alors la manipuler d'une des façons suivantes : Si vous ciblez une zone de terre meuble, vous pouvez instantanément la creuser, la déplacer sur le sol, et la déposer jusqu'à 1,50 mètre plus loin. Ce mouvement n'a pas assez de force pour causer des dégâts. Vous pouvez faire apparaître des formes et/ou des couleurs sur la terre ou la pierre, représentant des mots, créant des images ou formant des motifs. La modification dure 1 heure. Si la terre ou la pierre est au sol, vous pouvez la transformer en terrain difficile. À l'inverse, vous pouvez rendre normal un sol considéré comme terrain difficile. Ce changement dure 1 heure. Si vous lancez ce sort plusieurs fois, vous pouvez avoir jusqu'à deux de ces effets non-instantanés actifs à la fois, et vous pouvez en dissiper un en une action."},
    {"nom": "Ferrage foudroyant", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (rayon de 4,50 mètres)", "composantes": "V", "durée": "instantanée", "description": "Vous créez une décharge d'énergie foudroyante qui frappe une créature de votre choix que vous pouvez voir dans un rayon de 4,50 mètres autour de vous. La cible doit réussir un jet de sauvegarde de Force ou être attirée vers vous en ligne droite sur 3 mètres puis subir 1d8 dégâts de foudre si elle se retrouve à 1,50 mètre ou moins de vous. Les dégâts de ce sort augmentent de 1d8 lorsque vous atteignez les niveaux 5 (2d8), 11 (3d8) et 17 (4d8)."},
    {"nom": "Flamme sacrée", "type": "évocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Un rayonnement semblable à des flammes descend sur une créature que vous pouvez voir dans la portée du sort. La cible doit réussir un jet de sauvegarde de Dextérité ou subir 1d8 dégâts radiants. La cible ne gagne aucun bénéfice d'abri pour ce jet de sauvegarde. Les dégâts du sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8), et le niveau 17 (4d8)."},
    {"nom": "Flammes", "type": "invocation", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "10 minutes", "description": "Une flamme vacillante apparaît dans votre main. La flamme y reste pour la durée du sort et n'endommage pas votre équipement, ni ne vous blesse. La flamme diffuse une lumière vive dans un rayon de 3 mètres et une lumière faible dans un rayon supplémentaire de 3 mètres. Le sort prend fin si vous l'annulez par une action ou si vous le lancez de nouveau. Vous pouvez également attaquer avec la flamme, mettant ainsi un terme au sort. Lorsque vous incantez ce sort, ou en utilisant une action lors d'un tour suivant, vous pouvez lancer la flamme sur une créature située à 9 mètres de vous maximum. Faites une attaque à distance avec un sort. En cas de réussite, la cible subit 1d8 dégâts de feu. Les dégâts de ce sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8) et le niveau 17 (4d8)."},
    {"nom": "Fouet épineux", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (la tige d'une plante avec des épines)", "durée": "instantanée", "description": "Vous créez une longue et épaisse liane ressemblant à de la vigne et recouverte d'épines qui, selon vos ordres, s'accroche à une créature à portée. Effectuez une attaque au corps à corps avec un sort contre la cible. Si l'attaque touche, la créature subit 1d6 dégâts perforants, et si la créature est de taille G ou inférieure, vous la tirez de jusqu'à 3 mètres vers vous. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Gelure", "type": "évocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous faites se former une couche de gel engourdissante sur une créature que vous voyez à portée. La cible doit réussir un jet de sauvegarde de Constitution, sans quoi elle subit 1d6 dégâts de froid et obtient un désavantage à son prochain jet d'attaque avec une arme réalisé avant la fin de son prochain tour. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Glas", "type": "nécromancie", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous pointez une créature que vous pouvez voir à portée, et le son douloureux d'une cloche emplit l'air autour d'elle pendant un moment. La cible doit réussir un jet de sauvegarde de Sagesse ou subir 1d8 dégâts nécrotiques. Si la cible n'est pas à son maximum de points de vie, elle subit 1d12 de dégâts nécrotiques. Les dégâts du sort augmentent de un dé lorsque vous atteignez le niveau 5 (2d8 ou 2d12), le niveau 11 (3d8 ou 3d12) et le niveau 17 (4d8 ou 4d12)."},
    {"nom": "Gourdin magique", "type": "transmutation", "temps_incantation": "1 action bonus", "portée": "contact", "composantes": "V, S, M (du gui, une feuille de trèfle et un bâton ou un gourdin)", "durée": "1 minute", "description": "Le bois du bâton ou du gourdin que vous tenez est altéré par les pouvoirs de la nature. Pour la durée du sort, vous pouvez utiliser votre caractéristique d'incantation plutôt que votre Force pour les jets d'attaque au corps à corps et de dégâts avec cette arme, et les dégâts de l'arme deviennent des d8. De plus, l'arme devient une arme magique, si ce n'est pas déjà le cas. Ce sort se termine si vous le lancez de nouveau ou si vous lâchez l'arme enchantée."},
    {"nom": "Illusion mineure", "type": "illusion", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "S, M (un peu de laine de mouton)", "durée": "1 minute", "description": "Le lanceur de sorts crée un son ou l'image d'un objet à portée pendant une minute. Cette illusion se termine également si elle est révoquée au prix d'une action ou si ce sort est lancé une nouvelle fois. Si l'illusion est un son, le volume peut aller d'un simple chuchotement à un cri. Il peut s'agir de votre voix, de la voix de quelqu'un d'autre, du rugissement d'un lion, d'un roulement de tambours, ou tout autre son que vous choisissez. Le son peut autant ne pas diminuer en intensité pendant la durée du sort qu'être discret et produit à différents instants dans cet intervalle de temps. Si l'illusion est une image ou un objet (comme une chaise, des traces de pas boueuses ou un petit coffre) elle ne peut pas être plus large qu'un cube de 1,50 mètre d'arête. Cette image ne peut produire de son, lumière, odeur ou tout autre effet sensoriel. Une interaction physique avec l'image révèle l'illusion, car elle peut être traversée par n'importe quoi. Si une créature utilise une action pour examiner le son ou l'image, elle peut comprendre qu'il s'agit d'une illusion grâce à un jet d'Intelligence (Investigation) contre le DD de sauvegarde de votre sort. Si une créature discerne l'illusion pour ce qu'elle est, l'illusion s'évanouit pour la créature."},
    {"nom": "Infestation", "type": "invocation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (une puce vivante)", "durée": "instantanée", "description": "Vous faites apparaître momentanément sur une créature que vous pouvez voir à portée un nuage de mites, de puces ou d'autres parasites. La cible doit réussir un jet de sauvegarde de Constitution ou subir 1d6 dégâts de poison et se déplacer de 1,50 mètre dans une direction aléatoire, si elle peut se déplacer et que sa vitesse est d'au moins 1,50 mètre. Jetez un d4 pour la direction: 1=nord; 2=sud; 3=est; 4=ouest. Ce mouvement ne provoque pas d'attaques d'opportunité, et si la direction indiquée est bloquée la cible ne bouge pas. Les dégâts du sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Lame aux flammes vertes", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (rayon de 1,50 mètre)", "composantes": "V, M (une arme de corps à corps valant au moins 1 pa)", "durée": "instantanée", "description": "Vous brandissez l'arme utilisée pour l'incantation du sort et effectuez une attaque au corps à corps avec cette arme contre une créature à 1,50 mètre ou moins de vous. Si vous touchez, la cible subit les effets normaux de l'attaque et une flamme verdâtre jaillit de cette cible pour aller frapper une autre créature de votre choix que vous pouvez voir et qui se trouve dans un rayon de 1,50 mètre autour de la première créature. Cette seconde créature subit des dégâts de feu d'un montant égal au modificateur de votre caractéristique d'incantation. Les dégâts de ce sort augmentent suivant votre niveau. Au niveau 5, l'attaque de corps à corps inflige 1d8 dégâts de feu supplémentaires à la première cible, et les dégâts de feu subis par la seconde cible atteignent 1d8 + le modificateur de votre caractéristique d'incantation. Les deux jets de dégâts augmentent chacun de 1d8 supplémentaire aux niveaux 11 (2d8 et 2d8) et 17 (3d8 et 3d8)."},
    {"nom": "Lame retentissante", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (rayon de 1,50 mètre)", "composantes": "V, M (une arme de corps à corps valant au moins 1 pa)", "durée": "1 round", "description": "Vous brandissez l'arme utilisée pour l'incantation du sort et effectuez une attaque au corps à corps avec cette arme contre une créature à 1,50 mètre ou moins de vous. Si vous touchez, la cible subit les effets normaux de l'attaque et elle est enveloppée d'une énergie explosive jusqu'au début de votre prochain tour. Si la cible se déplace volontairement de 1,50 mètre ou plus pendant ce laps de temps, elle subit 1d8 dégâts de tonnerre et le sort se termine. Les dégâts de ce sort augmentent suivant votre niveau. Au niveau 5, l'attaque au corps à corps inflige 1d8 dégâts de tonnerre supplémentaires à la cible, et les dégâts que la cible subit si elle se déplace passent à 2d8. Les deux jets de dégâts augmentent ensuite de 1d8 aux niveaux 11 (2d8 et 3d8) et 17 (3d8 et 4d8)."},
    {"nom": "Lumière", "type": "évocation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, M (une luciole ou de la mousse phosphorescente)", "durée": "1 heure", "description": "Vous touchez un objet qui ne dépasse pas 3 mètres dans toutes les dimensions. Jusqu'à la fin du sort, l'objet émet une lumière vive dans un rayon de 6 mètres et une lumière faible sur 6 mètres supplémentaires. La lumière est de la couleur que vous voulez. Couvrir complètement l'objet avec quelque chose d'opaque bloque la lumière. Le sort se termine si vous le lancez de nouveau ou si vous le dissipez par une action. Si vous ciblez un objet tenu ou porté par une créature hostile, cette créature doit réussir un jet de sauvegarde de Dextérité pour éviter le sort."},
    {"nom": "Lumières dansantes", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S, M (un peu de phosphore ou d'écorce d'orme blanc, ou bien un ver luisant)", "durée": "concentration, jusqu'à 1 minute", "description": "Ce sort permet de créer jusqu'à quatre lumières, de la taille de torches, qui peuvent revêtir l'apparence de torches, de lanternes ou d'orbes brillantes qui flottent dans les airs. Il est possible de combiner les quatre lumières en une forme vaguement humanoïde brillante de taille M. Peu importe la forme choisie, chaque lumière produit une lumière faible qui éclaire dans un rayon de 3 mètres. Au prix d'une action bonus lors de votre tour, il est possible de déplacer les lumières jusqu'à 18 mètres vers un nouvel emplacement à portée. Une lumière doit se situer à 6 mètres ou moins d'une autre lumière créée par ce sort, et une lumière s'éclipse si elle se trouve au-delà de la portée du sort."},
    {"nom": "Main de mage", "type": "invocation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S", "durée": "1 minute", "description": "Une main spectrale apparaît à un point précis choisi à portée. La main expire à la fin de la durée du sort ou si elle est révoquée au prix d'une action. La main disparaît si elle se retrouve à plus de 9 mètres du lanceur de sorts ou si ce sort est jeté une nouvelle fois. Le lanceur de sorts peut utiliser son action pour contrôler la main. La main peut manipuler un objet, ouvrir une porte ou un contenant non verrouillé, ranger ou récupérer un objet d'un contenant ouvert, ou bien verser le contenu d'une fiole. La main peut être déplacée jusqu'à 9 mètres à chaque fois que vous l'utilisez. La main ne peut attaquer, activer des objets magiques ou transporter plus de 5 kg."},
    {"nom": "Message", "type": "transmutation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S, M (un petit bout de fil de cuivre)", "durée": "1 round", "description": "Vous pointez votre doigt en direction d'une créature à portée et murmurez un message. La cible (et seulement la cible) entend le message et peut répondre en un murmure que vous seul pouvez entendre. Vous pouvez lancer ce sort à travers des objets solides si vous connaissez bien la cible et que vous savez qu'elle est derrière l'obstacle. Ce sort est arrêté par un silence magique, 30 cm de pierre, 2,50 cm de métal, une fine feuille de plomb ou 90 cm de bois. Ce sort ne doit pas forcément suivre une ligne droite et peut contourner les angles ou passer par de petites ouvertures."},
    {"nom": "Moquerie cruelle", "type": "enchantement", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "instantanée", "description": "Vous vomissez un flot d'insultes entremêlées de subtils enchantements sur une créature à portée et que vous pouvez voir. Si la cible peut vous entendre (il n'est pas nécessaire qu'elle comprenne mais juste qu'elle devine votre intention), elle doit réussir un jet de sauvegarde de Sagesse ou subir 1d4 dégâts psychiques et avoir un désavantage au prochain jet d'attaque qu'elle fera avant la fin de son prochain tour. Les dégâts de ce sort augmentent de 1d4 lorsque vous atteignez le niveau 5 (2d4), le niveau 11 (3d4) et le niveau 17 (4d4)."},
    {"nom": "Mot de radiance", "type": "évocation", "temps_incantation": "1 action", "portée": "1,50 mètre", "composantes": "V, M (un symbole sacré)", "durée": "instantanée", "description": "Vous prononcez un mot divin et un éclat brûlant jaillit de vous. Toutes les créatures de votre choix à portée et que vous pouvez voir doivent réussir un jet de sauvegarde de Constitution ou bien prendre 1d6 dégâts radiants. Les dégâts du sort augmentent de 1d6 lorsque vous atteignez le niveau 5 (2d6), le niveau 11 (3d6) et le niveau 17 (4d6)."},
    {"nom": "Pierre magique", "type": "transmutation", "temps_incantation": "1 action bonus", "portée": "contact", "composantes": "V, S", "durée": "1 minute", "description": "Vous touchez un à trois cailloux et les imprégnez de magie. Vous ou quelqu'un d'autre peut faire une attaque à distance avec un sort avec un des ces cailloux en le jetant à la main ou en le lançant à l'aide d'une fronde. S'il est jeté, sa portée est de 18 mètres. Si quelqu'un d'autre attaque avec ces cailloux, il ajoute le modificateur de votre caractéristique d'incantation au jet d'attaque (et non pas la sienne). Si le coup touche, la cible prend 1d6 dégâts contondants + le modificateur de votre caractéristique d'incantation. Dans tous les cas, le caillou perd ses propriétés magiques. Si vous lancez ce sort à nouveau, le sort s'arrête pour tous les cailloux encore sous effet magique du sort précédent."},
    {"nom": "Piqûre mentale", "type": "enchantement", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "1 round", "description": "Vous injectez une pointe d'énergie psychique désorientante dans l'esprit d'une créature que vous pouvez voir à portée. La cible doit effectuer un jet de sauvegarde d'Intelligence. En cas d'échec, elle subit 1d6 dégâts psychiques et la première fois qu'elle effectuera un jet de sauvegarde avant la fin de votre prochain tour, elle devra lancer un d4 et soustraire le nombre obtenu du résultat de sa sauvegarde. Les dégâts de ce sort augmentent de 1d6 lorsque vous atteignez les niveaux 5 (2d6), 11 (3d6) et 17 (4d6)."},
    {"nom": "Poigne électrique", "type": "évocation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "instantanée", "description": "La foudre jaillit de votre main pour délivrer un choc électrique à une créature que vous essayez de toucher. Effectuez une attaque au corps à corps avec un sort contre la cible. Vous avez un avantage au jet d'attaque si la cible porte une armure en métal. En cas de réussite, la cible prend 1d8 dégâts de foudre, et elle ne peut pas prendre de réaction jusqu'au début de son prochain tour. Les dégâts du sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8) et le niveau 17 (4d8)."},
    {"nom": "Prestidigitation", "type": "transmutation", "temps_incantation": "1 action", "portée": "3 mètres", "composantes": "V, S", "durée": "jusqu'à 1 heure", "description": "Ce sort est un tour de magie mineur que les lanceurs de sorts novices emploient comme exercice. Ce sort permet de provoquer l'un des effets magiques suivants : Le sort crée instantanément un effet sensoriel inoffensif, comme une pluie d'étincelles, une bouffée d'air, de timides notes de musique, ou une étrange odeur. Le sort allume ou éteint instantanément une bougie, torche ou un petit feu de camp. Le sort nettoie ou souille instantanément un objet pas plus volumineux qu'un cube de 30 cm d'arête. Le sort réchauffe, refroidit ou assaisonne du matériel non vivant pouvant être contenu dans un cube de 30 cm d'arête pendant 1 heure. Le sort fait apparaître un symbole, une petite marque ou couleur sur un objet ou une surface pendant 1 heure. Le sort permet de créer une babiole non magique ou une image illusoire qui peut tenir dans votre main et qui dure jusqu'à la fin de votre prochain tour. Si le sort est lancé plusieurs fois, il est possible de conserver actifs 3 de ces effets non instantanés simultanément, et il est possible de révoquer ces effets au prix d'une action."},
    {"nom": "Protection contre les armes", "type": "abjuration", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "1 round", "description": "Vous tendez votre main et tracez un symbole de protection dans les airs. Jusqu'à la fin de votre prochain tour, vous obtenez la résistance contre les dégâts contondants, tranchants et perforants infligés par des attaques avec arme."},
    {"nom": "Rayon de givre", "type": "évocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Un faisceau glacial de lumière bleuâtre se dirige vers une créature dans la portée du sort. Effectuez une attaque à distance avec un sort contre la cible. S'il touche, la cible subit 1d8 dégâts de froid et sa vitesse est réduite de 3 mètres jusqu'à début de votre prochain tour. Les dégâts du sort augmentent de 1d8 lorsque vous atteignez le niveau 5 (2d8), le niveau 11 (3d8) et le niveau 17 (4d8)."},
    {"nom": "Réparation", "type": "transmutation", "temps_incantation": "1 minute", "portée": "contact", "composantes": "V, S, M (deux aimants)", "durée": "instantanée", "description": "Ce sort répare une simple fissure, déchirure ou fêlure sur un objet que vous touchez, comme un maillon de chaîne cassé, une clé brisée en deux morceaux, un accroc sur un manteau ou une fuite sur une outre. Tant que la fissure ou l'accroc n'excède pas 30 cm dans toutes les dimensions, vous le réparez, ne laissant aucune trace de la détérioration passée. Ce sort peut réparer physiquement un objet magique ou un artificiel, mais ne peut pas rendre sa magie à un objet."},
    {"nom": "Résistance", "type": "abjuration", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (une cape miniature)", "durée": "concentration, jusqu'à 1 minute", "description": "Vous touchez une créature consentante. Une fois avant la fin du sort, la cible peut lancer un d4 et ajouter le résultat du dé à un jet de sauvegarde de son choix. Elle peut lancer le dé avant ou après avoir effectué son jet de sauvegarde. Le sort prend alors fin."},
    {"nom": "Saute de vent", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous saisissez l'air et l'obligez à créer un des effets suivants à un point que vous pouvez voir à portée : Une créature de taille M ou plus petite que vous choisissez doit réussir un jet de sauvegarde de Force ou être repoussée de 1,50 mètre de vous. Vous créez une petite explosion d'air capable de bouger un objet qui n'est pas tenu ni porté et qui ne pèse pas plus que 2,5 kg. L'objet est repoussé de 3 mètres. Il n'est pas poussé avec assez de force pour faire des dégâts. Vous créez un effet sensoriel inoffensif qui utilise l'air, comme provoquer le bruissement de feuilles, faire claquer des volets ou faire onduler des vêtements dans une brise."},
    {"nom": "Sauvagerie primitive", "type": "transmutation", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "S", "durée": "instantanée", "description": "Vous canalisez la magie primale pour qu'elle aiguise vos dents ou vos ongles, le rendant prêts à livrer une attaque corrosive. Réalisez une attaque au corps à corps avec un sort contre une créature située à 1,50 mètre ou moins de vous. En cas de réussite, la cible prend 1d10 dégâts d'acide. Après que vous ayez effectué votre attaque, vos dents ou vos ongles reprennent leur état normal. Les dégâts du sort augmentent de 1d10 lorsque vous atteignez le niveau 5 (2d10), le niveau 11 (3d10) et le niveau 17 (4d10)."},
    {"nom": "Stabilisation", "type": "nécromancie", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "instantanée", "description": "Vous touchez une créature vivante qui est à 0 point de vie. La créature devient stable. Ce sort n'a pas d'effet sur les morts-vivants et les artificiels."},
    {"nom": "Thaumaturgie", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V", "durée": "jusqu'à 1 minute", "description": "Vous simulez une chose extraordinaire, un signe de puissance surnaturelle. Vous créez un des effets magiques suivants dans la limite de portée du sort : Votre voix devient trois fois plus puissante que la normale pour 1 minute. Vous faites vaciller des flammes, augmentez ou diminuez leur intensité, ou bien encore vous changez leur couleur pendant 1 minute. Vous causez des tremblements inoffensifs dans le sol pendant 1 minute. Vous créez un son instantané qui provient d'un point de votre choix dans la limite de portée du sort, tel qu'un grondement de tonnerre, le cri d'un corbeau ou des chuchotements de mauvais augure. Vous provoquez instantanément l'ouverture ou le claquement brusque d'une porte ou d'une fenêtre non verrouillée. Vous altérez l'apparence de vos yeux pendant 1 minute. Si vous lancez ce sort plusieurs fois, vous pouvez avoir activement jusqu'à trois de ses effets à la fois, et vous pouvez rompre un effet au prix d'une action."},
    {"nom": "Trait de feu", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous lancez un trait de feu sur une créature ou un objet à portée. Faites une attaque à distance avec un sort contre la cible. En cas de réussite, la cible prend 1d10 dégâts de feu. Un objet inflammable touché par ce sort prend feu s'il n'est pas porté. Les dégâts du sort augmentent de 1d10 aux niveaux 5 (2d10), 11 (3d10) et 17 (4d10)."}
]

sort_niveau_un=[
{"nom": "Absorption des éléments", "type": "abjuration", "temps_incantation": "1 réaction", "portée": "personnelle", "composantes": "S", "durée": "1 round", "description": "Le sort capte une partie de l'énergie entrante, ce qui réduit son effet sur vous et la stocke pour votre prochaine attaque au corps à corps. Vous obtenez une résistance à ce type de dégâts jusqu'au début de votre prochain tour. De plus, la première fois que vous touchez avec une attaque au corps à corps lors de votre prochain tour, la cible subit 1d6 dégâts supplémentaires du type d'élément ciblé, et le sort se termine. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts supplémentaires augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Alarme", "type": "abjuration (rituel)", "temps_incantation": "1 minute", "portée": "9 mètres", "composantes": "V, S, M (une petite clochette et un morceau de fil d'argent fin)", "durée": "8 heures", "description": "Vous mettez en place une alarme contre les intrusions indésirables. Choisissez une porte, une fenêtre, ou une zone à portée qui ne dépasse pas un cube de 6 mètres d'arête. Jusqu'à la fin du sort, une alarme vous alerte lorsqu'une créature de taille TP ou supérieure touche ou pénètre la zone surveillée. Lorsque vous lancez ce sort, vous pouvez désigner des créatures qui ne déclencheront pas l'alarme. Vous pouvez également choisir si l'alarme est audible ou juste mentale. Une alarme mentale vous alerte avec une sonnerie dans votre esprit à condition que vous soyez à 1,5 kilomètre maximum de la zone surveillée. Cette sonnerie vous réveille si vous êtes endormi. Une alarme audible produit le son d'une clochette à main, pendant 10 secondes, pouvant être entendue à 18 mètres."},
{"nom": "Amitié avec les animaux", "type": "enchantement", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (un morceau de nourriture)", "durée": "24 heures", "description": "Ce sort vous permet de persuader une bête que vous ne lui voulez aucun mal. Choisissez une bête que vous pouvez voir dans la portée du sort. Elle doit vous voir et vous entendre. Si l'Intelligence de la bête est de 4 ou plus, le sort échoue. Autrement, la bête doit réussir un jet de sauvegarde de Sagesse ou être charmée pour la durée du sort. Si vous, ou un de vos compagnons, blessez la cible, le sort prend fin. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez charmer une bête supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Appel de familier", "type": "invocation (rituel)", "temps_incantation": "1 heure", "portée": "3 mètres", "composantes": "V, S, M (du charbon de bois, de l'encens, et des herbes pour une valeur de totale minimum de 10 po, le tout étant consumé par le feu dans un chaudron en laiton)", "durée": "instantanée", "description": "Vous gagnez les services d'un familier, un esprit qui prend la forme d'un animal de votre choix : une araignée, une belette, un chat, une chauve-souris, une chouette, un corbeau, un crabe, un faucon, un hippocampe, une grenouille (crapaud), un lézard, une pieuvre, un rat, un poisson (piranha) ou un serpent venimeux. Apparaissant dans un espace inoccupé à portée, le familier a les statistiques de la forme choisie mais est du type céleste, fée ou fiélon (au choix), au lieu du type bête. Votre familier agit de manière indépendante, mais obéit toujours à vos ordres. En combat, il lance sa propre initiative et agit au cours de ses propres tours de jeu. Un familier ne peut pas attaquer, mais il peut utiliser normalement les autres actions. Lorsque le familier tombe à 0 point de vie, il disparaît, ne laissant aucune forme physique. Il réapparaît après que vous ayez à nouveau lancé ce sort. Par une action, vous pouvez temporairement renvoyer le familier dans une poche dimensionnelle. Vous pouvez aussi le renvoyer pour toujours. Au prix d'une action lorsqu'il est temporairement renvoyé, vous pouvez le faire réapparaître dans n'importe quel espace inoccupé dans un rayon de 9 mètres autour de vous. Chaque fois que le familier tombe à 0 point de vie ou disparaît dans la poche dimensionnelle, il laisse dans son espace tout ce qu'il portait. Lorsque votre familier se trouve à 30 mètres de vous maximum, vous pouvez communiquer avec lui par télépathie. De plus, par une action, vous pouvez voir au travers des yeux du familier et entendre ce qu'il entend jusqu'au début de votre prochain tour, bénéficiant alors des sens spéciaux de votre familier, s'il en a. Au cours de cette période, vous êtes considéré comme étant sourd et aveugle (en ce qui concerne vos propres sens). Vous ne pouvez pas avoir plus d'un familier à la fois. Si vous lancez ce sort alors que vous possédez déjà un familier, votre familier actuel prend une nouvelle forme. Choisissez cette nouvelle forme parmi celles présentées dans la liste ci-dessus. Votre familier prend alors la forme de la créature choisie. Enfin, lorsque vous lancez un sort qui a une portée de contact, votre familier peut lancer le sort comme s'il était celui qui avait réalisé l'incantation. Votre familier doit se situer à 30 mètres de vous maximum, et doit utiliser sa réaction pour lancer le sort au moment où vous l'incantez. Si le sort requiert un jet d'attaque, vous utilisez votre modificateur à l'attaque pour ce jet."},
{"nom": "Armure d'Agathys", "type": "abjuration", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S, M (une coupe d'eau)", "durée": "1 heure", "description": "Une force magique protectrice vous entoure, se manifestant sous la forme d'un givre spectral vous couvrant vous et votre équipement. Vous obtenez 5 points de vie temporaires pour la durée du sort. Si une créature vous touche avec une attaque au corps à corps alors que vous avez ces points de vie temporaires, la créature subit 5 dégâts de froid. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les points de vie temporaires et les dégâts de froid augmentent de 5 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Armure de mage", "type": "abjuration", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (un morceau de cuir tanné)", "durée": "8 heures", "description": "Vous touchez une créature consentante qui ne porte pas d'armure, et une force magique de protection l'englobe jusqu'à ce que le sort prenne fin. La CA de la cible passe à 13 + son modificateur de Dextérité. Le sort prend fin si la cible enfile une armure ou si vous prenez une action pour interrompre le sort."},
{"nom": "Baies nourricières", "type": "transmutation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (une branche de gui)", "durée": "instantanée", "description": "Jusqu'à dix baies imprégnées de magie apparaissent dans votre main pour la durée de leur potentiel (voir ci-dessous). Une créature peut utiliser son action pour manger une baie. Manger une baie rend 1 point de vie, et la baie est suffisamment nourrissante pour sustenter une créature pour une journée. Les baies perdent leur potentiel si elles n'ont pas été consommées dans les 24 heures qui suivent le lancement du sort."},
{"nom": "Barbes argentées", "type": "enchantement", "temps_incantation": "1 réaction", "portée": "18 mètres", "composantes": "V", "durée": "instantanée", "description": "La cible doit relancer le d20 et une autre créature gagne un avantage à son prochain jet d'attaque, de caractéristique ou de sauvegarde."},
{"nom": "Bénédiction", "type": "enchantement", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (une aspersion d'eau bénite)", "durée": "concentration, jusqu'à 1 minute", "description": "Vous bénissez jusqu'à trois créatures de votre choix, dans la portée du sort. À chaque fois qu'une cible fait un jet d'attaque ou de sauvegarde avant la fin du sort, la cible peut lancer un d4 et ajouter le résultat au jet d'attaque ou de sauvegarde. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Blessure", "type": "nécromancie", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "instantanée", "description": "Faites une attaque au corps à corps avec un sort contre une créature que vous pouvez toucher. En cas de réussite, la cible prend 3d10 dégâts nécrotiques. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d10 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Bouclier", "type": "abjuration", "temps_incantation": "1 réaction", "portée": "personnelle", "composantes": "V, S", "durée": "1 round", "description": "Une barrière invisible de force magique apparaît et vous protège. Jusqu'au début de votre prochain tour, vous obtenez un bonus de +5 à votre CA, y compris contre l'attaque qui a déclenché le sort, et vous ne prenez aucun dégât par le sort projectile magique."},
{"nom": "Bouclier de la foi", "type": "abjuration", "temps_incantation": "1 action bonus", "portée": "18 mètres", "composantes": "V, S, M (un bout de texte saint écrit sur un petit parchemin)", "durée": "concentration, jusqu'à 10 minutes", "description": "Un champ scintillant apparaît et entoure une créature de votre choix dans la portée du sort, lui accordant un bonus de +2 à la CA pour la durée du sort."},
{"nom": "Catapulte", "type": "transmutation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "S", "durée": "instantanée", "description": "Choisissez un objet pesant de 500 g à 2,5 kg à portée et qui n'est ni porté ni transporté. L'objet vole en ligne droite jusqu'à 27 mètres dans une direction que vous choisissez avant de tomber au sol, s'arrêtant plus tôt s'il rencontre une surface solide. Si l'objet va frapper une créature, cette créature doit faire un jet de sauvegarde de Dextérité. En cas d'échec à la sauvegarde, l'objet frappe la cible et arrête sa course. Lorsque l'objet heurte quelque chose, l'objet et ce qu'il frappe subissent chacun 3d8 dégâts contondants. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, le poids maximal de l'objet que vous pouvez cibler avec ce sort augmente de 2,5 kg et les dégâts augmentent de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Cérémonie", "type": "abjuration (rituel)", "temps_incantation": "1 heure", "portée": "contact", "composantes": "V, S, M (25 po de poudre d'argent, que le sort consomme)", "durée": "instantanée", "description": "Vous réalisez une cérémonie religieuse qui est imprégnée de magie. Lorsque vous lancez ce sort, choisissez l'un des rites suivants, la cible devant se trouver à 3 mètres ou moins de vous durant tout le temps d'incantation. Expiation. Vous touchez une créature consentante dont l'alignement a changé et faites un jet de Sagesse (Intuition) DD 20. En cas de réussite, vous restaurez l'alignement original de la cible. Eau bénite. Vous touchez une fiole d'eau et celle-ci devient de l'eau bénite. Passage à l'âge adulte. Vous touchez un humanoïde suffisamment âgé pour être un jeune adulte. Pendant les prochaines 24 heures, lorsque la cible effectue un jet de caractéristique, elle peut lancer un d4 et ajouter le résultat au jet de caractéristique. Une créature ne peut bénéficier de ce rite qu'une seule fois. Dévouement. Vous touchez un humanoïde qui souhaite se mettre au service de votre dieu. Pendant les prochaines 24 heures, lorsque la cible effectue un jet de sauvegarde, elle peut lancer un d4 et ajouter le résultat au jet de sauvegarde. Une créature ne peut bénéficier de ce rite qu'une seule fois. Rite funéraire. Vous touchez un cadavre et pendant les 7 prochains jours, la cible ne peut pas devenir un mort-vivant par aucun autre moyen que le sort souhait. Mariage. Vous touchez des humanoïdes adultes prêts à s'unir par les liens du mariage. Pour les 7 prochains jours, chaque cible gagne un bonus de +2 à la CA tant qu'ils sont à 9 mètres ou moins l'un de l'autre. Une créature ne peut bénéficier de nouveau de ce rite que si elle est veuve."},
{"nom": "Charme-personne", "type": "enchantement", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S", "durée": "1 heure", "description": "Vous pouvez tenter de charmer un humanoïde que vous pouvez voir à portée. Ce dernier doit effectuer un jet de sauvegarde de Sagesse, avec un avantage à son jet si vous ou vos compagnons le combattez. En cas d'échec, il est charmé jusqu'à la fin de la durée du sort ou jusqu'à ce que vous ou vos compagnons cherchiez à lui nuire. La créature charmée vous considère comme un bon ami. Quand le sort prend fin, la créature sait que vous l'avez charmée. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1. Les créatures doivent se trouver à 9 mètres maximum les unes des autres lorsque vous les ciblez."},
{"nom": "Châtiment calcinant", "type": "évocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "La prochaine fois que vous touchez une créature avec une attaque au corps à corps avec une arme pendant la durée du sort, votre arme est chauffée à blanc, et votre attaque inflige 1d6 dégâts de feu supplémentaires à la cible et l'enflamme. Au début de chacun de ses tours jusqu'à la fin du sort, la cible doit effectuer un jet de sauvegarde de Constitution. En cas d'échec, elle subit 1d6 dégâts de feu. En cas de réussite, le sort prend fin. Si la cible, ou une créature située à 1,50 mètre d'elle, utilise son action pour étouffer les flammes, ou si tout autre effet éteint les flammes (par exemple si la cible se plonge dans l'eau), le sort prend fin. Aux niveaux supérieurs. Si vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts supplémentaires initiaux infligés par l'attaque augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Châtiment courroucé", "type": "évocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "La prochaine fois que vous touchez une cible lors d'une attaque au corps à corps avec une arme pendant la durée du sort, votre attaque inflige 1d6 dégâts psychiques supplémentaires. De plus, si la cible est une créature, elle doit réussir un jet de sauvegarde de Sagesse ou être effrayée jusqu'à la fin du sort. Par une action, la créature peut effectuer un jet de Sagesse contre le DD de sauvegarde de votre sort pour mettre un terme à cet effet et au sort."},
{"nom": "Châtiment tonitruant", "type": "évocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "La première fois que vous touchez une cible lors une attaque au corps à corps avec une arme pendant que le sort est actif, votre arme résonne tel un tonnerre audible à 90 mètres à la ronde, et l'attaque inflige 2d6 dégâts de tonnerre supplémentaires à la cible. De plus, si la cible est une créature, elle doit réussir un jet de sauvegarde de Force sous peine d'être repoussée de vous sur 3 mètres puis de tomber à terre."},
{"nom": "Collet", "type": "abjuration", "temps_incantation": "1 minute", "portée": "contact", "composantes": "S, M (7,50 mètres de corde, que le sort consomme)", "durée": "8 heures", "description": "Lorsque vous lancez ce sort, vous utilisez la corde pour créer un cercle de 1,50 mètre de rayon au sol. Une fois le sort lancé, la corde disparaît et le cercle devient un piège magique. Le piège est presque invisible et demande un jet d'Intelligence (Investigation) réussi contre le DD de sauvegarde de votre sort pour être décelé. Le piège se déclenche lorsqu'une créature de taille P, M ou G marche sur le sol dans le rayon du sort. Cette créature doit réussir un jet de sauvegarde de Dextérité ou bien être magiquement hissée dans les airs, pour se retrouver pendue la tête à l'envers à 90 cm au-dessus du sol. La créature est entravée jusqu'à ce que le sort se termine. Une créature entravée peut effectuer un jet de sauvegarde de Dextérité à la fin de chacun de ses tours, mettant fin à l'effet sur elle-même en cas de réussite. La créature ou quelqu'un d'autre qui peut l'atteindre peut aussi utiliser son action pour effectuer un jet d'Intelligence (Arcanes) contre le DD de sauvegarde de votre sort. En cas de réussite, l'effet d'entrave prend fin. Après le déclenchement du piège, le sort se termine lorsque le piège ne retient plus aucune créature."},
{"nom": "Communication avec les animaux", "type": "divination (rituel)", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "10 minutes", "description": "Vous gagnez la capacité de comprendre et de communiquer verbalement (ou oralement) avec des bêtes pour la durée du sort. Les connaissances et la compréhension de nombreuses bêtes sont limitées par leur intelligence, mais au minimum, elles peuvent vous communiquer des informations sur les alentours et les bêtes à proximité, incluant tout ce qu'elles peuvent percevoir ou ont perçu au cours des derniers jours. Vous devriez être capable de convaincre une bête de vous rendre un petit service, à la discrétion du MD."},
{"nom": "Compréhension des langues", "type": "divination (rituel)", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S, M (une pincée de suie et de sel)", "durée": "1 heure", "description": "Pendant la durée du sort, vous comprenez la signification littérale de toute langue parlée que vous pouvez entendre. Vous comprenez également tout langage écrit que vous pouvez voir, mais vous devez toucher la surface sur laquelle les mots sont inscrits. Il faut une minute pour lire une page de texte. Ce sort ne décode pas les messages secrets dans un texte ou un glyphe, tel qu'un symbole magique, qui ne fait pas partie du langage écrit."},
{"nom": "Couleurs dansantes", "type": "illusion", "temps_incantation": "1 action", "portée": "personnelle (cône de 4,50 mètres)", "composantes": "V, S, M (une pincée de poudre ou de sable de couleur rouge, jaune et bleu)", "durée": "1 round", "description": "Un assortiment éblouissant de faisceaux lumineux et colorés fait éruption de votre main. Lancez 6d10. Cette valeur représente le nombre maximal de points de vie des créatures que vous pouvez affecter avec ce sort. Les créatures dans un cône de 4,50 mètres dont vous êtes l'origine sont affectées selon l'ordre croissant de leurs points de vie (en ignorant les créatures inconscientes et celles qui ne peuvent pas voir). En partant de la créature avec le plus petit nombre de points de vie, chaque créature affectée par ce sort est aveuglée jusqu'à la fin de votre prochain tour. Retirez les points de vie de chaque créature avant de passer à la prochaine créature avec le plus petit nombre de points de vie. Les points de vie d'une créature doivent être égaux ou inférieurs au total pour que cette créature soit affectée. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, ajoutez 2d10 au lancer initial pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Couteau de glace", "type": "invocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "S, M (une goutte d'eau ou un bout de glace)", "durée": "instantanée", "description": "Vous créez un éclat de glace et le lancez vers une créature dans la portée du sort. Faites une attaque à distance avec un sort contre la cible. Si elle réussit, la cible subit 1d10 dégâts perforants. Que l'attaque touche ou pas, l'éclat de glace explose. La cible et toutes les créatures dans un rayon de 1,50 mètre autour d'elle doivent réussir un jet de sauvegarde de Dextérité ou subir 2d6 dégâts de froid. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts de froid infligés augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Création ou destruction d'eau", "type": "transmutation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (une goutte d'eau pour la création d'eau ou quelques grains de sable pour la destruction d'eau)", "durée": "instantanée", "description": "Soit vous créez, soit vous détruisez de l'eau. Création d'eau. Vous créez jusqu'à 40 litres d'eau pure dans un contenant ouvert à portée. Vous pouvez sinon choisir de faire tomber l'eau sous forme de pluie dans un cube de 9 mètres d'arête à portée, éteignant ainsi les flammes non protégées de la zone. Destruction d'eau. Vous détruisez jusqu'à 40 litres d'eau présente dans un contenant ouvert à portée. Sinon, vous pouvez choisir de supprimer le brouillard dans un cube de 9 mètres d'arête à portée. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous créez ou détruisez 40 litres d'eau supplémentaires, ou augmentez la taille du cube de 1,50 mètre d'arête, pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Déguisement", "type": "illusion", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "1 heure", "description": "Vous changez d'apparence jusqu'à ce que le sort prenne fin ou que vous utilisiez une action pour le dissiper. Le changement inclut vos vêtements, votre armure, vos armes et les autres objets que vous portez. Vous pouvez paraître 30 cm plus grand ou plus petit, mince, obèse, ou entre les deux. Vous ne pouvez pas modifier votre type morphologique. Vous devez donc prendre une forme qui présente un arrangement similaire des membres. Par ailleurs, l'ampleur de l'illusion ne tient qu'à vous. Les modifications apportées par ce sort ne résistent pas à une inspection physique. Par exemple, si vous utilisez ce sort pour ajouter un chapeau à votre accoutrement, les objets passeront à travers le chapeau et si on y touche, on ne sentira pas sa présence ou on tâtera plutôt votre tête et votre chevelure. Si vous utilisez ce sort pour paraître plus mince, la main d'une personne qui veut vous toucher entrera en contact avec votre corps alors que sa main semble libre d'obstruction. Pour détecter que vous êtes déguisé, une créature peut utiliser son action pour inspecter votre apparence et elle doit réussir un jet d'Intelligence (Investigation) contre le DD de sauvegarde de votre sort."},
{"nom": "Détection de la magie", "type": "divination (rituel)", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "concentration, jusqu'à 10 minutes", "description": "Pour la durée du sort, vous percevez la présence de magie à 9 mètres ou moins de vous. Si vous percevez de la magie de cette manière, vous pouvez utiliser votre action pour discerner une faible aura enveloppant une créature ou un objet visible dans la zone qui présente de la magie. Vous déterminez aussi l'école de magie, le cas échéant. Le sort peut outrepasser la plupart des obstacles mais il est bloqué par 30 cm de pierre, 2,50 cm de métal ordinaire, une mince feuille de plomb ou 90 cm de bois ou de terre."},
{"nom": "Détection du mal et du bien", "type": "divination", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S", "durée": "concentration, jusqu'à 10 minutes", "description": "Pour la durée du sort, vous savez si une aberration, un céleste, un élémentaire, une fée, un fiélon ou un mort-vivant est présent dans un rayon de 9 mètres autour de vous. Vous pouvez aussi déterminer sa localisation. De la même manière, vous savez si un objet ou un lieu à 9 mètres ou moins de vous a été consacré ou profané. Le sort peut outrepasser la plupart des obstacles mais il est bloqué par 30 cm de pierre, 2,50 cm de métal ordinaire, une mince feuille de plomb ou 90 cm de bois ou de terre."},
{"nom": "Détection du poison et des maladies", "type": "divination (rituel)", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S, M (une feuille d'if)", "durée": "concentration, jusqu'à 10 minutes", "description": "Pour la durée du sort, vous pouvez percevoir la présence et localiser les poisons, les créatures venimeuses, et les maladies dans un rayon de 9 mètres autour de vous. Vous identifiez également le type de poison, de créature venimeuse, ou de maladie. Le sort peut outrepasser la plupart des obstacles mais il est bloqué par 30 cm de pierre, 2,50 cm de métal ordinaire, une mince feuille de plomb ou 90 cm de bois ou de terre."},
{"nom": "Disque flottant de Tenser", "type": "invocation (rituel)", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (une goutte de mercure)", "durée": "1 heure", "description": "Ce sort crée un plateau de force horizontal et circulaire, de 90 cm de diamètre et épais de 2,50 cm, qui flotte 90 cm au-dessus du sol dans un espace inoccupé de votre choix, à portée et que vous pouvez voir. Le disque reste en place pour la durée du sort et peut supporter 250 kg. Si plus de poids est placé sur le disque, le sort prend fin, et tout ce qui se trouve sur le disque tombe sur le sol. Le disque est immobile tant que vous vous trouvez à 6 mètres de lui. Si vous vous déplacez à plus de 6 mètres, le disque vous suit jusqu'à se retrouver de nouveau à 6 mètres de vous. Il peut se déplacer au-dessus de n'importe quel type de terrain, monter et descendre les escaliers, les pentes et tout ce qui y ressemble, mais il ne peut effectuer un changement brutal d'altitude égal ou supérieur à 3 mètres. Par exemple, le disque ne peut pas se déplacer au-dessus d'un gouffre de 3 mètres de profondeur, ou il ne peut pas sortir d'un gouffre de 3 mètres de haut s'il a été invoqué au fond. Si vous vous déplacez à plus de 30 mètres du disque (par exemple parce qu'il ne peut pas passer au-dessus d'un obstacle pour vous suivre), le sort prend fin."},
{"nom": "Duel forcé", "type": "enchantement", "temps_incantation": "1 action bonus", "portée": "9 mètres", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "Vous essayez de contraindre une créature d'engager un duel avec vous. Une créature à portée que vous pouvez voir doit effectuer un jet de sauvegarde de Sagesse. En cas d'échec, vous obnubilez la créature, contrainte par votre exigence divine. Pour toute la durée du sort, la créature a un désavantage aux jets d'attaque effectués contre d'autres créatures que vous, et doit effectuer un jet de sauvegarde de Sagesse à chaque fois qu'elle essaye de s'éloigner à plus de 9 mètres de vous ; si elle réussit son jet de sauvegarde, le sort ne restreint pas son mouvement pour ce tour. Ce sort se termine si vous attaquez une autre créature, si vous lancez un sort qui cible une autre créature hostile que la cible, si une créature qui vous est alliée inflige des dégâts à la cible ou lance un sort sur la cible qui lui est nuisible, ou si vous terminez votre tour à plus de 9 mètres de la cible."},
{"nom": "Éclair de chaos", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous projetez une masse d'énergie chaotique sifflante et ondulante vers une créature à portée. Effectuez un jet d'attaque à distance avec un sort contre la cible. En cas de réussite, la cible prend 2d8 + 1d6 points de dégâts. Choisissez l'un des d8. Le nombre tiré sur ce dé détermine le type de dégâts de l'attaque, comme indiqué ci-dessous. d8 Type de dégâts : 1 Acide, 2 Froid, 3 Feu, 4 Force, 5 Foudre, 6 Poison, 7 Psychique, 8 Tonnerre. Si vous avez fait un double avec les d8, l'énergie chaotique rebondit depuis la cible vers une autre créature de votre choix dans un rayon de 9 mètres autour de la première. Effectuez un nouveau jet d'attaque contre cette nouvelle créature et effectuez un jet de dégâts le cas échéant. L'énergie chaotique peut continuer de rebondir, bien qu'une créature ne puisse être affectée qu'une seule fois par chaque sort lancé. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, chaque cible reçoit 1d6 dégâts supplémentaires du type déterminé pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Éclair traçant", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "1 round", "description": "Un éclair silencieux fonce sur une créature de votre choix dans la portée du sort. Faites une attaque à distance avec un sort contre la cible. Si elle réussit, la cible subit 4d6 dégâts radiants et le prochain jet d'attaque effectué contre cette cible avant la fin du votre prochain tour bénéficie d'un avantage grâce à la lumière faible mystique qui illumine alors la cible. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts infligés augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Enchevêtrement", "type": "invocation", "temps_incantation": "1 action", "portée": "27 mètres", "composantes": "V, S", "durée": "concentration, jusqu'à 1 minute", "description": "Herbes et lianes germent du sol dans un carré de 6 mètres d'arête ayant son origine sur un point dans la portée du sort. Pour la durée du sort, ces plantes rendent le terrain difficile. Une créature prise dans la zone lorsque vous incantez le sort doit réussir un jet de sauvegarde de Force ou être entravée par l'enchevêtrement de plantes jusqu'à la fin du sort. Une créature entravée par les plantes peut utiliser une action pour faire un jet de sauvegarde de Force contre le DD de sauvegarde de votre sort. En cas de réussite, la créature se libère. Lorsque le sort prend fin, les plantes invoquées se fanent."},
{"nom": "Faveur divine", "type": "évocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V, S", "durée": "concentration, jusqu'à 1 minute", "description": "Votre prière vous donne de la puissance dans un rayonnement divin. Jusqu'à ce que le sort se termine, vos attaques avec une arme infligent 1d4 dégâts radiants supplémentaires lorsqu'elles touchent."},
{"nom": "Feuille morte", "type": "transmutation", "temps_incantation": "1 réaction, que vous prenez lorsque vous ou une créature à 18 mètres ou moins de vous tombez.", "portée": "18 mètres", "composantes": "V, M (une petite plume ou un peu de duvet)", "durée": "1 minute", "description": "Choisissez jusqu'à cinq créatures en chute libre dans la portée du sort. Le taux de descente d'une créature en chute libre est ramené à 18 mètres par round jusqu'à la fin du sort. Si la créature atterrit avant la fin du sort, elle ne subit aucun dégât de chute et elle retombe sur ses pieds. Le sort prend alors fin pour cette créature."},
{"nom": "Fléau", "type": "enchantement", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (une goutte de sang)", "durée": "concentration, jusqu'à 1 minute", "description": "Jusqu'à 3 créatures de votre choix, que vous pouvez voir et qui sont à portée, doivent effectuer un jet de sauvegarde de Charisme. Quand une cible qui a raté son jet de sauvegarde fait un jet d'attaque ou un autre jet de sauvegarde avant la fin du sort, elle doit lancer un d4 et soustraire le résultat à son jet d'attaque ou de sauvegarde. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Fou rire de Tasha", "type": "enchantement", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (de minuscules tartes et une plume qui est agitée dans les airs)", "durée": "concentration, jusqu'à 1 minute", "description": "Une créature de votre choix, que vous pouvez voir et à portée, a l'impression que tout ce qu'elle perçoit est hilarant et lui provoque une intense crise de fou rire. La cible doit réussir un jet de sauvegarde de Sagesse sous peine de tomber à terre, et être incapable d'agir et de se relever pour toute la durée du sort. Une créature ayant une Intelligence de 4 ou moins ne peut pas être affectée par ce sort. À la fin de chacun de ses tours, et à chaque fois qu'elle subit des dégâts, la cible peut effectuer un nouveau jet de sauvegarde de Sagesse. La cible a un avantage à son jet de sauvegarde s'il est déclenché par des dégâts. En cas de réussite, le sort prend fin."},
{"nom": "Frappe du zéphyr", "type": "transmutation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "Vous vous déplacez comme le vent. Tant que le sort n'est pas terminé, votre mouvement ne provoque pas d'attaques d'opportunité. Une fois avant que le sort ne se termine, vous pouvez vous donner un avantage à un jet d'attaque avec une arme à votre tour. Cette attaque inflige 1d8 dégâts de force supplémentaires si elle touche. Que vous touchiez ou non, votre vitesse augmente de 9 mètres jusqu'à la fin de ce tour."},
{"nom": "Frappe piégeuse", "type": "invocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "La prochaine fois que vous touchez une créature avec une attaque avec une arme avant que ce sort ne prenne fin, une masse tortueuse de lianes épineuses apparaît au point d'impact, et la cible doit réussir un jet de sauvegarde de Force sous peine d'être entravée par ces lianes magiques jusqu'à ce que le sort prenne fin. Une créature de taille G ou supérieure a un avantage à son jet de sauvegarde. Si la cible réussit son jet de sauvegarde, les lianes se flétrissent et tombent. Tant qu'elle est entravée par ce sort, la cible subit 1d6 dégâts perforants au début de chacun de ses tours. Une créature entravée par ces lianes, ou une autre créature capable de la toucher, peut utiliser son action pour effectuer un jet de Force contre le DD de sauvegarde de votre sort. En cas de réussite, la cible est libérée. Aux niveaux supérieurs. Si vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Frayeur", "type": "nécromancie", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "Vous éveillez le sens de la mortalité chez une créature que vous pouvez voir à portée. Les morts-vivants et les artificiels sont immunisés contre cet effet. La cible doit réussir un jet de sauvegarde de Sagesse ou être effrayée jusqu'à ce que le sort se termine. La cible effrayée peut répéter le jet de sauvegarde à la fin de chacun de ses tours, mettant fin à l'effet sur elle-même en cas de réussite. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1. Les créatures doivent être à 9 mètres ou moins les unes des autres lorsque vous les ciblez."},
{"nom": "Graisse", "type": "invocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S, M (une noix de beurre ou un peu de couenne de porc)", "durée": "1 minute", "description": "Une graisse visqueuse recouvre le sol sur un carré de 3 mètres de côté centré sur un point à portée, transformant cette zone en terrain difficile. Lorsque la graisse apparaît, chaque créature se tenant debout dans la zone doit réussir un jet de sauvegarde de Dextérité sous peine de tomber à terre. Une créature qui entre dans la zone ou y termine son tour doit également réussir un jet de sauvegarde de Dextérité si elle ne veut pas tomber à terre."},
{"nom": "Grande foulée", "type": "transmutation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (une pincée de terre)", "durée": "1 heure", "description": "Vous touchez une créature. La vitesse de la cible augmente de 3 mètres jusqu'à la fin du sort. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Grêle d'épines", "type": "invocation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "La prochaine fois que vous touchez une créature lors d'une attaque à distance avec une arme avant que le sort ne prenne fin, ce sort crée une pluie d'épines qui jaillissent de votre arme à distance ou de la munition. En plus de l'effet normal de l'attaque, la cible de l'attaque et toutes les créatures à 1,50 mètre ou moins d'elle doivent effectuer un jet de sauvegarde de Dextérité, subissant 1d10 dégâts perforants en cas d'échec, ou la moitié de ces dégâts en cas de réussite. Aux niveaux supérieurs. Si vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d10 pour chaque niveau d'emplacement au-delà du niveau 1 (jusqu'à un maximum de 6d10)."},
{"nom": "Héroïsme", "type": "enchantement", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "concentration, jusqu'à 1 minute", "description": "Une créature consentante que vous touchez est submergée par le courage. Jusqu'à la fin du sort, la créature est immunisée contre l'état effrayé et gagne un nombre de points de vie temporaires égal au modificateur de votre caractéristique d'incantation, et ce au début de chacun de ses tours. Lorsque le sort prend fin, la cible perd tous les points de vie temporaires qu'il lui restait et qui lui avaient été conférés par ce sort. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez cibler une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Identification", "type": "divination (rituel)", "temps_incantation": "1 minute", "portée": "contact", "composantes": "V, S, M (une perle d'une valeur d'au moins 100 po et une plume de hibou)", "durée": "instantanée", "description": "Vous choisissez un objet que vous devez toucher durant toute la durée du sort. Si l'objet est magique ou imprégné de magie, vous apprenez ses propriétés et comment les utiliser, s'il requiert un lien pour être utilisé et le nombre de charges qu'il contient, le cas échéant. Vous apprenez si des sorts affectent l'objet et quels sont ces sorts. Si l'objet a été créé par un ou plusieurs sorts, vous apprenez quels sorts ont permis de le créer. Si vous touchez une créature durant toute la durée du sort, au lieu d'un objet, vous apprenez quels sorts l'affectent actuellement, le cas échéant."},
{"nom": "Image silencieuse", "type": "illusion", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S, M (un peu de laine de mouton)", "durée": "concentration, jusqu'à 10 minutes", "description": "Vous créez l'image d'un objet, d'une créature ou d'un autre phénomène visible dont les dimensions n'excèdent pas un cube de 4,50 mètres d'arête. L'image apparaît à un endroit choisi à l'intérieur de la portée du sort et perdure pendant toute la durée du sort. L'image est purement visuelle ; ce qui implique qu'elle n'est pas accompagnée par un son, une odeur ou d'autres effets sensoriels. Vous pouvez utiliser votre action pour déplacer l'image à n'importe quel endroit dans la portée du sort. Comme l'image change de lieu, vous pouvez modifier son apparence afin que ses mouvements apparaissent fluides et naturels dans l'image. Par exemple, si vous créez l'image d'une créature et vous la déplacez, vous pouvez modifier l'image de sorte que la créature semble réellement marcher. Une interaction physique avec l'image révèle qu'il s'agit d'une illusion, parce que les choses peuvent passer au travers. Une créature qui utilise son action pour examiner l'image peut déterminer qu'il s'agit en fait d'une illusion en réussissant un jet d'Intelligence (Investigation) contre votre DD du jet de sauvegarde de ce sort. Si une créature voit l'illusion pour ce qu'elle est, la créature peut voir à travers l'image."},
{"nom": "Injonction", "type": "enchantement", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "1 round", "description": "Vous donnez un ordre d'un mot à une créature dans la portée du sort et que vous pouvez voir. La cible doit réussir un jet de sauvegarde de Sagesse ou suivre l'ordre lors de son prochain tour. Le sort n'a aucun effet si la cible est un mort-vivant, si elle ne comprend pas la langue, ou si votre ordre est directement nocif pour elle. Des injonctions typiques et leurs effets suivent. Vous pouvez émettre un ordre autre que ceux décrits ici. Si vous le faites, le MD détermine comment la cible se comporte. Si la cible est empêchée de suivre votre ordre, le sort prend fin. Approche. La cible se déplace vers vous par le chemin le plus court et le plus direct, terminant son tour si elle arrive à 1,50 mètre ou moins de vous. Lâche. La cible lâche tout ce qu'elle tient et termine alors à son tour. Fuis. La cible s'éloigne de vous le plus rapidement possible. Tombe. La cible tombe au sol et termine alors à son tour. Halte. La cible ne bouge plus et n'entreprend aucune action. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous pouvez affecter une créature supplémentaire pour chaque niveau d'emplacement au-delà du niveau 1. Les créatures que vous ciblez doivent toutes être dans un rayon de 9 mètres."},
{"nom": "Lien avec une bête", "type": "divination", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (un morceau de fourrure enveloppé dans un linge)", "durée": "concentration, jusqu'à 10 minutes", "description": "Vous établissez un lien télépathique avec une bête que vous touchez, qui est amicale ou que vous avez charmée. Le sort échoue si l'Intelligence de la bête est de 4 ou plus. Jusqu'à la fin du sort, le lien est actif tant que vous et la bête êtes à portée de vue. Via le lien, la bête peut comprendre vos messages télépathiques, et elle peut communiquer par télépathie ses émotions et des concepts simples en retour. Tant que le lien est actif, la bête à un avantage à ses jets attaque contre toute créature à 1,50 mètre de vous et que vous pouvez voir."},
{"nom": "Lueurs féeriques", "type": "évocation", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "concentration, jusqu'à 1 minute", "description": "Tous les objets à l'intérieur d'un cube de 6 mètres d'arête dans la portée du sort se distinguent par un halo bleu, vert ou violet (à votre choix). Toutes les créatures présentes dans la zone lors de l'incantation du sort sont également enveloppées du halo si elles échouent à un jet de sauvegarde de Dextérité. Pour la durée du sort, les objets et les créatures affectées émettent une lumière faible dans un rayon de 3 mètres. Les jets d'attaque contre des créatures affectées ou des objets bénéficient d'un avantage si l'attaquant peut les voir. Les créatures affectées ou les objets ne peuvent bénéficier de l'état invisible."},
{"nom": "Mains brûlantes", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (cône de 4,50 mètres)", "composantes": "V, S", "durée": "instantanée", "description": "En tendant vos mains, les pouces en contact et les doigts écartés, un mince rideau de flammes gicle du bout de tous vos doigts tendus. Toute créature se trouvant dans le cône de 4,50 mètres doit effectuer un jet de sauvegarde de Dextérité. La créature subit 3d6 dégâts de feu en cas d'échec, ou la moitié de ces dégâts en cas de réussite. Le feu embrase tous les objets inflammables qui se trouvent dans la zone d'effet et qui ne sont pas tenus ou portés. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Maléfice", "type": "enchantement", "temps_incantation": "1 action bonus", "portée": "27 mètres", "composantes": "V, S, M (l'œil pétrifié d'un triton)", "durée": "concentration, jusqu'à 1 heure", "description": "Vous placez une malédiction sur une créature à portée que vous pouvez voir. Jusqu'à la fin du sort vous infligez 1d6 dégâts nécrotiques supplémentaires à la cible à chaque fois que vous la touchez lors d'une attaque. De plus, choisissez une caractéristique lorsque vous lancez le sort. La cible obtient un désavantage aux jets de caractéristique effectués avec la caractéristique en question. Si la cible tombe à 0 point de vie avant que le sort ne se termine, vous pouvez utiliser votre action bonus lors d'un tour suivant pour maudire une nouvelle créature. Une délivrance des malédictions lancée sur la cible met fin au sort prématurément. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 3 ou 4, vous pouvez maintenir votre concentration sur ce sort pendant 8 heures. Si vous utilisez un emplacement de sort de niveau 5 ou supérieur, vous pouvez maintenir votre concentration sur ce sort pendant 24 heures."},
{"nom": "Marque du chasseur", "type": "divination", "temps_incantation": "1 action bonus", "portée": "27 mètres", "composantes": "V", "durée": "concentration, jusqu'à 1 heure", "description": "Vous choisissez une créature que vous pouvez voir et à portée, et la marquez magiquement comme étant votre cible. Jusqu'à ce que le sort prenne fin, vous infligez 1d6 dégâts supplémentaires à la cible lorsque vous la touchez lors d'une attaque avec une arme, et vous avez un avantage à tous vos jets de Sagesse (Perception) ou Sagesse (Survie) effectués pour la trouver. Si la cible tombe à 0 point de vie avant que le sort ne prenne fin, vous pouvez utiliser votre action bonus lors de l'un de vos tours suivants pour marquer une nouvelle créature. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 3 ou 4, vous pouvez maintenir votre concentration sur ce sort pendant 8 heures maximum. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 5 ou supérieur, vous pouvez maintenir votre concentration sur ce sort pendant 24 heures maximum."},
{"nom": "Mixture caustique de Tasha", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (ligne de 9 mètres)", "composantes": "V, S, M (un peu de nourriture pourrie)", "durée": "concentration, jusqu'à 1 minute", "description": "Les créatures sur une ligne de 9 x 1,50 m doivent réussir un JdS de Dex. ou subir 2d4 dégâts d'acide chaque tour (+2d4/niv)."},
{"nom": "Mot de guérison", "type": "évocation", "temps_incantation": "1 action bonus", "portée": "18 mètres", "composantes": "V", "durée": "instantanée", "description": "Une créature visible de votre choix récupère des points de vie à hauteur de 1d4 + le modificateur de votre caractéristique d'incantation. Ce sort n'a pas d'effet sur les morts-vivants et les artificiels. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les points de vie récupérés augmentent de 1d4 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Murmures dissonants", "type": "enchantement", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V", "durée": "instantanée", "description": "Vous murmurez une mélodie discordante qui ne peut être entendue que par une créature de votre choix à portée, la tourmentant terriblement. La cible doit effectuer un jet de sauvegarde de Sagesse. En cas d'échec, elle subit 3d6 dégâts psychiques et doit immédiatement utiliser sa réaction, si elle est encore disponible, pour s'éloigner de vous aussi loin que sa vitesse le lui permet. La créature ne se déplace pas vers des sols manifestement dangereux, comme des flammes ou un gouffre. En cas de réussite, la cible subit la moitié de ces dégâts et n'est pas contrainte de se déplacer. Une créature assourdie réussit automatiquement son jet de sauvegarde. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts sont augmentés de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Nappe de brouillard", "type": "invocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "concentration, jusqu'à 1 heure", "description": "Vous créez une sphère de brouillard de 6 mètres de rayon centrée sur un point dans la portée du sort. La sphère s'étend au-delà des coins et la visibilité dans la zone est nulle. Elle persiste pour la durée du sort ou jusqu'à ce qu'un vent de force modérée ou plus (au moins 15 km/h) la dissipe. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, le rayon de la sphère augmente de 6 mètres pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Orbe chromatique", "type": "évocation", "temps_incantation": "1 action", "portée": "27 mètres", "composantes": "V, S, M (un diamant valant au moins 50 po)", "durée": "instantanée", "description": "Vous projetez une sphère d'énergie de 10 cm de diamètre vers une créature que vous pouvez voir dans la portée du sort. Vous choisissez acide, foudre, feu, froid, poison ou tonnerre comme type d'orbe que vous créez. Vous faites ensuite une attaque à distance avec un sort contre la cible. Si l'attaque touche, la créature subit 3d8 dégâts du type préalablement déterminé. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Projectile élémentaire", "type": "évocation", "temps_incantation": "1 action", "portée": "27 m", "composantes": "V, S, M (une pierre précieuse d'une valeur d'au moins 50 po correspondant au type élémentaire du projectile que vous voulez lancer : un diamant pour l'air, un saphir pour l'eau, un rubis pour le feu, un jais pour la terre)", "durée": "instantanée", "description": "Vous créez un projectile d'énergie magique élémentaire et le lancez vers une créature dans la portée du sort. Faites une attaque à distance avec un sort contre la cible. Air. Le projectile est constitué d'électricité. Une créature touchée par ce missile subit 2d8 dégâts de foudre et doit réussir un jet de sauvegarde de Sagesse ou être aveuglée jusqu'à la fin de son prochain tour. Eau. Le projectile est constitué de glace. Une créature touchée par ce missile subit 2d8 dégâts de froid et doit réussir un jet de sauvegarde de Constitution ou voir sa vitesse réduite de moitié et avoir un désavantage à ses attaques jusqu'à la fin de son prochain tour. Feu. Le projectile est constitué de magma. Une créature touchée par ce missile subit 2d8 dégâts de feu et doit réussir un jet de sauvegarde de Dextérité ou prendre feu et subir 1d4 dégâts de feu au début de chacun de ses tours pendant un nombre de tours égal à votre bonus de caractéristique magique de lanceur de sorts. Une créature peut mettre fin à ces dégâts en utilisant son action pour éteindre les flammes. Terre. Le projectile est constitué d'une substance verdâtre liquide et corrosive. Une créature touchée par ce missile subit 2d8 dégâts d'acide et toutes les autres créatures dans un rayon de 1,50 mètre autour de la cible doivent réussir un jet de sauvegarde de Dextérité ou subir la moitié de ces dégâts. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Projectile magique", "type": "évocation", "temps_incantation": "1 action", "portée": "36 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous créez trois fléchettes de force magique d'un bleu lumineux. Chaque fléchette atteint une créature de votre choix que vous pouvez voir et dans la limite de portée du sort. Chaque projectile inflige 1d4 + 1 dégâts de force à sa cible. Les fléchettes frappent simultanément, et peuvent frapper une ou plusieurs créatures. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, il crée une fléchette additionnelle pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Protection contre le mal et le bien", "type": "abjuration", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (de l'eau bénite ou de la poudre d'argent et de fer, que le sort consomme)", "durée": "concentration, jusqu'à 10 minutes", "description": "Jusqu'à ce que le sort prenne fin, une créature consentante que vous touchez est protégée contre certains types de créatures : les aberrations, les célestes, les élémentaires, les fées, les fiélons et les morts-vivants. La protection confère un certain nombre de bénéfices. Les créatures de ces types ont un désavantage à leurs jets d'attaque effectués contre la cible. De plus, elles ne peuvent ni effrayer, ni charmer, ni posséder la cible. Si la cible est déjà charmée, effrayée, ou possédée par une telle créature, la cible a un avantage à tout nouveau jet de sauvegarde qu'elle effectuerait contre l'effet en question."},
{"nom": "Purification de nourriture et d'eau", "type": "transmutation (rituel)", "temps_incantation": "1 action", "portée": "3 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Toute la nourriture et toutes les boissons, non magiques, se trouvant dans une sphère de 1,50 mètre de rayon, et centrée sur un point de votre choix à portée, sont purifiées et débarrassées de tout poison et de toute maladie."},
{"nom": "Rayon empoisonné", "type": "nécromancie", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Un rayon d'énergie verdâtre et contagieuse est envoyé en direction d'une créature à portée. Effectuez une attaque à distance avec un sort contre la cible. Si le coup touche, la cible subit 2d8 dégâts de poison et doit effectuer un jet de sauvegarde de Constitution. En cas d'échec, la cible est empoisonnée jusqu'à la fin de votre prochain tour. Aux niveaux supérieurs. Si vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Repli expéditif", "type": "transmutation", "temps_incantation": "1 action bonus", "portée": "personnelle", "composantes": "V, S", "durée": "concentration, jusqu'à 10 minutes", "description": "Ce sort vous permet de vous déplacer à une vitesse incroyable. Lorsque vous lancez ce sort, puis par une action bonus à chacun de vos tours jusqu'à la fin du sort, vous pouvez effectuer l'action Foncer."},
{"nom": "Représailles infernales", "type": "évocation", "temps_incantation": "1 réaction, que vous prenez après avoir subi des dégâts par une créature située à 18 mètres maximum de vous et que vous pouvez voir.", "portée": "18 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous pointez votre doigt, et la créature qui vous a infligé des dégâts est momentanément entourée de flammes infernales. La créature doit effectuer un jet de sauvegarde de Dextérité, subissant 2d10 dégâts de feu en cas d'échec, ou la moitié de ces dégâts en cas de réussite. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts sont augmentés de 1d10 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Sanctuaire", "type": "abjuration", "temps_incantation": "1 action bonus", "portée": "9 mètres", "composantes": "V, S, M (un petit miroir en argent)", "durée": "1 minute", "description": "Vous protégez une créature dans la portée du sort contre les attaques. Jusqu'à ce que le sort se termine, toute créature qui cible la créature protégée avec une attaque ou un sort offensif doit d'abord effectuer un jet de sauvegarde de Sagesse. En cas d'échec, la créature doit choisir une nouvelle cible ou perdre son attaque ou son sort. Ce sort ne protège pas la créature protégée contre les sorts à zone d'effet, tel que l'explosion d'une boule de feu. Si la créature protégée fait une attaque, lance un sort qui affecte une créature ennemie ou inflige des dégâts à une autre créature, ce sort se termine."},
{"nom": "Saut", "type": "transmutation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S, M (la patte postérieure d'une sauterelle)", "durée": "1 minute", "description": "Vous touchez une créature. La distance de saut de la créature est triplée pour la durée du sort."},
{"nom": "Secousse sismique", "type": "évocation", "temps_incantation": "1 action", "portée": "3 mètres", "composantes": "V, S", "durée": "instantanée", "description": "Vous causez un tremblement dans le sol à portée. Chaque créature autre que vous-même dans cette zone doit faire un jet de sauvegarde de Dextérité. En cas d'échec, la créature subit 1d6 dégâts contondants et se retrouve à terre. Si le sol dans cette zone est de la terre meuble ou de la pierre, il devient un terrain difficile jusqu'à qu'il soit déblayé, et chaque portion de la zone de 1,50 mètre de diamètre nécessite au moins 1 minute pour être nettoyée à la main. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Serviteur invisible", "type": "invocation (rituel)", "temps_incantation": "1 action", "portée": "18 mètres", "composantes": "V, S, M (un morceau de ficelle et un bout de bois)", "durée": "1 heure", "description": "Ce sort crée une force invisible, sans volonté propre, informe mais de taille M, qui exécute les ordres simples que vous lui transmettez, jusqu'à la fin du sort. Le serviteur prend vie dans un espace inoccupé sur le sol et à portée. Il possède les caractéristiques suivantes : CA 10 ; 1 point de vie ; Force 2 ; ne peut pas attaquer. Le sort se termine si le serviteur tombe à 0 point de vie. Une fois par tour, par une action bonus, vous pouvez mentalement ordonner au serviteur de se déplacer de 4,50 mètres et d'interagir avec un objet. Le serviteur peut exécuter des tâches simples comme un serviteur humain le ferait, comme rapporter quelque chose, nettoyer, raccommoder, plier des vêtements, entretenir un feu, servir à manger, et verser du vin. Une fois votre ordre donné, le serviteur cherche à l'exécuter du mieux qu'il peut jusqu'à ce que la tâche soit accomplie, puis il attend votre ordre suivant. Si vous demandez à votre serviteur d'effectuer une tâche qui devrait l'envoyer à plus de 18 mètres de vous, le sort prend fin."},
{"nom": "Simulacre de vie", "type": "nécromancie", "temps_incantation": "1 action", "portée": "personnelle", "composantes": "V, S, M (une petite quantité d'alcool ou de spiritueux)", "durée": "1 heure", "description": "Vous vous protégez avec un semblant nécromantique de vie. Vous gagnez 1d4 + 4 points de vie temporaires pour la durée du sort. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, vous gagnez 5 points de vie temporaires supplémentaires pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Soins", "type": "évocation", "temps_incantation": "1 action", "portée": "contact", "composantes": "V, S", "durée": "instantanée", "description": "Une créature que vous touchez récupère un nombre de points de vie égal à 1d8 + le modificateur de votre caractéristique d'incantation. Ce sort n'a pas d'effet sur les morts-vivants et les artificiels. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, la quantité de points de vie récupérés est augmentée de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Sommeil", "type": "enchantement", "temps_incantation": "1 action", "portée": "27 mètres", "composantes": "V, S, M (une pincée de sable fin, de pétales de rose ou un grillon)", "durée": "1 minute", "description": "Ce sort expédie les créatures dans un sommeil magique. Lancez 5d8 ; le total est le nombre de points de vie des créatures que ce sort peut affecter. Les créatures à 6 mètres ou moins du point que vous choisissez dans la portée du sort sont affectées par ordre croissant de leurs points de vie actuels (en ignorant les créatures inconscientes). En commençant par la créature qui a le plus faible nombre de points de vie actuel, chaque créature affectée par ce sort tombe inconsciente jusqu'à ce que le sort se termine, que la créature endormie prenne des dégâts ou que quelqu'un utilise une action pour secouer ou frapper la créature endormie pour la réveiller. Soustrayez les points de vie de chaque créature du total permis par le sort avant de passer à la prochaine créature avec le plus faible nombre de points de vie. Le nombre de points de vie actuels d'une créature doit être égal ou inférieur au total restant permis par le sort pour que cette créature soit affectée. Les morts-vivants et les créatures immunisées contre les effets de charme ne sont pas affectés par ce sort. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, lancez 2d8 supplémentaires pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Tentacules de Hadar", "type": "invocation", "temps_incantation": "1 action", "portée": "personnelle (rayon de 3 mètres)", "composantes": "V, S", "durée": "instantanée", "description": "Vous invoquez le pouvoir de Hadar, la Sombre Famine. Des sarments d'énergie noire jaillissent de vous et frappent toutes les créatures se trouvant à 3 mètres ou moins de vous. Toute créature dans cette zone doit effectuer un jet de sauvegarde de Force. En cas d'échec, la cible subit 2d6 dégâts nécrotiques et ne peut pas utiliser de réaction jusqu'à son prochain tour. En cas de réussite, la cible subit la moitié de ces dégâts et ne souffre pas d'effets supplémentaires. Aux niveaux supérieurs. Si vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d6 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Texte illusoire", "type": "illusion (rituel)", "temps_incantation": "1 minute", "portée": "contact", "composantes": "S, M (une encre à base de plomb d'une valeur d'au moins 10 po, que le sort consomme)", "durée": "10 jours", "description": "Vous écrivez sur un parchemin, du papier, ou tout autre matériau adapté à l'écriture, et l'imprégnez d'une puissante illusion qui reste en place pour toute la durée du sort. Pour vous et pour toute créature que vous avez désignée lorsque vous avez lancé ce sort, l'écriture apparaît normalement, tracée de votre main, et transmet ce que vous souhaitiez communiquer lorsque vous avez lancé ce sort. Pour toutes les autres créatures, les écritures semblent être rédigées dans un dialecte inconnu ou magique, ce qui les rend inintelligibles. Vous pouvez sinon faire en sorte que les écritures transmettent un tout autre message, écrit d'une autre main et dans un autre langage, à condition que ce soit un langage que vous connaissiez. Dans le cas où le sort serait dissipé, le texte original et l'illusion disparaissent tous les deux. Une créature qui possède la vision véritable peut lire le message caché."},
{"nom": "Trait ensorcelé", "type": "évocation", "temps_incantation": "1 action", "portée": "9 mètres", "composantes": "V, S, M (la branche d'un arbre qui a été frappé par la foudre)", "durée": "concentration, jusqu'à 1 minute", "description": "Un rayon d'énergie bleu crépitante est projeté sur une créature à portée, formant un arc électrique continu entre la cible et vous. Effectuez une attaque à distance avec un sort contre la créature. Si vous touchez, la cible subit 1d12 dégâts de foudre, et à chacun de vos tours, pour la durée du sort, vous pouvez utiliser votre action pour infliger automatiquement 1d12 dégâts de foudre à la cible. Le sort se termine si vous utilisez votre action pour faire autre chose qu'infliger ces dégâts de foudre, si la cible se retrouve hors de la portée du sort, ou si elle obtient un abri total contre vous. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts initiaux sont augmentés de 1d12 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Vague tonnante", "type": "évocation", "temps_incantation": "1 action", "portée": "personnelle (cube de 4,50 mètres d'arête)", "composantes": "V, S", "durée": "instantanée", "description": "Une vague de force de tonnerre émane de vous. Toute créature se trouvant dans un cube de 4,50 mètres d'arête prenant origine à partir de vous-même doit effectuer un jet de sauvegarde de Constitution. En cas d'échec, la créature subit 2d8 dégâts de tonnerre et est repoussée de 3 mètres de vous. En cas de réussite, elle subit la moitié de ces dégâts et n'est pas repoussée. En outre, les objets non fixés qui se trouvent entièrement dans la zone d'effet sont automatiquement repoussés de 3 mètres par l'effet du sort, et le sort émet un coup de tonnerre audible jusqu'à 90 mètres. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, les dégâts augmentent de 1d8 pour chaque niveau d'emplacement au-delà du niveau 1."},
{"nom": "Vents contraires", "type": "évocation", "temps_incantation": "1 réaction", "portée": "1,50 m", "composantes": "V, S", "durée": "instantané", "description": "En réaction à une créature qui entre dans la portée du sort et avant que celle-ci n'attaque, vous pouvez la forcer à faire un jet de sauvegarde de Force. En cas d'échec, une puissante rafale de vent s'échappant de votre main la fait reculer de 1,50 mètre et la cible tombe à terre. Le recul ne provoque aucune attaque d'opportunité. Les créatures de taille G ont un avantage au jet de sauvegarde et les créatures de taille TG ou supérieure réussissent automatiquement ce jet. La créature peut se relever (cela coûte la moitié de sa vitesse), continuer à se déplacer et agir normalement après avoir été repoussée. Aux niveaux supérieurs. Lorsque vous lancez ce sort en utilisant un emplacement de sort de niveau 2 ou supérieur, la créature est repoussée de 1,50 mètre supplémentaire chaque niveau d'emplacement au-delà du niveau 1."}
    ]
capacites_historique = {
    'Abri du fidèle':"En tant qu'acolyte, vous imposez le respect à ceux qui partagent votre foi, et pouvez mener les cérémonies religieuses de votre divinité. Vous et vos compagnons aventuriers pouvez vous attendre à recevoir des soins gratuits dans un temple, un sanctuaire ou toute autre présence établie de votre foi, bien que vous soyez responsable de fournir toutes les composantes matérielles nécessaires aux sorts. Ceux qui partagent votre religion vous aideront (mais seulement vous) et vous offriront un mode de vie modeste. Vous pouvez également avoir des liens avec un temple spécifique dédié à votre divinité ou votre panthéon, et vous y avez une résidence. Cela pourrait être le temple où vous avez servi, si vous êtes resté en bons termes avec lui, ou un temple dans lequel vous avez trouvé une nouvelle maison. Lorsque vous êtes proche de votre temple, vous pouvez faire appel à des religieux pour vous aider, à condition que l'aide que vous demandiez ne soit pas dangereuse et que vous restiez en règle avec votre temple. ",
    'Membre de guilde':"En tant que membre établi et respecté de votre guilde, vous pouvez compter sur certains avantages que vous confère votre adhésion. Vos compagnons de guilde vous procureront le gîte et le couvert si nécessaire, et payeront pour vos funérailles si besoin. Dans certaines villes ou cités, les guildes offrent un endroit où vous pouvez rencontrer d'autres membres de votre profession, ce qui peut être un bon moyen pour faire la connaissance de patrons potentiels, d'alliés ou de larbins.Les guildes exercent souvent un important pouvoir politique. Si vous êtes accusé de crime, votre guilde vous soutiendra si de bons arguments peuvent être déployés pour prouver votre innocence, ou si le crime était justifié. Vous pouvez également avoir accès à certaines figures politiques puissantes grâce à la guilde, si vous êtes un membre de haut rang. Ces mises en relation peuvent toutefois nécessiter que vous fassiez un don d'or ou d'objet magique au coffre de la guilde. Vous devez payer 5 po par mois à la guilde. Si vous manquez un paiement, vous devrez compenser votre retard de cotisation pour revenir dans les bonnes grâces de la guilde. ",
    'Accointances avec la pègree':"Vous avez un contact fiable et digne de confiance qui agit comme votre agent de liaison avec un réseau d'autres criminels. Vous savez comment envoyer et recevoir des messages via votre contact, même sur de grandes distances. Concrètement, vous connaissez les messagers locaux, les maîtres de caravanes corrompus et les marins miteux qui peuvent délivrer des messages pour vous. "
    }
babioles = [
    "Une main de gobelin momifiée", "Un morceau de cristal qui brille faiblement au clair de lune", 
    "Une pièce d'or d'une terre inconnue", "Un journal écrit dans une langue que vous ne connaissez pas",
    "Un anneau de cuivre qui ne ternit pas", "Une vieille pièce d'échecs en verre",
    "Une paire de dés en osselet, chacun portant le symbole d'un crâne sur la face qui montrerait normalement le 6",
    "Une petite idole représentant une créature cauchemardesque qui vous donne des rêves troublants quand vous dormez près d'elle",
    "Un collier en corde duquel pendent quatre doigts elfes momifiés", "L'acte d'une parcelle de terrain d'un domaine que vous ne connaissez pas",
    "Un bloc de 30 grammes d'un matériau inconnu", "Une petite poupée de chiffon piquée avec des aiguilles",
    "Une dent d'une bête inconnue", "Une énorme écaille, peut-être d'un dragon", 
    "Une plume vert clair", "Une vieille carte de divination portant votre portrait", 
    "Un orbe en verre rempli de fumée qui se déplace", "Un oeuf de 30 grammes avec une coque rouge vif", 
    "Une pipe qui fait des bulles", "Un pot en verre contenant un morceau de chair bizarre qui flotte dans un liquide salé",
    "Une petite boîte à musique de gnome qui joue une chanson qui vous rappelle vaguement votre enfance", 
    "Une petite statuette en bois d'un halfelin béat", "Un orbe en cuivre gravé de runes étranges",
    "Un disque de pierre multicolore", "Une petite icône d'argent représentant un corbeau",
    "Un sac contenant quarante-sept dents humanoïdes, dont l'une est cariée", "Un fragment d'obsidienne qui se sent toujours chaud au toucher",
    "Une griffe osseuse d'un dragon suspendue à un collier de cuir lisse", "Une paire de vieilles chaussettes",
    "Un livre blanc dont les pages refusent de retenir l'encre, la craie, la graphite ou toute autre substance ou marquage", 
    "Un badge en argent qui représente une étoile à cinq branches", "Un couteau qui appartenait à un parent",
    "Un flacon de verre rempli de rognures d'ongles", "Un dispositif métallique et rectangulaire avec deux petites coupes en métal à une extrémité et qui jette des étincelles lorsqu'il est mouillé",
    "Un gant blanc pailleté aux dimensions d'un humain", "Une veste avec une centaine de minuscules poches",
    "Un petit bloc de pierre léger", "Un petit dessin qui représente le portrait d'un gobelin",
    "Un flacon de verre vide qui sent le parfum lorsqu'il est ouvert", "Une pierre précieuse qui ressemble à un morceau de charbon pour tout le monde, sauf pour vous",
    "Un morceau de tissu d'une vieille bannière", "Un insigne de grade d'un légionnaire perdu",
    "Une cloche en argent minuscule et sans battant", "Un canari mécanique à l'intérieur d'une lampe de gnome",
    "Un petit coffre avec de nombreux pieds sculptés sur le fond", "Une pixie morte à l'intérieur d'une bouteille en verre transparent",
    "Une boîte métallique qui n'a pas d'ouverture mais qui sonne comme si elle était remplie de liquide, de sable, d'araignées ou de verre brisé (au choix)",
    "Un orbe de verre rempli d'eau, dans lequel nage un poisson rouge mécanique", "Une cuillère d'argent avec un M gravé sur le manche",
    "Un scarabée mort de la taille de votre main", "Deux soldats de plomb, l'un avec la tête manquante",
    "Une petite boîte remplie de boutons de différentes tailles", "Une bougie qui ne peut pas être allumée",
    "Une petite cage sans porte", "Une vieille clé", 
    "Une carte au trésor indéchiffrable", "Une poigne d'épée brisée", 
    "Une patte de lapin", "Un œil de verre", 
    "Un camée (pendentif) sculpté à l'image d'une personne hideuse", "Un crâne en argent de la taille d'une pièce de monnaie",
    "Un masque d'albâtre", "Une pyramide de bâtonnets d'encens noir qui sent très mauvais",
    "Un bonnet de nuit qui, lorsqu'il est porté, vous donne des rêves agréables", 
    "Une chausse-trappe unique fabriquée à partir d'un os", "Un cadre de monocle en or sans la lentille",
    "Un cube de 2,50 cm d'arête, avec chaque face peinte d'une couleur différente", "Un bouton de porte en cristal",
    "Un petit paquet rempli de poussière rose", "Un fragment d'une belle chanson, écrite avec des notes de musique sur deux morceaux de parchemin",
    "Une boucle d'oreille en forme de goutte d'argent faite à partir d'une vraie larme", 
    "La coquille d'un oeuf peint avec des scènes de misère humaine d'un détail troublant", 
    "Un éventail qui, une fois déplié, montre un chat endormi", "Un ensemble de tubes d'os",
    "Un trèfle à quatre feuilles à l'intérieur d'un livre qui traite des bonnes manières et de l'étiquette", 
    "Une feuille de parchemin sur laquelle est dessiné un engin mécanique complexe", 
    "Un fourreau orné dans lequel à ce jour aucune lame ne rentre", "Une invitation à une fête où un assassinat a eu lieu",
    "Un pentacle de bronze avec la gravure d'une tête de rat au centre", 
    "Un mouchoir violet brodé avec le nom d'un puissant archimage", 
    "La moitié du plan d'un temple, d'un château, ou d'une autre structure", 
    "Un peu de tissu plié qui, une fois déplié, se transforme en un élégant chapeau", 
    "Un récépissé de dépôt dans une banque d'une ville très éloignée", "Un journal avec sept pages manquantes",
    "Une tabatière en argent vide et portant une inscription sur le dessus qui dit « rêves »", 
    "Un symbole sacré en fer et consacré à un dieu inconnu", 
    "Un livre qui raconte l'histoire de l'ascension et la chute d'un héros légendaire, avec le dernier chapitre manquant", 
    "Un flacon de sang de dragon", "Une ancienne flèche de conception elfique", 
    "Une aiguille qui ne se plie pas", "Une broche ornée de conception naine", 
    "Une bouteille de vin vide portant une jolie étiquette qui dit « Le magicien des vins, Cuvée du Dragon Rouge, 331422-W »",
    "Un couvercle avec une mosaïque multicolore en surface", "Une souris pétrifiée", 
    "Un drapeau de pirate noir orné d'un crâne et des os croisés d'un dragon", 
    "Un petit crabe ou araignée mécanique qui se déplace quand il n'est pas observé", 
    "Un pot de verre contenant du lard avec une étiquette qui dit « Graisse de griffon »", 
    "Une boîte en bois avec un fond en céramique qui contient un ver vivant avec une tête à chaque extrémité de son corps", 
    "Une urne en métal contenant les cendres d'un héros"
]

sacs = {
    "Sac d'artiste": [
        "un sac à dos", "un sac de couchage", "2 costumes", "5 bougies", 
        "5 jours de rations", "une gourde d'eau", "un kit de déguisement"
    ],
    "Sac de cambrioleur": [
        "un sac à dos", "un sac de 1000 billes", "3 mètres de chaîne", 
        "une cloche", "5 bougies", "un pied-de-biche", "un marteau", 
        "10 pitons", "une lanterne à capuchon", "2 flasques d'huile", 
        "5 jours de rations", "une boite d'allume-feu", "une gourde d'eau", 
        "15 mètres de corde de chanvre"
    ],
    "Sac de diplomate": [
        "un coffre", "2 étuis à cartes ou parchemins", "des vêtements fins", 
        "une bouteille d'encre", "une plume d'écriture", "une lampe", 
        "deux flasques d'huile", "5 feuilles de papier", "un flacon de parfum", 
        "cire à cacheter", "savon"
    ],
    "Sac d'ecclésiastique": [
        "un sac à dos", "une couverture", "10 bougies", 
        "une boite d'allume-feu", "une boîte pour l'aumône", "2 bâtonnets d'encens", 
        "un encensoir", "des habits de cérémonie", "2 jours de rations", "une gourde d'eau"
    ],
    "Sac d'érudit": [
        "un sac à dos", "un livre de connaissance", "une bouteille d'encre", 
        "une plume d'écriture", "10 feuilles de parchemin", 
        "un petit sac de sable", "un petit couteau"
    ],
    "Sac d'explorateur": [
        "un sac à dos", "un sac de couchage", "une gamelle", "une boite d'allume-feu", 
        "10 torches", "10 jours de rations", "une gourde d'eau", 
        "15 mètres de corde de chanvre"
    ],
    "Sac d'exploration souterraine": [
        "un sac à dos", "un pied de biche", "un marteau", 
        "10 pitons", "10 torches", "une boite d'allume-feu", 
        "10 jours de rations", "une gourde d'eau", "15 mètres de corde de chanvre"
    ]
}


armes = [
    {"Nom": "Bâton", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d6 contondant", "Prix": "2 pa", "Propriété": "Polyvalente (1d8)", "Modificateur": "Force"},
    {"Nom": "Dague", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d4 perforant", "Prix": "2 po", "Propriété": "Finesse, légère, lancer (portée 6 m/18 m)", "Modificateur": "Force ou Dextérité"},
    {"Nom": "Gourdin", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d4 contondant", "Prix": "1 pa", "Propriété": "Légère", "Modificateur": "Force"},
    {"Nom": "Hachette", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d6 tranchant", "Prix": "5 po", "Propriété": "Légère, lancer (portée 6 m/18 m)", "Modificateur": "Force"},
    {"Nom": "Javeline", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d6 perforant", "Prix": "5 pa", "Propriété": "Lancer (portée 9 m/36 m)", "Modificateur": "Force"},
    {"Nom": "Lance", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d6 perforant", "Prix": "1 po", "Propriété": "Lancer (portée 6 m/18 m), polyvalente (1d8)", "Modificateur": "Force"},
    {"Nom": "Marteau léger", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d4 contondant", "Prix": "2 po", "Propriété": "Légère, lancer (portée 6 m/18 m)", "Modificateur": "Force"},
    {"Nom": "Masse d'armes", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d6 contondant", "Prix": "5 po", "Propriété": "", "Modificateur": "Force"},
    {"Nom": "Massue", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d8 contondant", "Prix": "2 pa", "Propriété": "À deux mains", "Modificateur": "Force"},
    {"Nom": "Serpe", "Typologie": "Armes courantes", "Distance": "Corps à corps", "Dégât": "1d4 tranchant", "Prix": "1 po", "Propriété": "Légère", "Modificateur": "Force"},
    {"Nom": "Arbalète légère", "Typologie": "Armes courantes", "Distance": "Arme à distance", "Dégât": "1d8 perforant", "Prix": "25 po", "Propriété": "Munitions (portée 24 m/96 m), chargement, à deux mains", "Modificateur": "Dextérité"},
    {"Nom": "Arc court", "Typologie": "Armes courantes", "Distance": "Arme à distance", "Dégât": "1d6 perforant", "Prix": "25 po", "Propriété": "Munitions (portée 24 m/96 m), à deux mains", "Modificateur": "Dextérité"},
    {"Nom": "Fléchette", "Typologie": "Armes courantes", "Distance": "Arme à distance", "Dégât": "1d4 perforant", "Prix": "5 pc", "Propriété": "Finesse, lancer (portée 6 m/18 m)", "Modificateur": "Dextérité"},
    {"Nom": "Fronde", "Typologie": "Armes courantes", "Distance": "Arme à distance", "Dégât": "1d4 contondant", "Prix": "1 pa", "Propriété": "Munitions (portée 9 m/36 m)", "Modificateur": "Dextérité"},
    {"Nom": "Cimeterre", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d6 tranchant", "Prix": "25 po", "Propriété": "Finesse, légère", "Modificateur": "Force ou Dextérité"},
    {"Nom": "Glaive", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d10 tranchant", "Prix": "20 po", "Propriété": "Lourde, allonge, à deux mains", "Modificateur": "Force"},
    {"Nom": "Épée à deux mains", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "2d6 tranchant", "Prix": "50 po", "Propriété": "Lourde, à deux mains", "Modificateur": "Force"},
    {"Nom": "Épée courte", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d6 tranchant", "Prix": "10 po", "Propriété": "Finesse, légère", "Modificateur": "Force ou Dextérité"},
    {"Nom": "Épée longue", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 tranchant", "Prix": "15 po", "Propriété": "Polyvalente (1d10)", "Modificateur": "Force"},
    {"Nom": "Fléau d'armes", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 contondant", "Prix": "10 po", "Propriété": "", "Modificateur": "Force"},
    {"Nom": "Fouet", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d4 tranchant", "Prix": "2 po", "Propriété": "Finesse, allonge", "Modificateur": "Force ou Dextérité"},
    {"Nom": "Hache à deux mains", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d12 tranchant", "Prix": "30 po", "Propriété": "Lourde, à deux mains", "Modificateur": "Force"},
    {"Nom": "Hache d'armes", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 tranchant", "Prix": "10 po", "Propriété": "Polyvalente (1d10)", "Modificateur": "Force"},
    {"Nom": "Hallebarde", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d10 tranchant", "Prix": "20 po", "Propriété": "Lourde, à deux mains", "Modificateur": "Force"},
    {"Nom": "Lance d’arçon", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d12 perforant", "Prix": "10 po", "Propriété": "Allonge, lance d’arçon", "Modificateur": "Force"},
    {"Nom": "Maillet", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "2d6 contondant", "Prix": "10 po", "Propriété": "Lourde, à deux mains", "Modificateur": "Force"},
    {"Nom": "Marteau de guerre", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 contondant", "Prix": "15 po", "Propriété": "Polyvalente (1d10)", "Modificateur": "Force"},
    {"Nom": "Morgenstern", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 perforant", "Prix": "15 po", "Propriété": "", "Modificateur": "Force"},
    {"Nom": "Pic de guerre", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 perforant", "Prix": "5 po", "Propriété": "", "Modificateur": "Force"},
    {"Nom": "Pique", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d10 perforant", "Prix": "5 po", "Propriété": "Lourde, allonge, à deux mains", "Modificateur": "Force"},
    {"Nom": "Rapière", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d8 perforant", "Prix": "25 po", "Propriété": "Finesse", "Modificateur": "Force ou Dextérité"},
    {"Nom": "Trident", "Typologie": "Armes de guerre", "Distance": "Corps à corps", "Dégât": "1d6 perforant", "Prix": "5 po", "Propriété": "Lancer (portée 6 m/18 m), polyvalente (1d8)", "Modificateur": "Force"},
    {"Nom": "Arbalète de poing", "Typologie": "Armes de guerre", "Distance": "Arme à distance", "Dégât": "1d6 perforant", "Prix": "75 po", "Propriété": "Munitions (portée 9 m/36 m), légère, chargement", "Modificateur": "Dextérité"},
    {"Nom": "Arbalète lourde", "Typologie": "Armes de guerre", "Distance": "Arme à distance", "Dégât": "1d10 perforant", "Prix": "50 po", "Propriété": "Munitions (portée 30 m/120 m), lourde, chargement, à deux mains", "Modificateur": "Dextérité"},
    {"Nom": "Arc long", "Typologie": "Armes de guerre", "Distance": "Arme à distance", "Dégât": "1d8 perforant", "Prix": "50 po", "Propriété": "Munitions (portée 45 m/180 m), lourde, à deux mains", "Modificateur": "Dextérité"},
    {"Nom": "Filet", "Typologie": "Armes de guerre", "Distance": "Arme à distance", "Dégât": "", "Prix": "1 po", "Propriété": "Filet, lancer (portée 1,50 m/4,50 m)", "Modificateur": "Dextérité"},
    {"Nom": "Sarbacane", "Typologie": "Armes de guerre", "Distance": "Arme à distance", "Dégât": "1 perforant", "Prix": "10 po", "Propriété": "Munitions (portée 7,50 m/30 m), chargement", "Modificateur": "Dextérité"}
]

proprietes_arme = {
    "à deux mains": "Vous devez manier cette arme à deux mains pour effectuer une attaque.",
    "allonge": "Ce type d'arme vous permet de gagner 1,50 mètre d'allonge supplémentaire.",
    "chargement": "Cette arme nécessite un temps de chargement, limitant les attaques par tour.",
    "finesse": "Vous pouvez choisir d'ajouter votre modificateur de Force ou de Dextérité aux jets d'attaque et de dégâts.",
    "lancer": "Permet de lancer l'arme pour faire une attaque à distance.",
    "légère": "Cette arme est petite et facile à manier, idéale pour le combat à deux armes.",
    "lourde": "Les créatures de petite taille subissent un désavantage sur les jets d'attaque avec cette arme.",
    "munitions": "Vous ne pouvez utiliser cette arme que si vous avez les munitions nécessaires.",
    "portée": "Indique la portée de l'arme en mètres pour une attaque à distance.",
    "filet": "Une créature de taille G ou moins est entravée jusqu'à ce qu'elle soit libérée.",
    "lance d'arçon": "Vous subissez un désavantage si vous utilisez cette arme à courte portée.",
    "argent": "Certains monstres résistants aux armes non-magiques sont vulnérables aux armes en argent."
}

armures_et_boucliers = [
    {"Nom": "Matelassée", "Typologie": "Armures légères", "CA": "11 + Mod.Dex", "Minimum force": "", "Discrétion": "Désavantage", "Prix": "5 po"},
    {"Nom": "Cuir", "Typologie": "Armures légères", "CA": "11 + Mod.Dex", "Minimum force": "", "Discrétion": "", "Prix": "10 po"},
    {"Nom": "Cuir clouté", "Typologie": "Armures légères", "CA": "12 + Mod.Dex", "Minimum force": "", "Discrétion": "", "Prix": "45 po"},
    {"Nom": "Peaux", "Typologie": "Armures intermédiaires", "CA": "12 + Mod.Dex (max +2)", "Minimum force": "", "Discrétion": "", "Prix": "10 po"},
    {"Nom": "Chemise de mailles", "Typologie": "Armures intermédiaires", "CA": "13 + Mod.Dex (max +2)", "Minimum force": "", "Discrétion": "", "Prix": "50 po"},
    {"Nom": "Écailles", "Typologie": "Armures intermédiaires", "CA": "14 + Mod.Dex (max +2)", "Minimum force": "", "Discrétion": "Désavantage", "Prix": "50 po"},
    {"Nom": "Cuirasse", "Typologie": "Armures intermédiaires", "CA": "14 + Mod.Dex (max +2)", "Minimum force": "", "Discrétion": "", "Prix": "400 po"},
    {"Nom": "Demi-plate", "Typologie": "Armures intermédiaires", "CA": "15 + Mod.Dex (max +2)", "Minimum force": "", "Discrétion": "Désavantage", "Prix": "750 po"},
    {"Nom": "Broigne", "Typologie": "Armures lourdes", "CA": "14", "Minimum force": "", "Discrétion": "Désavantage", "Prix": "30 po"},
    {"Nom": "Cotte de mailles", "Typologie": "Armures lourdes", "CA": "16", "Minimum force": "13", "Discrétion": "Désavantage", "Prix": "75 po"},
    {"Nom": "Clibanion", "Typologie": "Armures lourdes", "CA": "17", "Minimum force": "15", "Discrétion": "Désavantage", "Prix": "200 po"},
    {"Nom": "Harnois", "Typologie": "Armures lourdes", "CA": "18", "Minimum force": "15", "Discrétion": "Désavantage", "Prix": "1500 po"},
    {"Nom": "Bouclier", "Typologie": "Boucliers", "CA": "+2", "Minimum force": "", "Discrétion": "", "Prix": "10 po"}
]

equipement_aventurier = [
    {"Nom": "Acide (fiole)", "Prix": "25 po", "Type": ""},
    {"Nom": "Antidote (fiole)", "Prix": "50 po", "Type": ""},
    {"Nom": "Balance de marchand", "Prix": "5 po", "Type": ""},
    {"Nom": "Bélier portable", "Prix": "4 po", "Type": ""},
    {"Nom": "Billes (sac de 1000)", "Prix": "1 po", "Type": ""},
    {"Nom": "Boite d'allume-feu", "Prix": "5 pa", "Type": ""},
    {"Nom": "Bougie", "Prix": "1 pc", "Type": ""},
    {"Nom": "Boulier", "Prix": "2 po", "Type": ""},
    {"Nom": "Bouteille en verre", "Prix": "2 po", "Type": ""},
    {"Nom": "Cadenas", "Prix": "10 po", "Type": ""},
    {"Nom": "Carquois", "Prix": "1 po", "Type": ""},
    {"Nom": "Chaîne (3 m)", "Prix": "5 po", "Type": ""},
    {"Nom": "Chausse-trappes (sac de 20)", "Prix": "1 po", "Type": ""},
    {"Nom": "Chevalière", "Prix": "5 po", "Type": ""},
    {"Nom": "Cire à cacheter", "Prix": "5 pa", "Type": ""},
    {"Nom": "Cloche", "Prix": "1 po", "Type": ""},
    {"Nom": "Coffre", "Prix": "5 po", "Type": ""},
    {"Nom": "Corde en chanvre (15 m)", "Prix": "1 po", "Type": ""},
    {"Nom": "Corde en soie (15 m)", "Prix": "10 po", "Type": ""},
    {"Nom": "Couverture", "Prix": "5 pa", "Type": ""},
    {"Nom": "Craie (un morceau)", "Prix": "1 pc", "Type": ""},
    {"Nom": "Cruche ou pichet", "Prix": "2 pc", "Type": ""},
    {"Nom": "Eau bénite (flasque)", "Prix": "25 po", "Type": ""},
    {"Nom": "Échelle (3 m)", "Prix": "1 pa", "Type": ""},
    {"Nom": "Encre (bouteille de 30 ml)", "Prix": "10 po", "Type": ""},
    {"Nom": "Étui à carreaux", "Prix": "1 po", "Type": ""},
    {"Nom": "Étui à cartes ou parchemins", "Prix": "1 po", "Type": ""},
    {"Nom": "Feu grégeois (flasque)", "Prix": "50 po", "Type": ""},
    {"Nom": "Fiole (10 cl)", "Prix": "2 pc", "Type": ""},
    {"Nom": "Flasque ou chope (50 cl)", "Prix": "5 po", "Type": ""},
    {"Nom": "Baguette", "Prix": "10 po", "Type": "Focaliseur arcanique"},
    {"Nom": "Bâton", "Prix": "5 po", "Type": "Focaliseur arcanique"},
    {"Nom": "Boule de cristal", "Prix": "10 po", "Type": "Focaliseur arcanique"},
    {"Nom": "Orbe", "Prix": "20 po", "Type": "Focaliseur arcanique"},
    {"Nom": "Sceptre", "Prix": "10 po", "Type": "Focaliseur arcanique"},
    {"Nom": "Baguette d'if", "Prix": "10 po", "Type": "Focaliseur druidique"},
    {"Nom": "Bâton", "Prix": "5 po", "Type": "Focaliseur druidique"},
    {"Nom": "Branche de gui", "Prix": "1 po", "Type": "Focaliseur druidique"},
    {"Nom": "Totem", "Prix": "1 po", "Type": "Focaliseur druidique"},
    {"Nom": "Gamelle", "Prix": "2 pa", "Type": ""},
    {"Nom": "Gourde (pleine)", "Prix": "2 pa", "Type": ""},
    {"Nom": "Grappin", "Prix": "2 po", "Type": ""},
    {"Nom": "Grimoire", "Prix": "50 po", "Type": ""},
    {"Nom": "Huile (flasque)", "Prix": "1 pa", "Type": ""},
    {"Nom": "Kit d’escalade", "Prix": "25 po", "Type": ""},
    {"Nom": "Lampe", "Prix": "5 pa", "Type": ""},
    {"Nom": "Lanterne à capote", "Prix": "5 po", "Type": ""},
    {"Nom": "Lanterne sourde", "Prix": "10 po", "Type": ""},
    {"Nom": "Livre", "Prix": "25 po", "Type": ""},
    {"Nom": "Longue-vue", "Prix": "1000 po", "Type": ""},
    {"Nom": "Loupe", "Prix": "100 po", "Type": ""},
    {"Nom": "Marteau", "Prix": "1 po", "Type": ""},
    {"Nom": "Marteau de forgeron", "Prix": "2 po", "Type": ""},
    {"Nom": "Matériel de pêche", "Prix": "1 po", "Type": ""},
    {"Nom": "Menottes", "Prix": "2 po", "Type": ""},
    {"Nom": "Miroir en acier", "Prix": "5 po", "Type": ""},
    {"Nom": "Aiguilles de sarbacane (50)", "Prix": "1 po", "Type": "Munitions"},
    {"Nom": "Billes de fronde (20)", "Prix": "4 pc", "Type": "Munitions"},
    {"Nom": "Carreaux d'arbalète (20)", "Prix": "1 po", "Type": "Munitions"},
    {"Nom": "Flèches (20)", "Prix": "1 po", "Type": "Munitions"},
    {"Nom": "Palan", "Prix": "1 po", "Type": ""},
    {"Nom": "Panier", "Prix": "4 pa", "Type": ""},
    {"Nom": "Papier (une feuille)", "Prix": "2 pa", "Type": ""},
    {"Nom": "Parchemin (une feuille)", "Prix": "1 pa", "Type": ""},
    {"Nom": "Parfum (fiole)", "Prix": "5 po", "Type": ""},
    {"Nom": "Pelle", "Prix": "2 po", "Type": ""},
    {"Nom": "Perche (3 m)", "Prix": "5 pc", "Type": ""},
    {"Nom": "Pied-de-biche", "Prix": "2 po", "Type": ""},
    {"Nom": "Piège à mâchoires", "Prix": "5 po", "Type": ""},
    {"Nom": "Pierre à aiguiser", "Prix": "1 pc", "Type": ""},
    {"Nom": "Pioche de mineur", "Prix": "2 po", "Type": ""},
    {"Nom": "Piton", "Prix": "5 pc", "Type": ""},
    {"Nom": "Plume d’écriture", "Prix": "2 pc", "Type": ""},
    {"Nom": "Pointes en fer (10)", "Prix": "1 po", "Type": ""},
    {"Nom": "Poison (fiole)", "Prix": "100 po", "Type": ""},
    {"Nom": "Pot en fer", "Prix": "2 po", "Type": ""},
    {"Nom": "Potion de guérison", "Prix": "50 po", "Type": ""},
    {"Nom": "Rations (1 jour)", "Prix": "5 pa", "Type": ""},
    {"Nom": "Robes", "Prix": "1 po", "Type": ""},
    {"Nom": "Sablier", "Prix": "25 po", "Type": ""},
    {"Nom": "Sac", "Prix": "1 pc", "Type": ""},
    {"Nom": "Sac à dos", "Prix": "2 po", "Type": ""},
    {"Nom": "Sac de couchage", "Prix": "1 po", "Type": ""},
    {"Nom": "Sacoche", "Prix": "5 pa", "Type": ""},
    {"Nom": "Sacoche à composantes", "Prix": "25 po", "Type": ""},
    {"Nom": "Savon", "Prix": "2 pc", "Type": ""},
    {"Nom": "Seau", "Prix": "5 pc", "Type": ""},
    {"Nom": "Sifflet", "Prix": "5 pc", "Type": ""},
    {"Nom": "Amulette", "Prix": "5 po", "Type": "Symbole sacré"},
    {"Nom": "Emblème", "Prix": "5 po", "Type": "Symbole sacré"},
    {"Nom": "Reliquaire", "Prix": "5 po", "Type": "Symbole sacré"},
    {"Nom": "Tente", "Prix": "2 po", "Type": ""},
    {"Nom": "Tonneau", "Prix": "2 po", "Type": ""},
    {"Nom": "Torche", "Prix": "1 pc", "Type": ""},
    {"Nom": "Trousse de soins", "Prix": "5 po", "Type": ""},
    {"Nom": "Vêtements, communs", "Prix": "5 pa", "Type": ""},
    {"Nom": "Vêtements, costume", "Prix": "5 po", "Type": ""},
    {"Nom": "Vêtements, fins", "Prix": "15 po", "Type": ""},
    {"Nom": "Vêtements, voyage", "Prix": "2 po", "Type": ""}
]

outils = [
    {"Nom": "Chalemie", "Prix": "2 po", "Type": "Instrument de musique"},
    {"Nom": "Cor", "Prix": "3 po", "Type": "Instrument de musique"},
    {"Nom": "Cornemuse", "Prix": "30 po", "Type": "Instrument de musique"},
    {"Nom": "Flûte", "Prix": "2 po", "Type": "Instrument de musique"},
    {"Nom": "Flûte de pan", "Prix": "12 po", "Type": "Instrument de musique"},
    {"Nom": "Luth", "Prix": "35 po", "Type": "Instrument de musique"},
    {"Nom": "Lyre", "Prix": "30 po", "Type": "Instrument de musique"},
    {"Nom": "Tambour", "Prix": "6 po", "Type": "Instrument de musique"},
    {"Nom": "Tympanon", "Prix": "25 po", "Type": "Instrument de musique"},
    {"Nom": "Viole", "Prix": "30 po", "Type": "Instrument de musique"},
    {"Nom": "Dés", "Prix": "1 pa", "Type": "Jeu"},
    {"Nom": "Jeu d'échecs draconiques", "Prix": "1 po", "Type": "Jeu"},
    {"Nom": "Jeu de cartes", "Prix": "5 pa", "Type": "Jeu"},
    {"Nom": "Jeu des Dragons", "Prix": "1 po", "Type": "Jeu"},
    {"Nom": "Kit d'empoisonneur", "Prix": "50 po", "Type": ""},
    {"Nom": "Kit d'herboriste", "Prix": "5 po", "Type": ""},
    {"Nom": "Kit de contrefaçon", "Prix": "15 po", "Type": ""},
    {"Nom": "Kit de déguisement", "Prix": "25 po", "Type": ""},
    {"Nom": "Matériel d'alchimiste", "Prix": "50 po", "Type": "Outils d'artisan"},
    {"Nom": "Matériel de brasseur", "Prix": "20 po", "Type": "Outils d'artisan"},
    {"Nom": "Matériel de calligraphe", "Prix": "10 po", "Type": "Outils d'artisan"},
    {"Nom": "Matériel de peintre", "Prix": "10 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de bijoutier", "Prix": "25 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de bricoleur", "Prix": "50 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de cartographe", "Prix": "15 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de charpentier", "Prix": "8 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de cordonnier", "Prix": "5 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de forgeron", "Prix": "20 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de maçon", "Prix": "10 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de menuisier", "Prix": "1 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de potier", "Prix": "10 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de souffleur de verre", "Prix": "30 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de tanneur", "Prix": "5 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de tisserand", "Prix": "1 po", "Type": "Outils d'artisan"},
    {"Nom": "Ustensiles de cuisinier", "Prix": "1 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de navigateur", "Prix": "25 po", "Type": "Outils d'artisan"},
    {"Nom": "Outils de voleur", "Prix": "25 po", "Type": "Outils d'artisan"}
]


costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}
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

styles_de_combat = [StyleDeCombat(nom, description) for nom, description in description_style_de_combat.items()]

classes = {
    'Barbare': Classe(
        nom='Barbare',
        description='Pour un barbare, la civilisation n\'est pas une vertu, c\'est un signe de faiblesse. Les forts assument leurs instincts naturels, leur physique primitif et leur rage féroce. Les barbares ne sont pas à l\'aise derrière des murs ou entourés par la foule. Ils prospèrent sur les étendues sauvages de leurs terres natales.',
        details=[
            'DV. 1d12',
            'Armures. armures légères, armures intermédiaires, boucliers',
            'Armes. Armes courantes, armes de guerre',
            'Jets de sauvegarde. Force, Constitution',
            'Choix de 2 compétences parmi Athlétisme, Dressage, Intimidation, Nature, Perception et Survie'
        ],
        capacites=[
            """
Rage : En combat, vous vous battez avec une férocité bestiale. Durant votre tour, vous pouvez entrer en rage en utilisant une action bonus. En rage, vous gagnez les bénéfices suivants si vous ne portez pas d'armure lourde :
    - Vous avez un avantage aux jets de Force et aux jets de sauvegarde de Force.
    - Quand vous effectuez une attaque au corps à corps avec une arme utilisant la Force, vous gagnez un bonus aux jets de dégâts de +2. Vous pouvez vous mettre en rage 2 fois par long repos. 
    - Vous avez la résistance aux dégâts contondants, perforants et tranchants.
    - Si vous êtes capable de lancer des sorts, vous ne pouvez les lancer ou vous concentrer sur eux pour toute la durée de la rage.
Votre rage dure 1 minute. Elle finit prématurément si vous devenez inconscient, ou si votre tour se termine et que vous n'avez ni attaqué une créature hostile, ni subi des dégâts, depuis votre précédent tour. Vous pouvez également mettre fin à votre rage durant votre tour par une action bonus. Vous récupérez les utilisations de rage dépensées après avoir terminé un repos long.

Défense sans armure : Tant que vous ne portez pas d'armure, votre classe d'armure est égale à 10 + votre modificateur de Dextérité + votre modificateur de Constitution. Vous pouvez utiliser un bouclier et continuer de profiter de cette capacité.
            """
        ],
        nombre_outils=0,
        outils=[],
        nombre_de_competence=2,
        competences='Athlétisme, Dressage, Intimidation, Nature, Perception , Survie',
        sort_mineur_classe=[],
        nombre_sort_mineur_classe=0,
        sort_niveau_un_classe=[],
        nombre_sort_niveau_un_classe=0,
        styles_de_combat=[],
        argent_classe='2d4 x 10',
        packs={'Pack (a)': ['Une hache à deux mains', 'Deux hachettes', 'Quatre javelines', 'Sac d\'explorateur'],
               'Pack (b)': ['Une arme de guerre de corps à corps au choix', 'Une arme courante au choix', 'Quatre javelines', 'Sac d\'explorateur']},
        ca='10 + modificateur de Dextérité + modificateur de Constitution',
        jets_de_sauvegarde='Force, Constitution',
        pv=12
    ),
    'Barde': Classe(
        nom='Barde',
        description='Fredonnant alors qu’elle passe ses doigts sur un ancien monument au cœur de ruines depuis longtemps oubliées, une demi-elfe vêtue de cuir robuste sent le savoir, invoqué par la magie de son chant, bondir dans son esprit. La plus grande force du barde est son incontestable polyvalence. De nombreux bardes préfèrent demeurer en retrait lors d’un combat, utilisant plutôt la magie pour inspirer leurs alliés et gêner leurs ennemis.',
        details=[
            'DV. 1d8',
            'Armures. armures légères',
            'Armes. armes courantes, arbalète de poing, épée longue, épée courte, rapière',
            'Jets de sauvegarde. Dextérité, Charisme',
            'Choix de 3 compétences parmi toutes celles disponibles'
        ],
        capacites=[
            """
Inspiration bardique : Vous pouvez inspirer les autres en maniant les mots ou la musique. Pour ce faire, utilisez une action bonus à votre tour pour choisir une créature autre que vous-même dans un rayon de 18 mètres autour de vous et qui peut vous entendre. Cette créature gagne un dé d'Inspiration bardique (d6). Une fois dans les 10 minutes suivantes, la créature peut lancer le dé et ajouter le nombre obtenu à un jet de caractéristique, d'attaque ou de sauvegarde qu'elle vient de faire. La créature peut attendre de voir le résultat de jet de caractéristique, d'attaque ou de sauvegarde avant de décider d'appliquer le dé d'Inspiration bardique, mais elle doit se décider avant que le MD ne dise si le jet est un succès ou un échec. Une fois le dé d'Inspiration bardique lancé, il est consommé. Une créature ne peut avoir qu'un seul dé d'Inspiration bardique à la fois.
    Vous pouvez utiliser cette capacité un nombre de fois égal à votre modificateur de Charisme (minimum 1). Vous regagnez vos dés d'Inspiration bardique après avoir terminé un repos long.
            """
        ],
        nombre_outils=3,
        outils='Chalemie, Cor, Cornemuse, Flûte,  Flûte de pan, Luth, Lyre, Tambour, Tympanon, Viole',
        nombre_de_competence=3,
        competences='Acrobaties, Arcanenes, Athlétisme, Discrétion, Dressage, Escamotage, Histoire, Intimidation, Investigation, Médecine, Nature, Perception, Perspicacité, Persuasion, Religion, Représentation, Survie, Tromperie',
        sort_mineur_classe=['Amis', 'Coup au but', 'Coup de tonnerre', 'Illusion mineure', 'Lumière', 'Lumières dansantes', 'Main de mage', 'Message', 'Moquerie cruelle', 'Prestidigitation', 'Protection contre les armes', 'Réparation'],
        nombre_sort_mineur_classe=2,
        sort_niveau_un_classe=['Amitié avec les animaux', 'Barbes argentées', 'Charme-personne', 'Communication avec les animaux', 'Compréhension des langues', 'Déguisement', 'Détection de la magie', 'Feuille morte', 'Fléau', 'Fou rire de Tasha', 'Grande foulée', 'Héroïsme', 'Identification', 'Image silencieuse', 'Lueurs féeriques', 'Mot de guérison', 'Murmures dissonants', 'Secousse sismique', 'Serviteur invisible', 'Soins', 'Sommeil', 'Texte illusoire', 'Vague tonnante'],
        nombre_sort_niveau_un_classe=4,
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Une rapière', 'Un luth', 'Armure de cuir', 'Une dague', 'Sac de diplomate'],
               'Pack (b)': ['Un instrument de musique au choix', 'Une arme courante au choix', 'Armure de cuir', 'Une dague', 'Sac d\'artiste']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur de Charisme',
        modificateur_attaque_sort='bonus de maîtrise + modificateur de Charisme',
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Dextérité, Charisme',
        pv=8
    ),
    'Clerc': Classe(
        nom='Clerc',
        description='Les bras et les yeux levés en direction du soleil, une prière sur les lèvres, un elfe commence à briller d\'une lumière intérieure qui s\'en va guérir ses compagnons usés par le combat. Les clercs combinent la magie utile de guérison et d\'inspiration de leurs alliés avec des sorts néfastes ou gênants pour les adversaires.',
        details=[
            'DV. 1d8',
            'Armures. armures légères et intermédiaires, boucliers',
            'Armes. armes courantes',
            'Jets de sauvegarde. Sagesse, Charisme',
            'Choix de 2 compétences parmi Histoire, Intuition, Médecine, Persuasion et Religion'
        ],
        capacites=[
            """
Préparer et lancer des sorts : Pour lancer un de ces sorts, vous devez dépenser un emplacement du niveau du sort ou supérieur. Vous regagnez tous les emplacements de sorts dépensés lorsque vous terminez un repos long. Vous pouvez lancez deux sorts de niveaux 1 par repos long. Vous devez préparer la liste des sorts de clerc qui vous sont disponibles pour les lancer. Pour ce faire, choisissez un nombre de sorts de clerc égal à votre modificateur de Sagesse + votre niveau de clerc (minimum un sort). Vous pouvez modifier votre liste de sorts préparés lorsque vous terminez un repos long. Préparer une nouvelle liste de sorts de clerc nécessite du temps pour prier et méditer : au moins 1 minute par niveau de sort pour chaque sort sur votre liste.
            """
        ],
        nombre_outils=0,
        outils=[],
        nombre_de_competence=2,
        competences='Histoire, Intuition, Médecine, Persuasion, Religion',
        sort_mineur_classe=['Assistance', 'Flamme sacrée', 'Glas', 'Lumière', 'Mot de radiance', 'Réparation', 'Résistance', 'Stabilisation', 'Thaumaturgie'],
        nombre_sort_mineur_classe=2,
        sort_niveau_un_classe=['Bénédiction', 'Blessure', 'Bouclier de la foi', 'Cérémonie', 'Création ou destruction d\'eau', 'Détection de la magie', 'Détection du mal et du bien', 'Détection du poison et des maladies', 'Éclair traçant ', 'Fléau', 'Injonction', 'Mot de guérison', 'Protection contre le mal et le bien', 'Purification de nourriture et d\'eau', 'Sanctuaire', 'Soins'],
        nombre_sort_niveau_un_classe="variable",
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Une masse d\'arme', 'Une armure d\'écaille', 'Une arbalète légère et 20 carreaux', 'un bouclier', 'Un symbole sacré', 'Sac  d\'ecclésiastique'],
               'Pack (b)': ['Un marteau de guerre', 'Une cotte de maille', 'Une arme courante au choix', 'un bouclier', 'un symbole sacré', 'Sac d\'explorateur']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur de Sagesse',
        modificateur_attaque_sort='bonus de maîtrise + modificateur de Sagesse',
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Sagesse, Charisme',
        pv=8
    ),
    'Druide': Classe(
        nom='Druide',
        description='Que ce soit en faisant appel aux forces élémentaires naturelles ou en imitant les créatures du monde animal, les druides sont des incarnations de la force, de la ruse, et de la colère de la nature. Ils ne se proclament pas maîtres de la nature. Ils se voient plutôt comme des extensions de la volonté indomptable de la nature.',
        details=[
            'DV. 1d8',
            'Armures. armures légères et intermédiaires, boucliers (un druide n\'utilisera pas d\'armure ou de bouclier en métal)',
            'Armes. gourdin, dague, fléchette, javeline, masse d\'armes, bâton, cimeterre, fronde, serpe, lance',
            'Jets de sauvegarde. Sagesse, Intelligence',
            'Choix de 2 compétences parmi Arcanes, Dressage, Intuition, Médecine, Nature, Perception, Survie et Religion'
        ],
        capacites=[
            """
Druidique
    Vous connaissez le druidique, le langage secret des druides. Vous pouvez parler cette langue et l'utiliser pour laisser des messages secrets. Vous, et les autres personnes connaissant ce langage, remarquez automatiquement un tel message. Les autres personnages remarquent la présence du message s'ils réussissent un jet de Sagesse (Perception) DD 15 mais ne peuvent pas le déchiffrer sans utiliser la magie.

Incantation
    Puisant dans l'essence divine de la nature elle-même, vous pouvez lancer des sorts pour modeler cette essence selon votre volonté. Vous devez préparer la liste des sorts de druide qui vous sont disponibles pour les lancer. Pour ce faire, choisissez un nombre de sorts de druide égal à votre modificateur de Sagesse + votre niveau de druide.
            """
        ],
        nombre_outils=1,
        outils=['Kit d\'herboriste'],
        nombre_de_competence=2,
        competences='Arcanes, Dressage, Intuition, Médecine, Nature, Perception, Survie, Religion',
        sort_mineur_classe=['Assistance, Bouffée de poison, Contrôle des flammes, Coup de tonnerre, Druidisme, Embrasement, Façonnage de l\'eau, Façonnage de la terre, Flammes, Fouet épineux, Gelure, Gourdin magique, Infestation, Pierre magique, Réparation, Résistance, Saute de vent, Sauvagerie primitive'],
        nombre_sort_mineur_classe=2,
        sort_niveau_un_classe=['Absorption des éléments, Amitié avec les animaux, Baies nourricières, Charme-personne, Collet, Communication avec les animaux, Couteau de glace, Création ou destruction d\'eau, Détection de la magie, Détection du poison et des maladies, Enchevêtrement, Grande foulée, Lien avec une bête, Lueurs féeriques, Mot de guérison, Soins, Nappe de brouillard, Purification de nourriture et d\'eau, Saut, Secousse sismique, Vague tonnante, Vents contraires'],
        nombre_sort_niveau_un_classe="variable",
        styles_de_combat=[],
        argent_classe='2d4 x 10',
        packs={'Pack (a)': ['Un bouclier de bois', 'Un cimeterre', 'Une armure de cuir', 'Un focaliseur druidique',  'Sac  d\'explorateur'],
               'Pack (b)': ['Une arme courante au choix', 'Une arme courante de corps à corps au choix', 'Une armure de cuir', 'Un focaliseur druidique',  'Sac  d\'explorateur']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur de Sagesse',
        modificateur_attaque_sort='bonus de maîtrise + modificateur de Sagesse',
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Intelligence, Sagesse',
        pv=8
    ),
    'Ensorceleur': Classe(
        nom='Ensorceleur',
        description='Les ensorceleurs sont les porteurs d’une magie innée qui prend sa source dans un lignage exotique, une quelconque influence d\'Outremonde ou une exposition à une force cosmique inouïe. On ne peut pas étudier la sorcellerie comme on apprend un langage, pas plus qu’on ne peut apprendre à vivre une vie de légende. Personne ne choisit la sorcellerie ; le pouvoir choisit l’ensorceleur.',
        details=[
            'DV. 1d6',
            'Armures. aucune',
            'Armes. dague, fléchette, fronde, bâton, arbalète légère',
            'Jets de sauvegarde. Constitution, Charisme',
            'Choix de 2 compétences parmi Arcanes, Intimidation, Intuition, Persuasion, Religion et Tromperie'
        ],
        capacites=[
            """
Incantation
    Un événement dans votre passé, ou dans la vie d'un parent ou un ancêtre, vous a laissé une marque indélébile, en vous insufflant la magie des arcanes. Cette source de magie, quelle que soit son origine, alimente vos sorts.
Origine magique : Différents ensorceleurs se réclameront de différents lignages en ce qui concerne l'origine de leur magie innée. Mais si de nombreuses variantes existent, la plupart de ces origines se répartissent en deux grandes catégories : la lignée draconique et la magie sauvage. Cliquez sur le bouton lié à l'origine pour en apprendre plus dessus. 
         """
        ],
        nombre_outils=0,
        outils=[],
        nombre_de_competence=2,
        competences='Arcanes, Intimidation, Intuition, Persuasion, Tromperie, Religion',
        sort_mineur_classe=['Amis', 'Aspersion d\'acide', 'Bouffée de poison', 'Contact glacial', 'Contôle des flammes', 'Coup au but', 'Façonnage de l\'eau', 'Façonnage de la terre', 'Ferrage foudroyant', 'Illusion mineure', 'Gelure', 'Lame aux flammes vertes', 'Infestation', 'Lame retentissante', 'Lumière', 'Lumières dansantes', 'Main de mage', 'Message', 'Piqûre mentale', 'Poigne électrique', 'Prestidigitation', 'Protection contre les armes', 'Rayon de givre', 'Réparation', 'Saute de vente', 'Trait de feu'],
        nombre_sort_mineur_classe=4,
        sort_niveau_un_classe=['Absorption des éléments', 'Armure de mage', 'Barbes argentées', 'Bouclier', 'Catapulte', 'Charme-personne', 'Compréhension des langues', 'Couleurs dansantes', 'Couteau de glace ', 'Déguisement', 'Détection de la magie', 'Éclair de chaos', 'Feuille morte', 'Image silencieuse', 'Mains brûlantes', 'Mixture caustique de Tasha', 'Nappe de brouillard', 'Orbe chromatique', 'Projectile élémentaire', 'Projectile magique', 'Rayon empoisonné', 'Repli expéditif', 'Saut', 'Secousse sismique', 'Simulacre de vie', 'Sommeil', 'Trait ensorcelé', 'Vague tonnante'],
        nombre_sort_niveau_un_classe=2,
        styles_de_combat=[],
        argent_classe='3d4 x 10',
        packs={'Pack (a)': ['Une arbalète légère et 20 carreaux', 'Une sacoche à composantes', 'Deux dagues', 'Sac  d\'explorateur'],
               'Pack (b)': ['Une arme courante au choix', 'Un focaliseur arcanique', 'Deux dagues',  'Sac  d\'exploration souterraine']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur de Charisme',
        modificateur_attaque_sort='bonus de maîtrise + modificateur de Charisme',
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Constitution, Charisme',
        pv=6
    ),
    'Guerrier': Classe(
        nom='Guerrier',
        description='Des combattants experts avec une variété d’armures et d’armes.',
        details=[
            'DV. 1d10',
            'Armures. Armures légère, armures intermédiaires, armures lourdes, boucliers',
            'Armes. Armes courantes, armes de guerre',
            'Jets de sauvegarde. Force, Constitution',
            'Choix de 2 compétences parmi Acrobaties, Athlétisme, Dressage, Histoire, Intimidation, Intuition, Perception, Survie'
        ],
        capacites=[
            """
Second souffle: Une fois par repos court ou long, vous pouvez utiliser une action bonus pour regagner un nombre de points de vie égal à 1d10 + votre niveau.

Style de combat: Vous choisissez un style de combat qui vous accorde des avantages en combat.            
            """
        ],
        nombre_outils=1,
        outils=['Matériel de forgeron', 'Matériel de brasseur'],
        nombre_de_competence=2,
        competences='Acrobaties, Athlétisme, Dressage, Histoire, Intimidation, Intuition, Perception, Survie',
        sort_mineur_classe=[],
        nombre_sort_mineur_classe=0,
        sort_niveau_un_classe=[],
        nombre_sort_niveau_un_classe=0,
        styles_de_combat=styles_de_combat,
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Cotte de mailles', 'Bouclier', '1 arme de guerre', 'Arbalète légère', 'Sac d\'exploration souterraine'],
               'Pack (b)': ['Armure de cuir', '2 armes de guerre', '2 hachettes', 'Arc long', 'Sac d\'explorateur']},
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Force, Constitution',
        pv=10
    ),
    'Magicien': Classe(
        nom='Magicien',
        description='Des lanceurs de sorts étudient les arcanes magiques et lancent des sorts puissants.',
        details=[
            'DV. 1d6',
            'Armes. Dague, fléchette, fronde, bâton, arbalète légère',
            'Jets de sauvegarde. Intelligence, Sagesse',
            'Choix de 2 compétences parmi Arcanes, Histoire, Intuition, Investigation, Médecine et Religion'
        ],
        capacites=[
            """
Sorts mineurs : Au niveau 1, vous connaissez trois sorts mineurs de magicien de votre choix. Vous apprendrez des sorts mineurs supplémentaires de votre choix aux niveaux supérieurs.
Grimoire : Au niveau 1, vous possédez un grimoire qui contient six sorts de magicien de niveau 1 de votre choix. Votre grimoire est le gardien des sorts de magicien que vous connaissez, à exception des sorts mineurs qui sont eux fixés dans votre esprit.

Préparer et lancer des sorts : Pour lancer un de ces sorts, vous devez dépenser un emplacement du niveau du sort ou supérieur, 2 aux niveau 1. Vous regagnez tous les emplacements de sorts dépensés lorsque vous terminez un repos long.
Vous devez préparer la liste des sorts de magicien qui vous sont disponibles pour les lancer. Pour ce faire, choisissez dans votre grimoire un nombre de sorts de magicien égal à votre modificateur d'Intelligence + votre niveau de magicien (minimum un sort).

Restauration arcanique : Vous avez appris à regagner une partie de votre énergie magique par l'étude de votre grimoire. Une fois par jour, lorsque vous terminez un repos court, vous pouvez choisir des emplacements de sorts dépensés à récupérer.
            """
        ],
        nombre_outils=0,
        outils=[],
        nombre_de_competence=2,
        competences='Arcanes, Histoire, Intuition, Investigation, Médecine, Religion',
        sort_mineur_classe=['Amis, Aspersion d\'acide, Bouffée de poison, Contact glacial, Contôle des flammes, Coup au but, Façonnage de l\'eau, Façonnage de la terre, Ferrage foudroyant, Illusion mineure, Gelure, Lame aux flammes vertes, Infestation, Lame retentissante, Lumière, Lumières dansantes, Main de mage, Message, Piqûre mentale, Poigne électrique, Prestidigitation, Protection contre les armes, Rayon de givre, Réparation, Saute de vente, Trait de feu'],
        nombre_sort_mineur_classe=3,
        sort_niveau_un_classe=['Absorption des éléments, Alarme, Appel de familier, Armure de mage, Barbes argentées, Bouclier, Compréhension des langues, Couleurs dansantes, Couteau de glace, Déguisement, Détection de la magie, Disque flottant de Tenser, Feuille morte, Fou rire de Tasha, Frayeur, Graisse, Grande foulée, Identification, Image silencieuse, Mains brûlantes, Orbe chromatique, Projectile magique, Protection contre le mal et le bien, Rayon empoisonné, Repli expéditif, Saut, Secousse sismique, Serviteur invisible, Sommeil, Texte illusoire, Trait ensorcelé, Vague tonnante, Vents contraires, Éclair de chaos, Mixture caustique de Tasha, Nappe de brouillard, Projectile élémentaire, Simulacre de vie'],
        nombre_sort_niveau_un_classe=6,
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Bâton', 'Grimoire', 'Sacoche à composantes', 'Sac d\'érudit'],
               'Pack (b)': ['Dague', 'Grimoire', 'Focalisateur arcanique', 'Sac d\'explorateur']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur d\'Intelligence',
        modificateur_attaque_sort='bonus de maîtrise + modificateur d\'Intelligence',        
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Intelligence, Sagesse',
        pv=6
    ),
    'Moine': Classe(
        nom='Moine',
        description='Quelle que soit leur discipline, les moines sont unis dans leur aptitude à exploiter magiquement l\'énergie qui parcourt leur corps. Canalisée en une remarquable démonstration de prouesse martiale ou en une subtile augmentation de capacité défensive et de vitesse, cette énergie imprègne tout ce que fait le moine.',
        details=[
            'DV. 1d8',
            'Armes. armes courantes, épée courte',
            'Jets de sauvegarde. Intelligence, Sagesse',
            'Choix de 2 compétences parmi Acrobaties, Athlétisme, Discrétion, Histoire, Intuition et Religion'
        ],
        capacites=[
            """
Défense sans armure : Tant que vous n'êtes équipé ni d'une armure, ni d'un bouclier, votre CA est égale à 10 + votre modificateur de Dextérité + votre modificateur de Sagesse.

Arts martiaux : Votre pratique des arts martiaux vous donne la maîtrise des styles de combat utilisant les attaques à mains nues et les armes de moine, qui sont l'épée courte et toutes les armes de corps à corps courantes qui n'ont ni la propriété à deux mains, ni la propriété lourde. Vous gagnez les avantages suivants lorsque vous êtes à mains nues ou ne maniez que des armes de moine et que vous n'êtes équipé ni d'armure ni de bouclier :
    Vous pouvez utiliser la Dextérité à la place de la Force aux jets d'attaque et de dégâts de vos attaques à mains nues et avec des armes de moine.
    Vous pouvez lancer un d4 à la place des dégâts normaux de votre attaque à mains nues ou de vos armes de moine. Ce dé change lorsque vous gagnez des niveaux de moine.
    Lorsque vous utilisez l'action Attaquer avec une attaque à mains nues ou une arme de moine au cours de votre tour, vous pouvez effectuer une attaque à mains nues au prix d'une action bonus. Par exemple, si vous prenez l'action Attaque et attaquez avec un bâton, vous pouvez également effectuer une attaque à mains nues avec votre action bonus, à condition que vous n'ayez pas déjà utilisé votre action bonus pour ce tour.'
            """
        ],
        nombre_outils=1,
        outils='Chalemie, Cor, Cornemuse, Flûte,  Flûte de pan, Luth, Lyre, Tambour, Tympanon, Viole, Matériel d\'alchimie, Matériel de brasseur, Matériel de calligraphe, Matériel de peintre, Matériel de bijoutier, Matériel de bricoleur, Matériel de cuisinier, Matériel de tisserand, Matériel de tanneur, Matériel de souffleur de verre, Matériel de potier, Matériel de menuisier, Matériel de bricoleur, Matériel de cartographe, Matériel de charpentier, Matériel de cordonnier, Matériel de forgeron, Matériel de maçon,',
        nombre_de_competence=2,
        competences='Acrobaties, Athlétisme, Discrétion, Histoire, Intuition, Religion',
        sort_mineur_classe=[],
        nombre_sort_mineur_classe=0,
        sort_niveau_un_classe=[],
        nombre_sort_niveau_un_classe=0,
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Une épée courte', '10 fléchettes',  'Sac d\'exploration souterraine'],
               'Pack (b)': ['Une arme courante au choix', '10 fléchettes',  'Sac  d\'explorateur']},      
        ca='10 + modificateur de Dextérité + modificateur de Sagesse',
        jets_de_sauvegarde='Force, Dextérité',
        pv=8
    ),
    'Occultiste': Classe(
        nom='Occultiste',
        description='Les occultistes sont des chercheurs de la connaissance dissimulée dans la trame du multivers. Par l’entremise de pactes conclus avec de mystérieux êtres dotés de pouvoirs surnaturels, les occultistes libèrent des effets magiques à la fois subtiles et spectaculaires. Tirant parti du savoir ancien d’êtres tels que les nobles fées, les démons, les diables, les sorcières et les entités extraplanaires du Royaume lointain, les occultistes assemblent les secrets arcaniques pour renforcer leur propre puissance.',
        details=[
            'DV. 1d8',
            'Armures. Armures légères',
            'Armes. Armes courantes',
            'Jets de sauvegarde. Sagesse, Charisme',
            'Choix de 2 compétences parmi Arcanes, Histoire, Intimidation, Investigation, Nature, Tromperie et Religion'
        ],
        capacites=[
            """
Patron d'Outremonde : Vous avez conclu un marché avec un être d'Outremonde de votre choix : l'Archifée, le Fiélon ou le Grand Ancien.
Manifestations occultes : Fragments d’un savoir interdit vous conférant une capacité magique permanente.
Magie de pacte : Pour lancer un sort d'occultiste de niveau 1 ou supérieur, vous devez dépenser un emplacement. Vous regagnez tous vos emplacements de sorts dépensés lorsque vous terminez un repos court ou long.
            """
        ],
        nombre_outils=0,
        outils=[],
        nombre_de_competence=2,
        competences='Arcanes, Histoire, Intuition, Investigation, Médecine, Religion',
        sort_mineur_classe=['Amis, Aspersion d\'acide, Bouffée de poison, Contact glacial, Contôle des flammes, Coup au but, Façonnage de l\'eau, Façonnage de la terre, Ferrage foudroyant, Illusion mineure, Gelure, Lame aux flammes vertes, Infestation, Lame retentissante, Lumière, Lumières dansantes, Main de mage, Message, Piqûre mentale, Poigne électrique, Prestidigitation, Protection contre les armes, Rayon de givre, Réparation, Saute de vente, Trait de feu'],
        nombre_sort_mineur_classe=3,
        sort_niveau_un_classe=['Absorption des éléments, Alarme, Appel de familier, Armure de mage, Barbes argentées, Bouclier, Compréhension des langues, Couleurs dansantes, Couteau de glace, Déguisement, Détection de la magie, Disque flottant de Tenser, Feuille morte, Fou rire de Tasha, Frayeur, Graisse, Grande foulée, Identification, Image silencieuse, Mains brûlantes, Orbe chromatique, Projectile magique, Protection contre le mal et le bien, Rayon empoisonné, Repli expéditif, Saut, Secousse sismique, Serviteur invisible, Sommeil, Texte illusoire, Trait ensorcelé, Vague tonnante, Vents contraires, Éclair de chaos, Mixture caustique de Tasha, Nappe de brouillard, Projectile élémentaire, Simulacre de vie'],
        nombre_sort_niveau_un_classe=6,
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Bâton', 'Grimoire', 'Sacoche à composantes', 'Sac d\'érudit'],
               'Pack (b)': ['Dague', 'Grimoire', 'Focalisateur arcanique', 'Sac d\'explorateur']},
        dd_sauvegarde_sorts='8 + bonus de maîtrise + modificateur d\'Intelligence',
        modificateur_attaque_sort='bonus de maîtrise + modificateur d\'Intelligence',        
        ca='10 + modificateur de Dextérité',
        jets_de_sauvegarde='Intelligence, Sagesse',
        pv=6
    ),
    'Roublard': Classe(
        nom='Roublard',
        description='Des spécialistes des techniques furtives et des attaques sournoises.',
        details=[
            'DV. 1d8',
            'Armures. Armures légères',
            'Armes. Armes courantes, arbalète de poing, épée courte, épée longue, rapière, arc court',
            'Outils. Outils de voleur',
            'Jets de sauvegarde. Dextérité, Intelligence',
            'Choix de 4 compétences parmi Acrobaties, Athlétisme, Discrétion, Escamotage, Intimidation, Intuition, Investigation, Perception, Persuasion, Représentation, Tromperie'
        ],
        capacites=[
            'Expertise: Vous doublez votre bonus de compétence pour deux compétences ou outils de votre choix.',
            'Attaque sournoise: Une fois par tour, vous pouvez infliger des dégâts supplémentaires à une cible que vous attaquez avec une arme de finesse ou à distance si vous avez l’avantage à l\'attaque ou si un allié est à portée de mêlée de la cible.',
            'Jargon des voleurs: Vous pouvez comprendre et parler le jargon des voleurs, un langage secret utilisé par les criminels.'
        ],
        nombre_outils=1,
        outils=['Outils de voleur'],
        nombre_de_competence=4,
        competences='Acrobaties, Athlétisme, Discrétion, Escamotage, Intimidation, Intuition, Investigation, Perception, Persuasion, Représentation, Tromperie',
        sort_mineur_classe=[],
        nombre_sort_mineur_classe=0,
        sort_niveau_un_classe=[],
        nombre_sort_niveau_un_classe=0,
        styles_de_combat=[],
        argent_classe='4d4 x 10',
        packs={'Pack (a)': ['Armure de cuir', 'Rapière', 'Arc court', '2 dagues', 'Outils de voleur', 'Sac de cambrioleur'],
               'Pack (b)': ['Armure de cuir', '2 épées courtes', '2 dagues', 'Outils de voleur', 'Sac d\'exploration souterraine']}
    )
}

races = {
    'Humain': Race(
        nom='Humain',
        description='Les Humains sont polyvalents et adaptables, avec une grande capacité à s’intégrer dans diverses cultures.',
        details=[
            'Augmentation de caractéristiques. Force +1, Dextérité +1, Constitution +1, Intelligence +1, Sagesse +1, Charisme +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Langues. Commun, une langue de votre choix'
        ],
        bonus={'Force': 1, 'Dextérité': 1, 'Constitution': 1, 'Intelligence': 1, 'Sagesse': 1, 'Charisme': 1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Une langue supplémentaire au choix'],
        nombre_de_langue=1,
        langue_parlee_race='Commun',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Elfe des bois': Race(
        nom='Elfe des bois',
        description='Les Elfes sont des êtres agiles et gracieux, dotés d’une longue durée de vie et de sens aiguisés. En tant qu\'elfe des bois, vous avez des sens aiguisés et une forte intuition.',
        details=[
            'Augmentation de caractéristiques. Dextérité +2, Sagesse +1',
            'Taille. M',
            'Vitesse. 10,5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique',
            'Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Entraînement aux armes elfiques',
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
        choix_bonus=0,
        competences=['Perception'],
        nombre_competences_race=1,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Elfique'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Elfique',
        armes_maitrisees_race=['Épée longue', 'Épée courte', 'Arc long', 'Arc court'],
        armures_maitrisees_race=[]
    ),
    'Elfe noir (drow)': Race(
        nom='Elfe noir',
        description='Les Elfes sont des êtres agiles et gracieux, dotés d’une longue durée de vie et de sens aiguisés. En tant que drow, vous êtes imprégné par la magie de l\'Outreterre, un royaume souterrain fait de merveilles et d\'horreurs que l\'on voit rarement à la surface.',
        details=[
            'Augmentation de caractéristiques. Dextérité +2, Charisme +1',
            'Taille. M',
            'Vitesse. 10,5 m/round',
            'Vision. Vision dans le noir (36 m)',
            'Langues. Commun, Elfique',
            'Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Magie drow. Vous connaissez le sort mineur lumières dansantes. Lorsque vous atteignez le niveau 3, vous pouvez lancer le sort lueurs féeriques une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Lorsque vous atteignez le niveau 5, vous pouvez lancer le sort ténèbres une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Le Charisme est votre caractéristique d\'incantation pour ces sorts.',
            'Entraînement aux armes elfiques',
            'Entraînement aux armes drows.'
            'Sensibilité au soleil. Vous avez un désavantage aux jets d\'attaque et aux jets de Sagesse (Perception) basés sur ​​la vue quand vous, la cible de l\'attaque ou ce que vous essayez de détecter est exposé à la lumière du soleil.'
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
        choix_bonus=0,
        competences=['Perception'],
        nombre_competences_race=1,
        outils=[],
        sort_race=[next(sort for sort in sort_mineur if sort["nom"] == "Lumières dansantes")],
        nombre_sort_race=1,
        langues=['Commun', 'Elfique'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Elfique',
        armes_maitrisees_race=['Épée longue', 'Épée courte', 'Arc long', 'Arc court'],
        armures_maitrisees_race=[]
    ),
    'Haut-elfe': Race(
        nom='Haut-elfe',
        description='Les Elfes sont des êtres agiles et gracieux, dotés d’une longue durée de vie et de sens aiguisés. En tant que Haut-elfe, vous avez l\esprit vif et connaissez les rudiments de la magie.',
        details=[
            'Augmentation de caractéristiques. Dextérité +2, Intelligence +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique, une langue de votre choix',
            'Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        bonus={'Dextérité': 2, 'Intelligence': 1},
        choix_bonus=0,
        competences=['Perception'],
        nombre_competences_race=1,
        outils=[],
        sort_race=sort_mineur,
        nombre_sort_race=1,
        langues=['Commun', 'Elfique', 'Une langue supplémentaire au choix'],
        nombre_de_langue=1,
        langue_parlee_race='Commun, Elfique',
        armes_maitrisees_race=['Épée longue', 'Épée courte', 'Arc long', 'Arc court'],
        armures_maitrisees_race=[]
    ),
    'Nain des montagnes': Race(
        nom='Nain des montagnes',
        description='Robustes et endurants, les Nains sont des artisans habiles avec une grande résistance. En tant que nain des montagnes, vous êtes fort et robuste, et habitué à une vie difficile en terrain accidenté.',
        details=[
            'Augmentation de caractéristiques. Force +2, Constitution +2',
            'Taille. M',
            'Vitesse. 7.5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Nain',
            'Résistance naine. AV aux JdS vs poison',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre. Bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre',
            'Formation au port des armures naines'
        ],
        bonus={'Force': 2, 'Constitution': 2},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=['Matériel de forgeron', 'Matériel de brasseur', 'Matériel de maçon'],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Nain'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Nain',
        armes_maitrisees_race=['Hachette', 'Hache d\'arme', 'Marteau léger', 'Marteau de guerre'],
        armures_maitrisees_race=['Armures légères', 'Arumures intermédiaires']
    ),
    'Halfelin pied-léger': Race(
        nom='Halfelin pied-léger',
        description='Les halfelins sont des gens affables, chaleureux et joyeux. Ils chérissent les liens de famille et l\'amitié ainsi que le confort du foyer, n’entretenant que peu de rêves d\'or et de gloire. Les plus téméraires parmi eux s\'aventurent généralement dans le monde pour des raisons liées à la communauté, l’amitié, l’envie de voyager ou la curiosité. En tant que halfelin pied-léger, vous pouvez facilement vous cacher, en utilisant même d\'autres personnes comme abri. Vous avez tendance à être affable et à bien vous entendre avec les autres.',
        details=[
            'Augmentation de caractéristiques. Dextérité +2, Charisme +1',
            'Taille. P',
            'Vitesse. 7.5 m/round',
            'Langues. Commun, Halfelin',
            'Chanceux. Lorsque vous obtenez un 1 au dé d\'un jet d\'attaque, de caractéristique ou de sauvegarde, vous pouvez relancer le dé et devez alors utiliser ce nouveau résultat.',
            'Brave. Vous avez un avantage aux jets de sauvegarde pour ne pas être effrayé.',
            'Agilité halfeline. Vous pouvez passer dans l\'espace de toute créature d\'une taille supérieure à la vôtre.'
            'Discrétion naturelle. Vous pouvez tenter de vous cacher si vous vous trouvez derrière une créature d\'une taille supérieure à la vôtre.)'
        ],
        bonus={'Dextérité': 2, 'Charisme':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Halfelin'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Halfelin',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Halfelin robuste': Race(
        nom='Halfelin robuste',
        description='Les halfelins sont des gens affables, chaleureux et joyeux. Ils chérissent les liens de famille et l\'amitié ainsi que le confort du foyer, n’entretenant que peu de rêves d\'or et de gloire. Les plus téméraires parmi eux s\'aventurent généralement dans le monde pour des raisons liées à la communauté, l\’amitié, l\’envie de voyager ou la curiosité. En tant que halfelin robuste, vous êtes plus costaud que la moyenne et possédez une certaine résistance au poison. Certains disent que les robustes ont du sang nain.',
        details=[
            'Augmentation de caractéristiques. Dextérité +2, Constitution +1',
            'Taille. P',
            'Vitesse. 7.5 m/round',
            'Langues. Commun, Halfelin',
            'Chanceux. Lorsque vous obtenez un 1 au dé d\'un jet d\'attaque, de caractéristique ou de sauvegarde, vous pouvez relancer le dé et devez alors utiliser ce nouveau résultat.',
            'Brave. Vous avez un avantage aux jets de sauvegarde pour ne pas être effrayé.',
            'Agilité halfeline. Vous pouvez passer dans l\'espace de toute créature d\'une taille supérieure à la vôtre.'
            'Résistance des robustes. Vous obtenez un avantage aux jets de sauvegarde contre le poison et la résistance contre les dégâts de poison.'
        ],
        bonus={'Dextérité': 2, 'Constitution':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Halfelin'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Halfelin',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Nain des collines': Race(
        nom='Nain des collines',
        description='Robustes et endurants, les nains sont des artisans habiles avec une grande résistance. En tant que nain des collines, vous avez les sens aiguisés, une forte intuition et une résistance remarquable.',
        details=[
            'Augmentation de caractéristiques. Constitution +2, Sagesse +1',
            'Taille. M',
            'Vitesse. 7.5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Nain',
            'Résistance naine. AV aux JdS vs poison',
            'Entraînement aux armes naines',
            'Maîtrise des outils nains',
            'Connaissance de la pierre. Bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre',
            'Ténacité naine. Votre maximum de points de vie augmente de 1 à chaque niveau.'
        ],
        bonus={'Constitution': 2, 'Sagesse':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Nain'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Nain',
        armes_maitrisees_race=['Hachette', 'Hache d\'arme', 'Marteau léger','Marteau de guerre'],
        armures_maitrisees_race=[]
    ),
    'Demi-elfe': Race(
        nom='Demi-elfe',
        description='Fréquentant deux mondes, mais n\'appartenant vraiment à aucun des deux, les demi-elfes combinent ce que certains disent être les meilleures qualités de leurs parents elfes et humains : la curiosité et la créativité humaine, et une ambition tempérée par des sens raffinés, l\'amour de la nature et les goûts artistiques des elfes.',
        details=[
            'Augmentation de caractéristiques. Charisme +2, Deux caractéristique au choix +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique et une langue au choix',
            'Ascendance féerique. Vous avez un avantage aux jets de sauvegarde contre les effets de charme et la magie ne peut pas vous endormir.',
            'Polyvalence.  Vous gagnez la maîtrise de deux compétences de votre choix.'
        ],
        bonus={'Charisme':2},
        choix_bonus=2,
        competences=['Acrobaties', 'Arcanes', 'Athlétisme', 'Discrétion', 'Dressage', 'Escamotage', 'Histoire', 'Intimidation', 'Investigation', 'Médecine', 'Nature', 'Perception', 'Perspicacité', 'Persuasion', 'Religion', 'Représentation', 'Survie', 'Tromperie'],
        nombre_competences_race=2,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Elfique', 'Une langue supplémentaire au choix'],
        nombre_de_langue=1,
        langue_parlee_race='Commun, Elfique',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Demi-orc': Race(
        nom='Demi-orc',
        description='Que ce soit unis sous la direction d\'un puissant occultiste ou lors de trêves après des années de conflit, les tribus orcs et humaines forment parfois des alliances, unissant leurs forces en une horde encore plus grande qui engendre la terreur dans les terres civilisées proches. Et lorsque ces alliances sont scellées par des mariages, des demi-orcs naissent.',
        details=[
            'Augmentation de caractéristiques. Force +2, Constitution +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Orc',
            'Endurance implacable. Lorsque vous tombez à 0 point de vie, mais que vous n\'êtes pas tué sur le coup, vous pouvez passer à 1 point de vie à la place. Vous devez terminer un repos long avant de pouvoir utiliser cette capacité de nouveau.',
            'Attaques sauvages. Lorsque vous réalisez un coup critique lors d\'une attaque au corps à corps avec une arme, vous pouvez lancer l\'un des dés de dégâts de l\'arme une deuxième fois et l\'ajouter aux dégâts supplémentaires du coup critique.'
        ],
        bonus={'Force': 2, 'Constitution':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Orc'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Orc',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Drakéide': Race(
        nom='Drakéide',
        description='Nés de dragons, les drakéides marchent fièrement dans un monde qui les accueille avec une incompréhension craintive. Les drakéides ressemblent beaucoup à des dragons sous forme humanoïde, bien qu\'ils leurs manquent des ailes et une queue.',
        details=[
            'Augmentation de caractéristiques. Force +2, Charisme +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Draconique',
            'Ascendance draconique. Vous avez une ascendance draconique. Choisissez un type de dragon, votre souffle et votre résistance aux dégâts sont déterminés par le type de dragon',
            'Souffle. Vous pouvez utiliser votre action pour libérer un souffle d\'énergie destructrice. Votre ascendance draconique détermine la taille, la forme et le type de dégâts de votre souffle. Lorsque vous utilisez votre souffle, toute créature dans la zone de l\'expiration doit faire un jet de sauvegarde, dont le type est déterminé par votre ascendance draconique. Le DD de ce jet de sauvegarde est égal à 8 + votre modificateur de Constitution + votre bonus de maîtrise. En cas d\'échec, la créature subit 2d6 dégâts, ou la moitié de ces dégâts en cas de réussite. Les dégâts augmentent à 3d6 au niveau 6, 4d6 au niveau 11, et 5d6 au niveau 16. Après avoir utilisé votre souffle, vous devez terminer un repos court ou long pour pouvoir l\'utiliser à nouveau.'
            'Résistance de dégâts. Vous obtenez la résistance au type de dégâts associé à votre ascendance draconique.'
        ],
        bonus={'Force': 2, 'Charisme':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Draconique'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Draconique',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Gnome des forêts': Race(
        nom='Gnome des forêts',
        description='L\'énergie et l’enthousiasme des gnomes pour la vie transparaît au travers de chaque pouce de la surface de son petit corps. Les gnomes des forêts se réunissent dans des communautés cachées au sein des forêts, souvent loin des routes et des chemins de la civilisation.',
        details=[
            'Augmentation de caractéristiques. Intelligence +2, Dextérité +1',
            'Taille. P',
            'Vitesse. 7,5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Gnome',
            'Ruse gnome. Vous avez un avantage aux jets de sauvegarde d\'Intelligence, de Sagesse et de Charisme contre la magie.',
            'Illusionniste-né. Vous connaissez le sort mineur illusion mineure. L\'Intelligence est votre caractéristique d\'incantation pour ce sort.'
            'Communication avec les petits animaux. À l\'aide de sons et de gestes, vous pouvez communiquer des idées simples à des bêtes de taille P ou plus petite. Les gnomes des forêts aiment les animaux et traitent de manière bienveillante comme un animal domestique tout animal qu\'ils peuvent trouver (écureuils, blaireaux, lapins, taupes, picidés, etc.).'
        ],
        bonus={'Intelligence': 2, 'Dextérité':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[next(sort for sort in sort_mineur if sort["nom"] == "Illusion mineure")],
        nombre_sort_race=1,
        langues=['Commun', 'Gnome'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Gnome',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Gnome des roches': Race(
        nom='Gnome des roches',
        description='L\'énergie et l’enthousiasme des gnomes pour la vie transparaît au travers de chaque pouce de la surface de son petit corps. Les gnomes des roches établissent leurs communautés dans les collines et les montagnes, là où ils peuvent avoir accès aux matériaux dont ils ont besoin pour construire et bricoler. souvent loin des routes et des chemins de la civilisation.',
        details=[
            'Augmentation de caractéristiques. Intelligence +2, Constitution +1',
            'Taille. P',
            'Vitesse. 7,5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Gnome',
            'Ruse gnome. Vous avez un avantage aux jets de sauvegarde d\'Intelligence, de Sagesse et de Charisme contre la magie.',
            'Connaissance en ingénierie. Chaque fois que vous effectuez un jet d\'Intelligence (Histoire) en relation avec l\'alchimie, des objets magiques ou des dispositifs technologiques, ajoutez le double de votre bonus de maîtrise au jet, au lieu du bonus de maîtrise normal.'
            'Bricoleur. Vous maîtrisez les outils de bricoleur. En utilisant ces outils, vous pouvez passer 1 heure et dépenser pour 10 po de matériaux pour construire un mécanisme de taille TP, de CA 5 et 1 pv. Le dispositif cesse de fonctionner après 24 heures (sauf si vous passez 1 heure à le réparer) ou si vous utilisez une action pour le démonter ; à ce moment, vous pouvez récupérer les matériaux que vous avez utilisés pour le créer. Vous pouvez avoir jusqu\'à trois de ces dispositifs actifs à la fois.'
        ],
        bonus={'Intelligence': 2, 'Constitution':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=['Matériel de bricoleur'],
        sort_race=[],
        nombre_sort_race=0,
        langues=['Commun', 'Gnome'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Gnome',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
    'Tieffelin': Race(
        nom='Tieffelin',
        description='Les tieffelins descendent d\'une lignée humaine et, dans l\'absolu, ils ressemblent toujours aux humains. Malgré tout, leur héritage infernal a laissé une marque claire et indélébile sur leur apparence.',
        details=[
            'Augmentation de caractéristiques. Charisme +2, Intelligence +1',
            'Taille. M',
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Infernal',
            'Résistance infernale. Vous avez la résistance aux dégâts de feu.',
            'Ascendance infernale. Vous connaissez le sort mineur thaumaturgie. Quand vous atteignez le niveau 3, vous pouvez lancer le sort représailles infernales comme un sort de niveau 2 une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Quand vous atteignez le niveau 5, vous pouvez lancer le sort ténèbres une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Le Charisme est votre caractéristique d\'incantation pour ces sorts.'
        ],
        bonus={'Charisme': 2, 'Intelligence':1},
        choix_bonus=0,
        competences=[],
        nombre_competences_race=0,
        outils=[],
        sort_race=[next(sort for sort in sort_mineur if sort["nom"] == "Thaumaturgie")],
        nombre_sort_race=1,
        langues=['Commun', 'Infernal'],
        nombre_de_langue=0,
        langue_parlee_race='Commun, Infernal',
        armes_maitrisees_race=[],
        armures_maitrisees_race=[]
    ),
}

historiques = {
    'Criminel': Historique(
        nom='Criminel',
        description='Les criminels possèdent des compétences spécifiques pour les activités illicites.',
        details=[
            'Compétences. Choix de 2 compétences parmi Acrobaties, Discrétion, Escamotage, Intimidation, Tromperie'
        ],
        competences=['Acrobaties', 'Discrétion', 'Escamotage', 'Intimidation', 'Tromperie'],
        outils=['Dés', 'Jeu d’échecs draconiques', 'Jeu de cartes', 'Jeu des Dragons'],
        choix_outils=['Kit d\'empoisonneur', 'Kit d\'herboriste', 'Kit de contrefaçon', 'Kit de déguisement', 'Kit de navigateur', 'Outils de voleur'],
        langues=[],
        equipement="un pied-de-biche, des vêtements communs sombres avec une capuche, une bourse",
        argent_historique=15,
        capacite="Accointances avec la pègre",
        nombre_de_competence=2,
        nombre_de_langue_historique=0
    ),
    'Artisan de guilde': Historique(
        nom='Artisan de guilde',
        description='Les artisans possèdent une expertise particulière dans divers outils et matériaux.',
        details=[
            'Langues. Une langue supplémentaire au choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Artisanat, Histoire, Investigation, Médecine, Nature',
            'Outils. choix d\'un outil spécifique à une profession'
        ],
        competences=['Arcanes', 'Artisanat', 'Histoire', 'Investigation', 'Médecine', 'Nature'],
        outils=['Matériel d’alchimie', 'Matériel de brasseur', 'Matériel de calligraphe', 'Matériel de peintre', 'Matériel de bijoutier', 'Matériel de bricoleur', 'Matériel de cartographe', 'Matériel de charpentier', 'Matériel de cordonnier', 'Matériel de forgeron', 'Matériel de maçon', 'Matériel de menuisier', 'Matériel de potier', 'Matériel de souffleur de verre', 'Matériel de tanneur', 'Matériel de tisserand', 'Matériel de cuisinier'],
        choix_outils=[],
        equipement="un jeu d'outil d'artisan, une lettre de recommandation de votre guilde, des vêtements de voyage, une bourse",
        argent_historique=15,
        capacite="Membre de guilde",
        langues=['Une langue supplémentaire au choix'],
        nombre_de_competence=2,
        nombre_de_langue_historique=1
    ),
    'Acolyte': Historique(
        nom='Acolyte',
        description='Les acolytes ont une formation religieuse approfondie et des compétences dans les rituels et le culte.',
        details=[
            'Langues. Deux langues supplémentaires aux choix',
            'Compétences. Choix de 2 compétences parmi Arcanes, Histoire, Médecine, Religion'
        ],
        competences=['Arcanes', 'Histoire', 'Médecine', 'Religion'],
        outils=[],
        choix_outils=[],
        equipement="symbole sacré, un livre de prières, 5 bâtons d'encens, des habits de cérémonie, des vêtements communs, une bourse",
        argent_historique=15,
        capacite="Abri du fidèle",
        langues=['Deux langues supplémentaires au choix'],
        nombre_de_competence=2,
        nombre_de_langue_historique=2
    )
}

# Création du personnage
personnage = Personnage(classes, races, historiques)

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
onglet_sorts_connus = ttk.Frame(tabControl)

tabControl.add(onglet_classe, text='Classe')
tabControl.add(onglet_race, text='Race')
tabControl.add(onglet_historique, text='Historique')
tabControl.add(onglet_caracteristiques, text='Caractéristiques')
tabControl.add(onglet_maitrise, text='Maîtrise')
tabControl.add(onglet_options, text='Options')
tabControl.add(onglet_sorts_connus, text='Sorts connus')

tabControl.pack(expand=1, fill="both")


# Frame pour la sélection de classe
frame_classe_selection = tk.Frame(onglet_classe)
frame_classe_selection.pack(anchor="w", pady=10)

# Label pour l'instruction de la classe
classe_label = tk.Label(frame_classe_selection, text="Sélectionnez une classe", font=('Arial', 12, 'bold'))
classe_label.pack(anchor="w")

# Combobox pour sélectionner la classe
classe_combobox = ttk.Combobox(frame_classe_selection, values=list(classes.keys()), state="readonly")
classe_combobox.pack(anchor="w", pady=5)

# Label pour afficher les détails de la classe
classe_details_label = tk.Label(onglet_classe, text="", wraplength=700, justify="left")
classe_details_label.pack(anchor="w", pady=10)

# --- Ajout des labels pour les sorts et capacités de l'Occultiste ---
sort_details_label = tk.Label(onglet_classe, text="", wraplength=700, justify="left")
sort_details_label.pack(anchor="w", pady=10)

capacites_details_label = tk.Label(onglet_classe, text="", wraplength=700, justify="left")
capacites_details_label.pack(anchor="w", pady=10)

# Frame pour la sélection de race
frame_race_selection = tk.Frame(onglet_race)
frame_race_selection.pack(anchor="w", pady=10)

# Label pour l'instruction de la race
race_label = tk.Label(frame_race_selection, text="Choisissez une race:", font=('Arial', 12, 'bold'))
race_label.pack(anchor="w")

# Combobox pour sélectionner la race
race_combobox = ttk.Combobox(frame_race_selection, values=list(races.keys()), state="readonly")
race_combobox.pack(anchor="w", pady=5)

# Label pour afficher les détails de la race
race_details_label = tk.Label(onglet_race, text="", wraplength=700, justify="left")
race_details_label.pack(anchor="w", pady=10)

# Ajout du label et du combobox pour l'ascendance draconique (initialement caché)
ascendance_label = tk.Label(onglet_race, text="Choisissez votre ascendance draconique", font=('Arial', 12, 'bold'))
ascendance_combobox = ttk.Combobox(onglet_race, values=["Blanc", "Bleu", "Noir", "Rouge", "Vert", "Airain", "Argent", "Bronze", "Cuivre", "Or"], state="readonly")

ascendance_label.pack_forget()  # Caché au départ
ascendance_combobox.pack_forget()  # Caché au départ

# Frame pour la sélection de l'historique
frame_historique_selection = tk.Frame(onglet_historique)
frame_historique_selection.pack(anchor="w", pady=10)

# Label pour l'instruction de l'historique
historique_label = tk.Label(frame_historique_selection, text="Choisissez un historique:", font=('Arial', 12, 'bold'))
historique_label.pack(anchor="w")

# Combobox pour sélectionner l'historique
historique_combobox = ttk.Combobox(frame_historique_selection, values=list(historiques.keys()), state="readonly")
historique_combobox.pack(anchor="w", pady=5)

# Label pour afficher les détails de l'historique
historique_details_label = tk.Label(onglet_historique, text="", wraplength=700, justify="left")
historique_details_label.pack(anchor="w", pady=10)

# Binding des comboboxes pour mettre à jour les détails et les choix
classe_combobox.bind("<<ComboboxSelected>>", lambda event: [
    personnage.reset_selected_values(),
    personnage.reset_comboboxes(),
    afficher_details_classe(),
    personnage.update_display(),
    personnage.update_maitrise(),# Réinitialise l'onglet Maîtrise
    update_options()
])

historique_combobox.bind("<<ComboboxSelected>>", lambda event: [
    afficher_details_historique(),
    personnage.update_maitrise()  # Met à jour les compétences/outils de l'historique dans l'onglet Maîtrise
])

def on_race_selected():
    # Mettre à jour le bonus racial
    update_bonus_racial()
    # Réinitialiser les valeurs sélectionnées et les comboboxes
    personnage.reset_selected_values()
    personnage.reset_comboboxes()
    # Afficher les détails de la race
    afficher_details_race()
    # Mettre à jour les compétences et les maîtrises
    personnage.update_maitrise()
    personnage.update_display()



race_combobox.bind("<<ComboboxSelected>>", lambda event: on_race_selected())

# Widgets pour l'onglet Caractéristiques
caracteristiques_labels = []
attribut_valeur_labels = []
attribut_bonus_labels = []
attribut_valeur_finale_labels = []

titre_label = tk.Label(onglet_caracteristiques, text="Répartition des caractéristiques", font=('Arial', 12, 'bold'))
titre_label.grid(row=0, column=0, columnspan=6, pady=4)



# Fonction pour mettre à jour les bonus raciaux
def update_bonus_racial():
    race_selectionnee = race_combobox.get()
    if race_selectionnee:
        race_info = personnage.races[race_selectionnee]
        
        # Récupérer les bonus raciaux de la race sélectionnée
        bonus = race_info.bonus

        # Mettre à jour les labels des bonus raciaux pour chaque attribut
        for i, attribut in enumerate(attributs_list):
            bonus_racial = bonus.get(attribut, 0)
            if bonus_racial != 0:
                # Affiche un "+" devant les bonus positifs
                attribut_bonus_labels[i].config(text=f"+{bonus_racial}" if bonus_racial > 0 else str(bonus_racial))
            else:
                attribut_bonus_labels[i].config(text="0")  # Met "0" si pas de bonus

        # Gestion des bonus supplémentaires pour certaines races (ex: Demi-elfe)
        if race_info.choix_bonus > 0:
            # Si la race a un choix de bonus supplémentaire, afficher le cadre correspondant
            choix_frame.grid(row=21, column=0, columnspan=6, pady=10)
        else:
            # Cacher le cadre des bonus supplémentaires s'il n'y en a pas
            choix_frame.grid_remove()

        # Mettre à jour les valeurs finales des caractéristiques
        update_valeur_finale()
        

# Liste des attributs restreints pour les choix bonus
choix_possibles = ["Force", "Dextérité", "Constitution", "Intelligence", "Sagesse"]

# Fonction pour mettre à jour les choix possibles dans les combobox de bonus
def update_choix_bonus():
    # Récupérer les valeurs sélectionnées dans chaque combobox
    choix_1 = choix_bonus_1_combobox.get()
    choix_2 = choix_bonus_2_combobox.get()

    # Exclure les choix déjà faits de la liste des options restantes
    valeurs_disponibles_1 = [attr for attr in choix_possibles if attr != choix_2]  # Exclure le choix 2 du combobox 1
    valeurs_disponibles_2 = [attr for attr in choix_possibles if attr != choix_1]  # Exclure le choix 1 du combobox 2

    # Mettre à jour les options disponibles dans les deux combobox
    choix_bonus_1_combobox['values'] = valeurs_disponibles_1
    choix_bonus_2_combobox['values'] = valeurs_disponibles_2

    # Si un choix actuel n'est plus dans les options disponibles, le réinitialiser
    if choix_1 not in valeurs_disponibles_1:
        choix_bonus_1_combobox.set('')
    if choix_2 not in valeurs_disponibles_2:
        choix_bonus_2_combobox.set('')


# Fonction pour gérer la sélection des bonus supplémentaires (spécifique au Demi-elfe)
def update_custom_bonus_racial():
    race_selectionnee = race_combobox.get()

    if race_selectionnee == "Demi-elfe":  # Vérifier que la race sélectionnée est bien Demi-elfe
        race_info = personnage.races[race_selectionnee]
        bonus = race_info.bonus.copy()  # Copier le bonus racial de base

        # Ajouter les bonus personnalisés choisis par l'utilisateur
        custom_bonus_1 = choix_bonus_1_combobox.get()
        custom_bonus_2 = choix_bonus_2_combobox.get()

        if custom_bonus_1:
            bonus[custom_bonus_1] = bonus.get(custom_bonus_1, 0) + 1
        if custom_bonus_2:
            bonus[custom_bonus_2] = bonus.get(custom_bonus_2, 0) + 1

        # Mettre à jour les labels pour afficher les bonus raciaux (incluant les bonus personnalisés)
        for i, attribut in enumerate(attributs_list):
            bonus_racial = bonus.get(attribut, 0)
            attribut_bonus_labels[i].config(text=f"+{bonus_racial}" if bonus_racial > 0 else "0")

        # Mettre à jour les valeurs finales des caractéristiques
        personnage.update_display()  # Appeler la méthode de mise à jour de l'affichage des valeurs

    # Mettre à jour les combobox après sélection
    update_choix_bonus()
    
    

# Appel initial pour afficher les valeurs finales correctes
def update_valeur_finale():
    for i, attribut in enumerate(attributs_list):
        try:
            valeur_brute = int(attribut_valeur_labels[i].cget("text"))
        except ValueError:
            valeur_brute = 0  # Valeur par défaut si le texte est vide

        bonus_racial = int(attribut_bonus_labels[i].cget("text")) if attribut_bonus_labels[i].cget("text") else 0

        valeur_finale = valeur_brute + bonus_racial
        attribut_valeur_finale_labels[i].config(text=str(valeur_finale))

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

# Ajout des boutons et labels pour chaque attribut
for i, attribut in enumerate(attributs_list):
    tk.Label(onglet_caracteristiques, text=attribut).grid(row=2+i, column=0, padx=5, sticky="w")
    tk.Button(onglet_caracteristiques, text="-", command=lambda a=attribut: personnage.diminuer_attribut(a)).grid(row=2+i, column=2, padx=0, sticky="ew")
    attribut_valeur_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_valeur_label.grid(row=2+i, column=3, padx=5, sticky="ew")
    tk.Button(onglet_caracteristiques, text="+", command=lambda a=attribut: personnage.augmenter_attribut(a)).grid(row=2+i, column=4, padx=0, sticky="ew")
    attribut_bonus_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_bonus_label.grid(row=2+i, column=1, padx=5, sticky="ew")
    attribut_valeur_finale_label = tk.Label(onglet_caracteristiques, text="", anchor="center")
    attribut_valeur_finale_label.grid(row=2+i, column=5, padx=5, sticky="ew")
    
    attribut_valeur_labels.append(attribut_valeur_label)
    attribut_bonus_labels.append(attribut_bonus_label)
    attribut_valeur_finale_labels.append(attribut_valeur_finale_label)

# Points restants
points_label = tk.Label(onglet_caracteristiques, text=f"Points restants: {personnage.points_disponibles}")
points_label.grid(row=20, column=0, columnspan=2, pady=10)


# Frame pour les choix de bonus supplémentaires pour les Demi-elfes
choix_frame = tk.Frame(onglet_caracteristiques)
choix_frame.grid(row=21, column=0, columnspan=6, pady=10)
choix_frame.pack_forget()  # Cache le cadre initialement

tk.Label(choix_frame, text="Choisissez deux caractéristiques à augmenter de 1:").pack(anchor="w")

choix_bonus_1_combobox = ttk.Combobox(choix_frame, values=choix_possibles, state="readonly")
choix_bonus_1_combobox.pack(side=tk.LEFT, padx=5)
choix_bonus_2_combobox = ttk.Combobox(choix_frame, values=choix_possibles, state="readonly")
choix_bonus_2_combobox.pack(side=tk.LEFT, padx=5)

# Appeler update_bonus_racial() lorsque la race est sélectionnée
race_combobox.bind("<<ComboboxSelected>>", lambda e: update_bonus_racial())

# Mettre à jour les bonus raciaux lorsque les combobox sont changés
choix_bonus_1_combobox.bind("<<ComboboxSelected>>", lambda e: update_custom_bonus_racial())
choix_bonus_2_combobox.bind("<<ComboboxSelected>>", lambda e: update_custom_bonus_racial())

# Appeler update_bonus_racial pour initialiser correctement lors du lancement
personnage.update_display()

# Appeler update_display pour initialiser les valeurs à l'affichage
personnage.update_display()

# Widgets pour l'onglet Maîtrise
maitrise_frame = tk.Frame(onglet_maitrise)
maitrise_frame.pack(pady=10, fill="x")

# Widgets pour l'onglet Options
options_frame = tk.Frame(onglet_options)
options_frame.pack(pady=10, fill="x")



# Variable global pour tracker le tableau
table_frame = None
magie_sauvage_table_frame = None

# Create a frame to hold the buttons side by side
button_frame = tk.Frame(onglet_classe)

# Global variables for the buttons
lignée_button = None
magie_sauvage_button = None

# Function to open a new window for Lignée Draconique
def open_lignee_window():
    # Create a new window
    lignee_window = tk.Toplevel()
    lignee_window.title("Lignée Draconique")
    lignee_window.geometry("400x400+100+200")  # Position the window to the left

    # Add the Lignée Draconique text to the new window
    lignee_text = tk.Label(lignee_window, text="""Lignée draconique:
Votre magie innée vient de la magie draconique qui a été mêlé avec votre sang ou celui de vos ancêtres. Le plus souvent, 
la généalogie des ensorceleurs de cette origine remonte jusqu'à un puissant ensorceleur des temps anciens 
qui a fait un pacte avec un dragon, ou qui pourrait même avoir un dragon comme parent. Certaines de ces lignées sont bien 
établies dans le monde, mais la plupart sont obscures. Tout ensorceleur donné pourrait être le premier d'une nouvelle lignée, 
à la suite d'un pacte ou d'une autre circonstance exceptionnelle.

Interaction draconique : Vous pouvez parler, lire et écrire le draconique. De plus, chaque fois que vous faites un 
jet de Charisme pour interagir avec des dragons, votre bonus de maîtrise est doublé s’il s’applique au jet.

Résistance draconique : La magie qui coule à travers votre corps fait émerger des traits physiques de vos ancêtres dragons. 
Au niveau 1, votre maximum de points de vie augmente de 1 et également de 1 à chaque fois que vous gagnez un niveau dans cette classe. 
En outre, des parties de votre peau sont couvertes d’un mince reflet d’écailles de dragon. Lorsque vous ne portez pas d'armure, 
votre CA est égale à 13 + votre modificateur de Dextérité.
""", wraplength=350, justify="left")
    lignee_text.pack(padx=10, pady=10)

# Function to wrap and insert text into Treeview
def insert_wrapped_text_in_treeview(treeview, d100_value, effect_text, max_width):
    """
    Inserts wrapped text into a Treeview widget by splitting it into multiple rows.
    Only the first line contains the d100 value; subsequent lines have an empty value for d100.
    """
    wrapped_lines = textwrap.wrap(effect_text, width=max_width)
    for idx, line in enumerate(wrapped_lines):
        # Only insert the d100_value for the first line, subsequent lines get empty d100
        if idx == 0:
            treeview.insert('', tk.END, values=(d100_value, line))
        else:
            treeview.insert('', tk.END, values=('', line))  # Empty d100 for subsequent lines

# Function to open a new window for Magie Sauvage
def open_magie_sauvage_window():
    # Create a new window
    magie_sauvage_window = tk.Toplevel()
    magie_sauvage_window.title("Magie Sauvage")
    magie_sauvage_window.geometry("600x800+900+200")  # Position the window to the right

    # Add the Magie Sauvage text and table to the new window
    magie_sauvage_text = tk.Label(magie_sauvage_window, text="""Magie Sauvage:
Votre magie innée provient des forces sauvages du chaos, à l'origine de l'ordre de la création. Vous pourriez avoir subit 
une exposition à une quelconque forme de magie brute, peut-être par le biais d'un portail vers Limbo, les Plans Élémentaires 
ou encore le mystérieux Royaume lointain. Peut-être avez-vous été béni par une puissante fée ou marqué par un démon. 
Ou votre magie pourrait être un don à la naissance sans aucune raison apparente. Quelle qu'en soit l'origine, cette magie 
chaotique vit en vous et ne demande qu'à sortir.

Marée du chaos : À partir du niveau 1, vous pouvez manipuler les forces du hasard et du chaos pour gagner un avantage à 
un jet d'attaque, un jet de caractéristique ou un jet de sauvegarde. Lorsque vous le faites, vous devez terminer un repos 
long avant de pouvoir l'utiliser à nouveau. Tant que vous n'avez pas récupéré l'usage de cette capacité, si vous lancez un 
sort d'ensorceleur de niveau 1 ou plus, le MD peut vous demander de faire un jet de Pic de magie sauvage (d100). Quel 
qu'en soit le résultat, vous récupérez ensuite cette capacité.""", wraplength=350, justify="left")
    magie_sauvage_text.pack(padx=10, pady=10)

    # Create the table with tkinter's Treeview
    colonnes = ("d100", "Effet")
    magie_sauvage_table = ttk.Treeview(magie_sauvage_window, columns=colonnes, show='headings', height=10)
    magie_sauvage_table.heading("d100", text="d100")
    magie_sauvage_table.heading("Effet", text="Effet")
    magie_sauvage_table.column("d100", width=50, anchor="center")
    magie_sauvage_table.column("Effet", width=400, anchor="w")  # Increased width for the Effect column

    # Insert the data
    data = [
        ("01-02", "Au début de vos prochains tours, refaites un jet de Pic de magie sauvage. Cet effet dure une minute."),
        ("03-04", "Pendant une minute, vous pouvez voir toutes les créatures invisibles tant qu'elles sont dans votre champ de vision."),
        ("05-06", "Un modron contrôlé par le MD apparaît à 1,50 mètre de vous. Il disparaît une minute plus tard."),
        ("07-08", "Vous lancez le sort boule de feu de niveau 3 centré sur vous."),
        ("09-10", "Vous lancez un sort projectile magique de niveau 5."),
        ("11-12", "Lancez un d10. Votre taille varie de 2,50 cm par le résultat du jet. Grandissez ou rapetissez."),
        ("13-14", "Vous lancez le sort confusion centré sur vous-même."),
        ("15-16", "Pendant une minute, vous regagnez 5 points de vie au début de chacun de vos tours."),
        ("17-18", "Une longue barbe faite de plumes vous pousse soudainement. Celle-ci s'évanouit dans un nuage de plumes lorsque vous éternuez."),
        ("19-20", "Vous lancez le sort graisse centré sur vous-même."),
        ("21-22", "Les créatures ont un désavantage à leur jets de sauvegarde contre le prochain sort que vous lancez dans la minute qui suit."),
        ("23-24", "Votre peau devient bleu. Un sort de délivrance des malédictions peut mettre fin à cet effet."),
        ("25-26", "Un oeil apparaît sur votre front pendant une minute. Pendant cette durée, vous avez un avantage à vos jets de Sagesse (Perception) qui se basent sur la vue."),
        ("27-28", "Pendant une minute, tout vos sorts dont le temps d'incantation est d'1 action ont un temps d'incantation d'1 action bonus."),
        ("29-30", "Vous vous téléportez à 18 mètres dans un espace inoccupé que vous pouvez voir."),
        ("31-32", "Vous êtes transporté dans le Plan Astral jusqu'à la fin de votre prochain tour, après quoi vous retournez à votre position d'origine."),
        ("33-34", "Le prochain sort que vous lancez dans la minute qui suit fait le maximum de dégâts."),
        ("35-36", "Lancez un d10. Votre âge varie d'un nombre d'années équivalent au résultat du jet. Si le résultat est pair, vous vieillissez, sinon vous rajeunissez."),
        ("37-38", "1d6 flumphs contrôlés par le MD apparaissent dans un périmètre de 18 mètres et ont peur de vous."),
        ("39-40", "Vous regagnez 2d10 points de vie."),
        ("41-42", "Vous vous transformez en plante en pot jusqu'au début de votre prochain tour. Sous cette forme, vous êtes incapable d'agir et avez la vulnérabilité à tous les types de dégâts."),
        ("43-44", "Pendant une minute, vous pouvez utiliser à chaque tour votre action bonus pour vous téléporter dans un rayon de 6 mètres."),
        ("45-46", "Vous lancez le sort lévitation sur vous."),
        ("47-48", "Une licorne contrôlée par le MD apparaît à 1,50 mètre de vous puis disparaît une minute plus tard."),
        ("49-50", "Vous ne pouvez plus parler pendant une minute. Chaque fois que vous essayez, des bulles roses sortent de votre bouche."),
        ("51-52", "Un bouclier spectral vous entoure pendant une minute, vous faisant bénéficier d'une bonus de +2 à la CA."),
        ("53-54", "Vous êtes immunisé à l'intoxication par l'alcool pour les 5d6 prochains jours."),
        ("55-56", "Vos cheveux tombent puis repoussent progressivement durant les prochaines 24 h."),
        ("57-58", "Pour la prochaine minute, tout objet inflammable que vous touchez qui n'est ni porté ni équipé par une autre créature prend feu."),
        ("59-60", "Vous regagnez votre emplacement de sort dépensé le plus faible."),
        ("61-62", "Pendant une minute, vous criez lorsque vous essayez de parler."),
        ("63-64", "Vous lancez le sort nappe de brouillard centré sur vous-même."),
        ("65-66", "Jusqu'à 3 créatures, que vous choisissez, situées à 9 mètres ou moins de vous, prennent 4d10 dégâts de foudre."),
        ("67-68", "Vous êtes effrayé par la créature la plus proche de vous jusqu'à la fin de votre prochain tour."),
        ("69-70", "Toutes les créatures dans un rayon de 9 mètres deviennent invisibles pendant une minute."),
        ("71-72", "Vous obtenez la résistance à tous les dégâts pendant une minute."),
        ("73-74", "Une créature aléatoire située dans un rayon de 18 mètres est empoisonnée pendant 1d4 heures."),
        ("75-76", "Vous vous mettez à briller dans un rayon de 9 mètres pendant une minute."),
        ("77-78", "Vous lancez le sort métamorphose sur vous-même. Si vous ratez votre jet de sauvegarde, vous vous transformez en mouton pour la durée du sort."),
        ("79-80", "Des illusions de papillons et de pétales de fleur flottent autour de vous dans un rayon de 3 mètres pendant une minute."),
        ("81-82", "Vous obtenez 1 action supplémentaire immédiatement."),
        ("83-84", "Toutes les créatures à 9 mètres ou moins prennent 1d10 de dégâts nécrotiques. Vous regagnez autant de points de vie que de dégâts infligés."),
        ("85-86", "Vous lancez le sort image miroir."),
        ("87-88", "Vous lancez le sort vol sur une créature aléatoire dans un rayon de 18 mètres."),
        ("89-90", "Vous devenez invisible pendant une minute."),
        ("91-92", "Si vous mourrez dans la minute qui suit, vous revenez immédiatement à la vie comme si vous étiez touché par le sort résurrection."),
        ("93-94", "Votre taille augmente d'une catégorie pendant une minute."),
        ("95-96", "Vous et toutes les créatures dans un rayon de 9 mètres obtenez la vulnérabilité aux dégâts perforants pendant une minute."),
        ("97-98", "Vous êtes entouré d'une faible musique éthérée pendant une minute."),
        ("99-100", "Vous regagnez tous vos points de sorcellerie."),
    ]

    # Insert each row of data and wrap the text in the 'Effet' column
    for row in data:
        insert_wrapped_text_in_treeview(magie_sauvage_table, row[0], row[1], max_width=70)  # Adjust width as needed

    magie_sauvage_table.pack(fill="both", expand=True, padx=10, pady=10)

# Fonctions pour afficher les détails de la classe
def afficher_details_classe():
    global patron_label, patron_combobox, tableau_frame, lignée_button, magie_sauvage_button
    
    # Réinitialiser les éléments spécifiques à l'Occultiste (ou à toute autre classe)
    if patron_label:
        patron_label.pack_forget()
        patron_label = None
    if patron_combobox:
        patron_combobox.pack_forget()
        patron_combobox = None
    if tableau_frame:
        tableau_frame.destroy()
        tableau_frame = None
    
    # Reset the Ensorceleur-specific elements (hide them)
    if magie_sauvage_table_frame:
        magie_sauvage_table_frame.pack_forget()
    lignée_button.pack_forget()
    magie_sauvage_button.pack_forget()

    # Récupérer la classe sélectionnée
    classe_selectionnee = classe_combobox.get()

    if classe_selectionnee:
        classe_info = classes[classe_selectionnee]
        # Afficher la description et les détails de la classe
        description = classe_info.description
        details = '\n'.join(classe_info.details)
        # Capacités de base à afficher par défaut
        capacites_base = '\n'.join(classe_info.capacites)
        # Affichage des informations de la classe
        classe_details_label.config(text=f"Description:\n{description}\n\nDétails de la Classe:\n{details}\n\nCapacités de la Classe:\n{capacites_base}")

        # Si la classe sélectionnée est "Occultiste", afficher le menu déroulant et le tableau
        if classe_selectionnee == 'Occultiste':
            # Ajouter le titre pour le choix du patron
            patron_label = tk.Label(onglet_classe, text="Choisissez votre patron :", font=('Arial', 12, 'bold'))
            patron_label.pack(anchor="center", pady=10)

            # Créer un menu déroulant pour sélectionner le patron
            patron_combobox = ttk.Combobox(onglet_classe, values=["L'Archifée", "Le Fiélon", "Le Grand Ancien"], state="readonly")
            patron_combobox.pack(anchor="center", padx=5, pady=5)

            # Bind le combobox pour mettre à jour les sorts et capacités en fonction du patron sélectionné
            patron_combobox.bind("<<ComboboxSelected>>", lambda event: update_patron(patron_combobox.get()))

            # Afficher le tableau des patrons
            afficher_tableau_patrons()
        
        # Si la classe sélectionnée est "Ensorceleur"
        if classe_selectionnee == "Ensorceleur":
            # Show buttons only for Ensorceleur
            lignée_button.pack(side="left", padx=10)
            magie_sauvage_button.pack(side="right", padx=10)
        else:
            # Hide buttons and their contents for other classes
            lignée_button.pack_forget()
            magie_sauvage_button.pack_forget()

    # Display general class details as usual (description and capacities)
    description = classes[classe_selectionnee].description
    details = '\n'.join(classes[classe_selectionnee].details)
    capacites = '\n'.join(classes[classe_selectionnee].capacites)
    
    classe_details_label.config(text=f"Description:\n{description}\n\nDétails de la Classe:\n{details}\n\nCapacités de la Classe:\n{capacites}")

# Create the buttons (placed inside a frame)
button_frame = tk.Frame(onglet_classe)
button_frame.pack(pady=5)  # Adjust padding as needed

lignée_button = tk.Button(button_frame, text="Afficher Lignée Draconique", command=open_lignee_window)
magie_sauvage_button = tk.Button(button_frame, text="Afficher Magie Sauvage", command=open_magie_sauvage_window)

# Initially, buttons should be hidden until Ensorceleur is selected
lignée_button.pack_forget()
magie_sauvage_button.pack_forget()

# Call afficher_details_classe when the class selection changes
classe_combobox.bind("<<ComboboxSelected>>", lambda event: afficher_details_classe())
        
# Variables globales pour les éléments spécifiques à l'Occultiste
patron_label = None
patron_combobox = None
tableau_frame = None

def afficher_tableau_patrons():
    global tableau_frame
    
    # Créer le frame qui contiendra le tableau
    tableau_frame = tk.Frame(onglet_classe)
    tableau_frame.pack(pady=10)

    # Créer un tableau avec Treeview
    colonnes = ("Patron", "Sorts conférés", "Capacité conférée")
    tableau = ttk.Treeview(tableau_frame, columns=colonnes, show='headings', height=3)

    # Configurer les en-têtes du tableau
    tableau.heading("Patron", text="Patron")
    tableau.heading("Sorts conférés", text="Sorts conférés")
    tableau.heading("Capacité conférée", text="Capacité conférée")

    # Définir la largeur des colonnes
    tableau.column("Patron", width=150, anchor="center")
    tableau.column("Sorts conférés", width=200, anchor="center")
    tableau.column("Capacité conférée", width=300, anchor="center")

    # Ajouter les données des patrons
    data = [
        ("L'Archifée", "Lueurs féeriques, Sommeil", "Présence féerique"),
        ("Le Fiélon", "Injonction, Mains brûlantes", "Bénédiction du ténébreux"),
        ("Le Grand Ancien", "Fou rire de Tasha, Murmures dissonants", "Esprit éveillé")
    ]

    # Insérer les lignes de données dans le tableau
    for row in data:
        tableau.insert('', tk.END, values=row)

    # Afficher le tableau
    tableau.pack(fill="both", expand=True)

def update_patron(patron_choisi):
    # Sorts de base avant ajout du patron
    sorts_base = ['Absorption des éléments, Alarme, Appel de familier, Armure de mage, Barbes argentées, Bouclier, Compréhension des langues, Couleurs dansantes, Couteau de glace, Déguisement, Détection de la magie, Disque flottant de Tenser, Feuille morte, Fou rire de Tasha, Frayeur, Graisse, Grande foulée, Identification, Image silencieuse, Mains brûlantes, Orbe chromatique, Projectile magique, Protection contre le mal et le bien, Rayon empoisonné, Repli expéditif, Saut, Secousse sismique, Serviteur invisible, Sommeil, Texte illusoire, Trait ensorcelé, Vague tonnante, Vents contraires, Éclair de chaos, Mixture caustique de Tasha, Nappe de brouillard, Projectile élémentaire, Simulacre de vie']
    
    #Description + detail occultiste
    classe_occultiste = classes['Occultiste']
    description = classe_occultiste.description
    details = '\n'.join(classe_occultiste.details)
    # Capacités de base sans patron
    capacites_base = """
Patron d'Outremonde : Vous avez conclu un marché avec un être d'Outremonde de votre choix : l'Archifée, le Fiélon ou le Grand Ancien.
Manifestations occultes : Fragments d’un savoir interdit vous conférant une capacité magique permanente.
Magie de pacte : Pour lancer un sort d'occultiste de niveau 1 ou supérieur, vous devez dépenser un emplacement. Vous regagnez tous vos emplacements de sorts dépensés lorsque vous terminez un repos court ou long.
    """

    # Initialiser les sorts et capacités en fonction du patron choisi
    if patron_choisi == "L'Archifée":
        sorts_patron = ['Lueurs féeriques', 'Sommeil']
        capacites_patron = "Présence féerique : votre patron vous permet de projeter la séduisante présence des fées. Par une action, vous pouvez charmer ou effrayer des créatures dans un cube de 3 mètres après un jet de Sagesse raté."
    elif patron_choisi == "Le Fiélon":
        sorts_patron = ['Injonction', 'Mains brûlantes']
        capacites_patron = "Bénédiction du ténébreux : Lorsque vous réduisez une créature hostile à 0 point de vie, vous gagnez des points de vie temporaires égaux à votre modificateur de Charisme + niveau d'occultiste."
    elif patron_choisi == "Le Grand Ancien":
        sorts_patron = ['Fou rire de Tasha', 'Murmures dissonants']
        capacites_patron = "Esprit éveillé : Communiquer télépathiquement avec toute créature visible à 9 mètres."

    # Mettre à jour les capacités et sorts dans l'objet personnage
    personnage.sort_niveau_un_classe = sorts_base + sorts_patron
    personnage.capacites = capacites_base + "\n" + capacites_patron

    # Mettre à jour seulement les capacités affichées, sans dupliquer tout le contenu
    classe_details_label.config(text=f"Description:\n{description}\n\nDétails de la Classe:\n{details}\n\nCapacités de la Classe:\n{capacites_base}\n{capacites_patron}")
    


def update_display_sorts_et_capacites():
    # Mettre à jour l'affichage pour montrer les sorts et capacités modifiés
    sort_details_label = personnage.sort_niveau_un_classe
    capacites_details_label.config(text=f"Capacités : {personnage.capacites}")

# Variables globales pour les éléments spécifiques à Drakéide
ascendance_label = None
ascendance_combobox = None
tableau_frame = None  # Utiliser tableau_frame au lieu de tableau_label


def afficher_tableau_draconic():
    global tableau_frame
    
    # Vérifier si le tableau existe déjà, et le supprimer s'il existe
    if tableau_frame:
        tableau_frame.destroy()

    # Créer le frame qui contiendra le tableau
    tableau_frame = tk.Frame(onglet_race)
    tableau_frame.pack(pady=10)

    # Créer un tableau avec Treeview
    colonnes = ("Dragon", "Type de dégâts", "Souffle", "Résistance")
    tableau = ttk.Treeview(tableau_frame, columns=colonnes, show='headings', height=10)

    # Configurer les en-têtes du tableau
    tableau.heading("Dragon", text="Dragon")
    tableau.heading("Type de dégâts", text="Type de dégâts")
    tableau.heading("Souffle", text="Souffle")
    tableau.heading("Résistance", text="Résistance")

    # Définir la largeur des colonnes
    tableau.column("Dragon", width=100, anchor="center")
    tableau.column("Type de dégâts", width=100, anchor="center")
    tableau.column("Souffle", width=200, anchor="center")
    tableau.column("Résistance", width=100, anchor="center")

    # Ajouter les données
    data = [
        ("Blanc", "Froid", "Cône de 4,50 m (JdS de Con.)", "Froid"),
        ("Bleu", "Foudre", "Ligne de 1,50 x 9 m (JdS de Dex.)", "Foudre"),
        ("Noir", "Acide", "Ligne de 1,50 x 9 m (JdS de Dex.)", "Acide"),
        ("Rouge", "Feu", "Cône de 4,50 m (JdS de Dex.)", "Feu"),
        ("Vert", "Poison", "Cône de 4,50 m (JdS de Con.)", "Poison"),
        ("Airain", "Feu", "Ligne de 1,50 x 9 m (JdS de Dex.)", "Feu"),
        ("Argent", "Froid", "Cône de 4,50 m (JdS de Con.)", "Froid"),
        ("Bronze", "Foudre", "Ligne de 1,50 x 9 m (JdS de Dex.)", "Foudre"),
        ("Cuivre", "Acide", "Ligne de 1,50 x 9 m (JdS de Dex.)", "Acide"),
        ("Or", "Feu", "Cône de 4,50 m (JdS de Dex.)", "Feu")
    ]

    # Insérer les lignes de données dans le tableau
    for row in data:
        tableau.insert('', tk.END, values=row)

    # Afficher le tableau
    tableau.pack(fill="both", expand=True)


# Fonctions pour afficher les détails de la race
def afficher_details_race():
    global ascendance_label, ascendance_combobox, tableau_frame
    
    race_selectionnee = race_combobox.get()

    # Effacer les éléments spécifiques à Drakéide s'ils existent
    if ascendance_label:
        ascendance_label.pack_forget()
        ascendance_label = None
    if ascendance_combobox:
        ascendance_combobox.pack_forget()
        ascendance_combobox = None
    if tableau_frame:
        tableau_frame.destroy()
        tableau_frame = None

    if race_selectionnee:
        race_info = races[race_selectionnee]

        # Afficher la description et les détails de la race
        description = race_info.description
        details = '\n'.join(race_info.details)
        race_details_label.config(text=f'Description:\n{description}\n\nDétails de la Race:\n{details}')

        # Si la race sélectionnée est Drakéide, afficher l'ascendance draconique et le tableau des résistances
        if race_selectionnee == 'Drakéide':
            # Ajouter le titre pour l'ascendance draconique
            ascendance_label = tk.Label(onglet_race, text="Choisissez votre ascendance draconique :", font=('Arial', 10, 'bold'))
            ascendance_label.pack(anchor="center", pady=10)

            # Créer un menu déroulant pour sélectionner l'ascendance draconique
            ascendance_options = ["Blanc", "Bleu", "Noir", "Rouge", "Vert", "Airain", "Argent", "Bronze", "Cuivre", "Or"]
            ascendance_combobox = ttk.Combobox(onglet_race, values=ascendance_options, state="readonly")
            ascendance_combobox.pack(anchor="center", padx=5, pady=5)

            # Afficher le tableau des dragons
            afficher_tableau_draconic()
            
            

# Fonction pour lancer un dé à 100 faces et retourner une babiole
def tirer_babiole():
    return random.choice(babioles)

def afficher_details_historique():
    historique_selectionne = historique_combobox.get()
    description = historiques[historique_selectionne].description
    details = historiques[historique_selectionne].details
    details_str = '\n'.join(details)
    
    # Tirer une babiole si nécessaire
    babiole = tirer_babiole()
    if "babiole" in historiques[historique_selectionne].equipement:
        equipement = historiques[historique_selectionne].equipement.replace("babiole", babiole)
    else:
        equipement = historiques[historique_selectionne].equipement
    
    historique_details_label.config(
        text=f'Description:\n{description}\n\nDétails de l\'Historique:\n{details_str}\n\nÉquipement:\n{equipement}\n\nPO: {historiques[historique_selectionne].argent_historique}\n\nCapacité:\n{historiques[historique_selectionne].capacite}'
    )
    
# Fonction pour mettre à jour les options en fonction de la classe sélectionnée
def update_options():
    for widget in options_frame.winfo_children():
        widget.destroy()

    classe_selectionnee = classe_combobox.get()

    if classe_selectionnee == 'Roublard':
        tk.Label(options_frame, text="Expertise (Roublard)", font=('Arial', 12, 'bold')).pack(anchor="w")
        expertise_frame = tk.Frame(options_frame)
        expertise_frame.pack(anchor="w", pady=5)

        # Filtrer les compétences et outils pour l'expertise
        competences_selectionnees = personnage.extraire_competences_selectionnees()

        # Exclure les langues des compétences disponibles pour l'expertise
        competences_et_outils = [
            competence for competence in competences_selectionnees
            if competence not in langues_standard + langues_exotiques
        ]

        def update_expertise_options():
            for i, combobox in enumerate(expertise_comboboxes):
                other_selection = personnage.expertise_selections[1 - i]
                values = [comp + " (déjà sélectionné)" if comp == other_selection else comp for comp in competences_et_outils]
                current_value = combobox.get()
                if current_value not in values:
                    combobox.set("")
                combobox['values'] = values

        def on_expertise_selected(index):
            def handler(event):
                personnage.expertise_selections[index] = event.widget.get().replace(" (déjà sélectionné)", "")
                update_expertise_options()
            return handler

        expertise_comboboxes = []
        for i in range(2):  # Deux menus déroulants pour l'expertise
            expertise_combobox = ttk.Combobox(expertise_frame, state="readonly")
            expertise_combobox.pack(side=tk.LEFT, padx=5)
            expertise_combobox.bind("<<ComboboxSelected>>", on_expertise_selected(i))
            expertise_comboboxes.append(expertise_combobox)

        update_expertise_options()  # Initial update with available options


    # Reste des options comme les styles de combat et les packs de départ
    if 'styles_de_combat' in classes[classe_selectionnee].__dict__ and classes[classe_selectionnee].styles_de_combat:
        tk.Label(options_frame, text="Style de combat", font=('Arial', 12, 'bold')).pack(anchor="w")
        styles_disponibles = [style.nom for style in classes[classe_selectionnee].styles_de_combat]
        style_combobox = ttk.Combobox(options_frame, values=styles_disponibles, state="readonly")
        style_combobox.pack(anchor="w", pady=5)

        def show_style_description(event):
            style = style_combobox.get()
            description = description_style_de_combat.get(style, '')
            description_label.config(text=description, fg="#802040", font=('Arial', 12, 'bold'))

        style_combobox.bind("<<ComboboxSelected>>", show_style_description)
        description_label = tk.Label(options_frame, text="", wraplength=500)
        description_label.pack(anchor="e", padx=20)

    if 'packs' in classes[classe_selectionnee].__dict__ and classes[classe_selectionnee].packs:
        tk.Label(options_frame, text="Pack de départ", font=('Arial', 12, 'bold')).pack(anchor="w")
        packs_disponibles = list(classes[classe_selectionnee].packs.keys())
        pack_combobox = ttk.Combobox(options_frame, values=packs_disponibles, state="readonly")
        pack_combobox.pack(anchor="w", pady=5)

        def show_pack_content(event):
            pack = pack_combobox.get()
            content = '\n'.join(classes[classe_selectionnee].packs[pack])
            pack_content_label.config(text=content)

        pack_combobox.bind("<<ComboboxSelected>>", show_pack_content)
        pack_content_label = tk.Label(options_frame, text="", justify=tk.LEFT, anchor="w", wraplength=500)
        pack_content_label.pack(anchor="w", pady=5)



# Lancement de la boucle principale
fenetre.mainloop()