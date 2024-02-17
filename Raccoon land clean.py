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
        self.image_right = pygame.transform.flip(self.image_left,flip_x=True,flip_y=False)
        self.current_image = self.image_right
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
                self.current_image=self.image_right
                self.player_facing='right'
            if self.move_right==True:
                self.player_position.x += 300 * dt
        elif direction =='left':
            if self.player_facing=='right':
                self.current_image=self.image_left
                self.player_facing='left'
            if self.move_left == True:
                self.player_position.x -= 300 * dt
    
    #fonction teleport changeant la position du joueur sur l'écran
    def teleport(self, coords = pygame.Vector2(44, 400)):
        self.player_position = coords
    
    
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

#création de la classe "World_data" contenant toutes les informations

class World_data:
    #initialisation
    def __init__(self):
        self.player = Player()
        self.background = Background()
        self.blocs = Blocks()
        self.gravite = 10
        self.resistance = 0
        self.collision = False

    #fonction "change_level" permettant de passer d'un niveau à un autre
    def change_level(self):
        self.blocs.current_level += 1
        self.player.teleport()
    
    #fonction "gravite_jeu" permettant de simuler la gravité du jeu
    def gravite_jeu(self,joueur):
        self.player.player_position.y += self.gravite+self.resistance

    #fonction "display" permettant d'afficher les elements du jeu
    def display(self):
        screen.blit(self.background.actual,(0,0))
        screen.blit(self.player.current_image,self.player.player_position)
        self.blocs.display(self.background.dim)
    
    #fonction "collisions" permettant de déctecter les collisions et agir en conséquence
    def collisions(self):
        self.collision = False
        left_collision = False
        right_collision = False
        #top_collision = False
        for bloc in self.blocs.rects:
            if bloc.colliderect(self.player.rect):
                self.collision = True

            bloc1 = bloc
            bloc2 = bloc
            bloc2.y+=5
            bloc1.y+=5
            bloc1.x-=5
            bloc2.x+=5
            if bloc1.colliderect(self.player.rect):
                left_collision = True
            if bloc2.colliderect(self.player.rect):
                right_collision=True

        if left_collision == True:
            self.player.move_left = False
            self.player.move_right = True
        if right_collision == True:
            self.player.move_right = False
            self.player.move_left = True
        if right_collision == True and left_collision == True:
            self.player.move_left = False
            self.player.move_right= False
        if right_collision == False and left_collision == False:
            self.player.move_left = True
            self.player.move_right = True
        
        
        if world.background.dim == 0:
            if self.blocs.specialrect.colliderect(self.player.rect):
                self.change_level()
        if self.collision == True:
            self.resistance =  -10
        else:
            self.resistance = 0


world = World_data()

#lancement du jeu 
while running == True:
    # code permettant de fermer le jeu quand la fenetre est fermée
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    #appel de la fonction display affichant tout le contenu du jeu
    world.display()
    #appel de la fonction "gravite_jeu" simulant la gravité
    world.gravite_jeu(world.player)
    #appel de la fonction "get_rekt" actualisant le rect du joueur
    world.player.get_rekt()
    #appel de la fonction "collisions" détéctant les collisions
    world.collisions()


    
    #récupération des touches presséees
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        world.player.move('right')
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        world.player.move('left')
    if keys[pygame.K_SPACE]:
        if world.collision==True:
            world.player.velocity=(700,20)


    world.player.player_position.y -= world.player.velocity[0] * dt
    world.player.velocity = (world.player.velocity[0],world.player.velocity[1]-1)
    if world.player.velocity[1]==0:
        world.player.velocity=(0,0)

    if keys[pygame.K_j] or keys[pygame.K_e]:
        world.background.switch()
        time.sleep(0.15)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
"""
# à ajouter 

    
"""