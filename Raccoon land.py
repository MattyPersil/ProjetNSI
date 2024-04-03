#importation de tout le nécéssaire au bon fonctionnement du jeu
import pygame
import time
from liste_des_levels import *
from liste_des_minijeux import *
import copy
from random import randint as rnd
#initialisation de pygame 
pygame.init
pygame.font.init()
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption('Raccoon Land')



#création de la classe "Player" permettant de stocker les informations relatives au joueur
class Player:
    #initialisation
    def __init__(self):
        self.position_default = pygame.Vector2(44, 400)
        self.player_position = pygame.Vector2(44, 400)
        self.hp = 6
        self.image_left = pygame.transform.scale_by(pygame.image.load("assets/Player_left.png"), 0.1)
        self.image_right = pygame.transform.flip(self.image_left,flip_x=True,flip_y=False)
        self.current_image = self.image_right
        self.rect = self.image_right.get_rect(topleft=self.player_position)
        self.player_facing = 'right'
        self.velocity = (0,0)
        self.move_left = True
        self.move_right = True
        self.allow_move = True


    #fonction "get_rekt" permettant de mettre à jour le rect du joueur
    def get_rekt(self):
        self.rect = self.image_right.get_rect(topleft=self.player_position)

    #fonction "move" permettant le déplacement du joueur ainsi que le changement de son orientation
    def move(self,direction):
        if self.allow_move == True:
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
    def teleport(self, destination = None):
        if destination == None:
            self.position_default = pygame.Vector2(44, 400)
            destination = self.position_default
        self.player_position = destination
        self.velocity = (0,0)
    
    
#création de la classe "Backgroud" permettant de stocker les informations relatives au fond du jeu
class Background:
    #initialisation
    def __init__(self):
        self.dim = 0
        self.sky0 = pygame.transform.scale(pygame.image.load("assets/background world 1.png"),(1000,600))
        self.sky1 = pygame.transform.scale(pygame.image.load("assets/background world 2.png"),(1000,600))
        self.actual=self.sky0

    #fonction "switch" permettant d'alterner entre les dimensions
    def switch(self,player):
        if self.dim==0:
            self.actual=self.sky1
            self.dim=1
        else:
            self.actual=self.sky0
            self.dim=0
        player.velocity = (0,0)


