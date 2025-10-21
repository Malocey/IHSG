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

        # Generate the procedural map
        self.map_generator = MapGenerator(width=100, height=75)
        self.map_grid = self.map_generator.generate_map()
        self.map_widget = MapWidget(self.map_grid, tile_size=64)
        self.add_widget(self.map_widget)

        self.camera = Camera()
        self.add_widget(self.camera)

        # Place hero on a random floor tile
        start_pos_tile = self.map_generator.get_random_floor_tile()
        start_pos_pixels = (start_pos_tile[0] * 64, start_pos_tile[1] * 64)

        self.hero = Hero(pos=start_pos_pixels)
        self.camera.add_widget(self.hero)

        self.enemies = []
        self.projectiles = []
        self.damage_numbers = []
        self.xp_crystals = []

        self.particle_system = ParticleSystem()
        self.camera.add_widget(self.particle_system)

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 10

        self.shoot_event = None
        self.hero_speed = 100

        self.wave_index = -1
        self.wave_time = 0
        self.spawn_event = None
        self.hero_wander_target = None

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.start_next_wave()

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

    def shoot(self, dt):
        target = self.get_closest_entity(self.hero, self.enemies)
        if not target:
            return

        projectile = Projectile(target=target)
        projectile.center = self.hero.center
        self.projectiles.append(projectile)
        self.camera.add_widget(projectile)

    def update(self, dt):
        # Center camera on hero
        self.camera.pos = (self.width / 2 - self.hero.center_x, self.height / 2 - self.hero.center_y)
        self.map_widget.pos = self.camera.pos

        # Update animations and particles
        self.hero.update_animation(dt)
        for enemy in self.enemies:
            enemy.update_animation(dt)
        self.particle_system.update(dt)

        # Update wave logic
        self.wave_time += dt
        if self.wave_index < len(WAVE_CONFIG):
            current_wave = WAVE_CONFIG[self.wave_index]
            if self.wave_time > current_wave['duration']:
                self.start_next_wave()

        # Hero AI movement
        self.update_hero_movement(dt)

        # Move projectiles and check for collisions
        for p in self.projectiles[:]:
            p.move(dt)
            if self.is_wall(p.center_x, p.center_y):
                self.projectiles.remove(p)
                self.camera.remove_widget(p)
                continue

            for enemy in self.enemies[:]:
                if not enemy.is_dying and p.collide_widget(enemy):
                    self.projectiles.remove(p)
                    self.camera.remove_widget(p)

                    damage = self.hero.attack_damage
                    is_dead = enemy.take_damage(damage)

                    damage_number = DamageNumber(text=str(damage), center=enemy.center)
                    self.camera.add_widget(damage_number)

                    if is_dead:
                        enemy.die(on_death_callback=lambda e=enemy: self.on_enemy_death(e))
                    break

        # Move enemies
        for enemy in self.enemies[:]:
            if not enemy.is_dying:
                # Simple movement towards hero with wall collision
                direction_x, direction_y = self.hero.center_x - enemy.center_x, self.hero.center_y - enemy.center_y
                distance = (direction_x**2 + direction_y**2)**0.5
                if distance > 1:
                    vx = (direction_x / distance) * 80 * dt # 80 is enemy speed
                    vy = (direction_y / distance) * 80 * dt

                    new_x = enemy.x + vx
                    new_y = enemy.y + vy
                    if not self.is_wall(new_x + enemy.width / 2, new_y + enemy.height / 2):
                        enemy.pos = (new_x, new_y)
                    else:
                        # Simple wall sliding
                        if not self.is_wall(enemy.x + vx + enemy.width/2, enemy.y + enemy.height/2):
                            enemy.x += vx
                        elif not self.is_wall(enemy.x + enemy.width/2, enemy.y + vy + enemy.height/2):
                            enemy.y += vy

        # Collect XP crystals
        for crystal in self.xp_crystals[:]:
            if self.hero.collide_widget(crystal):
                self.xp_crystals.remove(crystal)
                self.camera.remove_widget(crystal)
                self.xp += crystal.xp_value
                if self.xp >= self.xp_to_next_level:
                    self.level_up()

    def on_enemy_death(self, enemy):
        if enemy in self.enemies:
            self.particle_system.create_explosion(enemy.center)
            xp_crystal = XPCrystal(center=enemy.center)
            self.xp_crystals.append(xp_crystal)
            self.camera.add_widget(xp_crystal)

            Clock.schedule_once(lambda dt, e=enemy: self.remove_enemy(e), 0.5)
            self.screen_shake()

    def remove_enemy(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
            self.camera.remove_widget(enemy)

    def update_hero_movement(self, dt):
        target = self.get_closest_entity(self.hero, self.xp_crystals)
        if not target:
            target = self.get_closest_entity(self.hero, self.enemies)

        if not target:
            # Wander behavior when no targets are present
            if not self.hero_wander_target or self.hero.collide_point(*self.hero_wander_target):
                random_tile = self.map_generator.get_random_floor_tile()
                self.hero_wander_target = (random_tile[0] * self.map_widget.tile_size,
                                           random_tile[1] * self.map_widget.tile_size)

            target_pos = self.hero_wander_target
        else:
            target_pos = target.center

        direction_x, direction_y = target_pos[0] - self.hero.center_x, target_pos[1] - self.hero.center_y
        distance = (direction_x**2 + direction_y**2)**0.5
        if distance > 1:
            vx = (direction_x / distance) * self.hero_speed * dt
            vy = (direction_y / distance) * self.hero_speed * dt

            # Check for wall collision before moving
            new_x = self.hero.x + vx
            new_y = self.hero.y + vy
            if not self.is_wall(new_x + self.hero.width / 2, new_y + self.hero.height / 2):
                self.hero.pos = (new_x, new_y)
            else:
                # Simple wall sliding: try moving only on X or Y axis
                if not self.is_wall(self.hero.x + vx + self.hero.width / 2, self.hero.y + self.hero.height/2):
                    self.hero.x += vx
                elif not self.is_wall(self.hero.x + self.hero.width/2, self.hero.y + vy + self.hero.height/2):
                    self.hero.y += vy

    def get_closest_entity(self, entity, entity_list):
        closest_entity = None
        min_dist_sq = float('inf')
        for other in entity_list:
            if hasattr(other, 'is_dying') and other.is_dying:
                continue
            dist_sq = entity.collide_point(*other.center)**2
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_entity = other
        return closest_entity

    def screen_shake(self, duration=0.1, magnitude=5):
        original_pos = self.camera.pos
        anim = Animation(x=original_pos[0] + magnitude, y=original_pos[1] - magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] + magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] - magnitude, duration=duration / 4)
        anim += Animation(pos=original_pos, duration=0.05)
        anim.start(self.camera)

    def is_wall(self, x, y):
        """ Checks if a given pixel coordinate is a wall. """
        tile_x = int(x // self.map_widget.tile_size)
        tile_y = int(y // self.map_widget.tile_size)
        if 0 <= tile_y < len(self.map_grid) and 0 <= tile_x < len(self.map_grid[0]):
            return self.map_grid[tile_y][tile_x] == 'WALL'
        return True # Treat out of bounds as a wall

    def start_next_wave(self):
        self.wave_index += 1
        if self.wave_index >= len(WAVE_CONFIG):
            print("All waves completed!")
            self.wave_index = 0 # Loop waves for now

        self.wave_time = 0
        wave_data = WAVE_CONFIG[self.wave_index]
        print(f"Wave {self.wave_index + 1} starting!")

        if self.spawn_event:
            self.spawn_event.cancel()
        self.spawn_event = Clock.schedule_interval(self.spawn_enemy, wave_data['spawn_interval'])

    def spawn_enemy(self, dt):
        wave_data = WAVE_CONFIG[self.wave_index]
        if len(self.enemies) >= wave_data['max_enemies']:
            return

        # Find a valid spawn point on a floor tile, not too close to the player
        for _ in range(50): # Try 50 times to find a valid spot
            spawn_tile = self.map_generator.get_random_floor_tile()
            spawn_pos = (spawn_tile[0] * self.map_widget.tile_size,
                         spawn_tile[1] * self.map_widget.tile_size)

            # Check distance from hero
            dist_x = self.hero.center_x - spawn_pos[0]
            dist_y = self.hero.center_y - spawn_pos[1]
            distance_sq = dist_x**2 + dist_y**2

            # Ensure enemies spawn off-screen but not thousands of miles away
            # Use screen dimensions for spawn distance relative to player's view
            min_dist_sq = (self.width * 0.6)**2  # Just outside the screen
            max_dist_sq = (self.width * 2.0)**2 # A bit further out

            if min_dist_sq < distance_sq < max_dist_sq:
                enemy = Enemy(pos=spawn_pos)
                self.enemies.append(enemy)
                self.camera.add_widget(enemy)
                return # Successfully spawned