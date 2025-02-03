import pygame, sys
import os
import random
import json
import time

player_lives = 3                                                #keep track of lives
score = 0                                                        #keeps track of score
fruits = ['apple', 'orange', 'lemon', 'kiwi', 'watermelon', 'bomb', 'ice' ]    #entities in the game


# Configure the window
WIDTH = 800
HEIGHT = 500
FPS = 12

pygame.init()
pygame.display.set_caption("FRUIT SLICER")
gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
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


#------------------------------------------------------------------ Background
background = pygame.image.load("images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font = pygame.font.Font(os.path.join(os.getcwd(), 'comic.ttf'), 32)
# score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
lives_icon = pygame.image.load('images/red_lives.png')

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


# 2. Generalize structure of the fruit of the dictionnary
def generate_random_fruits(fruit, data):
    smiley_path = f"images/{fruit}-smiley.png"
    sliced_path = f"images/{fruit}-sliced.png"


    if os.path.exists(smiley_path) and os.path.exists(sliced_path):
        original_size = (200, 200) 
        data[fruit] = {
            'img_smiley': pygame.transform.scale(pygame.image.load(smiley_path), original_size),
            'img_sliced': pygame.transform.scale(pygame.image.load(sliced_path), original_size),
            'current_img': pygame.transform.scale(pygame.image.load(smiley_path), original_size),
            'x' : random.randint(100,500),
            'y' : 800,
            'speed_x': random.randint(-10,10),
            'speed_y': random.randint(-90, -60),
            'throw': random.random() >= 0.75,
            't': 0,
            'hit': False,
        }

    if random.random() >= 0.75:     #Return the next random floating point number in the range [0.0, 1.0) to keep the fruits inside the gameDisplay
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False

# # Dictionary to hold the data the random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit, data)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/white_lives.png"), (x, y))

# 3. Method to draw font 
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

# show game over display & front display
# -------------------------------------------------------------------Showing level menu
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

def start_game(level, language, player_lives, score, data):  # Add an argument level
    game_over = False
    player_lives = 3
    score = 0
    data.clear()
    combo_hits = 0
    time_paused = 0 
    frame_count = 0

    for fruit in fruits:
        generate_random_fruits(fruit, data)
    

    if level == "light":
        fruit_spawn_rate = 30
        for fruit in data:
            data[fruit]['speed_y'] = random.randint(-10, -40)
    elif level == "hard":
        fruit_spawn_rate = 15
        for fruit in data:
            data[fruit]['speed_y'] = random.randint(-100, -80)

    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))

    while not game_over:
        frame_count += 1

        if time_paused > 0:
            time_paused -= 1
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                key_fruit_map = {
                    pygame.K_a: 'apple',
                    pygame.K_o: 'orange',
                    pygame.K_l: 'lemon',
                    pygame.K_k: 'kiwi',
                    pygame.K_w: 'watermelon',
                    pygame.K_b: 'bomb',
                    pygame.K_SPACE: 'ice'
                }
                if event.key in key_fruit_map:
                    fruit = key_fruit_map[event.key]
                    if fruit in data and not data[fruit]['hit']:
                        data[fruit]['current_img'] = data[fruit]['img_sliced']
                        cut_sound.play()
                        data[fruit]['hit'] = True

                        if fruit == 'bomb':
                            explosion_sound.play()  
                            game_over = True  # end game
                            show_gameover_screen(score, player_lives, language)  # game over screen
                            return score, player_lives
                        
                        if fruit == 'ice':
                            time_paused = random.randint(3, 5) * FPS  #stop the time for 3/5sec
                            time_sound.play() 
                        else:
                            score += 1
                        score_text = font.render('Score : ' + str(score), True, (255, 255, 255))


                        if fruit != 'bomb':
                            score += 1
                        score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
                # if event.type == pygame.KEYDOWN:
                    # pygame.K_ESCAPE: show_gameover_screen()

        combo_hits = 0
        current_position = pygame.mouse.get_pos()
        for fruit, value in data.items():
            if not value['hit'] and value['x'] < current_position[0] < value['x'] + 30 and \
                    value['y'] < current_position[1] < value['y'] + 30:
                if fruit == 'bomb':
                    explosion_sound.play() 
                    player_lives -= 1
                    hide_cross_lives(player_lives)
                    if player_lives == 2:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1:
                        hide_cross_lives(725, 15)
                    elif player_lives == 0:
                        hide_cross_lives(760, 15)
                        game_over = True
                        show_gameover_screen(score, player_lives, language)  
                        return score, player_lives
                elif fruit == 'ice':
                        time_paused = random.randint(3, 5) * FPS  
                        time_sound.play()
                else:
                    value['current_img'] = data[fruit]['img_sliced']  # Change image
                    value['hit'] = True
                    if fruit != 'bomb':
                        combo_hits += 1
                    score_text = font.render('Score : ' + str(score), True, (255, 255, 255))

            if combo_hits > 1:
                score += combo_hits  # Додаємо бонусні очки за комбо
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))

        gameDisplay.blit(background, (0, 0))
        gameDisplay.blit(score_text, (0, 0))
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/white_lives.png')

        for key, value in data.items():
            if value['throw']:
                value['x'] += value['speed_x']
                value['y'] += value['speed_y']
                value['speed_y'] += (1 * value['t'])
                value['t'] += 1

                if value['y'] <= 850:
                    gameDisplay.blit(value['current_img'], (value['x'], value['y']))
                else:
                    generate_random_fruits(key, data)

        if frame_count % fruit_spawn_rate == 0:
            random_fruit = random.choice(fruits)
            generate_random_fruits(random_fruit, data)

        pygame.display.update()
        clock.tick(FPS)
    return score, player_lives  


def show_gameover_screen(score, player_lives, language):
    gameDisplay.blit(background, (0,0))
    draw_text(gameDisplay, "FRUIT SLICER!", 90, WIDTH / 2, HEIGHT / 4)
    draw_text(gameDisplay,"Score : " + str(score), 50, WIDTH / 2, HEIGHT /2)
    draw_text(gameDisplay, "Press 'ENTER' to begin!", 64, WIDTH / 2, HEIGHT * 3 / 4)
    draw_text(gameDisplay,"Go back: press 'm'" + str(score), 78, WIDTH / 2, HEIGHT /2)

    pygame.display.flip()

    waiting = True
    selected_level = None

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN]:
                waiting = False
            if event.type == pygame.KEYDOWN and event.key in [pygame.K_m]:
                waiting = False
                main_menu(language)
    if selected_level:
        score, player_lives = start_game(selected_level, language, player_lives, score, data)
        show_gameover_screen(score, player_lives, language)
    

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


# Scores history
# Initialize history
# history = []

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
                                start_game(selected_level, language, player_lives, score, data)  
                        elif index == 1:
                            if 'level' not in locals():
                                level = menu_level(language)  # Choose the level
                            if level:
                                start_game(level, language, player_lives, score, data)
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
# game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
language = change_language("en")
player_lives = 3  # Ініціалізуємо player_lives
score = 0  # Ініціалізуємо score
data = {} # Ініціалізуємо data

while game_running:
    if first_round:
        main_menu(language)
        first_round = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    level = menu_level(language)
    if level:
        score, player_lives = start_game(level, language, player_lives, score, data)
        show_gameover_screen(score, player_lives, language)

    pygame.display.update()
    clock.tick(FPS)      # keep loop running at the right speed (manages the frame/second. The loop should update afer every 1/12th pf the sec
                       

#  Last message with score


# Run the menu
language = change_language("en")
main_menu(language)    
pygame.quit()

if __name__ == '__main_menu__':
    main_menu()
