import pygame
import sys
import random
import json

# Ініціалізація Pygame
pygame.init()

# Загрузка JSON файлу з текстами для різних мов
with open('languages.json', 'r', encoding='utf-8') as f:
    languages = json.load(f)

# Вибір мови
current_language = "uk"

# Окна та шрифти
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption(languages[current_language]["title"])

font = pygame.font.SysFont('Arial', 30)
big_font = pygame.font.SysFont('Arial', 50)

# Статус гри
score = 0
strikes = 0
level = "Light level"
history = []

# Функція для відображення меню
def show_menu(menu_options, title=""):
    screen.fill((255, 255, 255))  # Очистити екран
    if title:
        title_surface = big_font.render(title, True, (0, 0, 0))
        screen.blit(title_surface, (300, 50))
    for i, option in enumerate(menu_options):
        text_surface = font.render(option, True, (0, 0, 0))
        screen.blit(text_surface, (350, 150 + i * 50))
    pygame.display.update()

# Функція для відображення правил
def show_rules():
    screen.fill((255, 255, 255))
    rules = languages[current_language]["rules"]
    for i, rule in enumerate(rules):
        text_surface = font.render(rule, True, (0, 0, 0))
        screen.blit(text_surface, (50, 100 + i * 40))
    pygame.display.update()

# Функція для відображення вибору мови
def show_language_menu():
    screen.fill((255, 255, 255))
    languages_list = languages[current_language]["Language"]
    for i, language in enumerate(languages_list):
        text_surface = font.render(language, True, (0, 0, 0))
        screen.blit(text_surface, (350, 150 + i * 50))
    pygame.display.update()

# Функція для гри
def play_game(level):
    global score, strikes
    fruits = ['a', 'b', 'i', 'k', 'l', 'o', 'w']
    fruit_positions = [(random.randint(0, 750), random.randint(100, 500)) for _ in range(7)]
    run_game = True
    while run_game:
        screen.fill((255, 255, 255))  # Очищаємо екран перед малюванням нових фруктів
        for i, fruit in enumerate(fruits):
            text_surface = font.render(fruit, True, (0, 0, 0))
            screen.blit(text_surface, fruit_positions[i])
        pygame.display.update()  # Оновлюємо екран

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
            elif event.type == pygame.KEYDOWN:
                if event.unicode in fruits:
                    score += 1
                    fruits.remove(event.unicode)
                    fruits.append(random.choice(['a', 'b', 'i', 'k', 'l', 'o', 'w']))
                    fruit_positions = [(random.randint(0, 750), random.randint(100, 500)) for _ in range(7)]
                if event.unicode == 'b':  # Бомба
                    run_game = False
                    break
                elif event.unicode == 'i':  # Лід (заморожує час)
                    pass

# Головна функція
def main():
    global current_language
    running = True  # Ініціалізація змінної running
    selected_option = 0  # Початковий вибір меню
    menu_options = languages[current_language]["menu"]

    while running:
        show_menu(menu_options, languages[current_language]["title"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Переміщення вниз по меню
                    selected_option = (selected_option + 1) % len(menu_options)
                if event.key == pygame.K_UP:  # Переміщення вгору по меню
                    selected_option = (selected_option - 1) % len(menu_options)

                # Вибір пункту меню за допомогою Enter
                if event.key == pygame.K_RETURN:
                    if selected_option == 0:  # "Level"
                        level_menu()
                    elif selected_option == 1:  # "Play"
                        play_game(level)
                    elif selected_option == 2:  # "Rules"
                        show_rules()
                    elif selected_option == 3:  # "Language"
                        show_language_menu()
                    elif selected_option == 4:  # "Scores"
                        pass  # Тут буде обробка рахунків
                    elif selected_option == 5:  # "Exit"
                        running = False

        # Підсвічування вибраного пункту меню
        for i, option in enumerate(menu_options):
            color = (0, 0, 0)
            if i == selected_option:
                color = (255, 0, 0)  # Червоний колір для вибраного пункту
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (350, 150 + i * 50))
        
        pygame.display.update()  # Оновлюємо екран після кожного кадру

# Функція для вибору рівня
def level_menu():
    global level
    running = True
    level_options = languages[current_language]["level"]
    selected_option = 0

    while running:
        show_menu(level_options, "Choose Level")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(level_options)
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(level_options)

                if event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        level = "Light level"
                    elif selected_option == 1:
                        level = "Hard level"
                    elif selected_option == 2:
                        running = False
                    return

        for i, option in enumerate(level_options):
            color = (0, 0, 0)
            if i == selected_option:
                color = (255, 0, 0)  # Червоний колір для вибраного пункту
            text_surface = font.render(option, True, color)
            screen.blit(text_surface, (350, 150 + i * 50))
        
        pygame.display.update()  # Оновлюємо екран

# Запуск гри
if __name__ == '__main__':
    main()


