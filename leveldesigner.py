import tkinter as tk
from functools import partial

fen = tk.Tk()
liste_boutons = []
color = ['white','brown','green']

#fonction clic
def clic(x,y):
    if liste_boutons[x][y]['bg']=='white':
        liste_finale[x][y]=1
        liste_boutons[x][y]['bg']='brown'
    elif liste_boutons[x][y]['bg']=='brown':
        liste_finale[x][y]=2
        liste_boutons[x][y]['bg']='green'
    elif liste_boutons[x][y]['bg']=='green':
        liste_finale[x][y]=3
        liste_boutons[x][y]['bg']='black'
    elif liste_boutons[x][y]['bg']=='black':
        liste_finale[x][y]=4
        liste_boutons[x][y]['bg']='yellow'
    elif liste_boutons[x][y]['bg']=='yellow':
        liste_finale[x][y]=5
        liste_boutons[x][y]['bg']='cyan'
    elif liste_boutons[x][y]['bg']=='cyan':
        liste_finale[x][y]=6
        liste_boutons[x][y]['bg']='blue'
    elif liste_boutons[x][y]['bg']=='blue':
        liste_finale[x][y]=9
        liste_boutons[x][y]['bg']='#8712E8'
    elif liste_boutons[x][y]['bg']=='#8712E8':
        liste_finale[x][y]=10
        liste_boutons[x][y]['bg']='#74E567'
    elif liste_boutons[x][y]['bg']=='#74E567':
        liste_finale[x][y]=0
        liste_boutons[x][y]['bg']='white'



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

quit_button = tk.Button(fen, text="Quit", command=quit)
quit_button.grid(column=0,row=17)

fen.mainloop()