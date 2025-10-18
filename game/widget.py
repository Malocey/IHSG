import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.app import App
from kivy.animation import Animation
import random

from game.entities import Hero, Enemy, Projectile, GoldCoin, SoulEssence, LootDrop
from game.ui import DamageNumber, XPCrystal
from game.config import WAVE_CONFIG
from game.effects import ParticleSystem

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hero = Hero(pos=(375, 50))
        self.add_widget(self.hero)

        self.enemies = []
        self.projectiles = []
        self.damage_numbers = []
        self.xp_crystals = []
        self.gold_coins = []

        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 10

        app = App.get_running_app()

        # UI für Währungen
        self.currency_layout = BoxLayout(orientation='vertical', pos=(10, 0), size_hint=(None, None))
        self.gold_label = Label(text=f"Gold: {app.player_data.gold}", font_size='20sp')
        self.soul_essence_label = Label(text=f"Essenz: {app.player_data.soul_essence}", font_size='20sp')
        self.currency_layout.add_widget(self.gold_label)
        self.currency_layout.add_widget(self.soul_essence_label)
        self.add_widget(self.currency_layout)

        self.bind(size=self._update_currency_labels_pos)

        self.current_wave_index = 0
        self.wave_time = 0
        self.wave_event = None
        self.spawn_event = None
        self.shoot_event = None
        self.hero_speed = 100 # Standardwert

        Clock.schedule_interval(self.update, 1.0 / 60.0)
        self.start_next_wave()

    def update_hero_stats(self, damage, speed, attack_cooldown, max_health, armor):
        """
        Wird von der App-Klasse aufgerufen, um die Werte des Helden zu aktualisieren.
        """
        self.hero.attack_damage = damage
        self.hero.speed = speed
        self.hero.armor = armor

        # Nur max_health aktualisieren, wenn es sich geändert hat, um Heilung zu vermeiden
        if self.hero.max_health != max_health:
            health_percentage = self.hero.health / self.hero.max_health if self.hero.max_health > 0 else 1
            self.hero.max_health = max_health
            self.hero.health = self.hero.max_health * health_percentage

        # Planen des Schießens neu starten, um den neuen Cooldown zu verwenden
        if self.shoot_event:
            self.shoot_event.cancel()
        self.shoot_event = Clock.schedule_interval(self.shoot, attack_cooldown)

    def level_up(self):
        """
        Wird aufgerufen, wenn der Spieler genug XP gesammelt hat.
        """
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5) # Nächstes Level benötigt mehr XP
        print(f"Level Up! Level {self.level}")

        # Wechsel zum Kartenauswahl-Bildschirm
        App.get_running_app().screen_manager.current = 'card_selection'

    def start_next_wave(self):
        """
        Startet die nächste Welle basierend auf der Konfiguration.
        """
        if self.wave_event:
            self.wave_event.cancel()
        if self.spawn_event:
            self.spawn_event.cancel()

        wave_data = WAVE_CONFIG[self.current_wave_index % len(WAVE_CONFIG)]
        self.wave_time = wave_data['duration']

        # Plant das Ende der Welle
        self.wave_event = Clock.schedule_once(self.end_wave, self.wave_time)
        # Startet das Spawnen von Gegnern für diese Welle
        self.spawn_event = Clock.schedule_interval(self.spawn_enemy, wave_data['spawn_interval'])
        print(f"Welle {self.current_wave_index + 1} gestartet!")

    def end_wave(self, dt):
        """
        Beendet die aktuelle Welle und startet die nächste.
        """
        print(f"Welle {self.current_wave_index + 1} beendet!")
        self.current_wave_index += 1
        # Optional: Kurze Pause zwischen den Wellen
        Clock.schedule_once(lambda dt: self.start_next_wave(), 3)

    def spawn_enemy(self, dt):
        """
        Spawnt einen zufälligen Gegner aus der aktuellen Wellenkonfiguration.
        """
        wave_data = WAVE_CONFIG[self.current_wave_index % len(WAVE_CONFIG)]
        if len(self.enemies) >= wave_data['max_enemies']:
            return

        enemy_type = random.choice(wave_data['enemies'])

        # Hier könnte man je nach `enemy_type` unterschiedliche Klassen instanziieren.
        # Vorerst verwenden wir nur die Standard-`Enemy`-Klasse.
        enemy = Enemy()
        enemy.x = random.randint(0, self.width - enemy.width)
        enemy.y = self.height

        # Erhöht die Lebenspunkte der Gegner mit jeder Runde durch die Wellen
        difficulty_multiplier = 1 + 0.1 * (self.current_wave_index // len(WAVE_CONFIG))
        enemy.max_health *= difficulty_multiplier
        enemy.health = enemy.max_health

        self.enemies.append(enemy)
        self.add_widget(enemy)

    def shoot(self, dt):
        projectile = Projectile()
        projectile.center_x = self.hero.center_x
        projectile.y = self.hero.top
        self.projectiles.append(projectile)
        self.add_widget(projectile)

    def update(self, dt):
        # Aktualisiert die Animationen für alle animierten Objekte.
        self.hero.update_animation(dt)
        for enemy in self.enemies:
            enemy.update_animation(dt)

        # Bewegt den Helden und setzt seine Position zurück, wenn er den Bildschirmrand erreicht.
        self.hero.x += self.hero_speed * dt
        if self.hero.right > self.width or self.hero.x < 0:
            self.hero.x = 0

        # Bewegt Projektile und prüft auf Kollisionen.
        for p in self.projectiles[:]:
            p.move(dt)
            if p.y > self.height:
                self.projectiles.remove(p)
                self.remove_widget(p)
                continue

            for enemy in self.enemies[:]:
                if not enemy.is_dying and p.collide_widget(enemy):
                    # Projektil entfernen
                    self.projectiles.remove(p)
                    self.remove_widget(p)

                    # Schaden zufügen und Schadenszahl anzeigen
                    is_dead = enemy.take_damage(self.hero.attack_damage)
                    damage_number = DamageNumber(damage=self.hero.attack_damage, center_x=enemy.center_x, y=enemy.top)
                    self.add_widget(damage_number)

                    # Partikel-Explosion erzeugen
                    ParticleSystem.create_explosion(self, pos=enemy.center)

                    if is_dead:
                        # Todesanimation starten
                        enemy.die(on_death_callback=lambda e=enemy: self.on_enemy_death(e))
                    break

        # Bewegt Gegner, die nicht gerade sterben.
        for enemy in self.enemies[:]:
            if not enemy.is_dying:
                enemy.y -= 100 * dt
                if enemy.top < 0:
                    self.enemies.remove(enemy)
                    self.remove_widget(enemy)

        # Sammelt XP-Kristalle auf und prüft auf Fusion
        self.check_crystal_fusion()
        for crystal in self.xp_crystals[:]:
            # Kristalle bewegen sich auf den Helden zu
            direction = self.hero.center_x - crystal.center_x, self.hero.center_y - crystal.center_y
            distance = (direction[0]**2 + direction[1]**2)**0.5
            if distance < 1:
                distance = 1

            crystal.velocity = (direction[0] / distance * 200, direction[1] / distance * 200)
            crystal.x += crystal.velocity[0] * dt
            crystal.y += crystal.velocity[1] * dt

            if self.hero.collide_widget(crystal):
                app = App.get_running_app()
                # XP-Bonus anwenden
                xp_to_add = crystal.xp_value * (1 + app.xp_gain_percent)
                self.xp += xp_to_add

                self.xp_crystals.remove(crystal)
                self.remove_widget(crystal)
                print(f"XP gesammelt: {self.xp}/{self.xp_to_next_level}")
                if self.xp >= self.xp_to_next_level:
                    self.level_up()

        # Sammelt Goldmünzen, Seelenessenz und Loot auf
        for item in self.children[:]:
            if self.hero.collide_widget(item):
                app = App.get_running_app()
                if isinstance(item, GoldCoin):
                    gold_to_add = item.value * (1 + app.gold_find_percent)
                    app.player_data.gold += int(gold_to_add)
                    self.gold_label.text = f"Gold: {app.player_data.gold}"
                    self.remove_widget(item)
                elif isinstance(item, SoulEssence):
                    app.player_data.soul_essence += item.value
                    self.soul_essence_label.text = f"Essenz: {app.player_data.soul_essence}"
                    self.remove_widget(item)
                elif isinstance(item, LootDrop):
                    app.player_data.add_item_to_inventory(item.item_id)
                    self.remove_widget(item)

                app.player_data.save_data()

    def _update_currency_labels_pos(self, instance, value):
        self.currency_layout.pos = (10, self.height - self.currency_layout.height - 10)

    def check_crystal_fusion(self):
        """
        Prüft, ob XP-Kristalle fusioniert werden können.
        """
        crystals_by_tier = {}
        for crystal in self.xp_crystals:
            if crystal.tier not in crystals_by_tier:
                crystals_by_tier[crystal.tier] = []
            crystals_by_tier[crystal.tier].append(crystal)

        for tier, crystals in crystals_by_tier.items():
            if len(crystals) < 5:
                continue

            # Finde Gruppen von 5 Kristallen, die nahe beieinander liegen
            for i in range(len(crystals) - 4):
                group_to_fuse = [crystals[i]]
                for j in range(i + 1, len(crystals)):
                    if len(group_to_fuse) < 5:
                        # Prüfe Distanz zum ersten Kristall der potenziellen Gruppe
                        dist_x = crystals[j].center_x - group_to_fuse[0].center_x
                        dist_y = crystals[j].center_y - group_to_fuse[0].center_y
                        if (dist_x**2 + dist_y**2)**0.5 < 100: # Fusions-Radius
                            group_to_fuse.append(crystals[j])

                if len(group_to_fuse) >= 5:
                    # Fusion durchführen
                    avg_x = sum(c.center_x for c in group_to_fuse) / 5
                    avg_y = sum(c.center_y for c in group_to_fuse) / 5

                    # Alten Kristalle entfernen
                    for c in group_to_fuse:
                        self.xp_crystals.remove(c)
                        self.remove_widget(c)

                    # Neuen, höherstufigen Kristall erstellen
                    new_crystal = XPCrystal(tier=tier + 1, center=(avg_x, avg_y))
                    self.xp_crystals.append(new_crystal)
                    self.add_widget(new_crystal)

                    # Nach einer Fusion die Prüfung für diesen Frame beenden, um Komplexität zu reduzieren
                    return


    def on_enemy_death(self, enemy):
        """
        Wird aufgerufen, wenn die Todesanimation eines Gegners abgeschlossen ist.
        """
        if enemy in self.enemies:
            # XP-Kristall an der Position des Gegners erstellen
            xp_crystal = XPCrystal(center=enemy.center)
            self.xp_crystals.append(xp_crystal)
            self.add_widget(xp_crystal)

            self.enemies.remove(enemy)
            self.remove_widget(enemy)
            # Löst einen Screen-Shake aus, wenn ein Gegner besiegt wird.
            self.screen_shake()

    def screen_shake(self, duration=0.1, magnitude=5):
        """
        Schüttelt den Bildschirm, indem die Position des Haupt-Widgets animiert wird.
        """
        original_pos = self.pos

        # Eine Sequenz von schnellen Bewegungen, um einen Schütteleffekt zu erzeugen
        anim = Animation(x=original_pos[0] + magnitude, y=original_pos[1] - magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] + magnitude, y=original_pos[1] + magnitude, duration=duration / 4) + \
               Animation(x=original_pos[0] - magnitude, y=original_pos[1] - magnitude, duration=duration / 4)

        # Am Ende zur ursprünglichen Position zurückkehren
        anim += Animation(pos=original_pos, duration=0.05)
        anim.start(self)