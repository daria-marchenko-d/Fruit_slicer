import pygame
import sys
import os
import random
import json

# ----------------------------- Game display -------------------
player_lives = 3
score = 0
fruits = ['apple', 'orange', 'lemon', 'kiwi', 'watermelon', 'bomb', 'ice']

# Creating display window
WIDTH = 800
HEIGHT = 500
FPS = 20

pygame.init()
pygame.display.set_caption('FRUIT SLICER--DataFlair')
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 200, 50)

# ----------------------------------------------------------------Check or initialize the JSON file
if not os.path.exists("history.json"):
    with open("history.json", "w") as file: 
        json.dump({"scores": []}, file)  # Initialize with an empty structure

# ------------------------------- Background ------------------
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_name = pygame.font.match_font('comic.ttf')
font = pygame.font.Font(font_name, 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load('images/white_lives.png')


# Add sounds and music
music = pygame.mixer.music.load("sounds/music-game.mp3")
fail_sound = pygame.mixer.Sound("sounds/failfare.mp3")
click_sound = pygame.mixer.Sound("sounds/click.mp3")
explosion_sound = pygame.mixer.Sound("sounds/explosion.mp3")
jump_sound = pygame.mixer.Sound("sounds/jump.mp3")
cut_sound = pygame.mixer.Sound("sounds/slice.mp3")
time_sound = pygame.mixer.Sound("sounds/time-sound.mp3")
win_sound = pygame.mixer.Sound("sounds/fanfare.mp3")

pygame.mixer.music.play(-1)

# --------------------------------------------------------------------Function for button
def draw_button(x, y, width, height, text, default_color, hover_color, action=None, radius=15, padding=5):
    # Draws a button with hover and click effects
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(gameDisplay, hover_color, (x, y, width, height))
        # color = hover_color
        if click[0] == 1 and action is not None:
            click_sound.play()
            pygame.time.delay(150)
            action()
    else:
        # color = default_color
        pygame.draw.rect(gameDisplay, default_color, (x, y, width, height), border_radius=radius)


    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))  
    gameDisplay.blit(text_surface, text_rect)

# Languages
def change_language():
    print("")

# Menu languages
def menu_lang():
    running = True
    try:
        while running: 
            # Clear the screen each frame
                gameDisplay.blit(background, (0, 0))  

                # Corrected button positions (using numbers for coordinates)
                draw_button(300, 150, 200, 50, "English", YELLOW, GREEN)
                draw_button(300, 220, 200, 50, "French", YELLOW, GREEN)
                draw_button(300, 290, 200, 50, "Ukrainian", YELLOW, GREEN, change_language)
                draw_button(300, 360, 200, 50, "Main menu", YELLOW, GREEN, main_menu)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                clock.tick(FPS)
    except KeyboardInterrupt:
        print("Finish")

# ------------------------------- Fruits ----------------------
data = {}
def generate_random_fruits(fruit):
    smiley_path = f"images/{fruit}-smiley.png"
    sliced_path = f"images/{fruit}-sliced.png"
    
    data[fruit] = {
        'img_smiley': pygame.image.load(smiley_path),
        'img_sliced': pygame.image.load(sliced_path),
        'current_img': pygame.image.load(smiley_path),  
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-90, -60),
        'throw': random.random() >= 0.75,
        't': 0,
        'hit': False
    }

for fruit in fruits:
    generate_random_fruits(fruit)

def draw_lives(display, x, y, lives, image):
    for i in range(lives):
        img = pygame.image.load(image)
        img_rect = img.get_rect()
        img_rect.x = int(x + 35 * i)
        img_rect.y = y
        display.blit(img, img_rect)

def hide_cross_lives(x, y):
    pygame.draw.rect(gameDisplay, BLACK, (x, y, 35, 35))

def show_gameover_screen():
    print("Game Over")

def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)

def save_score(score):
    with open("highscores.json", "a") as file:
        json.dump({"score": score}, file)
        file.write("\n")

