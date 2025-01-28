import pygame
import sys
import os
import random

# 1. Global variables
player_lives = 3  
score = 0  
fruits = ['apple', 'orange', 'kiwi', 'watermelon', 'lemon', 'ice', 'bomb']  
WIDTH = 800  
HEIGHT = 500  
FPS = 12  

# Colors defined using RGB tuples
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize the game
def init_game():
    global gameDisplay, clock, font, background, score_text, lives_icon
    pygame.init() 
    pygame.display.set_caption('FRUIT NINJA--DataFlair')  
    gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))  
    clock = pygame.time.Clock()  
    # Load resources
    background = load_image('back.jpg')  
    font = load_font('comic.ttf', 32)  
    score_text = font.render('Score : ' + str(score), True, WHITE)  
    lives_icon = load_image('images/white_lives.png')  

    # Fill the screen with a black background
    gameDisplay.fill(BLACK)

# Load an image with error handling
def load_image(path):
    try:
        return pygame.image.load(path)  
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")  
        sys.exit(1)  

# Load a font with error handling
def load_font(path, size):
    try:
        return pygame.font.Font(os.path.join(os.getcwd(), path), size)  
    except pygame.error as e:
        print(f"Error loading font {path}: {e}")  
        sys.exit(1)  

# Initialize the game
init_game()

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
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

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
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                value['hit'] = True
        else:
            generate_random_fruits(key)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()    

#Comment