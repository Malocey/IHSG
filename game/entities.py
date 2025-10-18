import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
import random

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
        Startet die Todesanimation, lässt möglicherweise Gold fallen und entfernt die Lebensanzeige.
        """
        self.is_dying = True
        self.remove_widget(self.health_bar)

        # Gold-Drop-Logik
        if random.random() < 0.8:  # 80% Chance, Gold fallen zu lassen
            gold_coin = GoldCoin(center=self.center)
            if self.parent:
                self.parent.add_widget(gold_coin)

        # Seelenessenz-Drop-Logik
        if random.random() < 0.1: # 10% Chance, Seelenessenz fallen zu lassen
            soul_essence = SoulEssence(center=(self.center_x, self.center_y + 10))
            if self.parent:
                self.parent.add_widget(soul_essence)

        # Todesanimation starten
        self.set_animation('die', loop=False, on_end=on_death_callback)


class GoldCoin(Widget):
    """
    Eine Goldmünze, die von Gegnern fallengelassen und vom Spieler eingesammelt werden kann.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (20, 20)
        self.value = 1  # Jede Münze ist 1 Gold wert

        with self.canvas:
            texture = CoreImage('assets/items/GoldCoin.png').texture
            self.rect = Rectangle(texture=texture, pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos


class SoulEssence(Widget):
    """
    Eine seltene Seelenessenz, die von Gegnern fallengelassen wird.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (22, 22)
        self.value = 1

        with self.canvas:
            # Annahme: Es gibt ein Bild für die Seelenessenz
            texture = CoreImage('assets/items/SoulEssence.png').texture
            self.rect = Rectangle(texture=texture, pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos


class Projectile(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (24, 24)
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
        self.y += 300 * dt
        if not self.parent:
            self.trail_event.cancel()