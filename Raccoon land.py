#importation de pygame et mise en place des variables nécéssaires
import pygame
import time 
pygame.init
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption('Raccoon Land')
#pygame.display.set_icon(pygame.image.load("assets/Icon.png"))

#création de la classe player utilisée pour enregistrer le joueur 
#on définit le monde, où il est, sa barre de vie et son image
class Player:


    def __init__(self,position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2),world=0, hp = 3):
        self.player_position = position
        self.world = world
        self.hp = hp
        self.image_left = pygame.transform.scale_by(pygame.image.load("assets/Player_left.png"), 0.2)
        self.image_right = pygame.transform.scale_by(pygame.image.load("assets/Player_right.png"),0.2)
        self.image=self.image_right
        self.image_top = pygame.transform.rotate(self.image_right,90)
        self.rect = self.image.get_rect(topleft=self.player_position)
        self.player_facing = 'right'
        self.height = self.image.get_height()
        self.velocity = (0,0)


    #création de la fonction move permettant de bouger le joueur
    def getrect(self):
        self.rect = self.image.get_rect(topleft=self.player_position)

    def move(self, direction):

        if direction == 'right':
            if self.player_facing=='left':
                self.image=self.image_right
                self.player_facing='right'

            self.player_position.x += 300 * dt

        elif direction =='left':
            if self.player_facing=='right':
                self.image=self.image_left
                self.player_facing='left'

            self.player_position.x -= 300 * dt
            

class World:
    def __init__(self,monde=0):
        self.world=monde
        self.sky0 = pygame.image.load("assets/sky0.png")
        self.sky1 = pygame.image.load("assets/sky1.png")
        self.background=self.sky0

    def switch(self):
        if self.world==0:
            self.background=self.sky1
            self.world=1
        else:
            self.background=self.sky0
            self.world=0


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/ground.jpg")
        self.rect = self.image.get_rect()
        self.rect.y = 540
        self.gravite = (0,10)
        self.resistance = (0,0)

    def gravite_jeu(self,joueur):
        joueur.player_position.y += self.gravite[1]+self.resistance[1]
        
    
class  Platform(pygame.sprite.Sprite):
    def __init_(self):
        super().__init__()
        #self.image = pygame.image.lead("")
        self.rect.x = self.image.get_rect()
        self.rect.x = 580
        self.rect.y = 500

#création du joueur
player_1 = Player()
world = World()
ground = Ground()
platform=Platform()

#lancement du jeu
while running == True:
    # code permettant de fermer le jeu quand la fenetre est fermée 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

    screen.blit(world.background,(0,0))
    #pygame.draw.circle(screen, "blue", player_1.player_position, 40)
    screen.blit(ground.image, ground.rect)
    screen.blit(player_1.image, player_1.player_position)
    ground.gravite_jeu(player_1)
    player_1.getrect()
    if ground.rect.colliderect(player_1.rect):
        ground.resistance = (0,-10)
    else:
        ground.resistance =(0,0)
    #screen.blit(platform.image, platform.rect)

    #récupération des touches presséees 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player_1.move('right')
    if keys[pygame.K_q]:
        player_1.move('left')
    if keys[pygame.K_SPACE]:
        if ground.rect.colliderect(player_1.rect):
            player_1.velocity=(700,20)
        
    player_1.player_position.y -= player_1.velocity[0] * dt
    player_1.velocity = (player_1.velocity[0],player_1.velocity[1]-1)
    if player_1.velocity[1]!=0:
        player_1.image=player_1.image_top
    if player_1.velocity[1]==0:
        player_1.velocity=(0,0)

    if keys[pygame.K_j]:
        world.switch()
        time.sleep(0.1)

    pygame.display.flip()
    dt = clock.tick(60) / 1000



