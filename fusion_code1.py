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
        score -= player_lives # loose point for the bomb
    else:
        score += 1 # gain 1 points for each fruit
    return score 


# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit, speed_multiplier=1):
    data[fruit] = {
        'img': pygame.image.load('images/' + fruit + '.png'),
        'x': random.randint(0, WIDTH - 100),  # Position the fruit across the entire width of the screen
        'y': HEIGHT,  # Initialize fruits at the bottom of the screen
        'speed_x': random.randint(-10, 10) * speed_multiplier,  # Speed ​​in x for a diagonal movement
        'speed_y': -random.randint(45, 55) * speed_multiplier,  # Vertical speed to make them go up
        't': 0,
        'hit': False,
        'throw': random.random() >= 0.75
    }

def update_fruit_position(value):
    value['x'] += value['speed_x']
    value['y'] += value['speed_y']
    value['speed_y'] += (1 * value['t'])  # Simulate the gravity effect
    value['t'] += 1

    # Reverse vertical speed direction after reaching the top of the screen
    if value['y'] <= 0:  # If the fruit reaches the top of the screen
        value['speed_y'] = abs(value['speed_y'])  # Bring the fruits back down
    elif value['y'] >= HEIGHT:  # If the fruit reaches the bottom of the screen
        value['speed_y'] = -abs(value['speed_y'])  # Bringing up the fruits  
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
   

def Light_level():
    global game_running, game_over, first_round, player_lives, score, start_time, speed_multiplier, score_text

   # Initialize the time counter and speed multiplier
    start_time = pygame.time.get_ticks()
    speed_multiplier = 1 # Constant initial velocity
    score = 0  # Initialize the score
    score_text = font.render('Score : ' + str(score), True, WHITE)  # Initialize the score_text
def Hard_level():
    global game_running, game_over, first_round, player_lives, score, start_time, speed_multiplier, score_text
    # Initialize the time counter and speed multiplier
    start_time = pygame.time.get_ticks()
    speed_multiplier = 2 # Slow initial speed
    score = 0
    score_text = font.render('Score : ' + str(score), True, WHITE)  # Initialize score_text


def show_menu():
    gameDisplay.blit(background, (0, 0))
    draw_text(gameDisplay, "FRUIT NINJA!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay, "Press 1 for Light Level", 40, WIDTH / 2, HEIGHT / 2)
    draw_text(gameDisplay, "Press 2 for Hard Level", 40, WIDTH / 2, HEIGHT / 2 + 50)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    waiting = False
                    Light_level()
                elif event.key == pygame.K_2:
                    waiting = False
                    Hard_level()

# Show main menu
show_menu()     
    
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
        start_time = pygame.time.get_ticks() # Reset time counter
        speed_multiplier = 1 # Reset speed multiplier 
        speed_text = font.render('Score :' + str(score), True, WHITE)

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False  
            # Add more actions for specific keys here  

    # Gradually increase the speed of the fruits every 10 seconds
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000 # Elapsed time in seconds
    if elapsed_time > 10:
        speed_multiplier += 0.1  # Increase speed slightly
        start_time = pygame.time.get_ticks()  # Reset time counter       

    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            update_fruit_position(value)
            value['x'] += value['speed_x']          #moving the fruits in x-coordinates
            value['y'] += value['speed_y']          #moving the fruits in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                        #increasing speed_y for next loop

            if value['y'] <= HEIGHT:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
            else:
                 if value['y'] > HEIGHT:
                    if value['hit']: 
                        generate_random_fruits(key, speed_multiplier) # Return the fruit to its original state with the new speed
                    else:
                        generate_random_fruits(key, speed_multiplier) # Generate new fruit with new speed   

            current_position = pygame.mouse.get_pos()
            # Dictionary to map keyboard keys to fruits
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
                   if os.path.exists(half_fruit_path):
                       value['img'] = pygame.image.load(half_fruit_path) # Replace the image of the fruit with the image of half of the fruit
                   else:
                       print(f"Image not found: {half_fruit_path}")    
               score = calculate_points(key, score) #Score Update    
               score_text = font.render('Score : ' + str(score), True, WHITE)
               value['hit'] = True   
            # Keyboard key collision detection
            keys = pygame.key.get_pressed()
            for k, fruit in key_fruit_map.items():
                if keys[k] and key == fruit:
                    if key == 'bomb':
                        game_over = True
                    else:
                        half_fruit_path = 'images/half_' + key + '.png'
                        if os.path.exists(half_fruit_path):
                            value['img'] = pygame.image.load(half_fruit_path) # Replace the image of the fruit with the image of half of the fruit
                        else:
                            print(f"Image not found: {half_fruit_path}")    
                    score = calculate_points(key, score) #Update Score    
                    score_text = font.render('Score : ' + str(score), True, WHITE)  
                    value['hit'] = True   
                        
        else:
            generate_random_fruits(key, speed_multiplier)   
            
    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the second)


pygame.quit()
sys.exit()

