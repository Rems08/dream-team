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


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 255, 255)
        self.text = text
        self.font = pygame.font.SysFont('comicsansms', 30)
        self.txt_surface = self.font.render(text, True, self.color)
    

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):  # Vérifie si la souris est sur l'InputBox
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Affiche le texte de cette InputBox
                    self.text = ''  # Réinitialise uniquement le texte de cette InputBox
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Enlève le dernier caractère de cette InputBox
                else:
                    self.text += event.unicode  # Ajoute le caractère tapé à cette InputBox
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def show_settings_menu(settings_menu: SettingsMenu, screen, logo_image, menu_background_image, prev_button_image):
    input_box_rabbit = InputBox(300, 200, 140, 32)
    input_box_carrot = InputBox(300, 240, 140, 32)
    input_boxes = [input_box_rabbit, input_box_carrot]
    
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

            for box in input_boxes:
                box.handle_event(event)  # Gère les événements pour chaque InputBox

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

            is_hunter_enabled = settings_menu.is_hunter_enabled and text == "Hunter:"
            is_fox_enabled = settings_menu.is_fox_enabled and text == "Fox:"

            image = on_image if is_hunter_enabled or is_fox_enabled else off_image
            image_rect = image.get_rect(left=screen.get_width() // 2 + 150, top=y_offset_right)
            screen.blit(image, image_rect)

            if clicked and image_rect.collidepoint(mouse_pos):
                if text == "Hunter:":
                    settings_menu.is_hunter_enabled = not settings_menu.is_hunter_enabled
                elif text == "Fox:":
                    settings_menu.is_fox_enabled = not settings_menu.is_fox_enabled

            y_offset_right += 60
        
        for box in input_boxes:
            box.update()  # Met à jour chaque InputBox séparément
            box.draw(screen)  # Dessine chaque InputBox sur l'écran

        pygame.display.update()

        # Vérifier si le bouton retour a été cliqué
        if clicked and prev_button_rect.collidepoint(mouse_pos):
            is_menu_opened = False
