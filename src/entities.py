# src/entities.py
# Definiert die Spiel-Entitäten wie den Helden und die Gegner.

import os
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

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

class VFX(Widget):
    """
    Eine Klasse für visuelle Effekte, die sich nach einer kurzen Dauer selbst entfernen.
    """
    def __init__(self, duration=0.2, **kwargs):
        super().__init__(**kwargs)
        self.size = (30, 30)

        with self.canvas.before:
            Color(1, 0.8, 0.2, 1) # Orange/Gelbe Farbe für den Funken
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)
        # Plane das Entfernen des Widgets nach 'duration' Sekunden.
        Clock.schedule_once(self.self_destruct, duration)

    def self_destruct(self, dt):
        if self.parent:
            self.parent.remove_widget(self)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Projectile(Widget):
    # Die Projektil-Klasse.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (10, 10)

        with self.canvas.before:
            Color(1, 1, 0, 1) # Gelbe Farbe
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        # Aktualisiert die Position und Größe des gezeichneten Rechtecks.
        self.rect.pos = self.pos
        self.rect.size = self.size

    def move(self):
        # Bewegt das Projektil nach oben.
        self.y += 300 * (1/60) # Bewegung pro Frame (angenommene 60 FPS)

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