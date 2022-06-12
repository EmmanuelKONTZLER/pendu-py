#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      emman
#
# Created:     02/06/2022
# Copyright:   (c) emman 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import easygui
import random
from tkinter import *

## ----- Création de la fênetre de jeu -----

mainFenetre = Tk()

mainFenetre.title("Pendu")
mainFenetre.config(bg = "#dedede")
mainFenetre.geometry("400x600")
mainFenetre.resizable(0,0)

themeFrame = Frame (mainFenetre, bg = "#dedede")
themeFrame.pack(pady=20)


labelTheme = Label(themeFrame, text="THEME", bg = "#dedede")
labelTheme.pack()


niveauFrame = Frame (mainFenetre, bg = "#dedede")

clavierFrame = Frame (mainFenetre, bg = "#dedede")
clavierLigne1 = ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P"]
clavierLigne2 = ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"]
clavierLigne3 = ["W", "X", "C", "V", "B", "N"]

for lettre in clavierLigne1:
    Button(clavierFrame, text=lettre, width=20, command=lambda: chercheLettre(lettre)).grid(row=0, column=clavierLigne1.index(lettre))
for lettre in clavierLigne2:
    Button(clavierFrame, text=lettre, width=20, command=lambda: chercheLettre(lettre)).grid(row=1, column=clavierLigne2.index(lettre))
for lettre in clavierLigne3:
    Button(clavierFrame, text=lettre, width=20, command=lambda: chercheLettre(lettre)).grid(row=2, column=clavierLigne3.index(lettre)+2)
clavierFrame.grid_columnconfigure(0, weight=1)
clavierFrame.grid_columnconfigure(1, weight=1)
clavierFrame.grid_columnconfigure(2, weight=1)
clavierFrame.grid_columnconfigure(3, weight=1)
clavierFrame.grid_columnconfigure(4, weight=1)
clavierFrame.grid_columnconfigure(5, weight=1)
clavierFrame.grid_columnconfigure(6, weight=1)
clavierFrame.grid_columnconfigure(7, weight=1)
clavierFrame.grid_columnconfigure(8, weight=1)
clavierFrame.grid_columnconfigure(9, weight=1)


secretFrame = Frame(mainFenetre, bg = "#dedede")


## ----- Connexion à la database pour récupérer les thèmes et niveaux disponibles -----

import psycopg2
cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
crs = cnx.cursor()
## Execution des requêtes et enregistrement du resultat dans des variables
crs.execute('select * from tb_theme;')
vwtheme = crs.fetchall()
crs.execute('select * from tb_niveau;')
vwniveau = crs.fetchall()
## Fermeture de la connexion
crs.close()
cnx.close()




