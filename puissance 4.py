# -*- coding: utf-8 -*-
from tkinter import *
import random

# Déclaration des variables globales
player = 0
game_grid = [['' for _ in range(7)] for _ in range(6)]  # Grille de jeu

def pile_ou_face():
    P1 = 0
    P2 = 1
    resultat = random.randint(0, 1)
    if resultat == P1:
        return 0  # Joueur 1 commence
    else:
        return 1  # Joueur 2 commence

def init_ui():
    """
    Initialise la fenêtre avec la bibliothèque tkinter
    """
    global frame, canvas, winner_label

    # Fenêtre tkinter
    frame = Tk()
    frame.title("Puissance 4")
    frame.geometry("600x500")

    # Zone de dessin
    canvas = Canvas(frame, width=600, height=400)
    canvas.pack()

    # Label pour afficher le gagnant
    winner_label = Label(frame, text="", font=("Arial", 14))
    winner_label.pack()

def init_game_grid():
    """
    Initialise la grille de jeu.
    """
    global text_label

    # Label contenant le joueur actuel
    text_label = StringVar()
    label = Label(canvas, textvariable=text_label, height=1, width=5).place(x=450, y=0)

    # Lignes
    for i in range(9):
        x = i * 50
        canvas.create_line(x, 0, x, 300, width=2)

    # Colonnes
    for j in range(7):
        y = j * 50
        canvas.create_line(50, y, 400, y, width=2)

def update_game_grid():
    """
    Met à jour l'affichage des pions dans la grille.
    """
    for line in range(len(game_grid)):  # Ligne
        for column in range(len(game_grid[0])):  # Colonne
            if game_grid[line][column] != '':  # Case vide ?
                # Couleur du pion
                if game_grid[line][column] == 'X':  # Joueur 1
                    color = "red"
                else:  # Joueur 2
                    color = "yellow"

                # Calcul des coordonnées
                x1 = column * 50 + 55
                y1 = line * 50 + 5
                x2 = x1 + 40
                y2 = y1 + 40

                # Dessine le pion
                canvas.create_oval(x1, y1, x2, y2, fill=color, outline="black")

def column_select():
    """
    Initialise les boutons pour la sélection de la colonne et met à jour le texte.
    """
    if player == 0:
        text_label.set("Rouge")
    elif player == 1:
        text_label.set("Jaune")

    for i in range(7):
        Button(canvas, text=str(i+1), command=lambda col=i: select_column(col)).place(x=65 + i*50, y=325)

def gravity(column):
    """
    Détermine la première ligne vide où un pion peut être placé dans une colonne donnée.
    """
    line = -1
    for i in range(len(game_grid)):
        if game_grid[i][column] == '':
            line = i
    return line

def select_column(col):
    """
    Place un pion dans la colonne choisie.
    """
    global player
    line = gravity(col)
    if line != -1:
        if player == 0:
            game_grid[line][col] = 'X'
        else:
            game_grid[line][col] = 'O'

        update_game_grid()

        # Vérification du gagnant
        winner = check_winner(game_grid)
        if winner:
            winner_label.config(text="Le joueur " + ('rouge' if winner == 'X' else 'jaune') + " à gagné !")
        else:
            # Changement de joueur
            player = 1 if player == 0 else 0
            column_select()

def check_winner(board):
    rows = len(board)
    cols = len(board[0])

    # Vérification des lignes
    for row in range(rows):
        for col in range(cols - 3):
            if board[row][col] != '' and board[row][col] == board[row][col+1] == board[row][col+2] == board[row][col+3]:
                return board[row][col]

    # Vérification des colonnes
    for col in range(cols):
        for row in range(rows - 3):
            if board[row][col] != '' and board[row][col] == board[row+1][col] == board[row+2][col] == board[row+3][col]:
                return board[row][col]

    # Vérification des diagonales montantes
    for row in range(3, rows):
        for col in range(cols - 3):
            if board[row][col] != '' and board[row][col] == board[row-1][col+1] == board[row-2][col+2] == board[row-3][col+3]:
                return board[row][col]

    # Vérification des diagonales descendantes
    for row in range(rows - 3):
        for col in range(cols - 3):
            if board[row][col] != '' and board[row][col] == board[row+1][col+1] == board[row+2][col+2] == board[row+3][col+3]:
                return board[row][col]

    return None  # Aucun gagnant pour le moment

# Initialisation de l'interface graphique
init_ui()
init_game_grid()

# Détermine qui commence la partie
player = pile_ou_face()

# Lancement du jeu
column_select()

frame.mainloop()