#création de la classe "Blocks" contenant les informations sur tout les blocks
class Blocks:
    #initialsation
    def __init__(self):
        self.image_size = ((screen.get_width()/27)+1,(screen.get_height()/16)+1)
        self.dirt = pygame.transform.scale(pygame.image.load("assets/dirt.png"),self.image_size)
        self.stone = pygame.transform.scale(pygame.image.load("assets/Stone.png"),self.image_size)
        self.cloud = pygame.transform.scale(pygame.image.load("assets/cloud.png"),self.image_size)
        self.spike = pygame.transform.scale(pygame.image.load("assets/spike.png"), self.image_size)
        self.flowers = pygame.transform.scale(pygame.image.load("assets/flowers.png"),self.image_size)
        self.trashcan_f = pygame.transform.scale(pygame.image.load("assets/trashcan_f.png"),self.image_size)
        self.trashcan = pygame.transform.scale(pygame.image.load("assets/trashcan.png"),self.image_size)
        self.grassblock = pygame.transform.scale(pygame.image.load("assets/grassblock.png"),self.image_size)
        self.change_level_block = pygame.transform.scale(pygame.image.load("assets/Change Level.png"),self.image_size)

        self.helldirt = pygame.transform.scale(pygame.image.load("assets/helldirt.png"),self.image_size)
        self.helldirt2 = pygame.transform.scale(pygame.image.load("assets/helldirt 2.png"),self.image_size)
        self.hellstone = pygame.transform.scale(pygame.image.load("assets/hellstone.png"),self.image_size)
        self.hellspike = pygame.transform.scale(pygame.image.load("assets/hellspike.png"),self.image_size)
        self.helltrashcan = pygame.transform.scale(pygame.image.load("assets/helltrashcan.png"),self.image_size)
        self.hellgrassblock = pygame.transform.scale(pygame.image.load("assets/hellgrass.png"),self.image_size)
        self.hellflower = pygame.transform.scale(pygame.image.load("assets/hellflowers.png"),self.image_size)
        self.hellgrassblock2 = pygame.transform.scale(pygame.image.load("assets/hellgrass 2.png"),self.image_size)
        self.rects = []
        self.spikerect = [] 
        self.specialrect = None
        self.trashcanrect = None
        self.levels = [(level_test_1,level_test_2),
                       (level_2_world_1,level_2_world_2),
                       (level_3_world_1,level_3_world_2),
                       (level_4_world_1,level_4_world_2),
                       (level_5_world_1,level_5_world_2),
                       (level_6_world_1,level_6_world_2),
                       (level_7_world_1,level_7_world_2),
                       (level_8_world_1,level_8_world_2),
                       (level_9_world_1,level_9_world_2),
                       (level_10_world_1,level_10_world_2),
                       (level_11_world_1,level_11_world_2)]
        self.current_level = 0
    #fonction "randomizer" permettant de changer aléatoirement les blocs de terre dans le deuxieme monde
    def randomizer(self):
        for i in range(len(self.levels)):
            for ligne in range(len(self.levels[i][1])):
                for bloc in range(len(self.levels[i][1][ligne])):
                    if self.levels[i][1][ligne][bloc] == 1 and rnd(1,4)==4:
                        self.levels[i][1][ligne][bloc] = 7
                    if self.levels[i][1][ligne][bloc] == 2 and rnd(1,3) == 3:
                        self.levels[i][1][ligne][bloc] = 8

    #fonction "display" permettant d'afficher les blocs
    def display(self,dim,player):
        self.rects=[]
        self.specialrect = None
        self.spikerect = []
        w = self.levels[self.current_level][dim]
        
        y=1
        for i in w:
            x=1
            for n in i:
                if n == 1 or n == 7:        
                    if dim ==0:
                        screen.blit(self.dirt ,(x,y))
                    else:
                        if n==7:
                            screen.blit(self.helldirt,(x,y))
                        else:
                            screen.blit(self.helldirt2,(x,y))
                    self.rects.append(self.dirt.get_rect(topleft=(x,y)))
    
                if n == 2 or n == 8:
                    if dim == 0:
                        screen.blit(self.grassblock ,(x,y))
                    else:
                        if n ==2:
                            screen.blit(self.hellgrassblock2 ,(x,y))
                        else:
                            screen.blit(self.hellgrassblock, (x,y))
                    self.rects.append(self.grassblock.get_rect(topleft=(x,y)))
                if n == 3:
                    
                    if dim == 0:
                        screen.blit(self.stone ,(x,y))
                    else:
                        screen.blit(self.hellstone ,(x,y))
                    self.rects.append(self.stone.get_rect(topleft=(x,y)))
                if n == 4:
                    
                    if dim == 0:
                        screen.blit(self.flowers ,(x,y))
                    else:
                        screen.blit(self.hellflower ,(x,y))
                if n == 5:
                    screen.blit(self.cloud,(x,y))
                    self.rects.append(self.cloud.get_rect(topleft=(x,y)))
                if n == 6:
                    self.trashcanrect = self.trashcan.get_rect(topleft=(x,y))
                    if self.trashcanrect.colliderect(player.rect):
                        screen.blit(self.trashcan_f,(x,y))
                        
                    else:                    
                        if dim == 0:
                            screen.blit(self.trashcan ,(x,y))
                        else:
                            screen.blit(self.helltrashcan ,(x,y))                
                if n == 10:
                
                    if dim == 0:
                        screen.blit(self.spike ,(x,y))
                    else:
                        screen.blit(self.hellspike ,(x,y))
                    self.spikerect.append(self.spike.get_rect(topleft=(x,y)))
                if n == 9:
                    screen.blit(self.change_level_block,(x,y))
                    self.specialrect = self.change_level_block.get_rect(bottomleft=(x,y+self.image_size[1]))
                x+=self.image_size[0]-1
            y+=self.image_size[1]-1

