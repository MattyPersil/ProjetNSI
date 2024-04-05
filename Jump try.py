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

is_jumping = False
is_falling = True

movey = 0

def gravity():
    global is_falling,movey
    if is_falling == True:
        movey += 1

ground_rect = ground.get_rect(topleft = (0,y*10))

def jump():
    global is_jumping,is_falling,movey
    if is_jumping is False:
        is_falling = False
        is_jumping = True
        movey -= 33


def collisions():
    global ground_rect,image_rect,movey,is_falling
    if ground_rect.colliderect(image_rect):
        is_falling = False
        movey = 0
        """image_rect = image_rect.move(image_rect.x,ground_rect.top)"""
        image_rect.update((image_rect.x, ground_rect.y-image_rect.y))

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
    collisions()

    image_coords[1] += movey

    """
    if is_jumping and is_falling is False:
        is_falling = True
        movey -= 33  # how high to jump
    
    if image_rect.colliderect(ground_rect):
        ground_hit_list = [ground_rect]
    else :
        ground_hit_list = []

    for g in ground_hit_list:
        movey = 0
        image_rect.bottom = g.top
        is_jumping = False  # stop jumping
    """
    """
    for p in plat_hit_list:
        is_jumping = False
        movey = 0

        if image_rect.bottom <= p.top:
            image.rect.bottom = p.top
        else:
            movey += 3.2"""


    pygame.display.flip()
    dt = clock.tick(60) / 1000