def load_highscores():
    try:
        with open("highscores.json", "r") as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []

def main_menu():
    print("Main Menu")

def play_sound(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()


# Initialize history
history = []


def write_json(name, bomb, lives, result):
    with open("history.json", "r+") as file:
        data = json.load(file)  # Charge les données existantes
        if name is None and lives is None and bomb is None:
            # Cas d'une expression brute
            data["scores"].append({
                "expression": result,  # Enregistre l'expression brute avec son résultat
                "result": result
            })
        else:
            # Cas classique
            data["scores"].append({
                "fails": bomb,
                "name": name,
                "lives": lives,
                "result": result
            })
        file.seek(0)  # Retourne au début du fichier
        json.dump(data, file, indent=4)  # Écrit les nouvelles données


def read_history():
    with open("history.json", "r") as file:
        data = json.load(file)  # Charge les données de l'historique
        if data["scores"]:
            print("\nScore History:")
            for calc in data["scores"]:
                if "expression" in calc:
                    # Affiche une expression brute
                    print(f"Expression: {calc['expression']} = {calc['result']}")
                else:
                    # Affiche un calcul classique
                    print(f"{calc['name: ']} {calc['fails']} {calc['lives']} = {calc['result']}")
        else:
            print("No scores found in history.")

# ---------------------------------------------------------------------Showing the menu

def main_menu():
    running = True
    try:
        while running:
            # Clear the screen each frame
            gameDisplay.blit(background, (0, 0))  

            # Corrected button positions (using numbers for coordinates)
            draw_button(300, 150, 200, 50, "The level", YELLOW, GREEN)
            draw_button(300, 220, 200, 50, "Play", YELLOW, GREEN)
            draw_button(300, 290, 200, 50, "Language", YELLOW, GREEN, menu_lang)
            draw_button(300, 360, 200, 50, "Exit", YELLOW, GREEN, quit_game)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
            clock.tick(FPS)
    except KeyboardInterrupt:
        print("Finish")
        
def quit_game():
    pygame.quit()
    sys.exit()
    
# ------------------------------ Game loop ------------------
first_round = True
game_over = True
game_running = True
while game_running:
    if game_over:
        if first_round:
            main_menu()  
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        
        if event.type == pygame.KEYDOWN:
            key_fruit_map = {
                pygame.K_a: 'apple',
                pygame.K_z: 'orange',
                pygame.K_e: 'lemon',
                pygame.K_q: 'kiwi',
                pygame.K_s: 'watermelon',
                pygame.K_d: 'bomb',
                pygame.K_SPACE: 'ice'
            }
            if event.key in key_fruit_map:
                fruit = key_fruit_map[event.key]
                if fruit in data and not data[fruit]['hit']:
                    data[fruit]['current_img'] = data[fruit]['img_sliced']  
                    data[fruit]['hit'] = True
                    score += 1  
                    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
    
    current_position = pygame.mouse.get_pos()
    for fruit, value in data.items():
        if not value['hit'] and value['x'] < current_position[0] < value['x'] + 30 and value['y'] < current_position[1] < value['y'] + 30:
            if fruit == 'bomb':
                player_lives -= 1
                if player_lives == 2:
                    hide_cross_lives(690, 15)
                elif player_lives == 1:
                    hide_cross_lives(725, 15)
                elif player_lives == 0:
                    hide_cross_lives(760, 15)
                    show_gameover_screen()
                    game_over = True
                half_fruit_path = "images/white_lives.png"
            else:
                half_fruit_path = "images/half_" + fruit + ".png"
            value['current_img'] = pygame.image.load(half_fruit_path)
            value['hit'] = True
            value['speed_x'] += 10
            if fruit != 'bomb':
                score += 1
            score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
    
    gameDisplay.blit(background, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
    
    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']
            value['y'] += value['speed_y']
            value['speed_y'] += (1 * value['t'])
            value['t'] += 1
            if value['y'] <= 850:
                gameDisplay.blit(value['current_img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
