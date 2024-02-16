#importation de tout le nécéssaire au bon fonctionnement du jeu
import pygame
import time
from liste_des_levels import *

#initialisation de pygame 
pygame.init
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption('Raccoon Land')



#création de la classe "Player" permettant de stocker les informations relatives au joueur
class Player:
    #initialisation
    def __init__(self):
        self.player_position = pygame.Vector2(44, 400)
        self.hp = 3
        self.image_left = pygame.transform.scale_by(pygame.image.load("assets/Player_left.png"), 0.1)
        self.image_right = pygame.transform.flip(self.image_left)
        self.rect = self.image_right.get_rect(topleft=self.player_position)
        self.player_facing = 'right'
        self.velocity = (0,0)
        self.move_left = True
        self.move_right = True


    #fonction "get_rekt" permettant de mettre à jour le rect du joueur
    def get_rekt(self):
        self.rect = self.image_right.get_rect(topleft=self.player_position)

    #fonction "move" permettant le déplacement du joueur ainsi que le changement de son orientation
    def move(self,direction):
        if direction == 'right':
            if self.player_facing=='left':
                self.image=self.image_right
                self.player_facing='right'
            if self.move_right==True:
                self.player_position.x += 300 * dt
        elif direction =='left':
            if self.player_facing=='right':
                self.image=self.image_left
                self.player_facing='left'
            if self.move_left == True:
                self.player_position.x -= 300 * dt
    
#création de la classe "Backgroud" permettant de stocker les informations relatives au fond du jeu
class Background:
    #initialisation
    def __init__(self):
        self.dim = 0
        self.sky0 = pygame.transform.scale(pygame.image.load("assets/sky0.png"),(1000,600))
        self.sky1 = pygame.transform.scale(pygame.image.load("assets/sky1.png"),(1000,600))
        self.actual=self.sky0

    #fonction "switch" permettant d'alterner entre les dimensions
    def switch(self):
        if self.dim==0:
            self.actual=self.sky1
            self.dim=1
        else:
            self.actual=self.sky0
            self.dim=0

#création de la classe "Blocks" contenant les informations sur tout les blocks
class Blocks:
    #initialsation
    def __init__(self):
        self.image_size = ((screen.get_width()/27)+1,(screen.get_height()/16)+1)
        self.dirt = pygame.transform.scale(pygame.image.load("assets/dirt.png"),self.image_size)
        self.stone = pygame.transform.scale(pygame.image.load("assets/Stone.png"),self.image_size)
        self.cloud = pygame.transform.scale(pygame.image.load("assets/cloud.png"),self.image_size)
        self.flowers = pygame.transform.scale(pygame.image.load("assets/flowers.png"),self.image_size)
        self.trashcan = pygame.transform.scale(pygame.image.load("assets/trashcan.png"),self.image_size)
        self.grassblock = pygame.transform.scale(pygame.image.load("assets/grassblock.png"),self.image_size)
        self.change_level_block = pygame.transform.scale(pygame.image.load("assets/Change Level.png"),self.image_size)
        #self.spike = pygame.transform.scale(pygame.image.load("assets/pique.png"),self.image_size)
        self.rects = [] 
        self.specialrect = None
        self.levels = [(level_test_1,level_test_2),
                       (level_2_world_1,level_2_world_2),
                       (level_3_world_1,level_3_world_2),
                       (level_4_world_1,level_4_world_2),
                       (level_5_world_1,level_5_world_2),
                       (level_6_world_1,level_6_world_2),
                       (level_7_world_1,level_7_world_2),
                       (level_8_world_1,level_8_world_2)]
        self.current_level = 0

    #fonction "display" permettant d'afficher les blocs
    def display(self,dim):
        self.rects=[]
        self.specialrect = None
        w = self.levels[self.current_level][dim]
        
        y=1
        for i in w:
            x=1
            for n in i:
                if n == 1:
                    screen.blit(self.dirt ,(x,y))
                    self.rects.append(self.dirt.get_rect(topleft=(x,y)))
                if n == 2:
                    screen.blit(self.grassblock,(x,y))
                    self.rects.append(self.grassblock.get_rect(topleft=(x,y)))
                if n == 3:
                    screen.blit(self.stone,(x,y))
                    self.rects.append(self.grassblock.get_rect(topleft=(x,y)))
                if n == 4:
                    screen.blit(self.flowers,(x,y))
                if n == 5:
                    screen.blit(self.cloud,(x,y))
                    self.rects.append(self.grassblock.get_rect(topleft=(x,y)))
                if n == 6:
                    screen.blit(self.trashcan,(x,y))
                    self.rects.append(self.grassblock.get_rect(topleft=(x,y)))
                if n == 9:
                    screen.blit(self.change_level_block,(x,y))
                    self.specialrect = self.change_level_block.get_rect(topleft=(x,y))
                x+=self.image_size[0]-1
            y+=self.image_size[1]-1

#créat
"""
# à ajouter 

    def change_level(self):
        blocks.wld+=1
        player_1.player_position = pygame.Vector2(44, 400)


    self.gravite = 10
    self.resistance = 0
    def gravite_jeu(self,joueur):
        joueur.player_position.y += self.gravite+self.resistance

    
"""