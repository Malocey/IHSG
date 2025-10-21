import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage

from kivy.clock import Clock
from game.animation import AnimatedSprite, SpriteManager
from game.ui import HealthBar
from game.effects import TrailParticle

class Hero(AnimatedSprite):
    def __init__(self, **kwargs):
        super().__init__(
            sheet_path='assets/hero/Body_A/Animations/Walk_Base/Walk_Side-Sheet.png',
            frame_width=64, frame_height=64, **kwargs)
        self.size = (96, 96)
        self.add_animation('walk_side', frame_indices=list(range(6)), frame_rate=1.0/10.0)
        self.set_animation('walk_side')
        self.attack_damage = 10  # Platzhalter-Wert


class Enemy(AnimatedSprite):
    def __init__(self, **kwargs):
        super().__init__(
            sheet_path='assets/enemies/Orc - Base/Run/Run-Sheet.png',
            frame_width=16, frame_height=16, **kwargs)
        self.size = (48, 48)
        self.max_health = 30
        self.health = self.max_health
        self.is_dying = False

        self.health_bar = HealthBar(size=(self.width, 5))
        self.add_widget(self.health_bar)
        self.bind(pos=self._update_health_bar_pos)

        self.death_sprite_manager = SpriteManager(
            'assets/enemies/Orc - Base/Death/Death-Sheet.png', 16, 16)

        self.add_animation('run', frame_indices=list(range(6)), frame_rate=1.0/8.0)
        self.sprite_manager.animations['die'] = {
            'frames': self.death_sprite_manager._frames, 'frame_rate': 1.0/10.0}
        self.set_animation('run')

    def _update_health_bar_pos(self, *args):
        self.health_bar.pos = (self.x, self.top + 5)

    def take_damage(self, damage):
        """
        Verringert die Lebenspunkte des Gegners und gibt zurück, ob er gestorben ist.
        """
        self.health -= damage
        health_percent = self.health / self.max_health
        self.health_bar.set_health_percent(health_percent)

        if self.health <= 0 and not self.is_dying:
            return True
        return False

    def die(self, on_death_callback):
        """
        Startet die Todesanimation und entfernt die Lebensanzeige.
        """
        self.is_dying = True
        self.remove_widget(self.health_bar)
        self.set_animation('die', loop=False, on_end=on_death_callback)


class Projectile(Widget):
    def __init__(self, target, **kwargs):
        super().__init__(**kwargs)
        self.size = (24, 24)
        self.speed = 400
        self.target = target

        # Richtung zum Ziel berechnen
        direction_x = self.target.center_x - self.center_x
        direction_y = self.target.center_y - self.center_y
        distance = (direction_x**2 + direction_y**2)**0.5
        if distance > 0:
            self.velocity_x = (direction_x / distance) * self.speed
            self.velocity_y = (direction_y / distance) * self.speed
        else:
            self.velocity_x = 0
            self.velocity_y = self.speed # Fallback: nach oben bewegen

        with self.canvas:
            texture = CoreImage('assets/projectile/Wood/Wood.png').texture
            self.rect = Rectangle(texture=texture, pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.trail_event = Clock.schedule_interval(self.spawn_trail, 1.0 / 30.0)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def spawn_trail(self, dt):
        """
        Erzeugt ein Schweif-Partikel.
        """
        if not self.parent:
            self.trail_event.cancel()
            return

        trail_particle = TrailParticle(center=self.center)
        self.parent.add_widget(trail_particle, index=len(self.parent.children))

    def move(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        if not self.parent:
            self.trail_event.cancel()