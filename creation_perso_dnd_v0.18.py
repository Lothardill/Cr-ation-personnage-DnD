import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# Classes de données pour encapsuler les caractéristiques du jeu
class StyleDeCombat:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description

class Classe:
    def __init__(self, nom, description, details, capacites, outils, nombre_de_competence, competences, sort_mineur_classe, nombre_sort_mineur_classe, sort_niveau_un_classe, nombre_sort_niveau_un_classe, styles_de_combat, argent_classe, packs):
        self.nom = nom
        self.description = description
        self.details = details
        self.capacites = capacites
        self.outils = outils
        self.nombre_de_competence = nombre_de_competence
        self.competences = competences
        self.sort_mineur_classe = sort_mineur_classe
        self.nombre_sort_mineur_classe=nombre_sort_mineur_classe
        self.sort_niveau_un_classe=sort_niveau_un_classe
        self.nombre_sort_niveau_un_classe= nombre_sort_niveau_un_classe
        self.styles_de_combat = styles_de_combat
        self.argent_classe = argent_classe
        self.packs = packs
        
    def calculer_argent(self):
        des, multiplicateur = map(int, self.argent_classe.split('d4 x '))
        somme = sum(random.randint(1, 4) for _ in range(des))
        return somme * multiplicateur

class Race:
    def __init__(self, nom, description, details, bonus, competences, nombre_competences_race, outils, sort_race, nombre_sort_race, langues, nombre_de_langue, langue_parlee_race, armes_maitrisees_race, armures_maitrisees_race):
        self.nom = nom
        self.description = description
        self.details = details
        self.bonus = bonus
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
            competences_disponibles_classe.update(self.races[race_selectionnee].competences)
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
        for i, attribut in enumerate(attributs_list):
            valeur = self.attributs_personnage[attribut]
            bonus = self.races[race_combobox.get()].bonus.get(attribut, 0) if race_combobox.get() else 0
            total = valeur + bonus
            modificateur = self.calculer_modificateur(total)

            attribut_valeur_labels[i].config(text=f"{valeur}")
            attribut_bonus_labels[i].config(text=f"{bonus:+d}")
            attribut_valeur_finale_labels[i].config(text=f"{total} ({modificateur:+d})")

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
        competences_disponibles_classe, competences_disponibles_historique, langues_disponibles, outils_disponibles = self.extraire_competences_et_langues(
            classe_combobox.get(), race_combobox.get(), historique_combobox.get()
        )

        # Effacer les widgets existants
        for widget in onglet_sorts_connus.winfo_children():
            widget.destroy()

        # Réinitialiser les comboboxes
        self.comboboxes = []

        # Compétences de la race
        race_selectionnee = race_combobox.get()
        if race_selectionnee:
            competences_race = self.races[race_selectionnee].competences
            self.creer_menu_deroulant(competences_race, "Compétences de la race", maitrise_frame)
        
        if race_selectionnee == "Demi-elfe":
            competences_race = personnage.races[race_selectionnee].competences_race
            personnage.creer_menu_deroulant(competences_race, "Compétences de la race", maitrise_frame, nombre=2)

        # Compétences de la classe
        classe_selectionnee = classe_combobox.get()
        if classe_selectionnee:
            nombre_de_competence = self.classes[classe_selectionnee].nombre_de_competence
            competences_classe = list(competences_disponibles_classe)
            self.creer_menu_deroulant(competences_classe, "Compétences de la classe", maitrise_frame, nombre=nombre_de_competence)

        # Compétences de l'historique
        historique_selectionne = historique_combobox.get()
        if historique_selectionne:
            nombre_de_competence_historique = self.historiques[historique_selectionne].nombre_de_competence
            competences_historique = list(competences_disponibles_historique)
            self.creer_menu_deroulant(competences_historique, "Compétences de l'historique", maitrise_frame, nombre=nombre_de_competence_historique)

        # Outils de la race
        if race_selectionnee:
            outils_race = self.races[race_selectionnee].outils
            self.creer_menu_deroulant(outils_race, "Outils de la race", maitrise_frame, 1)

        # Outils de la classe
        self.creer_menu_deroulant(self.classes[classe_selectionnee].outils, "Outils de la classe", maitrise_frame, nombre=1)

        # Outils de l'historique
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
                    combobox_outils_historique.bind("<<ComboboxSelected>>", lambda event: [self.update_selected_values()])
                    self.comboboxes.append((combobox_outils_historique, "Outils de l'historique"))
                if choix_outils_historiques:
                    formatted_choix_outils_historiques = [self.format_value(opt) for opt in sorted(choix_outils_historiques)]
                    combobox_choix_outils_historiques = ttk.Combobox(outils_historiques_frame, values=formatted_choix_outils_historiques, state="readonly")
                    combobox_choix_outils_historiques.pack(side=tk.LEFT, padx=5)
                    combobox_choix_outils_historiques.bind("<<ComboboxSelected>>", lambda event: [self.update_selected_values()])
                    self.comboboxes.append((combobox_choix_outils_historiques, "Choix d'outils de l'historique"))

        # Langues de la race
        if race_selectionnee:
            langues_parlees_race = self.races[race_selectionnee].langue_parlee_race.split(', ')
            if langues_parlees_race or self.races[race_selectionnee].nombre_de_langue > 0:
                tk.Label(maitrise_frame, text="Langues de la race", font=('Arial', 10, 'bold')).pack(anchor="w")
                langues_race_frame = tk.Frame(maitrise_frame)
                langues_race_frame.pack(anchor="w", pady=5)
                for langue in langues_parlees_race:
                    tk.Label(langues_race_frame, text=langue, font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
                all_langues = sorted(langues_standard + langues_exotiques)
                formatted_all_langues = [self.format_value(opt) for opt in all_langues]
                for _ in range(self.races[race_selectionnee].nombre_de_langue):
                    combobox_langues_supplementaires_race = ttk.Combobox(langues_race_frame, values=formatted_all_langues, state="readonly")
                    combobox_langues_supplementaires_race.pack(side=tk.LEFT, padx=5)
                    combobox_langues_supplementaires_race.bind("<<ComboboxSelected>>", lambda event: [self.update_selected_values()])
                    self.comboboxes.append((combobox_langues_supplementaires_race, "Langues de la race"))

        # Langues de l'historique
        if historique_selectionne:
            nombre_de_langue_historique = self.historiques[historique_selectionne].nombre_de_langue_historique
            if nombre_de_langue_historique > 0:
                self.creer_menu_deroulant(langues_standard + langues_exotiques, "Langues de l'historique", maitrise_frame, nombre=nombre_de_langue_historique)
 

# Données de jeu
attributs_list = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse', 'Charisme']
competences_completes = ['Acrobaties', 'Arcanes', 'Athlétisme', 'Discrétion', 'Dressage', 'Escamotage', 'Histoire', 'Intimidation', 'Investigation', 'Médecine', 'Nature', 'Perception', 'Perspicacité', 'Persuasion', 'Religion', 'Représentation', 'Survie', 'Tromperie']
langues_standard = ['Commun', 'Elfique', 'Géant', 'Gnome', 'Gobelin', 'Halfelin', 'Nain', 'Orc']
langues_exotiques = ['Abyssal', 'Céleste', 'Commun des profondeurs', 'Draconique', 'Infernal', 'Primordial', 'Profond', 'Sylvestre']
sort_mineur = [
    {"nom": "Amis", "type": "enchantement", "description": "Le lanceur obtient l'avantage aux jets de Charisme contre une créature choisie qui ne lui est pas hostile."},
    {"nom": "Aspersion d'acide", "type": "invocation", "description": "1 ou 2 créatures dans un rayon de 1,50 m doivent réussir un JdS de Dex. ou subir 1d6 dégâts d'acide (dégâts/niv)."},
    {"nom": "Bouffée de poison", "type": "invocation", "description": "La cible doit réussir un JdS de Con. ou subir 1d12 dégâts de poison (dégâts/niv)."},
    {"nom": "Contact glacial", "type": "nécromancie", "description": "Si l'attaque avec un sort touche, inflige 1d8 dégâts nécrotiques (dégâts/niv) et la cible ne peut récupérer ses pv de suite."},
    {"nom": "Coup au but", "type": "divination", "description": "Le lanceur obtient l'avantage à son prochain jet d'attaque contre une cible."},
    {"nom": "Illusion mineure", "type": "illusion", "description": "Crée l'illusion d'un son ou d'une image immobile pas plus grande qu'un cube de 1,50 m."},
    {"nom": "Lumière", "type": "évocation", "description": "Fait qu'un objet émette une lumière vive sur 6 m et une lumière faible sur 6 m supplémentaires."},
    {"nom": "Lumières dansantes", "type": "évocation", "description": "Crée jusqu'à 4 lumières de la taille d'une torche qui émettent une lumière faible sur 3 m et qu'on peut déplacer jusqu'à 18 m."},
    {"nom": "Main de mage", "type": "invocation", "description": "Crée une main spectrale qui peut dans un rayon de 9 m manipuler un objet, ouvrir une porte, saisir un objet, etc."},
    {"nom": "Message", "type": "transmutation", "description": "Le lanceur murmure un message à une créature à 36 m qui sera la seule à l'entendre. Elle pourra répondre de la même façon."},
    {"nom": "Poigne électrique", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 1d8 dégâts de foudre (dégâts/niv) et la cible ne peut pas prendre de réaction."},
    {"nom": "Prestidigitation", "type": "transmutation", "description": "Tour de magie (effet sensoriel, allume une torche, nettoie un objet, réchauffe, fait apparaître un symbole, crée une babiole)."},
    {"nom": "Protection contre les armes", "type": "abjuration", "description": "Le lanceur obtient la résistance contre les dégâts contondants, tranchants et perforants infligés par des attaques avec arme."},
    {"nom": "Rayon de givre", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 1d8 dégâts de froid (dégâts/niv) et la vitesse de la cible est réduite de 3 m."},
    {"nom": "Réparation", "type": "transmutation", "description": "Répare fissure, déchirure, fêlure d'un objet (maillon de chaîne cassé, clé brisée, accroc sur un manteau, fuite d'une gourde)."},
    {"nom": "Trait de feu", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 1d10 dégâts de feu (dégâts/niv). Un objet peut prendre feu."},
    {"nom": "Contrôle des flammes", "type": "transmutation", "description": "Contrôle les feux non magiques pour les allumer, éteindre, faire grossir, faire apparaître des formes simples, etc."},
    {"nom": "Coup de tonnerre", "type": "évocation", "description": "Les créatures dans un rayon de 1,50 m doivent réussir un JdS de Con. ou subir 1d6 dégâts tonnerre (dégâts/niv)."},
    {"nom": "Embrasement", "type": "invocation", "description": "Les créatures dans un cube de 1,50 m doivent réussir un JdS de Dex. ou subir 1d8 dégâts de feu (dégâts/niv)."},
    {"nom": "Façonnage de l'eau", "type": "transmutation", "description": "Contrôle l'eau pour obtenir divers effets mineurs comme changer sa couleur, la faire geler, changer le sens du courant, etc."},
    {"nom": "Gelure", "type": "évocation", "description": "La cible doit réussir un JdS de Con. ou subir 1d6 dégâts de froid et avoir un désavantage à l'attaque (dégâts/niv)."},
    {"nom": "Glas", "type": "nécromancie", "description": "La cible doit réussir un JdS de Sag. ou subir 1d8 ou 1d12 dégâts nécrotiques (dégâts/niv)."},
    {"nom": "Infestation", "type": "invocation", "description": "La cible doit réussir un JdS de Con. ou subir 1d6 dégâts de poison et se déplacer de 1,50 m au hasard (dégâts/niv)."},
    {"nom": "Saute de vent", "type": "transmutation", "description": "Contrôle l'air afin de déplacer des objets ou des créatures (taille M max) ou de créer des effets sensoriels inoffensifs."},
    {"nom": "Éruption de lames", "type": "invocation", "description": "Les créatures dans un rayon de 1,50 m doivent réussir un JdS de Dex. ou subir 1d6 de force (dégâts/niv)."},
    {"nom": "Ferrage foudroyant", "type": "évocation", "description": "La cible doit réussir un JdS de For. ou subir 1d8 dégâts de foudre (dégâts/niv) et être poussée de 3 m."},
    {"nom": "Lame aux flammes vertes", "type": "évocation", "description": "Si une attaque avec une arme touche, inflige aussi des dégâts de feu égaux au Mod.Carac.Inc à une autre créature (dégâts/niv)."},
    {"nom": "Lame retentissante", "type": "évocation", "description": "Si une attaque avec une arme touche, inflige 1d8 dégâts de tonnerre si la cible bouge (dégâts/niv)."},
    {"nom": "Piqûre mentale", "type": "enchantement", "description": "La cible doit réussir un JdS d'Int. ou subir 1d6 dégâts psychiques et soustraire 1d4 à son prochain JdS (dégâts/niv)."}
]
sort_niveau_un=[{"nom": "Alarme", "type": "abjuration (rituel)", "description": "Alerte le lanceur ou active une alarme si une créature de taille TP ou supérieure pénètre dans un cube surveillé de 6 m."},
{"nom": "Appel de familier", "type": "invocation (rituel)", "description": "Invoque un petit animal qui obéit au lanceur du sort et qui partage ses sens avec lui par télépathie."},
{"nom": "Armure de mage", "type": "abjuration", "description": "La cible, si elle est consentante et ne porte pas d'armure, obtient une CA de 13+Mod.Dex."},
{"nom": "Bouclier", "type": "abjuration", "description": "En réaction, le lanceur gagne un bonus de +5 à la CA et ne prend aucun dégât du sort projectile magique."},
{"nom": "Charme-personne", "type": "enchantement", "description": "La cible humanoïde doit réussir un JdS de Sag. ou être charmée par le lanceur (+1 créature/niv)."},
{"nom": "Compréhension des langues", "type": "divination (rituel)", "description": "Le lanceur comprend toutes les langues parlées ou écrites (1 min/page). Ne décode pas les messages secrets."},
{"nom": "Couleurs dansantes", "type": "illusion", "description": "6d10 pv de créatures sont éblouies par ordre croissant de leurs pv actuels (+2d10 pv/niv)."},
{"nom": "Déguisement", "type": "illusion", "description": "Modifie l'apparence du lanceur (son physique et son équipement) grâce à une illusion."},
{"nom": "Détection de la magie", "type": "divination (rituel)", "description": "Le lanceur détecte toutes émanations magiques dans un rayon de 9 m et en détermine l'école."},
{"nom": "Disque flottant de tenser", "type": "invocation (rituel)", "description": "Crée un plateau flottant de 90 cm de diamètre qui peut supporter jusqu'à 250 kg et suit le lanceur."},
{"nom": "Feuille morte", "type": "transmutation", "description": "Jusqu'à 5 créatures tombent à une vitesse de 18 mètres par round et ne subissent pas de dégâts de chute si le sort est actif."},
{"nom": "Fou rire de tasha", "type": "enchantement", "description": "La cible doit réussir un JdS de Sag. ou être prise d'une intense crise de fou rire, tomber à terre et être incapable d'agir."},
{"nom": "Graisse", "type": "invocation", "description": "Les créatures dans un carré de 3 m (terrain difficile) doivent réussir un JdS de Dex. pour ne pas tomber."},
{"nom": "Grande foulée", "type": "transmutation", "description": "La cible obtient une vitesse augmentée de 3 m (+1 créature/niv)."},
{"nom": "Identification", "type": "divination (rituel)", "description": "Le lanceur obtient les propriétés d'un objet magique (lien, charges) ou est informé si un sort affecte un objet ou une créature."},
{"nom": "Image silencieuse", "type": "illusion", "description": "Crée l'image d'un objet ou d'une créature (sans son et de la taille d'un cube de 4,50 m max) et permet de la faire bouger."},
{"nom": "Mains brûlantes", "type": "évocation", "description": "Les créatures dans un cône de 4,50 m doivent réussir un JdS de Dex. ou subir 3d6 dégâts de feu (dégâts/niv)."},
{"nom": "Nappe de brouillard", "type": "invocation", "description": "Rend la visibilité nulle dans une sphère de 6 m de rayon (+6 m/niv)."},
{"nom": "Orbe chromatique", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 3d8 dégâts d'un type préalablement déterminé (dégâts/niv)."},
{"nom": "Projectile magique", "type": "évocation", "description": "3 projectiles infligent automatiquement 1d4+1 dégâts de force chacun à une ou plusieurs créatures (+1 projectile/niv)."},
{"nom": "Protection contre le mal et le bien", "type": "abjuration", "description": "La cible est protégée (désavantage à l'attaque) des aberrations, célestes, élémentaires, fées, fiélons et morts-vivants."},
{"nom": "Rayon empoisonné", "type": "nécromancie", "description": "Si l'attaque touche, inflige 2d8 dégâts de poison (dégâts/niv) et la cible peut être empoisonnée (JdS de Con)."},
{"nom": "Repli expéditif", "type": "transmutation", "description": "Le lanceur peut effectuer l'action Foncer en utilisant une action bonus."},
{"nom": "Saut", "type": "transmutation", "description": "La cible obtient une distance de saut multipliée par 3."},
{"nom": "Serviteur invisible", "type": "invocation (rituel)", "description": "Crée un serviteur invisible qui exécute des tâches simples (rapporter qq chose, nettoyer, entretenir un feu, servir, etc)."},
{"nom": "Simulacre de vie", "type": "nécromancie", "description": "Le lanceur gagne 1d4+4 pv temporaires (+5 pv/niv)."},
{"nom": "Sommeil", "type": "enchantement", "description": "5d8 pv de créatures s'endorment, par ordre croissant de leurs pv actuels (+2d8 pv/niv)."},
{"nom": "Texte illusoire", "type": "illusion (rituel)", "description": "Rédige un message secret qui ne peut être lu que par une cible désignée ou une créature qui possède vision véritable."},
{"nom": "Trait ensorcelé", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 1d12 dégâts de foudre (dégâts/niv) à chaque round."},
{"nom": "Vague tonnante", "type": "évocation", "description": "Les créatures dans un cube de 4,50 m doivent réussir un JdS de Con. ou subir 2d8 dégâts de tonnerre (dégâts/niv)."},
{"nom": "Absorption des éléments", "type": "abjuration", "description": "Le lanceur a la résistance aux dégâts reçus et inflige 1d6 dégâts extra du même type à sa prochaine attaque (dégâts/niv)."},
{"nom": "Catapulte", "type": "transmutation", "description": "La cible doit réussir un JdS de Dex. ou subir 3d8 dégâts contondants d'un objet de 2,5 kg max (+2,5 kg et +1d8/niv)."},
{"nom": "Collet", "type": "abjuration", "description": "Crée un piège magique (JdS de Dex. ou la créature de taille P à G est hissée en l'air)."},
{"nom": "Couteau de glace", "type": "invocation", "description": "Si l'attaque avec un sort touche, inflige 1d10 dégâts perforants + JdS de Dex. ou 2d6 dégâts de froid (dégâts/niv) à 1,50 m."},
{"nom": "Frayeur", "type": "nécromancie", "description": "La cible doit réussir un JdS de Sag. ou être effrayée (nbre de cibles/niv)."},
{"nom": "Secousse sismique", "type": "évocation", "description": "Les créatures dans un rayon de 3m doivent réussir un JdS de Dex. ou subir 1d6 dégâts contondants et tomber à terre (dégâts/niv)."},
{"nom": "Mixture caustique de tasha", "type": "évocation", "description": "Les créatures sur une ligne de 9 x 1,50 m doivent réussir un JdS de Dex. ou subir 2d4 dégâts d'acide chaque tour (+2d4/niv)."},
{"nom": "Barbes argentées", "type": "enchantement", "description": "La cible doit relancer le d20 et une autre créature gagne un avantage à son prochain jet d'attaque, de carac ou de sauvegarde."},
{"nom": "Projectile élémentaire", "type": "évocation", "description": "Si l'attaque avec un sort touche, inflige 2d8 dégâts en fonction de l'élément invoqué (dégâts/niv)."}
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
            'Second souffle: Une fois par repos court ou long, vous pouvez utiliser une action bonus pour regagner un nombre de points de vie égal à 1d10 + votre niveau.',
            'Style de combat: Vous choisissez un style de combat qui vous accorde des avantages en combat.'
        ],
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
               'Pack (b)': ['Armure de cuir', '2 armes de guerre', '2 hachettes', 'Arc long', 'Sac d\'explorateur']}
    ),
    'Magicien': Classe(
        nom='Magicien',
        description='Des lanceurs de sorts étudient les arcanes magiques et lancent des sorts puissants.',
        details=[
            'DV. 1d6',
            'Armes. Dague, fléchette, fronde, bâton, arbalète légère',
            'Jets de sauvegarde. Intelligence, Sagesse',
            'Choix de 2 compétences parmi Arcanes, Histoire, Intuition, Investigation, Médecine, Religion'
        ],
        capacites=[
            'Incantation: Vous pouvez lancer des sorts de votre liste de sorts.',
            'Restauration arcanique (1/jour): Vous récupérez un nombre d’emplacements de sorts égal à [niv/2] (maximum niveau 5).'
        ],
        outils=[],
        nombre_de_competence=2,
        competences='Arcanes, Histoire, Intuition, Investigation, Médecine, Religion',
        sort_mineur_classe=sort_mineur,
        nombre_sort_mineur_classe=3,
        sort_niveau_un_classe=sort_niveau_un,
        nombre_sort_niveau_un_classe=6,
        styles_de_combat=[],
        argent_classe='5d4 x 10',
        packs={'Pack (a)': ['Bâton', 'Grimoire', 'Sacoche à composantes', 'Sac d\'érudit'],
               'Pack (b)': ['Dague', 'Grimoire', 'Focalisateur arcanique', 'Sac d\'explorateur']}
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
            'Traits. Sens aiguisés *',
            'Ascendance féerique (AV aux JdS vs charme et la magie ne peut pas vous endormir)',
            'Transe (4h de méditation remplacent 8h de sommeil)',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
        competences=[],
        nombre_competences_race=0,
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
            'Traits. Sens aiguisés *',
            'Ascendance féerique (AV aux JdS vs charme et la magie ne peut pas vous endormir)',
            'Transe (4h de méditation remplacent 8h de sommeil)',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Magie drow (Vous connaissez le sort mineur lumières dansantes. Lorsque vous atteignez le niveau 3, vous pouvez lancer le sort lueurs féeriques une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Lorsque vous atteignez le niveau 5, vous pouvez lancer le sort ténèbres une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Le Charisme est votre caractéristique d\'incantation pour ces sorts.)',
            'Entraînement aux armes elfiques *',
            'Entraînement aux armes drows.'
            'Sensibilité au soleil. Vous avez un désavantage aux jets d\'attaque et aux jets de Sagesse (Perception) basés sur ​​la vue quand vous, la cible de l\'attaque ou ce que vous essayez de détecter est exposé à la lumière du soleil.'
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
        competences=[],
        nombre_competences_race=0,
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
            'Traits. Sens aiguisés *',
            'Ascendance féerique (AV aux JdS vs charme et la magie ne peut pas vous endormir)',
            'Transe (4h de méditation remplacent 8h de sommeil)',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        bonus={'Dextérité': 2, 'Intelligence': 1},
        competences=[],
        nombre_competences_race=0,
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
            'Traits. Résistance naine (AV aux JdS vs poison)',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre (bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre)',
            'Formation au port des armures naines'
        ],
        bonus={'Force': 2, 'Constitution': 2},
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
            'Chanceux (Lorsque vous obtenez un 1 au dé d\'un jet d\'attaque, de caractéristique ou de sauvegarde, vous pouvez relancer le dé et devez alors utiliser ce nouveau résultat.)',
            'Brave (Vous avez un avantage aux jets de sauvegarde pour ne pas être effrayé.)',
            'Agilité halfeline (Vous pouvez passer dans l\'espace de toute créature d\'une taille supérieure à la vôtre.)'
            'Discrétion naturelle. (Vous pouvez tenter de vous cacher si vous vous trouvez derrière une créature d\'une taille supérieure à la vôtre.)'
        ],
        bonus={'Dextérité': 2, 'Charisme':1},
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
            'Chanceux (Lorsque vous obtenez un 1 au dé d\'un jet d\'attaque, de caractéristique ou de sauvegarde, vous pouvez relancer le dé et devez alors utiliser ce nouveau résultat.)',
            'Brave (Vous avez un avantage aux jets de sauvegarde pour ne pas être effrayé.)',
            'Agilité halfeline (Vous pouvez passer dans l\'espace de toute créature d\'une taille supérieure à la vôtre.)'
            'Résistance des robustes (Vous obtenez un avantage aux jets de sauvegarde contre le poison et la résistance contre les dégâts de poison.)'
        ],
        bonus={'Dextérité': 2, 'Constitution':1},
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
            'Traits. Résistance naine (AV aux JdS vs poison)',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre (bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre)',
            'Ténacité naine (Votre maximum de points de vie augmente de 1 à chaque niveau.)'
        ],
        bonus={'Constitution': 2, 'Sagesse':1},
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
            'Vitesse. 7.5 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique et une langue au choix',
            'Ascendance féerique (Vous avez un avantage aux jets de sauvegarde contre les effets de charme et la magie ne peut pas vous endormir.)',
            'Polyvalence  (Vous gagnez la maîtrise de deux compétences de votre choix.)'
        ],
        bonus={'Charime': 2, 'Au choix':1, 'Au choix':1},
        competences=competences_completes,
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

# Création des comboboxes pour les classes, races et historiques
classe_combobox = ttk.Combobox(onglet_classe, values=list(classes.keys()), state="readonly")
classe_combobox.pack(pady=10)

race_combobox = ttk.Combobox(onglet_race, values=list(races.keys()), state="readonly")
race_combobox.pack(pady=10)

historique_combobox = ttk.Combobox(onglet_historique, values=list(historiques.keys()), state="readonly")
historique_combobox.pack(pady=10)

# Binding des comboboxes pour mettre à jour les détails et les choix
classe_combobox.bind("<<ComboboxSelected>>", lambda event: [personnage.reset_selected_values(), personnage.reset_comboboxes(), afficher_details_classe(), personnage.update_display(), personnage.update_maitrise(), update_options()])
race_combobox.bind("<<ComboboxSelected>>", lambda event: [personnage.reset_selected_values(), personnage.reset_comboboxes(), afficher_details_race(), personnage.update_display(), personnage.update_maitrise()])
historique_combobox.bind("<<ComboboxSelected>>", lambda event: [personnage.reset_selected_values(), personnage.reset_comboboxes(), afficher_details_historique(), personnage.update_maitrise()])

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

# Bouton de validation
tk.Button(onglet_caracteristiques, text="Valider répartition", command=personnage.valider_repartition).grid(row=20, column=2, columnspan=2, pady=10)

# Appeler update_display pour initialiser les valeurs à l'affichage
personnage.update_display()

# Widgets pour l'onglet Maîtrise
maitrise_frame = tk.Frame(onglet_maitrise)
maitrise_frame.pack(pady=10, fill="x")

# Widgets pour l'onglet Options
options_frame = tk.Frame(onglet_options)
options_frame.pack(pady=10, fill="x")

# Bouton pour enregistrer le personnage
def enregistrer_personnage():
    selected_values_print = "\n".join(personnage.selected_values)
    messagebox.showinfo("Enregistrement", f"Personnage enregistré avec succès!\nCompétences sélectionnées:\n{selected_values_print}")

enregistrer_button = tk.Button(fenetre, text="Enregistrer le personnage", command=enregistrer_personnage)
enregistrer_button.pack(pady=10)

# Fonctions pour afficher les détails
def afficher_details_classe():
    classe_selectionnee = classe_combobox.get()
    if classe_selectionnee:
        description = classes[classe_selectionnee].description
        details = classes[classe_selectionnee].details
        capacites = classes[classe_selectionnee].capacites
        details_str = '\n'.join(details)
        capacites_str = '\n'.join(capacites)
        classe_details_label.config(text=f'Description:\n{description}\n\nDétails de la Classe:\n{details_str}\n\nCapacités de la Classe:\n{capacites_str}')

def afficher_details_race():
    race_selectionnee = race_combobox.get()
    if race_selectionnee:
        description = races[race_selectionnee].description
        details = races[race_selectionnee].details
        details_str = '\n'.join(details)
        race_details_label.config(text=f'Description:\n{description}\n\nDétails de la Race:\n{details_str}')

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

# Fonction pour afficher les menus déroulants des sorts mineurs et de niveau 1
def afficher_sorts_connus():
    # Effacer les widgets existants (pour permettre la mise à jour lors du changement de classe/race)
    for widget in onglet_sorts_connus.winfo_children():
        widget.destroy()

    # Ajouter la description générale
    description_label = tk.Label(
        onglet_sorts_connus,
        text="Déterminez les sorts connus du personnage (pas les sorts mémorisés), comme les sorts du grimoire d'un magicien ou les sorts mineurs d'un clerc.",
        wraplength=700,
        justify=tk.LEFT
    )
    description_label.pack(pady=10, anchor="w")

    # Ajouter le titre "Sort mineur"
    sort_mineur_label = tk.Label(onglet_sorts_connus, text="Sort mineur", font=('Arial', 12, 'bold'))
    sort_mineur_label.pack(pady=5, anchor="w")

    # Frame pour les menus déroulants des sorts mineurs
    sort_mineur_frame = tk.Frame(onglet_sorts_connus)
    sort_mineur_frame.pack(anchor="w", pady=5, padx=5)

    # Extraire les sorts mineurs et le nombre de sorts disponibles
    classe_selectionnee = classe_combobox.get()
    race_selectionnee = race_combobox.get()

    sorts_mineurs = []
    nombre_de_sorts_mineurs = 0

    if classe_selectionnee:
        sorts_mineurs.extend(personnage.classes[classe_selectionnee].sort_mineur_classe)
        nombre_de_sorts_mineurs += personnage.classes[classe_selectionnee].nombre_sort_mineur_classe

    if race_selectionnee:
        sorts_mineurs.extend(personnage.races[race_selectionnee].sort_race)
        nombre_de_sorts_mineurs += personnage.races[race_selectionnee].nombre_sort_race

    # Variable pour stocker les choix déjà sélectionnés
    selected_sort_mineur_values = []

    # Fonction pour mettre à jour les autres menus déroulants après une sélection
    def update_sort_mineur_options():
        for combobox in sort_mineur_comboboxes:
            current_value = combobox.get()
            values = [sort['nom'] for sort in sorts_mineurs]
            updated_values = [value + " (déjà sélectionné)" if value in selected_sort_mineur_values and value != current_value else value for value in values]
            combobox['values'] = updated_values

    # Si aucun sort mineur n'est disponible, afficher un message
    if nombre_de_sorts_mineurs == 0:
        no_sorts_label = tk.Label(onglet_sorts_connus, text="Aucun sort mineur disponible pour cette classe/race.", font=('Arial', 10))
        no_sorts_label.pack(pady=10, anchor="w")
    else:
        # Liste pour stocker les comboboxes de sorts mineurs
        sort_mineur_comboboxes = []

        # Créer les menus déroulants pour les sorts mineurs
        for i in range(nombre_de_sorts_mineurs):
            if i % 4 == 0:  # Créer une nouvelle ligne après 4 menus déroulants
                row_frame = tk.Frame(sort_mineur_frame)
                row_frame.pack(anchor="w", pady=5)
            sort_combobox = ttk.Combobox(row_frame, values=[sort['nom'] for sort in sorts_mineurs], state="readonly")
            sort_combobox.pack(side=tk.LEFT, padx=5, pady=5)

            sort_mineur_comboboxes.append(sort_combobox)

            # Lier la fonction à l'événement de sélection d'un sort
            sort_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=sort_combobox: afficher_details_sort_mineur(event, combobox))

    # Créer un label pour afficher les détails des sorts mineurs
    sort_mineur_details_labels = [tk.Label(onglet_sorts_connus, text="", justify=tk.LEFT, wraplength=700) for _ in range(2)]
    for label in sort_mineur_details_labels:
        label.pack(pady=5, anchor="w")

    # Ajouter le titre "Sort de niveau 1"
    sort_niveau_un_label = tk.Label(onglet_sorts_connus, text="Sort de niveau 1", font=('Arial', 12, 'bold'))
    sort_niveau_un_label.pack(pady=15, anchor="w")

    # Frame pour les menus déroulants des sorts de niveau 1
    sort_niveau_un_frame = tk.Frame(onglet_sorts_connus)
    sort_niveau_un_frame.pack(anchor="w", pady=5, padx=5)

    # Extraire les sorts de niveau 1 et le nombre de sorts disponibles
    sorts_niveau_un = []
    nombre_de_sorts_niveau_un = 0

    if classe_selectionnee:
        sorts_niveau_un.extend(personnage.classes[classe_selectionnee].sort_niveau_un_classe)
        nombre_de_sorts_niveau_un += personnage.classes[classe_selectionnee].nombre_sort_niveau_un_classe

    # Variable pour stocker les choix déjà sélectionnés
    selected_sort_niveau_un_values = []

    # Fonction pour mettre à jour les autres menus déroulants après une sélection
    def update_sort_niveau_un_options():
        for combobox in sort_niveau_un_comboboxes:
            current_value = combobox.get()
            values = [sort['nom'] for sort in sorts_niveau_un]
            updated_values = [value + " (déjà sélectionné)" if value in selected_sort_niveau_un_values and value != current_value else value for value in values]
            combobox['values'] = updated_values

    # Si aucun sort de niveau 1 n'est disponible, afficher un message
    if nombre_de_sorts_niveau_un == 0:
        no_sorts_niveau_un_label = tk.Label(onglet_sorts_connus, text="Aucun sort de niveau 1 disponible pour cette classe/race.", font=('Arial', 10))
        no_sorts_niveau_un_label.pack(pady=10, anchor="w")
    else:
        # Liste pour stocker les comboboxes de sorts de niveau 1
        sort_niveau_un_comboboxes = []

        # Créer les menus déroulants pour les sorts de niveau 1
        for i in range(nombre_de_sorts_niveau_un):
            if i % 4 == 0:  # Créer une nouvelle ligne après 4 menus déroulants
                row_frame = tk.Frame(sort_niveau_un_frame)
                row_frame.pack(anchor="w", pady=5)
            sort_combobox = ttk.Combobox(row_frame, values=[sort['nom'] for sort in sorts_niveau_un], state="readonly")
            sort_combobox.pack(side=tk.LEFT, padx=5, pady=5)

            sort_niveau_un_comboboxes.append(sort_combobox)

            # Lier la fonction à l'événement de sélection d'un sort
            sort_combobox.bind("<<ComboboxSelected>>", lambda event, combobox=sort_combobox: afficher_details_sort_niveau_un(event, combobox))

    # Créer un label pour afficher les détails des sorts de niveau 1
    sort_niveau_un_details_labels = [tk.Label(onglet_sorts_connus, text="", justify=tk.LEFT, wraplength=700) for _ in range(2)]
    for label in sort_niveau_un_details_labels:
        label.pack(pady=5, anchor="w")

    # Fonction pour afficher les détails d'un sort mineur sélectionné
    def afficher_details_sort_mineur(event, combobox):
        sort_name = combobox.get()
        sort_info = next((sort for sort in sorts_mineurs if sort['nom'] == sort_name), None)
        if sort_info:
            # Ajouter le choix à la liste des sélections et mettre à jour les menus déroulants
            selected_sort_mineur_values.append(sort_name)
            update_sort_mineur_options()

            # Afficher la description et effacer la plus ancienne si nécessaire
            sort_mineur_details_labels[1].config(text=sort_mineur_details_labels[0].cget("text"))
            sort_mineur_details_labels[0].config(
                text=f"Nom : {sort_info['nom']}\nType : {sort_info['type'].capitalize()}\nDescription : {sort_info['description']}"
            )

    # Fonction pour afficher les détails d'un sort de niveau 1 sélectionné
    def afficher_details_sort_niveau_un(event, combobox):
        sort_name = combobox.get()
        sort_info = next((sort for sort in sorts_niveau_un if sort['nom'] == sort_name), None)
        if sort_info:
            # Ajouter le choix à la liste des sélections et mettre à jour les menus déroulants
            selected_sort_niveau_un_values.append(sort_name)
            update_sort_niveau_un_options()

            # Afficher la description et effacer la plus ancienne si nécessaire
            sort_niveau_un_details_labels[1].config(text=sort_niveau_un_details_labels[0].cget("text"))
            sort_niveau_un_details_labels[0].config(
                text=f"Nom : {sort_info['nom']}\nType : {sort_info['type'].capitalize()}\nDescription : {sort_info['description']}"
            )

# Mettre à jour les sorts connus lors du changement de classe/race et réinitialiser les sélections
def reset_sorts_selection():
    global selected_sort_mineur_values, selected_sort_niveau_un_values
    selected_sort_mineur_values = []
    selected_sort_niveau_un_values = []
    afficher_sorts_connus()

def update_caracteristiques_bonus():
        race_selectionnee = race_combobox.get()
    
    # Reset des bonus de caractéristiques
        personnage.reset_caracteristiques_bonus()
    
        if race_selectionnee == "Demi-elfe":
        # Ajouter automatiquement +2 en Charisme
            personnage.ajouter_bonus_caracteristique("Charisme", 2)
        
        # Ajouter deux menus déroulants pour sélectionner les autres caractéristiques
            for i in range(2):
                caract_choice = ttk.Combobox(maitrise_frame, values=["Force", "Dextérité", "Constitution", "Intelligence", "Sagesse"])
                caract_choice.grid(row=i, column=1)
                caract_choice.bind("<<ComboboxSelected>>", lambda event, idx=i: personnage.ajouter_bonus_caracteristique(caract_choice.get(), 1))
            

# Lancement de la boucle principale
fenetre.mainloop()