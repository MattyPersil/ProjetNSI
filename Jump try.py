import pygame
import time
pygame.init
screen = pygame.display.set_mode((1000,600))
clock = pygame.time.Clock()
running = True
dt = 0

y = screen.get_height()/16
x = screen.get_width()/27


image = pygame.transform.scale(pygame.image.load("assets/pizza.png"), (x,y))
ground =pygame.transform.scale(pygame.image.load("assets/ground.jpg"), (1000,600))
bg = pygame.transform.scale(pygame.image.load("assets/sky0.png"), (1000,600))
image_coords = [0,0]
image_rect = image.get_rect(topleft = image_coords)

#is_jumping = False
is_falling = True
ground_rect = ground.get_rect(topleft = (0,y*15))

movey = 0
collision_cd = 0

def collisions():
    global ground_rect,image_rect,collision_cd
    if collision_cd >0:
        collision_cd-=1
    else:
        if ground_rect.colliderect(image_rect):
            return True
        else:
            return False

def stick():
    pass
    """global ground_rect,image_rect
    while collisions()==True:
        image_rect.move(image_rect.x,image_rect.y-5)"""

def gravity():
    global image_rect, is_falling, movey
    if is_falling == True:
        movey += 1
    if collisions() == True:
        movey = 0
        stick()
        is_falling = False

def jump():
    global movey,is_falling,collision_cd
    if is_falling == False:
        is_falling = True
        movey = -20
        collision_cd = 5

while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
    image_rect = image.get_rect(topleft = image_coords)

    screen.blit(bg, (0,0))
    screen.blit(ground,ground_rect)
    screen.blit(image,image_rect)


    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        image_coords[0] += 300*dt
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        image_coords[0] -= 300*dt

    if keys[pygame.K_SPACE]:
       jump()

    gravity()

    image_coords[1] += movey

    pygame.display.flip()
    dt = clock.tick(60) / 1000