#création de la classe "Counters" permettant d'afficher les informations tel que la vie du joueur et le nombre de poubelles collectés
class Counters:
    #initialisation
    def __init__(self,normal,normal_image,golden,golden_image,hp,font):
        self.unit = screen.get_height()/32
        self.normal_trash = normal
        self.normal_image = normal_image
        self.golden_trash = golden
        self.golden_image = golden_image
        self.hp = hp
        self.heart_full = pygame.transform.scale(pygame.image.load("assets/coeur plein.png"),(screen.get_width()/24,screen.get_width()/24))
        self.heart_half = pygame.transform.scale(pygame.image.load("assets/demi-coeur.png"),(screen.get_width()/24,screen.get_width()/24))
        self.heart_empty = pygame.transform.scale(pygame.image.load("assets/coeur vide.png"),(screen.get_width()/24,screen.get_width()/24))
        self.hearts = {"1": [self.heart_half,self.heart_empty,self.heart_empty],
                       "2": [self.heart_full,self.heart_empty,self.heart_empty],
                       "3": [self.heart_full,self.heart_half,self.heart_empty],
                       "4": [self.heart_full,self.heart_full,self.heart_empty],
                       "5": [self.heart_full,self.heart_full,self.heart_half],
                       "6": [self.heart_full,self.heart_full,self.heart_full]}
        self.font = font
    #fonction render_counters permettant d'afficher les compteurs
    def render_counters(self):
        coords = [self.unit,self.unit]
        for i in range(3):
            screen.blit(self.hearts[str(self.hp)][i],coords)
            coords[0] += self.unit+screen.get_width()/32

        coords = [self.unit,self.unit*2+screen.get_width()/32]

        screen.blit(self.normal_image,coords)
        text = self.font.render(str(self.normal_trash), False, (0, 0, 0))
        coords[0] = coords[0]*2+screen.get_width()/16
        screen.blit(text, coords) 

        coords = [self.unit,self.unit*3+screen.get_width()/32*1.5]
        coords = [self.unit,self.unit*3+screen.get_width()/32*1.5]
        screen.blit(self.golden_image,coords)
        text = self.font.render(str(self.golden_trash), False, (0, 0, 0))
        coords[0] = coords[0]*2+screen.get_width()/16
        screen.blit(text, coords)
    #fonction refresh permettant d'actualiser les compteurs 
    def refresh(self,normal,gold,hp):
        self.normal_trash = normal
        self.golden_trash = gold
        self.hp = hp

