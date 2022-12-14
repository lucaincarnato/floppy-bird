import pygame 
from sys import exit
from player import Floppy
from obstacle import Usb

# Method to check collisions
def collision():
    # If usb group is not empty and the collision mask is true gameover
    # Collision mask is preferred to make the space between usb available
    if usb.sprites():
        if pygame.sprite.collide_mask(floppy.sprite,usb.sprites()[0]):
            usb.empty()
            return False
    return True

# Function to register the score
def score_detection():
    # Score in the game
    score_font = pygame.font.Font('Assets/scorefont.ttf',90)
    score_surf = score_font.render(f'{score}',False,(0,0,0))
    score_rect = score_surf.get_rect(center = (200,75))
    screen.blit(score_surf,score_rect)
    # The collision will return True for the entire time the two sprite have contact
    if pygame.sprite.spritecollide(floppy.sprite,usb,False):
        return 1
    return 0

# Method to display the score in the main page
def score_main():
    score_font_main = pygame.font.Font('Assets/titlefont.ttf',90)
    score_surf_main = score_font_main.render(f'{score}',False,(0,0,0))
    score_rect_main = score_surf_main.get_rect(center = (200,230))
    screen.blit(score_surf_main,score_rect_main)
    

pygame.init()
screen = pygame.display.set_mode((400,700))
game_icon = pygame.image.load('Assets/icon.png')
pygame.display.set_caption('Floppy bird')
pygame.display.set_icon(game_icon)
clock = pygame.time.Clock()
score = 0
collision_score = 0
game_state = False

# Sky and Ground surface
sky = pygame.image.load('Assets/sky.png').convert()
ground = pygame.image.load('Assets/ground.png').convert()

# Messages for the main page
title_font = pygame.font.Font('Assets/titlefont.ttf',90)
title_surf = title_font.render('Floppy Bird',False,(31,30,30))
title_rect = title_surf.get_rect(center = (200,230))

# Icon of the game
icon_surface = pygame.image.load('Assets/floppy/floppy1.png').convert_alpha()
icon_surface = pygame.transform.rotozoom(icon_surface,0,2)
icon_rectangle = icon_surface.get_rect(center = (200,370))

# Istruction in case score != 0
istruction_font = pygame.font.Font('Assets/titlefont.ttf',50)
istruction_surf = istruction_font.render('Press space to play',False,(0,0,0))
istruction_rect = istruction_surf.get_rect(center = (200,475))

# Credits
credit_font = pygame.font.Font('Assets/titlefont.ttf',23)
credit_surf = credit_font.render('Made by Luca Maria Incarnato',False,(0,0,0))
credit_rect = credit_surf.get_rect(midbottom = (200,680))

# USB image for the main page
usb_image = pygame.image.load('Assets/usb/usb4.png').convert_alpha()
usb_image = pygame.transform.rotozoom(usb_image,0,2)
usb_image_rect = usb_image.get_rect(center = (200,350))

# Initializing the floppy Sprite Group
floppy = pygame.sprite.GroupSingle()
floppy.add(Floppy())

# Initializing the Sprite Group
usb = pygame.sprite.Group()

# Timer to render multiple usb
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,4000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT
            exit()

        if game_state:
            # Render a new usb if the timer ticks
            if event.type == obstacle_timer:
                usb.add(Usb())
        else:
            # If pressed space 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # The game will be activated and score will be zero
                game_state = True
                score = 0

    if game_state:
        # Sky and Ground on screen
        screen.blit(sky,(0,0))
        screen.blit(ground,(0,600))

        # Drawing and updating the Floppy on the screen
        floppy.draw(screen)
        floppy.update()

        # Drawing and updating the usb on the screen
        usb.draw(screen)
        usb.update()

        # Changing the game state depending on collisions
        game_state = collision()
        # The function will increment the collision score up to 91/92
        collision_score += score_detection()
        # When collision score is 91, so the collision is finished, the score will increment and the collision score goes to zero
        if collision_score == 91:
            score += 1
            collision_score = 0

    else: 
        # Finished the game the collision score goes to zero for the next game
        collision_score = 0
        screen.fill((171,205,239))
        screen.blit(usb_image,usb_image_rect)
        if score == 0:
            screen.blit(title_surf,title_rect)
        else:
            score_main()
        screen.blit(icon_surface,icon_rectangle)
        screen.blit(istruction_surf,istruction_rect)
        screen.blit(credit_surf,credit_rect)

    pygame.display.update()
    clock.tick(60)

# ! The score does not increment correctly