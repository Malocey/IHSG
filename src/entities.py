# src/entities.py
# Definiert die Spiel-Entitäten wie den Helden und die Gegner.

import os
import math
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.image import Image as CoreImage

CRYSTAL_TYPES = {
    "blue": {"value": 1, "color": (0.2, 0.8, 1, 1), "size": (12, 12), "merges_to": "green", "merge_count": 5},
    "green": {"value": 5, "color": (0.2, 1, 0.2, 1), "size": (14, 14), "merges_to": "red", "merge_count": 5},
    "red": {"value": 25, "color": (1, 0.2, 0.2, 1), "size": (16, 16), "merges_to": None, "merge_count": 0},
}

class AnimatedWidget(Widget):
    """Eine Basis-Klasse für alle animierten Objekte im Spiel."""

    def __init__(self, animation_path, animation_speed=0.1, **kwargs):
        super().__init__(**kwargs)
        self.animation_path = animation_path
        self.animation_speed = animation_speed
        self.frames = []
        self.current_frame_index = 0

        with self.canvas.before:
            self.color_instruction = Color(1, 1, 1, 1) # Standard-Farbe
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.load_animation_frames()

        self.bind(pos=self.update_rect, size=self.update_rect)
        if self.frames:
            Clock.schedule_interval(self.update_animation, self.animation_speed)

    def load_animation_frames(self):
        """Lädt die Bilddateien für die Animation aus dem angegebenen Pfad."""
        if not os.path.exists(self.animation_path) or not os.listdir(self.animation_path):
            self.color_instruction.rgba = getattr(self, 'fallback_color', (1, 1, 1, 1))
            return

        image_files = sorted([f for f in os.listdir(self.animation_path) if f.endswith('.png')])
        for f in image_files:
            texture = CoreImage(os.path.join(self.animation_path, f)).texture
            if texture:
                self.frames.append(texture)

        if self.frames:
            self.rect.texture = self.frames[0]
            self.color_instruction.rgba = (1, 1, 1, 1) # Mache die Farbe weiß, damit das Bild nicht getönt wird
        else:
            self.color_instruction.rgba = getattr(self, 'fallback_color', (1, 1, 1, 1))

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
        self.fallback_color = (1, 1, 1, 1)
        self.active_abilities = ["default_attack"]
        super().__init__(animation_path='assets/characters/knight/idle', **kwargs)
        self.size = (32, 32)

class Enemy(AnimatedWidget):
    def __init__(self, **kwargs):
        self.fallback_color = (1, 0, 0, 1)
        super().__init__(animation_path='assets/enemies/goblin/idle', **kwargs)
        self.size = (32, 32)

    def on_hit(self):
        original_color = self.color_instruction.rgba
        self.color_instruction.rgba = (1, 1, 1, 1)
        Clock.schedule_once(lambda dt: self.reset_color(original_color), 0.1)

    def reset_color(self, color):
        if hasattr(self, 'color_instruction'):
            self.color_instruction.rgba = color

class Projectile(AnimatedWidget):
    def __init__(self, angle=90, **kwargs):
        self.fallback_color = (1, 1, 0, 1)
        super().__init__(animation_path='assets/projectiles/fireball/fly', animation_speed=0.05, **kwargs)
        self.size = (16, 16)
        self.angle = math.radians(angle)
        self.velocity_x = math.cos(self.angle) * 300
        self.velocity_y = math.sin(self.angle) * 300

    def move(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

class VFX(AnimatedWidget):
    def __init__(self, animation_path, duration_multiplier=1.0, **kwargs):
        self.fallback_color = (1, 0.8, 0.2, 1)
        super().__init__(animation_path=animation_path, **kwargs)
        self.size = kwargs.get('size', (32, 32))

        duration = len(self.frames) * self.animation_speed * duration_multiplier if self.frames else 0.2
        Clock.schedule_once(self.self_destruct, duration)

    def self_destruct(self, dt):
        if self.parent:
            self.parent.remove_widget(self)

class XPCrystal(Widget):
    def __init__(self, crystal_type="blue", **kwargs):
        super().__init__(**kwargs)
        self.type_data = CRYSTAL_TYPES[crystal_type]
        self.crystal_type = crystal_type
        self.value = self.type_data["value"]
        self.size = self.type_data["size"]

        with self.canvas:
            self.color_instruction = Color(*self.type_data["color"])
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos

    def move_towards(self, target_pos, dt):
        dir_x = target_pos[0] - self.center_x
        dir_y = target_pos[1] - self.center_y
        dist = (dir_x**2 + dir_y**2)**0.5
        if dist > 0:
            dir_x /= dist
            dir_y /= dist

        speed = 150
        self.x += dir_x * speed * dt
        self.y += dir_y * speed * dt