## ----- Définition des fonctions qui lancent le jeu -----
def pendu():
    ## Lance le pendu
     ## Définition des variables
      # Variables Globales qui seront appelées et modifiées dans des fonctions
    global pénalité
    pénalité = 0
    global messageErreur
    messageErreur = ""
    global word
    word = ""
    global niveau
    niveau = StringVar(value=0)


      # Variables locales -dans la fonction pendu()- qui ne seront pas modifiées dans les fonctions
    lettresProposées = []
    secret = ""
    win = False
    lost = False
    theme = StringVar(value=0)


    global boutonPlayFrame
    boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")

    global boutonPlay
    boutonPlay = Button(boutonPlayFrame, text="PLAY", bg = "#dedede")

    def afficheMotSecret():
        ## Affiche le mot mystère sous forme de "_" ou de lettres en lien avec le tableau de lettres proposées
        secret = ""
        for i in range(len(word)):
            lettreIncluse = False
            for j in range(len(lettresProposées)):
                if lettresProposées[j] == word[i]:
                    lettreIncluse = not lettreIncluse
                else:
                    lettreIncluse = lettreIncluse
            if lettreIncluse == True or word[i] == " ":
                secret += (word[i]+" ")
                lettreIncluse = not lettreIncluse
            else:
                secret += ("_ ")
        return secret



    def motMystere():
        global word, secret
        ## Récupère la liste de mots correspondant au niveau sélectionné et selectionne 1 de celui-ci comme mot mystère
        cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
        crs = cnx.cursor()
        crs.execute(f'select * from fx_mot2({niveau.get()});')
        dataMot = crs.fetchall()
        crs.close()
        cnx.close()
        word=list(dataMot[random.randint(0, len(dataMot)-1)])[0]
        secret = afficheMotSecret()
        boutonPlayFrame.destroy()
        niveauFrame.destroy()
        themeFrame.destroy()
        secretLabel = Label(secretFrame, text = secret, bg = "#dedede")
        secretLabel.pack()
        secretFrame.pack()
        clavierFrame.pack()





    def boutonPlay():
        ## Affiche un bouton PLAY fois le thème choisi pour déterminer le mot choisi
        global boutonPlayFrame
        boutonPlayFrame.destroy()
        boutonPlayFrame = Frame(mainFenetre, bg = "#dedede")
        boutonPlayFrame.pack(side = BOTTOM, pady=50)
        global boutonPlay
        boutonPlay = Button(boutonPlayFrame, text="PLAY", bg = "#dedede", command=motMystere)
        boutonPlay.pack()


    def choixNiveau():
        ## Propose les niveaux correspondant au thème selectionné
          # Connexion à la database pour récupérer les thèmes
        cnx = psycopg2.connect(host='localhost', port='5432', database='db_pendu', user='emmanuel', password='Tournevis@00')
        crs = cnx.cursor()
        crs.execute(f'select * from fx_niveau({theme.get()});')
        vwniveau = crs.fetchall()
        crs.close()
        cnx.close()
          # Destruction de la frame niveau au cas où l'utilisateur change de thème
        global mainFenetre
        global niveauFrame
        niveauFrame.destroy()
        global niveau
          # Sélectionne par défaut le premier niveau du thème sélectionné
        niveau = StringVar(value=vwniveau[0][0])
          #Création et affichage de la frame niveau
        niveauFrame = Frame (mainFenetre)
        niveauFrame.pack()
        labelNiveau = Label(niveauFrame, text="NIVEAU", bg = "#dedede")
        labelNiveau.pack()
        for n in vwniveau:
            Radiobutton(niveauFrame, text=str(list(n)[1]), bg = "#dedede", value= list(n)[0], variable = niveau, command=boutonPlay).pack()


    #Création et affichage de la frame thème
    for t in vwtheme:
        Radiobutton(themeFrame, text=str(list(t)[1]), bg = "#dedede", value= list(t)[0], variable = theme, command=choixNiveau).pack()





    mainFenetre.mainloop()







    def chercheLettre(n):
        ## Vérifie si la lettre renseignée est dans le mot, l'ajoute dans le tableau de lettres proposées incrémmente le compteur de pénalité le cas échéant
        global pénalité
        lettre=n
        messageErreur = ""

        pénalité = pénalité

        if len(lettre) != 1:
            messageErreur = "Veuillez renseigner 1 et une seule lettre"
            return messageErreur, pénalité
        elif ord(lettre.upper())<65 or ord(lettre.upper())>90:
            messageErreur = "Veuillez renseigner une lettre entre A et Z"
            return messageErreur, pénalité
        elif lettre in lettresProposées:
            messageErreur = "Vous avez déja proposé cette lettre"
            return messageErreur, pénalité
        else:
            letterIsInclude = lettre in word
            lettresProposées.append(lettre)
            if (not letterIsInclude):
                pénalité = pénalité + 1
            return messageErreur, pénalité


    def victoire():
        ## Vérifie si toutes les lettres du mot mystère ont été trouvées et passe le booléen de victoire à True le cas échéant
        victoire = False
        if secret.count("_") == 0:
            victoire = True
            print("Bravo vous avez gagné")
            ## msgbox ("Bravo, vous avez gagné", title = "pendu")
            easygui.msgbox(f"{word}\nBravo, vous avez gagné", "Le Pendu", "Ok !")
        return victoire

    def defaite():
        ## Vérifie si le compteur de pénalité a atteint le max et passe le booléen de défaite à True le cas échéant
        defaite = False
        if pénalité == 5:
            defaite = True
            print("Dommage, vous avez perdu")
            easygui.msgbox(f"{word}\nDommage, vous avez perdu", "Le Pendu", "Ok !")
        return defaite


    while (win == False and lost == False):
        ## Tant que le joueur n'a ni gagné, ni perdu, la boucle demande des lettres à l'utilisateur, vérifie si elle est contenue dans le mot mystère et les condition de victoire et défaite
        secret = afficheMotSecret()
        messageErreur, pénalité = chercheLettre()
        if messageErreur != "":
            easygui.msgbox(f"{messageErreur}")
            messageErreur = ""
        secret = afficheMotSecret()
        win = victoire()
        lost = defaite()








## ----- Lancement de la fonction jeu -----
pendu()