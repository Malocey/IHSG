import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
import random

from game.entities import Hero, Enemy, Projectile
from game.ui import DamageNumber, XPCrystal
from game.config import WAVE_CONFIG
from game.effects import ParticleSystem
from game.map import MapGenerator, MapWidget

class Camera(Widget):
    pass

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.map_generator = MapGenerator(width=50, height=50, tile_size=64)
        self.map_grid = self.map_generator.generate_map()
        self.map_widget = MapWidget(self.map_grid, self.map_generator.tile_size)
        self.add_widget(self.map_widget)

        self.camera = Camera()
        self.add_widget(self.camera)

        self.hero = Hero(pos=(
            self.map_generator.width * self.map_generator.tile_size / 2,
            self.map_generator.height * self.map_generator.tile_size / 2
        ))
        self.camera.add_widget(self.hero)

        self.enemies = []
        self.projectiles = []
        self.damage_numbers = []
        self.xp_crystals = []

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 10

        self.shoot_event = None
        self.hero_speed = 100
        self.game_time = 0
        self.max_enemies = 10

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_dynamic_enemies, 3.0)

    def update_hero_stats(self, damage, speed, attack_cooldown):
        self.hero.attack_damage = damage
        self.hero_speed = speed
        if self.shoot_event:
            self.shoot_event.cancel()
        self.shoot_event = Clock.schedule_interval(self.shoot, attack_cooldown)

    def level_up(self):
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        print(f"Level Up! Level {self.level}")
        App.get_running_app().screen_manager.current = 'card_selection'

    def spawn_dynamic_enemies(self, dt):
        if len(self.enemies) >= self.max_enemies:
            return

        self.max_enemies = 10 + int(self.game_time / 20)

        # TODO: Add new enemy types
        EnemyClass = Enemy

        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            x = random.uniform(self.camera.x, self.camera.right)
            y = self.camera.top + 50
        elif side == 'bottom':
            x = random.uniform(self.camera.x, self.camera.right)
            y = self.camera.y - 50
        elif side == 'left':
            x = self.camera.x - 50
            y = random.uniform(self.camera.y, self.camera.top)
        else: # right
            x = self.camera.right + 50
            y = random.uniform(self.camera.y, self.camera.top)

        enemy = EnemyClass(pos=(x, y))
        self.enemies.append(enemy)
        self.camera.add_widget(enemy)

    def shoot(self, dt):
        projectile = Projectile()
        projectile.center_x = self.hero.center_x
        projectile.y = self.hero.top
        self.projectiles.append(projectile)
        self.camera.add_widget(projectile)

    def update(self, dt):
        self.game_time += dt

        # Kamera auf den Helden zentrieren
        self.camera.pos = (self.width / 2 - self.hero.center_x, self.height / 2 - self.hero.center_y)
        self.map_widget.pos = self.camera.pos

        # Animationen aktualisieren
        self.hero.update_animation(dt)
        for enemy in self.enemies:
            enemy.update_animation(dt)

        # Held bewegen (einfache KI)
        if self.enemies:
            target = min(self.enemies, key=lambda e: (e.center_x - self.hero.center_x)**2 + (e.center_y - self.hero.center_y)**2)
            direction_x, direction_y = target.center_x - self.hero.center_x, target.center_y - self.hero.center_y
            distance = (direction_x**2 + direction_y**2)**0.5
            if distance > 1:
                self.hero.x += (direction_x / distance) * self.hero_speed * dt
                self.hero.y += (direction_y / distance) * self.hero_speed * dt

        # Projektile bewegen und Kollisionen prüfen
        for p in self.projectiles[:]:
            p.move(dt)
            if p.y > self.height:
                self.projectiles.remove(p)
                self.camera.remove_widget(p)
                continue
            for enemy in self.enemies[:]:
                if not enemy.is_dying and p.collide_widget(enemy):
                    self.projectiles.remove(p)
                    self.camera.remove_widget(p)
                    is_dead = enemy.take_damage(self.hero.attack_damage)
                    damage_number = DamageNumber(damage=self.hero.attack_damage, center_x=enemy.center_x, y=enemy.top)
                    self.camera.add_widget(damage_number)
                    ParticleSystem.create_explosion(self.camera, pos=enemy.center)
                    if is_dead:
                        enemy.die(on_death_callback=lambda e=enemy: self.on_enemy_death(e))
                    break

        # Gegner bewegen
        for enemy in self.enemies[:]:
            if not enemy.is_dying:
                direction_x, direction_y = self.hero.center_x - enemy.center_x, self.hero.center_y - enemy.center_y
                distance = (direction_x**2 + direction_y**2)**0.5
                if distance > 1:
                    enemy.x += (direction_x / distance) * 50 * dt
                    enemy.y += (direction_y / distance) * 50 * dt

        # XP-Kristalle aufsammeln
        for crystal in self.xp_crystals[:]:
            if self.hero.collide_widget(crystal):
                self.xp_crystals.remove(crystal)
                self.camera.remove_widget(crystal)
                self.xp += crystal.xp_value
                if self.xp >= self.xp_to_next_level:
                    self.level_up()

    def on_enemy_death(self, enemy):
        if enemy in self.enemies:
            xp_crystal = XPCrystal(center=enemy.center)
            self.xp_crystals.append(xp_crystal)
            self.camera.add_widget(xp_crystal)
            self.enemies.remove(enemy)
            self.camera.remove_widget(enemy)
            self.screen_shake()

    def screen_shake(self, duration=0.1, magnitude=5):
        original_pos = self.camera.pos
        anim = Animation(x=original_pos[0] + magnitude, y=original_pos[1] - magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] + magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] - magnitude, duration=duration / 4)
        anim += Animation(pos=original_pos, duration=0.05)
        anim.start(self.camera)