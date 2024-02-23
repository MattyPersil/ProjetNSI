import tkinter as tk
from functools import partial

fen = tk.Tk()
liste_boutons = []
liste_boutons_2 = []
liste_finale = []
colors = ['white','#939597','#BED3C3','#4A919E','#08C5D1','#00353F','#242423','#FCFE19','#BD3100']
actual_color = colors[0]
actual_button = 0

#fonction clic 
def clic(x,y):
    liste_boutons[y][x]['bg'] = actual_color
    liste_finale[y][x] = colors.index(actual_color)

def change_color(couleur,coor):
    global actual_color,actual_button
    print(actual_color)
    liste_boutons_2[actual_button]['text']=''
    actual_color = couleur
    liste_boutons_2[coor]['text']=actual_color
    actual_button = coor

def quit():
    global fen
    fen.quit()
    print(liste_finale)

for i in range(16):
    l1 = []
    liste = []
    for j in range(16):
        l1.append(0)
        liste.append(tk.Button(fen,text = '',bg = 'white',width=4,height=2,command=partial(clic,j,i)))
        liste[-1].grid(column = j,row = i+1)
    liste_finale.append(l1)
    liste_boutons.append(liste)

for i in range(len(colors)):
    bouton = tk.Button(fen,text='',bg=colors[i],width=8,height=2,command=partial(change_color,colors[i],i))
    liste_boutons_2.append(bouton)
    bouton.grid(column=16,row = i+1)

quit_button=tk.Button(fen,text='Quit',command=quit)
quit_button.grid(column=0,row=17)

fen.mainloop()
