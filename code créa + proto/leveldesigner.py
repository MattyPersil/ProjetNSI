import tkinter as tk
from functools import partial

fen = tk.Tk()
liste_boutons = []
color = ['white','brown','green','black','yellow','cyan','blue','#8712E8','#74E567']
actual_color = color[0]
actual_button = 0

#fonction clic
def clic(x,y):
    liste_boutons[x][y]['bg']=actual_color
    if actual_color == 'white':
        liste_finale[x][y]=0

    elif actual_color == 'brown':
        liste_finale[x][y]=1

    elif actual_color == 'green':
        liste_finale[x][y]=2

    elif actual_color == 'black':
        liste_finale[x][y]=3

    elif actual_color == 'yellow':
        liste_finale[x][y]=4

    elif actual_color == 'cyan':
        liste_finale[x][y]=5

    elif actual_color == 'blue':
        liste_finale[x][y]=6

    elif actual_color == '#8712E8':
        liste_finale[x][y]=9

    elif actual_color == '#74E567':
        liste_finale[x][y]=10

def change_color(couleur,coor):
    global actual_button,actual_color
    print(actual_color)
    liste_boutons_2[actual_button]['text']=''

    actual_color = couleur
    liste_boutons_2[coor]['text']=actual_color
    actual_button = coor
"""
def lecteur_liste(liste):
    liste_bis = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    for i in liste:
        for n in range(len(i)):
            liste_bis[n].append(i[n])
    print(liste_bis)

    for i in range(27):
        for j in range(16):
            liste_boutons[i][j] = liste_bis[i][j]
    liste_finale= liste_bis
    """

def quit():
    global fen
    fen.quit()
    liste_f = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    for i in liste_finale:
        for n in range(len(i)):
            liste_f[n].append(i[n])

    print(liste_f)


liste_finale = []
for i in range(27):
    l1 =[]
    liste=[]
    for j in range(16):
        l1.append(0)
        liste.append(tk.Button(fen,text='',bg='white',width=4,height=2,command=partial(clic,i,j)))
        liste[-1].grid(column=i,row=j+1)
    liste_finale.append(l1)
    liste_boutons.append(liste)

    
liste_boutons_2 = []
for i in range(len(color)):
    bouton = tk.Button(fen,text='',bg=color[i],width=8,height=2,command=partial(change_color,color[i],i))
    liste_boutons_2.append(bouton)
    bouton.grid(column=27,row=i+1)

    

quit_button = tk.Button(fen, text="Quit", command=quit)
quit_button.grid(column=0,row=17)
"""liste_a_lire = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4,0, 0, 0], [2, 2, 2, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1], [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3]]
load_list_button = tk.Button(fen, text = "Load", command=partial(lecteur_liste,liste_a_lire))
load_list_button.grid(column = 1,row = 17)"""
fen.mainloop()