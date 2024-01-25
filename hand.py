import random
import time

import matplotlib.pyplot as plt
import pygame

from animals import Gender
from garden import Garden
from settings_menu import SettingsMenu, show_settings_menu

# Constantes et configurations
WINDOW_SIZE = (1024, 576)
IMAGE_PATHS = {
    "logo": 'img/logo.png',
    "loading": 'img/loading.png',
    "menu_background": 'img/menuBackground.png',
    "play_button": 'img/play.png',
    "setting_button": 'img/setting.png',
    "exit_button": 'img/exit.png',
    "prev_button": 'img/prev.png',
    "garden": 'img/garden.png',
    "rabbit": 'img/rabbit.png',
    "carrot": 'img/carrot.png'
}
FADE_DURATION = 1.0
STAY_DURATION = 1.0
RABBIT_SCALE = 0.1
CARROT_SIZE = (20, 20)
MARGIN = 0.07

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Rabbit Garden")


# Fonctions auxiliaires
def load_and_scale_image(path, scale=None):
    """
    Charge une image à partir d'un chemin et la redimensionne si nécessaire.

    :param path: Chemin du fichier image.
    :param scale: Tuple (largeur, hauteur) pour redimensionner l'image. Si None, l'image n'est pas redimensionnée.
    :return: Image pygame redimensionnée.
    """
    # Chargement de l'image à partir du chemin
    image = pygame.image.load(path)

    # Redimensionnement de l'image si une échelle est fournie
    if scale:
        image = pygame.transform.scale(image, scale)

    return image


def fade_in_out(image, logo, screen, duration, stay_time):
    """
    Effectue un fondu en entrée et sortie pour une image et un logo sur l'écran.
    """
    fade_in_duration = fade_out_duration = duration / 2
    start_time = time.time()
    image_rect = image.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    logo_rect = logo.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Calcul de l'alpha pour le fondu
        if elapsed_time < fade_in_duration:
            alpha = (elapsed_time / fade_in_duration) * 255
        elif elapsed_time < fade_in_duration + stay_time:
            alpha = 255
        elif elapsed_time < fade_in_duration + stay_time + fade_out_duration:
            alpha = 255 - ((elapsed_time - fade_in_duration - stay_time) / fade_out_duration) * 255
        else:
            break

        image.set_alpha(alpha)
        logo.set_alpha(alpha)
        screen.fill((0, 0, 0))
        screen.blit(image, image_rect)
        screen.blit(logo, logo_rect)
        pygame.display.update()


def show_menu(screen, images):
    """
    Affiche le menu principal et gère les interactions utilisateur.
    """
    menu = True
    settings_menu = SettingsMenu(2, 200, False, False)  # Exemple de configuration

    # Chargement des images des boutons
    play_button_image = images['play_button']
    setting_button_image = images['setting_button']
    exit_button_image = images['exit_button']

    # Positionnement des boutons
    button_y_position = 300
    play_button_rect = play_button_image.get_rect(center=(WINDOW_SIZE[0] // 2 - 150, button_y_position))
    setting_button_rect = setting_button_image.get_rect(center=(WINDOW_SIZE[0] // 2, button_y_position))
    exit_button_rect = exit_button_image.get_rect(center=(WINDOW_SIZE[0] // 2 + 150, button_y_position))

    while menu:
        screen.blit(images['menu_background'], (0, 0))
        screen.blit(play_button_image, play_button_rect)
        screen.blit(setting_button_image, setting_button_rect)
        screen.blit(exit_button_image, exit_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

                # Actions des boutons
                if play_button_rect.collidepoint(mouse_pos):
                    menu = False  # Quitter le menu et lancer la partie
                elif setting_button_rect.collidepoint(mouse_pos):
                    show_settings_menu(settings_menu, screen, images['logo'], images['menu_background'], images['prev_button'])
                elif exit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    quit()


def display_simulation(screen, garden, images):
    """
    Affiche les éléments de la simulation.
    """
    screen.blit(images['garden'], (0, 0))
    for pos in garden.carrots.positions:
        screen.blit(images['carrot'], pos)

    for rabbit in garden.rabbits:
        rabbit_img = images['rabbit']
        if rabbit.gender == Gender.MALE:
            rabbit_img = pygame.transform.flip(rabbit_img, True, False)

        # Générer une position aléatoire pour chaque lapin
        pos_x = random.randint(0, WINDOW_SIZE[0] - rabbit_img.get_width())
        pos_y = random.randint(0, WINDOW_SIZE[1] - rabbit_img.get_height())
        screen.blit(rabbit_img, (pos_x, pos_y))



def update_simulation(garden):
    """
    Met à jour l'état de la simulation.
    """
    garden.weekly_update()
    # Autres mises à jour si nécessaire...


def display_statistics(screen, garden):
    """
    Affiche des statistiques sur l'écran.
    """
    font = pygame.font.Font(None, 36)
    rabbit_text = font.render(f'Lapins: {len(garden.rabbits)}', True, (255, 255, 255))
    carrot_text = font.render(f'Carottes: {garden.carrots.count}', True, (255, 255, 255))
    # ... Positionner et afficher le texte sur l'écran ...


def plot_data(weeks, rabbit_counts, carrot_counts, rabbit_killed_counts):
    """
    Visualise les données collectées à l'aide de matplotlib.
    """
    plt.plot(weeks, rabbit_counts, label='Lapins')
    plt.plot(weeks, carrot_counts, label='Carottes')
    if rabbit_killed_counts:
        plt.plot(weeks, rabbit_killed_counts, label='Lapins tués')
    plt.xlabel('Semaines')
    plt.ylabel('Nombre')
    plt.title('Évolution du Jardin')
    plt.legend()
    plt.show()


# Chargement des images
images = {name: load_and_scale_image(IMAGE_PATHS[name],
                                     WINDOW_SIZE if name in ['loading', 'menu_background', 'garden'] else None)
          for name in IMAGE_PATHS}
images['rabbit'] = load_and_scale_image(IMAGE_PATHS['rabbit'], (int(images['rabbit'].get_width() * RABBIT_SCALE),
                                                                int(images['rabbit'].get_height() * RABBIT_SCALE)))
images['carrot'] = load_and_scale_image(IMAGE_PATHS['carrot'], CARROT_SIZE)

# Affichage de l'écran de chargement
fade_in_out(images['loading'], images['logo'], screen, FADE_DURATION, STAY_DURATION)

# Affichage du menu
show_menu(screen, images)

# Configuration du jeu
garden = Garden(WINDOW_SIZE, int(WINDOW_SIZE[0] * MARGIN), int(WINDOW_SIZE[1] * MARGIN), has_fox=False)

# Variables pour la visualisation des données
weeks, rabbit_counts, carrot_counts, rabbit_killed_counts = [], [], [], []

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_simulation(screen, garden, images)
    update_simulation(garden)
    display_statistics(screen, garden)

    # Collecte des données pour la visualisation
    weeks.append(garden.current_week)
    rabbit_counts.append(len(garden.rabbits))
    carrot_counts.append(garden.carrots.count)
    if garden.fox is not None:
        rabbit_killed_counts.append(garden.fox.killed_rabbits)

    pygame.display.flip()
    pygame.time.delay(100)

# Visualisation des données
plot_data(weeks, rabbit_counts, carrot_counts, rabbit_killed_counts)

pygame.quit()
