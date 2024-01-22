# settings_menu.py
import pygame


class SettingsMenu:
    def __init__(self, rabbit_count, carrot_count, is_hunter_enabled, is_fox_enabled):
        self._rabbit_count = rabbit_count
        self._carrot_count = carrot_count
        self._is_hunter_enabled = is_hunter_enabled
        self._is_fox_enabled = is_fox_enabled

    @property
    def rabbit_count(self):
        """Getter pour rabbit_count."""
        return self._rabbit_count

    @rabbit_count.setter
    def rabbit_count(self, value):
        """Setter pour rabbit_count avec validation si nécessaire."""
        if value < 0:
            raise ValueError("Le nombre de lapins ne peut pas être négatif.")
        self._rabbit_count = value

    @property
    def carrot_count(self):
        """Getter pour carrot_count."""
        return self._carrot_count

    @carrot_count.setter
    def carrot_count(self, value):
        """Setter pour carrot_count avec validation si nécessaire."""
        if value < 0:
            raise ValueError("Le nombre de carottes ne peut pas être négatif.")
        self._carrot_count = value

    @property
    def is_hunter_enabled(self):
        """Getter pour is_hunter_enabled."""
        return self._is_hunter_enabled

    @is_hunter_enabled.setter
    def is_hunter_enabled(self, value):
        """Setter pour is_hunter_enabled."""
        if not isinstance(value, bool):
            raise ValueError("is_hunter_enabled doit être un booléen.")
        self._is_hunter_enabled = value

    @property
    def is_fox_enabled(self):
        """Getter pour is_fox_enabled."""
        return self._is_fox_enabled

    @is_fox_enabled.setter
    def is_fox_enabled(self, value):
        """Setter pour is_fox_enabled."""
        if not isinstance(value, bool):
            raise ValueError("is_fox_enabled doit être un booléen.")
        self._is_fox_enabled = value


def show_settings_menu(settings_menu: SettingsMenu, screen, logo_image, menu_background_image, prev_button_image):
    pygame.init()
    font = pygame.font.SysFont('comicsansms', 30)

    # Chargement des images on/off
    on_image = pygame.transform.scale(pygame.image.load('img/on.png'), (90, 40))
    off_image = pygame.transform.scale(pygame.image.load('img/off.png'), (90, 40))

    is_menu_opened = True
    while is_menu_opened:
        clicked = False
        mouse_pos = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                clicked = True

        screen.blit(menu_background_image, (0, 0))
        logo_rect = logo_image.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(logo_image, logo_rect)

        prev_button_rect = prev_button_image.get_rect(topleft=(10, 10))
        screen.blit(prev_button_image, prev_button_rect)

        # Affichage des textes et des boutons on/off
        texts_left = ["Carrot count:", "Rabbit count:"]
        texts_right = ["Hunter:", "Fox:"]
        y_offset_left = 200
        y_offset_right = 200

        # Afficher les textes à gauche
        for text in texts_left:
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(left=50, top=y_offset_left)
            screen.blit(text_surface, text_rect)
            y_offset_left += 40

        # Afficher les textes et boutons on/off à droite
        for text in texts_right:
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(left=screen.get_width() // 2, top=y_offset_right)
            screen.blit(text_surface, text_rect)

            image = on_image if (text == "Hunter:" and settings_menu.is_hunter_enabled) or (
                        text == "Fox:" and settings_menu.is_fox_enabled) else off_image
            image_rect = image.get_rect(left=screen.get_width() // 2 + 150, top=y_offset_right)
            screen.blit(image, image_rect)

            if clicked and image_rect.collidepoint(mouse_pos):
                if text == "Hunter:":
                    settings_menu.is_hunter_enabled = not settings_menu.is_hunter_enabled
                    hunter_enabled = not settings_menu.is_hunter_enabled
                else:  # "Fox:"
                    settings_menu.is_fox_enabled = not settings_menu.is_fox_enabled

            y_offset_right += 60

        pygame.display.update()

        # Vérifier si le bouton retour a été cliqué
        if clicked and prev_button_rect.collidepoint(mouse_pos):
            is_menu_opened = False
