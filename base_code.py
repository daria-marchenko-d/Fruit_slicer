import pygame
import sys
import os
import random

# 1. Creating display window
player_lives = 3
score = 0
fruits = ['apple', 'orange', 'watermelon', 'lemon', 'kiwi', 'ice', 'bomb']
WIDTH = 800
HEIGHT = 500
FPS = 12

pygame.init()
pygame.display.set_caption('FRUIT NINJA--DataFlair')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

gameDisplay.fill((BLACK))
background = pygame.image.load('Images/background.png')
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 32)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load('images/white_lives.png')

# Function to draw player lives

def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

# Function to hide lives with a cross

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y)) 

# Show end game screen  
def show_gameover_screen():
    gameDisplay.blit(background, (0, 0))         
    draw_text(gameDisplay, "FRUIT NINJA!", 64, WIDTH / 2, HEIGHT / 4)
    if not game_over:
        draw_text(gameDisplay, "Score:" + str(score), 40, WIDTH / 2, 250)
    draw_text(gameDisplay, "Press a key to begin!", 24, WIDTH /2, HEIGHT * 3 / 4)

    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)

        for envent in pygame.event.get(): # Check all pygame events
            if event.type == pygame.QUIT: # If the user clicks on the window cross
                pygame.quit()

            if event.type == pygame.KEYUP: # If the user presses a key
               waiting = False # Exit the waiting loop       

# 2. Generalize structure of the fruit of the dictionnary

def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),               
        'y' : 800,
        'speed_x': random.randint(-10,10),    
        'speed_y': random.randint(-80, -60),    
        'throw': False,                       
        't': 0,                               
        'hit': False,
    }

    if random.random() >= 0.75:     
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

# 3. Method to draw font 

font_name = pygame.font.match_font('comic.ttf')

def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)  

 # 4. Draw players lives

def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()      
        img_rect.x = int(x + 35 * i)   
        img_rect.y = y                 
        display.blit(img, img_rect)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))      

# 5. Show game over display & front display

def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 64, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 40, WIDTH / 2, 250)


    draw_text(gameDisplay, "Press a key to begin!", 24, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False   

#  Function to display end of game results and messages    
def display_final_result(points, remaining_lives):
    gameDisplay.blit (background, (0, 0))
    draw_text(gameDisplay, "Score Final : " + str(points), 48, WIDTH /2, HEIGHT / 4)  
    draw_text(gameDisplay, "Vies Perdues : " + str(3 - remaining_lives), 36, WIDTH / 2, HEIGHT / 2)  
    if points >= 50:
        message = "Ninja Expert !"
    elif points >= 30:
        message = "Well done!" 
    else: 
        message = "Keep training!"

    draw_text(gameDisplay, message, 42, WIDTH / 2, HEIGHT * 3 / 4)  
    pygame.display.flip()     

    waiting = True # Wait for player action to continue 
    while waiting:  
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False        

# Function to calculate points
def  calculate_points(fruit_type, score):
    if fruit_type == 'bomb':
        score -= 10 # loose point for the bomb
    else:
        score += 5 # gain 5 points for each fruit
    return score 

# 6. Game Loop

first_round = True
game_over = True        
game_running = True    
while game_running :
    if game_over :
        if first_round :
            show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/white_lives.png')
        score = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/white_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)
                  
                    if player_lives < 0 :
                        show_gameover_screen()
                        game_over = True

                    half_fruit_path = "images/explosion.png"
                else:
                    half_fruit_path = "images/" + "half_" + key + ".png"

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score = calculate_points(key, score) # Score update
                score_text = font.render('Score : ' + str(score), True, WHITE)
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()    
sys.exit