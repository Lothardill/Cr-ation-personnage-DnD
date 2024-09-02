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
        for widget in maitrise_frame.winfo_children():
            widget.destroy()
        
        self.comboboxes = []
    
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
            nombre_competences_race = 0
            self.creer_menu_deroulant(competences_race, "Compétences de la race", maitrise_frame, nombre=nombre_competences_race)

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
 
        self.update_comboboxes()
        

        
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
            'Traits. Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
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
            'Traits. Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Cachette naturelle. Vous pouvez tenter de vous cacher dans une zone à visibilité réduite, comme en présence de branchages, de forte pluie, de neige qui tombe, de brume ou autre phénomène naturel.',
            'Magie drow. Vous connaissez le sort mineur lumières dansantes. Lorsque vous atteignez le niveau 3, vous pouvez lancer le sort lueurs féeriques une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Lorsque vous atteignez le niveau 5, vous pouvez lancer le sort ténèbres une fois avec ce trait et regagnez cette capacité lorsque vous terminez un repos long. Le Charisme est votre caractéristique d\'incantation pour ces sorts.',
            'Entraînement aux armes elfiques *',
            'Entraînement aux armes drows.'
            'Sensibilité au soleil. Vous avez un désavantage aux jets d\'attaque et aux jets de Sagesse (Perception) basés sur ​​la vue quand vous, la cible de l\'attaque ou ce que vous essayez de détecter est exposé à la lumière du soleil.'
        ],
        bonus={'Dextérité': 2, 'Sagesse': 1},
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
            'Traits. Sens aiguisés. Vous maîtrisez la compétence Perception.',
            'Ascendance féerique. AV aux JdS vs charme et la magie ne peut pas vous endormir',
            'Transe. 4h de méditation remplacent 8h de sommeil',
            'Entraînement aux armes elfiques *',
            'Sort mineur'
        ],
        bonus={'Dextérité': 2, 'Intelligence': 1},
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
            'Traits. Résistance naine (AV aux JdS vs poison)',
            'Entraînement aux armes naines',
            'Maîtrise des outils',
            'Connaissance de la pierre. Bonus de maîtrise x2 aux jets d\'Int (Histoire) en relation avec la pierre',
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
            'Chanceux. Lorsque vous obtenez un 1 au dé d\'un jet d\'attaque, de caractéristique ou de sauvegarde, vous pouvez relancer le dé et devez alors utiliser ce nouveau résultat.',
            'Brave. Vous avez un avantage aux jets de sauvegarde pour ne pas être effrayé.',
            'Agilité halfeline. Vous pouvez passer dans l\'espace de toute créature d\'une taille supérieure à la vôtre.'
            'Discrétion naturelle. Vous pouvez tenter de vous cacher si vous vous trouvez derrière une créature d\'une taille supérieure à la vôtre.)'
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
            'Vitesse. 9 m/round',
            'Vision. Vision dans le noir (18 m)',
            'Langues. Commun, Elfique et une langue au choix',
            'Ascendance féerique. Vous avez un avantage aux jets de sauvegarde contre les effets de charme et la magie ne peut pas vous endormir.',
            'Polyvalence.  Vous gagnez la maîtrise de deux compétences de votre choix.'
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

# Création des comboboxes pour les classes, races et historiques
classe_combobox = ttk.Combobox(onglet_classe, values=list(classes.keys()), state="readonly")
classe_combobox.pack(pady=10)

race_combobox = ttk.Combobox(onglet_race, values=list(races.keys()), state="readonly")
race_combobox.pack(pady=10)

historique_combobox = ttk.Combobox(onglet_historique, values=list(historiques.keys()), state="readonly")
historique_combobox.pack(pady=10)

# Binding des comboboxes pour mettre à jour les détails et les choix
classe_combobox.bind("<<ComboboxSelected>>", lambda event: [
    personnage.reset_selected_values(),
    personnage.reset_comboboxes(),
    afficher_details_classe(),
    personnage.update_display(),
    personnage.update_maitrise(),  # Réinitialise l'onglet Maîtrise
    update_options()
])

