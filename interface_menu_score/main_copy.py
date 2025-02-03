import pygame, sys
import os
import random
import json

player_lives = 3                                                #keep track of lives
score = 0                                                       #keeps track of score
fruits = ['melon', 'orange', 'pomegranate', 'guava', 'bomb']    #entities in the game

# initialize pygame and create window
WIDTH = 800
HEIGHT = 500
FPS = 12                                                 #controls how often the gameDisplay should refresh. In our case, it will refresh every 1/12th second
pygame.init()
pygame.display.set_caption("FRUIT SLICER")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))   #setting game display size
clock = pygame.time.Clock()

# Define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 200, 50)

# ----------------------------------------------------------------Check or initialize the JSON file
if not os.path.exists("history.json"):
    with open("history.json", "w", ensure_ascii=False, encoding='utf-8') as file: 
        json.dump({"scores": []}, file, indent=4)  # Initialize with an empty structure

# - Background
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
score_text = font.render('Score : ' + str(score), True, (255, 255, 255))    #score display
lives_icon = pygame.image.load('images/white_lives.png')                    #images that shows remaining lives


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

# Generalized structure of the fruit Dictionary
def generate_random_fruits(fruit):
    fruit_path = "images/" + fruit + ".png"
    data[fruit] = {
        'img': pygame.image.load(fruit_path),
        'x' : random.randint(100,500),          #where the fruit should be positioned on x-coordinate
        'y' : 800,
        'speed_x': random.randint(-10,10),      #how fast the fruit should move in x direction. Controls the diagonal movement of fruits
        'speed_y': random.randint(-80, -60),    #control the speed of fruits in y-directionn ( UP )
        'throw': False,                         #determines if the generated coordinate of the fruits is outside the gameDisplay or not. If outside, then it will be discarded
        't': 0,                                 #manages the
        'hit': False,
    }

    if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

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

# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)

# -Showing level menu
# Menu levels
def menu_level(language):
    running = True
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
    options = language["level"]
    y_positions = [200, 250, 300]
    selected_level = None

    while running:
        gameDisplay.blit(background, (0, 0))
        
        # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            print("Light level selected")
                            selected_level = "light"
                        elif index == 1:
                            print("Hard level selected")
                            selected_level = "hard"
                        elif index == 2:
                            # to go to the main menu
                            main_menu(language)
                            running = False
                            break
                        if selected_level:
                            running = False  # Break the cycle
                            break
        if not running: # If we need to go out from cycle
            break
    # if selected_level: # If level is selected, start the game
    #     start_game(selected_level)
    return selected_level

# show game over display & front display
def show_gameover_screen():
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT NINJA!", 90, WIDTH / 2, HEIGHT / 4)
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)

    draw_text(gameDisplay, "Press a key to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


# Rules
def rules(language):
    running = True
    while running:
        gameDisplay.blit(background, (0, 0))
        font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 22)
        options = language["rules"]  # Взяти правила з мови
        y_positions = [90, 130, 170, 210, 250, 290, 330, 370]

        for i, text in enumerate(options):
            text_rendered = font.render(text, True, BLACK)
            gameDisplay.blit(text_rendered, (200, y_positions[i]))

        # gameDisplay.blit(back_text_rendered, (back_text_x, back_text_y))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_x, mouse_y = event.pos
                if 200 < mouse_x < 500:  
                    if 370 < mouse_y < 450:
                        text_rendered = font.render(text, True, YELLOW)
                        main_menu(language) 
                        running = False

# Languages
def change_language(lang):
    with open("languages.json", "r", encoding="utf-8") as file:
        languages = json.load(file) 

    print(f"Language set to: {lang}") 
    return languages.get(lang, languages["en"])
# -------------------------------------------------------------------Showing Languages menu
# Menu languages
def menu_lang(language):
    running = True
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
    options = language["Language"]
    languages = ["en", "fr", "uk"]
    y_positions = [150, 200, 250, 300]

    while running:
        gameDisplay.blit(background, (0, 0))
        # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):     
                        if index == 3:  # "Go back"
                            return language  
                        else:
                            return languages[index]
                running = False       

def write_json(name, bomb, lives, result):
    with open("history.json", "r+", encoding='utf-8') as file:
        data = json.load(file)  
        if name is None and lives is None and bomb is None:
            # Cas d'une expression brute
            data["scores"].append({
                "name": name,  
                "result": result
            })
        else:
            # Cas classique
            data["scores"].append({
                "name": name,
                "lives": lives,
                "fails": bomb,
                "result": result
            })
        file.seek(0)  # Retourne au début du fichier
        json.dump(data, file, ensure_ascii=False, indent=4)  # Écrit les nouvelles données

def delete_history():
    with open("history.json", "w", encoding='utf-8') as file:
        json.dump({"scores": []}, file, indent=4)


# -------------------------------------------------------------------Showing scores history menu
def read_history():
            with open("history.json", "r", encoding='utf-8') as file:
                data = json.load(file)  # Charge les données de l'historique
                if data["scores"]:
                    print("\nScore History:")

                    # for calc in data["scores"]:
                    #     if "expression" in calc:
                    #         # Affiche une expression brute
                    #         print(f"Expression: {calc['expression']} = {calc['result']}")
                    #     else:
                    #         # Affiche un calcul classique
                    #         print(f"{calc['name: ']} {calc['fails']} {calc['lives']} = {calc['result']}")
                else:
                    print("No scores found in history.")

def menu_history(language):
    running = True
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)
    options = language["history"]
    y_positions = [200, 250]

    read_history()

    while running:
        gameDisplay.blit(background, (0, 0)) 
         # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        text_rects = []
        for i, text in enumerate(options):
            text_color = BLACK if y_positions[i] - 15 < mouse_y < y_positions[i] + 15 else YELLOW
            rendered_text = font.render(text, True, text_color)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))



        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        if index == 0:
                            delete_history()
                            print("The history is deleted")
                        elif index == 1:
                            main_menu(language)
                        running = False



# ---------------------------------------------------------------------Showing the menu
def main_menu(language):
    running = True
    font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 42)

    while running:
        options = language["menu"]
        y_positions = [100, 150, 200, 250, 300, 350]

        gameDisplay.blit(background, (0, 0)) 
         # Mouse coordinates
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Center text
        text_rects = []
        for i, text in enumerate(options):
            rendered_text = font.render(text, True, YELLOW)
            text_rect = rendered_text.get_rect(center=(WIDTH // 2, y_positions[i]))
            gameDisplay.blit(rendered_text, text_rect)
            text_rects.append((text_rect, i))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for text_rect, index in text_rects:
                    if text_rect.collidepoint(event.pos):
                        print(f"Main menu option {options[index]} selected.")
                        if index == 0:
                            selected_level = menu_level(language)
                            if selected_level:
                                show_gameover_screen()  
                        elif index == 1:
                            if 'level' not in locals():
                                level = menu_level(language)  # Choose the level
                            if level:
                                show_gameover_screen()
                        elif index == 2:
                            rules(language)
                        elif index == 3:
                            new_language = menu_lang(language)
                            if new_language != language:
                                language = change_language(new_language)  
                        elif index == 4:
                            menu_history(language)
                        elif index == 5:
                            quit_game(language)
                        # running = False
                        pygame.display.flip()
                        clock.tick(FPS)
        
def quit_game(language):
    pygame.quit()
    sys.exit()

# Game Loop
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
while game_running :
    if game_over :
        if first_round :
            language = change_language("en")
            main_menu(language)
            # show_gameover_screen()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
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

            current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

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
                    #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
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
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                        

pygame.quit()