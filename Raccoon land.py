#importation de tout le nécéssaire au bon fonctionnement du jeu
import pygame
import time
from liste_des_levels import *
from liste_des_minijeux import *
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
        self.position_default = pygame.Vector2(44, 400)
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
        self.spike_cooldown = 0
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
        self.sky0 = pygame.transform.scale(pygame.image.load("assets/sky0.png"),(1000,600))
        self.sky1 = pygame.transform.scale(pygame.image.load("assets/sky1.png"),(1000,600))
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
        self.trashcan = pygame.transform.scale(pygame.image.load("assets/trashcan.png"),self.image_size)
        self.grassblock = pygame.transform.scale(pygame.image.load("assets/grassblock.png"),self.image_size)
        self.change_level_block = pygame.transform.scale(pygame.image.load("assets/Change Level.png"),self.image_size)
        #self.spike = pygame.transform.scale(pygame.image.load("assets/pique.png"),self.image_size)
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
                       (level_9_world_1,level_9_world_2)]
        self.current_level = 0

    #fonction "display" permettant d'afficher les blocs
    def display(self,dim):
        self.rects=[]
        self.specialrect = None
        self.spikerect = []
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
                    self.rects.append(self.stone.get_rect(topleft=(x,y)))
                if n == 4:
                    screen.blit(self.flowers,(x,y))
                if n == 5:
                    screen.blit(self.cloud,(x,y))
                    self.rects.append(self.cloud.get_rect(topleft=(x,y)))
                if n == 6:
                    screen.blit(self.trashcan,(x,y))
                    self.trashcanrect = self.trashcan.get_rect(topleft=(x,y))
                if n == 10:
                    screen.blit(self.spike,(x,y))
                    self.spikerect.append(self.spike.get_rect(topleft=(x,y)))
                if n == 9:
                    screen.blit(self.change_level_block,(x,y))
                    self.specialrect = self.change_level_block.get_rect(bottomleft=(x,y+self.image_size[1]))
                x+=self.image_size[0]-1
            y+=self.image_size[1]-1

#création de la classe "Minigame" permettant de stocker les informations relatives au minijeu 
class Minigame:
    #initialisation
    def __init__(self):
        self.minigame_player_image = None
        self.minigame_is_activated = False
        self.minigame_ground_image = pygame.transform.scale(pygame.image.load("assets/ground_minigame.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_wall_image = pygame.transform.scale(pygame.image.load("assets/Wall.png"),((screen.get_width()/27)+0.5,(screen.get_height()/16)+0.5))
        self.minigame_moving_wall_image = pygame.transform.scale(pygame.image.load("assets/moving_wall.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_button_image = pygame.transform.scale(pygame.image.load("assets/pizza.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_plate_image = None
        self.minigame_trash_image = pygame.transform.scale(pygame.image.load("assets/normal_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_golden_trash_image = pygame.transform.scale(pygame.image.load("assets/golden_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_deadly_trash_image = pygame.transform.scale(pygame.image.load("assets/deadly_trash.png"),((screen.get_width()/27)+1,(screen.get_height()/16)+1))
        self.minigame_background = pygame.transform.scale(pygame.image.load("assets/ground.png"),(1000,600))
        self.minigame_levels = [level_1_mini,level_2_mini,level_3_mini,level_4_mini]
    
    #fonction render permettant d'afficher le minijeu
    def render(self,image_size,actual_level):
        screen.blit(self.minigame_background,(0,0))
        y = 1
        for i in self.minigame_levels[actual_level]:
            x = 5*image_size[0] + image_size[0]/2
            for j in i:
                if j == 0:
                    screen.blit(self.minigame_ground_image,(x,y))
                if j == 1:
                    screen.blit(self.minigame_wall_image,(x,y))
                #if j == 2:
                    #screen.blit(self.minigame_plate_image,(x,y))
                if j == 3:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_button_image,(x,y))
                if j == 4:
                    screen.blit(self.minigame_moving_wall_image,(x,y))
                if j == 5:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_trash_image,(x,y))
                if j == 6:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_golden_trash_image,(x,y))
                if j == 7:
                    screen.blit(self.minigame_ground_image,(x,y))
                    screen.blit(self.minigame_deadly_trash_image,(x,y))
                x+=image_size[0]-1
            y+=image_size[1]-1
                    

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
    
    #fonction spike_collision 
    def spike_collision(self):
        if self.player.spike_cooldown == 0:
            self.player.spike_cooldown = 60
            self.player.hp -= 1
            self.player.velocity = (700,20)
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
        if self.blocs.trashcanrect.colliderect(self.player.rect):
            player.allow_move = False
            self.minigame.render(self.blocs.image_size,self.blocs.current_level)

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
    if keys[pygame.K_p]:
        if world.player.allow_move == True:
            world.change_level()
            time.sleep(1)
    if keys[pygame.K_f]:
        world.minigame.minigame_is_activated = True
    
    if world.minigame.minigame_is_activated == True:
        world.minigame_activate(world.player)
        
    if world.player.spike_cooldown > 1:
        world.player.spike_cooldown-=1
        
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