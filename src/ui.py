import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font, action=None):
        # -- Initialisiert einen Button --
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.action = action
        self.is_hovered = False

    def draw(self, surface):
        # -- Zeichnet den Button --
        # Wählt die Farbe basierend darauf, ob die Maus darüber schwebt.
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)

        # Zeichnet den Text auf den Button.
        # Wir verwenden eine feste Textfarbe (Weiß) für die Lesbarkeit.
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        # -- Verarbeitet Benutzerinteraktionen --
        # Überprüft, ob die Maus über dem Button ist.
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        # Überprüft, ob der Button geklickt wurde.
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and self.action:
                self.action() # Führt die zugewiesene Aktion aus.
                return True # Signalisiert, dass das Event verarbeitet wurde.
        return False