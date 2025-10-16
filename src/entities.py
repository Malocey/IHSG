# src/entities.py
# Definiert die Spiel-Entitäten wie den Helden und die Gegner.

import os
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

class AnimatedWidget(Widget):
    """Eine Basis-Klasse für alle animierten Objekte im Spiel."""

    def __init__(self, animation_path, animation_speed=0.1, **kwargs):
        super().__init__(**kwargs)
        self.animation_path = animation_path
        self.animation_speed = animation_speed
        self.frames = []
        self.current_frame_index = 0

        self.load_animation_frames()

        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos)
            if self.frames:
                self.rect.texture = self.frames[0]

        self.bind(pos=self.update_rect, size=self.update_rect)
        Clock.schedule_interval(self.update_animation, self.animation_speed)

    def load_animation_frames(self):
        """Lädt die Bilddateien für die Animation aus dem angegebenen Pfad."""
        if not os.path.exists(self.animation_path) or not os.listdir(self.animation_path):
            print(f"Warnung: Animationspfad nicht gefunden oder leer: {self.animation_path}")
            with self.canvas.before:
                Color(*getattr(self, 'fallback_color', (1, 1, 1, 1)))
            return

        image_files = sorted([f for f in os.listdir(self.animation_path) if f.endswith('.png')])
        for f in image_files:
            self.frames.append(CoreImage(os.path.join(self.animation_path, f)).texture)

        if not self.frames:
             print(f"Warnung: Keine Frames im Pfad gefunden: {self.animation_path}")
             with self.canvas.before:
                Color(*getattr(self, 'fallback_color', (1, 1, 1, 1)))

    def update_animation(self, dt):
        """Wechselt zum nächsten Frame der Animation."""
        if not self.frames:
            return

        self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.rect.texture = self.frames[self.current_frame_index]

    def update_rect(self, *args):
        """Aktualisiert die Position und Größe des Rechtecks."""
        self.rect.pos = self.pos
        self.rect.size = self.size

class Hero(AnimatedWidget):
    def __init__(self, **kwargs):
        self.fallback_color = (1, 1, 1, 1) # Weiß
        # TODO: Später dynamisch machen, um verschiedene Helden zu ermöglichen
        super().__init__(animation_path='assets/characters/knight/idle', **kwargs)
        self.size = (32, 32) # Angepasst an gängige Sprite-Größen

class Enemy(AnimatedWidget):
    def __init__(self, **kwargs):
        self.fallback_color = (1, 0, 0, 1) # Rot
        # TODO: Später dynamisch machen, um verschiedene Gegner zu ermöglichen
        super().__init__(animation_path='assets/enemies/goblin/idle', **kwargs)
        self.size = (32, 32) # Angepasst an gängige Sprite-Größen

    def on_hit(self):
        """Wird aufgerufen, wenn der Gegner getroffen wird. Löst einen visuellen Effekt aus."""
        original_color = self.rect.color
        self.rect.color = (1, 1, 1, 1)
        Clock.schedule_once(lambda dt: self.reset_color(original_color), 0.1)

    def reset_color(self, color):
        self.rect.color = color

class Projectile(AnimatedWidget):
    def __init__(self, **kwargs):
        self.fallback_color = (1, 1, 0, 1) # Gelb
        super().__init__(animation_path='assets/projectiles/fireball/fly', animation_speed=0.05, **kwargs)
        self.size = (16, 16)

    def move(self):
        self.y += 300 * (1/60)

class VFX(AnimatedWidget):
    def __init__(self, animation_path, duration_multiplier=1.0, **kwargs):
        self.fallback_color = (1, 0.8, 0.2, 1) # Orange
        super().__init__(animation_path=animation_path, **kwargs)
        self.size = kwargs.get('size', (32, 32))

        duration = len(self.frames) * self.animation_speed * duration_multiplier if self.frames else 0.2
        Clock.schedule_once(self.self_destruct, duration)

    def self_destruct(self, dt):
        if self.parent:
            self.parent.remove_widget(self)