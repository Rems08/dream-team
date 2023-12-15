import pygame
import matplotlib.pyplot as plt
from garden import Garden
import random

from gender import Gender


def init_pygame(window_size):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Rabbit Garden")
    return screen

def load_images(window_size):
    background_image = pygame.image.load('img/garden.png')
    background_image = pygame.transform.scale(background_image, window_size)

    rabbit_image = pygame.image.load('img/rabbit.png')
    rabbit_image = pygame.transform.scale(rabbit_image, (int(rabbit_image.get_width() * 0.1), int(rabbit_image.get_height() * 0.1)))

    carrot_image = pygame.image.load('img/carrot.png')
    carrot_image = pygame.transform.scale(carrot_image, (20, 20))

    return background_image, rabbit_image, carrot_image

def display_garden(screen, garden, rabbit_image, carrot_image, margin_x, margin_y, window_size):
    """Displays the entire garden including rabbits and carrots."""
    screen.blit(background_image, (0, 0))
    display_carrots(screen, garden.carrots.count, carrot_image, margin_x, margin_y, window_size)
    display_rabbits(screen, garden.rabbits, rabbit_image, margin_x, margin_y, window_size)

def display_carrots(screen, carrot_count, carrot_image, margin_x, margin_y, window_size):
    """Displays carrots on the screen."""
    for _ in range(carrot_count):
        pos_x = random.randint(margin_x, window_size[0] - margin_x - carrot_image.get_width())
        pos_y = random.randint(margin_y, window_size[1] - margin_y - carrot_image.get_height())
        screen.blit(carrot_image, (pos_x, pos_y))

def display_rabbits(screen, rabbits, rabbit_image, margin_x, margin_y, window_size):
    """Displays rabbits on the screen."""
    for rabbit in rabbits:
        pos_x = random.randint(margin_x, window_size[0] - margin_x - rabbit_image.get_width())
        pos_y = random.randint(margin_y, window_size[1] - margin_y - rabbit_image.get_height())
        if rabbit.gender == Gender.MALE:
            rabbit_image_flipped = pygame.transform.flip(rabbit_image, True, False)
            screen.blit(rabbit_image_flipped, pos_x, pos_y)
        else:
            screen.blit(rabbit_image, (pos_x, pos_y))

window_size = (800, 600)
screen = init_pygame(window_size)
background_image, rabbit_image, carrot_image = load_images(window_size)

margin = 0.07
margin_x = int(window_size[0] * margin)
margin_y = int(window_size[1] * margin)

garden = Garden()
weeks, rabbit_counts, carrot_counts = [], [], []

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_garden(screen, garden, rabbit_image, carrot_image, margin_x, margin_y)
    pygame.display.flip()
    garden.weekly_update()
    pygame.time.delay(100)

    weeks.append(garden.current_week)
    rabbit_counts.append(len(garden.rabbits))
    carrot_counts.append(garden.carrots.count)

# ... Matplotlib plotting ...

pygame.quit()
