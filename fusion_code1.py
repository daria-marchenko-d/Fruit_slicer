import pygame 
import sys
import os
import random

player_lives = 3                                                #keep track of lives
score = 0                                                       #keeps track of score
fruits = ['apple', 'orange', 'lemon', 'kiwi', 'watermelon', 'bomb', 'ice' ]    #entities in the game

# initialize pygame and create window
WIDTH = 800
HEIGHT = 500
FPS = 10                                                #controls how often the gameDisplay should refresh. In our case, it will refresh every 1/12th second
pygame.init()
pygame.display.set_caption('Fruit-Ninja Game -- DataFlair')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #setting game display size
clock = pygame.time.Clock()

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

background = pygame.image.load('Images/background.png')                               #game background
background =pygame.transform.scale(background, (WIDTH, HEIGHT))
font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, WHITE)    #score display
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

        for event in pygame.event.get(): # Check all pygame events
            if event.type == pygame.QUIT: # If the user clicks on the window cross
                pygame.quit()

            if event.type == pygame.KEYUP: # If the user presses a key
               waiting = False # Exit the waiting loop       
                     #images that shows remaining lives
# Function to calculate points
def  calculate_points(fruit_type, score):
    if fruit_type == 'bomb':
        score -= 10 # loose point for the bomb
    else:
        score += 1 # gain 1 points for each fruit
    return score                     

# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    #fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load('images/' + fruit + '.png'),
        'x' : random.randint(100,500),          #where the fruit should be positioned on x-coordinate
        'y' : 800,
        'speed_x': random.randint(-10,10),      #how fast the fruit should move in x direction. Controls the diagonal movement of fruits
        'speed_y': random.randint(-90, -60),    #control the speed of fruits in y-directionn ( UP )
        'throw': False,                         #determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside, then it will be discarded
        't': 0,                               
        'hit': False,
        'throw': random.random() >= 0.75
    }

    #if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
       # data[fruit]['throw'] = True
   # else:
        #data[fruit]['throw'] = False

# Dictionary to hold the data the random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))

# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')

def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

                

# Game Loop
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
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
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False  

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #moving the fruits in x-coordinates
            value['y'] += value['speed_y']          #moving the fruits in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                         #increasing speed_y for next loop

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()
             # add keytouch
            key_fruit_map = {
                pygame.K_a: 'apple',
                pygame.K_o: 'orange',
                pygame.K_l: 'lemon',
                pygame.K_k: 'kiwi',
                pygame.K_w: 'watermelon',
                pygame.K_b: 'bomb',
                pygame.K_SPACE: 'ice'
            }
            # Mouse collision detection
            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x'] + 60 \
                and current_position[1] > value['y'] and current_position[1] < value['y'] + 60:
               if key == 'bomb':
                   game_over = True
               else:
                   half_fruit_path = 'images/half_' + key + '.png'
                   value['img'] = pygame.image.load(half_fruit_path) # Replace the image of the fruit with the image of half of the fruit
               score = calculate_points(key, score) #Score Update    
               score_text = font.render('Score : ' + str(score), True, WHITE)
               value['hit'] = True   
            # Keyboard key collision detection
            keys = pygame.key.get_pressed()
            for k, fruit in key_fruit_map.items():
                if keys[k] and key == fruit:
                    if keys == 'bomb':
                        game_over = True
                    else:
                        half_fruit_path = 'images/half_' + key + '.png'
                        value['img'] = pygame.image.load(half_fruit_path) # Replace the image of the fruit with the image of half of the fruit
                    score = calculate_points(key, score) #Update Score    
                    score_text = font.render('Score : ' + str(score), True, WHITE)  
                    value['hit'] = True         
        else:
            generate_random_fruits(key)                 
                

    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                        

pygame.quit()