#création de la classe "Minigame Player" permettant de stocker les informations relatives au personnage du minijeu
class Minigame_player:
    #initialisation
    def __init__(self):
        self.minigame_player_image = pygame.transform.scale(pygame.image.load("assets/minigame_racoon.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.player_position = {'y' :14, 'x':1}
    #fonction render permettant d'afficher le player
    def render(self,image_size):
        screen.blit(self.minigame_player_image,(self.player_position['x']*(image_size[0]-1) +(5*image_size[0] + image_size[0]/2),self.player_position['y']*(image_size[0]-0.5)))

#création de la classe "Minigame_counters" permettant d'afficher et compter le nombre d'argent du jeu
class Minigame_counters:
    #initialisation
    def __init__(self,normal,golden):
        self.normal_image = normal
        self.normal_count = 0
        self.normal_coords = (screen.get_width()/5*4,screen.get_height()/16)
        self.golden_image = golden
        self.golden_count = 0
        self.golden_coords = (screen.get_width()/5*4,screen.get_height()/8)
        self.temp_counts ={'n':0,'g':0}
        self.font = pygame.font.SysFont('Comic Sans MS', 30)


    #fonction render_counters permettant d'afficher les compteurs
    def render_counters(self):
        screen.blit(self.normal_image,self.normal_coords)
        screen.blit(self.golden_image,self.golden_coords)
        text = self.font.render(str(self.normal_count), False, (0, 0, 0))
        screen.blit(text, (self.normal_coords[0]+screen.get_width()/24,self.normal_coords[1])) 
        text = self.font.render(str(self.golden_count), False, (0, 0, 0))
        screen.blit(text, (self.golden_coords[0]+screen.get_width()/24,self.golden_coords[1]))


#création de la classe "Minigame" permettant de stocker les informations relatives au minijeu 
class Minigame:
    #initialisation
    def __init__(self):
        self.mini_player = Minigame_player()
        self.mini_player_2 = Minigame_player()
        self.minigame_is_activated = False
        self.moving_wall_activation = True
        self.minigame_ground_image = pygame.transform.scale(pygame.image.load("assets/ground_minigame.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_wall_image = pygame.transform.scale(pygame.image.load("assets/Wall.png"),((screen.get_width()/27)+0.5,(screen.get_height()/16)+0.5))
        self.minigame_moving_wall_image = pygame.transform.scale(pygame.image.load("assets/moving_wall.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_button_image = pygame.transform.scale(pygame.image.load("assets/pizza.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_plate_image = pygame.transform.scale(pygame.image.load("assets/plate.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_trash_image = pygame.transform.scale(pygame.image.load("assets/normal_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_golden_trash_image = pygame.transform.scale(pygame.image.load("assets/golden_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_deadly_trash_image = pygame.transform.scale(pygame.image.load("assets/deadly_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_background = pygame.transform.scale(pygame.image.load("assets/ground.png"),(1000,600))
        self.minigame_levels = [level_1_mini,
                                level_2_mini,
                                level_3_mini,
                                level_4_mini,
                                level_5_mini,
                                level_6_mini,
                                level_7_mini,
                                level_8_mini,
                                level_9_mini,
                                level_10_mini,
                                level_11_mini,
                                level_12_mini]
        self.minigame_levels_copy = copy.deepcopy(self.minigame_levels)
        self.counters = Minigame_counters(self.minigame_trash_image,self.minigame_golden_trash_image)
    
    #fonction render permettant d'afficher le minijeu
    def render(self,image_size,actual_level):
        screen.blit(self.minigame_background,(0,0))
        y = 0
        for i in self.minigame_levels[actual_level]:
            x = 5*image_size[0] + image_size[0]/2
            for j in i:
                if j == 0:
                    screen.blit(self.minigame_ground_image,(x,y))
                if j == 1:
                    screen.blit(self.minigame_wall_image,(x,y))
                if j == 2:
                    screen.blit(self.minigame_ground_image,(x,y))
                if j == 10:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_plate_image,(x,y))
                if j == 3:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_button_image,(x,y))
                if j == 4:
                    if self.moving_wall_activation == True:
                        screen.blit(self.minigame_moving_wall_image,(x,y))
                    else:
                        screen.blit(self.minigame_ground_image,(x,y))
                if j == 6:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_trash_image,(x,y))
                if j == 7:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_golden_trash_image,(x,y))
                if j == 8:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_deadly_trash_image,(x,y))
                x+=image_size[0]-1
            y+=image_size[1]-1
        self.counters.render_counters()
        self.mini_player.render(image_size)
        self.mini_player_2.render(image_size)
    
    #fonction level_reset permettant de reset un level
    def level_reset(self,actual_level):
        self.minigame_levels = copy.deepcopy(self.minigame_levels_copy)
        self.mini_player.player_position = {'y' :14, 'x':1}
        self.counters.normal_count-=self.counters.temp_counts['n']
        self.counters.golden_count-=self.counters.temp_counts['g']
        self.counters.temp_counts = {'n':0,'g':0}


    #fonction move permettant de bouger le joueur dans le minijeu
    def move(self,keys,actual_level):
        level = self.minigame_levels[actual_level]

        if keys[pygame.K_r]:
            self.level_reset(actual_level)

        players = {self.mini_player:[pygame.K_RIGHT,pygame.K_LEFT,pygame.K_UP,pygame.K_DOWN],self.mini_player_2:[pygame.K_d,pygame.K_q,pygame.K_z,pygame.K_s]}

        for p,k in players.items():
            if keys[k[0]]:
                right_block = level[p.player_position['y']][p.player_position['x']+1]
                if right_block in [0,6,3,2,10,7]:
                    p.player_position['x'] += 1
                if right_block == 4 and self.moving_wall_activation == False:
                    p.player_position['x'] += 1

                    
            if keys[k[1]] :
                left_block = level[p.player_position['y']][p.player_position['x']-1]
                if left_block in [0,6,3,2,10,7]:
                    p.player_position['x'] -= 1
                if left_block == 4 and self.moving_wall_activation == False:
                    p.player_position['x'] -= 1
                
            if keys[k[2]]:
                upper_block = level[p.player_position['y']-1][p.player_position['x']]
                if upper_block in [0,6,3,2,10,7]:
                    p.player_position['y'] -= 1
                if upper_block == 4 and self.moving_wall_activation == False:
                    p.player_position['y'] -= 1

            if keys[k[3]]:
                lower_block = level[p.player_position['y']+1][p.player_position['x']]
                if lower_block in [0,6,3,2,10,7]:
                    p.player_position['y'] += 1
                if lower_block == 4 and self.moving_wall_activation == False:
                    p.player_position['y'] += 1

            time.sleep(0.1)
            actual_block = self.minigame_levels[actual_level][p.player_position['y']][p.player_position['x']]
            if actual_block == 6:
                self.minigame_levels[actual_level][p.player_position['y']][p.player_position['x']] =0
                self.counters.normal_count+=1
                self.counters.temp_counts['n'] +=1
            if actual_block == 7:
                self.minigame_levels[actual_level][p.player_position['y']][p.player_position['x']] =0
                self.counters.golden_count+=1
                self.counters.temp_counts['g'] +=1
            if actual_block == 3:
                self.moving_wall_activation = False
            if actual_block == 2 or actual_block == 10:
                self.minigame_levels[actual_level][p.player_position['y']][p.player_position['x']] =10
                self.moving_wall_activation = True



    

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
        self.minigame = Minigame()
        self.counters = Counters(self.minigame.counters.normal_count,
                                 self.minigame.counters.normal_image,
                                 self.minigame.counters.golden_count,
                                 self.minigame.counters.golden_image,
                                 self.player.hp,self.minigame.counters.font)
        
    #fonction "change_level" permettant de passer d'un niveau à un autre
    def change_level(self):
        self.blocs.current_level += 1
        self.minigame.mini_player.player_position = {'y' :14, 'x':1}
        self.minigame.counters.temp_counts = {'n':0,'g':0}
        self.player.teleport()
    
    #fonction "gravite_jeu" permettant de simuler la gravité du jeu
    def gravite_jeu(self,joueur):
        self.player.player_position.y += self.gravite+self.resistance

    #fonction "display" permettant d'afficher les elements du jeu
    def display(self):
        self.counters.refresh(self.minigame.counters.normal_count,self.minigame.counters.golden_count,self.player.hp)
        screen.blit(self.background.actual,(0,0))
        screen.blit(self.player.current_image,self.player.player_position)
        self.blocs.display(self.background.dim,self.player)
        self.counters.render_counters()
    
    #fonction spike_collision 
    def spike_collision(self):
        if self.player.hp>1:
            self.player.hp -= 1
        self.player.teleport()
        if self.background.dim == 1:
            self.background.switch(self.player)
        print(self.player.hp)
    
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

        for spike in self.blocs.spikerect:
            if spike.colliderect(self.player.rect):
                self.spike_collision()

        if self.collision == True:
            self.resistance =  -10
        else:
            self.resistance = 0

    #fonction minigame permettant d'activer le minijeu
    def minigame_activate(self,player):
        player.allow_move = False
        self.minigame.render(self.blocs.image_size,self.blocs.current_level)

world = World_data()
world.blocs.randomizer()
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
    if keys[pygame.K_p]:
        if world.player.allow_move == True:
            world.change_level()
            time.sleep(1)
    if keys[pygame.K_ESCAPE]:
        world.minigame.minigame_is_activated = False
    if keys[pygame.K_f]:
        if world.blocs.trashcanrect.colliderect(world.player.rect):
            world.minigame.minigame_is_activated = True
    if keys[pygame.K_m]:
        world.minigame.minigame_is_activated = True
    if world.minigame.minigame_is_activated == True:
        world.minigame_activate(world.player)
        world.minigame.move(keys,world.blocs.current_level)


    else:
        world.player.allow_move = True
        
    if world.player.allow_move == True:
        world.player.player_position.y -= world.player.velocity[0] * dt
        world.player.velocity = (world.player.velocity[0],world.player.velocity[1]-1)
        if world.player.velocity[1]==0:
            world.player.velocity=(0,0)

    if keys[pygame.K_j] or keys[pygame.K_e]:
        world.background.switch(world.player)
        time.sleep(0.15)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
"""
# à ajouter 

    
"""

class entity:
    #lieu de définition de toute les entités extérieur du joueur.
    def tortuto(x=0,y=0):
        self.tortuto_right = pygame.transform.scale(pygame.image.load("assets/tortuto right.png"),self.image_size)
        self.tortuto_left = pygame.transform.scale(pygame.image.load("assets/tortuto left.png"),self.image_size)