race_combobox.bind("<<ComboboxSelected>>", lambda event: [
    personnage.reset_selected_values(),
    personnage.reset_comboboxes(),
    afficher_details_race(),
    personnage.update_display(),
    personnage.update_maitrise()  # Réinitialise l'onglet Maîtrise
])

historique_combobox.bind("<<ComboboxSelected>>", lambda event: [
    personnage.reset_selected_values(),
    personnage.reset_comboboxes(),
    afficher_details_historique(),
    personnage.update_maitrise()  # Réinitialise l'onglet Maîtrise
])
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


# Variables pour stocker la race sélectionnée et les bonus de caractéristiques
race_choisie = tk.StringVar()
bonus_caracteristiques = {'Premier bonus': '', 'Deuxième bonus': ''}
attribut_combobox_1=[]
attribut_combobox_2=[]
attributs_disponibles=['Force','Dextérité','Constitution','Intelligence','Sagesse']

# Initialisation des comboboxes en dehors de la fonction on_race_change
def afficher_details_race():
    def update_attribut_comboboxes(event):
        selection_1 = attribut_combobox_1.get()
        selection_2 = attribut_combobox_2.get()

        options_1 = [attr for attr in attributs_disponibles if attr != selection_2]
        options_2 = [attr for attr in attributs_disponibles if attr != selection_1]

        attribut_combobox_1['values'] = options_1
        attribut_combobox_2['values'] = options_2

        if selection_1 in options_1:
            attribut_combobox_1.set(selection_1)
        else:
            attribut_combobox_1.set('')

        if selection_2 in options_2:
            attribut_combobox_2.set(selection_2)
        else:
            attribut_combobox_2.set('')

        bonus_caracteristiques['Premier bonus'] = attribut_combobox_1.get()
        bonus_caracteristiques['Deuxième bonus'] = attribut_combobox_2.get()

    def on_race_change(event):
        race_choisie.set(race_combobox.get())

        race_selectionnee = race_choisie.get()
        if race_selectionnee:
            description = races[race_selectionnee].description
            details = races[race_selectionnee].details
            details_str = '\n'.join(details)
            race_details_label.config(text=f'Description:\n{description}\n\nDétails de la Race:\n{details_str}')

            bonus_caracteristiques['Premier bonus'] = ''
            bonus_caracteristiques['Deuxième bonus'] = ''
            attribut_combobox_1.set('')
            attribut_combobox_2.set('')

            if race_selectionnee == "Demi-elfe":
                attributs_disponibles = ['Force', 'Dextérité', 'Constitution', 'Intelligence', 'Sagesse']

                titre_label = tk.Label(onglet_race, text="Choisissez vos bonus de caractéristique", font=('Arial', 12, 'bold'))
                titre_label.pack(pady=10)

                demi_elfe_frame = tk.Frame(onglet_race)
                demi_elfe_frame.pack(pady=10)

                tk.Label(demi_elfe_frame, text="Premier bonus", font=('Arial', 10, 'bold')).grid(row=0, column=0, padx=10)
                attribut_combobox_1.grid(row=1, column=0, padx=10, pady=5)

                tk.Label(demi_elfe_frame, text="Deuxième bonus", font=('Arial', 10, 'bold')).grid(row=0, column=1, padx=10)
                attribut_combobox_2.grid(row=1, column=1, padx=10, pady=5)

                attribut_combobox_1.bind("<<ComboboxSelected>>", update_attribut_comboboxes)
                attribut_combobox_2.bind("<<ComboboxSelected>>", update_attribut_comboboxes)

    # Initialisation des comboboxes ici pour qu'elles existent avant toute utilisation
    attribut_combobox_1 = ttk.Combobox(onglet_race, values=attributs_disponibles, state="readonly")
    attribut_combobox_2 = ttk.Combobox(onglet_race, values=attributs_disponibles, state="readonly")

    # Lier le changement de race à la fonction on_race_change
    race_combobox.bind("<<ComboboxSelected>>", on_race_change)

            

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



# Lancement de la boucle principale
fenetre.mainloop()