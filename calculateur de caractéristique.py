import tkinter as tk
from tkinter import messagebox

# Points disponibles pour acheter les attributs
points_disponibles = 27

# Coût de chaque valeur d'attribut
costs = {8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9}

# Attributs initiaux à 8
attributs = {'Force': 8, 'Dextérité': 8, 'Constitution': 8, 'Intelligence': 8, 'Sagesse': 8, 'Charisme': 8}

# Fonction pour augmenter une valeur d'attribut
def augmenter_attribut(attribut):
    global points_disponibles
    if points_disponibles > 0:
        current_value = attributs[attribut]
        next_value = current_value + 1
        if next_value in costs:
            cost = costs[next_value] - costs[current_value]
            if cost <= points_disponibles:
                attributs[attribut] = next_value
                points_disponibles -= cost
                update_display()
            else:
                messagebox.showwarning("Attention", "Vous n'avez pas suffisamment de points pour augmenter cet attribut.")
        else:
            messagebox.showwarning("Attention", "Cette valeur d'attribut est au maximum permis.")

# Fonction pour diminuer une valeur d'attribut
def diminuer_attribut(attribut):
    global points_disponibles
    current_value = attributs[attribut]
    previous_value = current_value - 1
    if previous_value in costs:
        cost = costs[current_value] - costs[previous_value]
        attributs[attribut] = previous_value
        points_disponibles += cost
        update_display()
    else:
        messagebox.showwarning("Attention", "Cette valeur d'attribut est au minimum permis.")

# Fonction pour mettre à jour l'affichage des attributs et points disponibles
def update_display():
    for i, attribut in enumerate(attributs.keys()):
        attribut_labels[i].config(text=f"{attribut}: {attributs[attribut]}")
    points_label.config(text=f"Points restants: {points_disponibles}")

# Interface utilisateur avec Tkinter
root = tk.Tk()
root.title("Répartition des Points d'Attributs")

# Cadre pour les attributs et les boutons
frame_attributs = tk.Frame(root)
frame_attributs.pack(padx=20, pady=10)

# Affichage des attributs et boutons +/-
attribut_labels = []
for attribut in attributs:
    label = tk.Label(frame_attributs, text=f"{attribut}: {attributs[attribut]}")
    label.pack()
    attribut_labels.append(label)
    
    button_frame = tk.Frame(frame_attributs)
    button_frame.pack()
    
    plus_button = tk.Button(button_frame, text="-", command=lambda attr=attribut: diminuer_attribut(attr))
    plus_button.pack(side=tk.LEFT)
    
    minus_button = tk.Button(button_frame, text="-", command=lambda attr=attribut: diminuer_attribut(attr))
    minus_button.pack(side=tk.RIGHT)

# Affichage des points restants
points_label = tk.Label(root, text=f"Points restants: {points_disponibles}")
points_label.pack()

# Bouton de validation
def valider_repartition():
    global attributs, points_disponibles
    # Vérifier si tous les points ont été utilisés
    if points_disponibles == 0:
        # Masquer la fenêtre ou faire autre chose après validation
        messagebox.showinfo("Validation", "Répartition des points d'attributs validée.")
    else:
        messagebox.showwarning("Attention", "Vous devez utiliser tous les points disponibles pour valider la répartition.")

valider_button = tk.Button(root, text="Valider Répartition", command=valider_repartition)
valider_button.pack(pady=10)

# Lancer la fenêtre principale
root.mainloop()
