import pygame
import random

class Hero:
    def __init__(self, x, y):
        # -- Initialisiert den Helden --
        # Setzt die Startposition des Helden.
        self.x = x
        self.y = y
        # Legt die Größe des Helden fest.
        self.width = 24
        self.height = 24
        # Erstellt ein pygame.Rect-Objekt für die einfache Kollisionserkennung und Positionierung.
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # Definiert die Farbe des Helden.
        self.color = (0, 128, 255) # Ein Blauton
        # Legt die Bewegungsgeschwindigkeit des Helden fest (Pixel pro Frame).
        self.speed = 5
        # Speichert den Zustand der Bewegungstasten.
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        # Kampf-Attribute
        self.health = 100
        self.damage = 10
        self.attack_speed = 1.0 # Angriffe pro Sekunde
        self.gold = 0

    def move(self):
        # -- Bewegt den Helden basierend auf den gedrückten Tasten --
        if self.moving_left:
            self.x -= self.speed
        if self.moving_right:
            self.x += self.speed
        if self.moving_up:
            self.y -= self.speed
        if self.moving_down:
            self.y += self.speed

        # Aktualisiert die Position des rect-Objekts.
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        # -- Zeichnet den Helden auf die angegebene Oberfläche --
        pygame.draw.rect(surface, self.color, self.rect)

class Enemy:
    def __init__(self, x, y, width, height, color):
        # -- Initialisiert einen generischen Gegner --
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.health = 0
        self.damage = 0
        self.gold_reward = 0

    def draw(self, surface):
        # -- Zeichnet den Gegner --
        pygame.draw.rect(surface, self.color, self.rect)

class Slime(Enemy):
    def __init__(self, x, y):
        # -- Initialisiert einen Schleim-Gegner --
        super().__init__(x, y, 16, 16, (0, 255, 0)) # Grün
        self.health = 20
        self.damage = 5
        self.gold_reward = 2

class SkeletonArcher(Enemy):
    def __init__(self, x, y):
        # -- Initialisiert einen Skelett-Bogenschützen --
        super().__init__(x, y, 16, 16, (200, 200, 200)) # Hellgrau
        self.health = 15
        self.damage = 10
        self.gold_reward = 5