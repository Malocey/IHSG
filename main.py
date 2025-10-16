import kivy
kivy.require('2.1.0') # Ensure compatibility

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage
import random

class Sprite(Widget):
    def __init__(self, image_path, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.texture = CoreImage(image_path).texture
            self.rect = Rectangle(texture=self.texture, pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class Hero(Sprite):
    def __init__(self, **kwargs):
        super().__init__(image_path='assets/hero/hero.png', **kwargs)
        self.size = (48, 48) # Upscaled for visibility

class Enemy(Sprite):
    def __init__(self, **kwargs):
        super().__init__(image_path='assets/enemy/enemy.png', **kwargs)
        self.size = (32, 32) # Upscaled for visibility

class Projectile(Sprite):
    def __init__(self, **kwargs):
        super().__init__(image_path='assets/projectile/projectile.png', **kwargs)
        self.size = (24, 24)

    def move(self, dt):
        self.y += 300 * dt

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hero = Hero(pos=(375, 50))
        self.add_widget(self.hero)

        self.enemies = []
        self.projectiles = []

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 2.0)
        Clock.schedule_interval(self.shoot, 0.5)

    def spawn_enemy(self, dt):
        enemy = Enemy()
        enemy.x = random.randint(0, self.width - enemy.width)
        enemy.y = self.height
        self.enemies.append(enemy)
        self.add_widget(enemy)

    def shoot(self, dt):
        projectile = Projectile()
        projectile.center_x = self.hero.center_x
        projectile.y = self.hero.top
        self.projectiles.append(projectile)
        self.add_widget(projectile)

    def update(self, dt):
        # Move hero
        self.hero.x += 100 * dt
        if self.hero.right > self.width or self.hero.x < 0:
            self.hero.x = 0

        # Move projectiles and check for collisions
        for p in self.projectiles[:]:
            p.move(dt)
            if p.y > self.height:
                self.projectiles.remove(p)
                self.remove_widget(p)
                continue

            for enemy in self.enemies[:]:
                if p.collide_widget(enemy):
                    self.enemies.remove(enemy)
                    self.remove_widget(enemy)
                    self.projectiles.remove(p)
                    self.remove_widget(p)
                    break

        # Move enemies
        for enemy in self.enemies[:]:
            enemy.y -= 100 * dt
            if enemy.top < 0:
                self.enemies.remove(enemy)
                self.remove_widget(enemy)

class IdleHordeSlayerApp(App):
    def build(self):
        return GameWidget()

if __name__ == '__main__':
    IdleHordeSlayerApp().run()