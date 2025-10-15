# src/entities.py
# Definiert die Spiel-Entitäten wie den Helden und die Gegner.

import os
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class Hero(Widget):
    # Die Held-Klasse.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Setze die Größe des Helden.
        self.size = (24, 24)

        # Pfad zum Heldenbild
        image_path = 'assets/hero.png'

        with self.canvas.before:
            # Überprüfe, ob die Bilddatei existiert.
            if os.path.exists(image_path):
                # Wenn ja, verwende das Bild.
                self.rect = Rectangle(source=image_path, size=self.size, pos=self.pos)
            else:
                # Wenn nicht, zeichne ein weißes Rechteck als Platzhalter.
                Color(1, 1, 1, 1)
                self.rect = Rectangle(size=self.size, pos=self.pos)

        # Binde die 'update_rect'-Methode an Positions- und Größenänderungen.
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # Aktualisiert die Position und Größe des gezeichneten Rechtecks.
        self.rect.pos = self.pos
        self.rect.size = self.size

class Enemy(Widget):
    # Die Gegner-Klasse.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Setze die Größe des Gegners.
        self.size = (16, 16)

        # Pfad zum Gegnerbild
        image_path = 'assets/enemy.png'

        with self.canvas.before:
            # Überprüfe, ob die Bilddatei existiert.
            if os.path.exists(image_path):
                # Wenn ja, verwende das Bild.
                self.rect = Rectangle(source=image_path, size=self.size, pos=self.pos)
            else:
                # Wenn nicht, zeichne ein rotes Rechteck als Platzhalter.
                Color(1, 0, 0, 1)
                self.rect = Rectangle(size=self.size, pos=self.pos)

        # Binde die 'update_rect'-Methode an Positions- und Größenänderungen.
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # Aktualisiert die Position und Größe des gezeichneten Rechtecks.
        self.rect.pos = self.pos
        self.rect.size = self.size