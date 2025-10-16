# main.py
# Haupt-Skript zum Starten des Spiels.

# Kivy-Bibliotheken importieren
import random
import os
from functools import partial

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout

# Lokale Klassen importieren
from src.entities import Hero, Enemy, Projectile, VFX
from src.skills import SKILL_TREE

class GameWidget(Widget):
    # Dieses Widget wird das Haupt-Widget für unser Spiel sein.
    # Hier werden wir die Spiellogik und die Darstellung implementieren.

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_enemy_killed')

        # Erstelle eine Instanz des Helden.
        self.hero = Hero()
        self.hero.pos = (self.width / 2, 50)
        self.add_widget(self.hero)

        # Listen, um alle Spiel-Objekte zu speichern.
        self.enemies = []
        self.projectiles = []

        # Referenz zur Haupt-App, um auf Stats zuzugreifen
        self.app = App.get_running_app()

        # Starte die Spiel-Schleife (update-Methode) 60 mal pro Sekunde.
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        # Erzeuge alle 2 Sekunden einen neuen Gegner.
        Clock.schedule_interval(self.spawn_enemy, 2.0)
        # Setze den initialen Angriffs-Timer
        self.attack_cooldown = 0

    def on_enemy_killed(self, *args):
        # Platzhalter-Methode für das Event. Wird benötigt, damit das Event registriert wird.
        pass

    def spawn_enemy(self, dt):
        # Erzeugt einen neuen Gegner an einer zufälligen Position.
        enemy = Enemy()
        enemy.x = random.randint(0, self.width - enemy.width)
        enemy.y = random.randint(self.height // 2, self.height - enemy.height)
        self.enemies.append(enemy)
        self.add_widget(enemy)

    def attack(self):
        """Erzeugt ein Projektil, das vom Helden abgefeuert wird."""
        projectile = Projectile()
        projectile.pos = (self.hero.center_x - projectile.width / 2, self.hero.top)
        self.projectiles.append(projectile)
        self.add_widget(projectile)

    def update(self, dt):
        # Bewegungslogik des Helden
        base_speed = self.app.character_stats.get('hero_speed', 100)
        speed_multiplier = 1 + (self.app.character_stats.get('hero_speed_percent', 0) / 100.0)
        hero_speed = base_speed * speed_multiplier
        self.hero.x += hero_speed * dt
        if self.hero.right > self.width:
            self.hero.x = 0

        # Angriffslogik des Helden
        self.attack_cooldown -= dt
        if self.attack_cooldown <= 0:
            self.attack()
            attack_speed_stat = 1 + (self.app.character_stats.get('attack_speed_percent', 0) / 100.0)
            if attack_speed_stat == 0:
                attack_speed_stat = 1
            self.attack_cooldown = 1.0 / attack_speed_stat

        # Projektil-Logik
        for p in self.projectiles[:]:
            p.move()
            # Entferne Projektile, die den Bildschirm verlassen
            if p.top > self.height:
                self.projectiles.remove(p)
                self.remove_widget(p)
                continue

            # Kollisionserkennung mit Gegnern
            for enemy in self.enemies[:]:
                if p.collide_widget(enemy):
                    # Treffer!
                    enemy.on_hit() # Löse den "Aufleucht"-Effekt aus

                    # Entferne das Projektil sofort
                    if p in self.projectiles:
                        self.projectiles.remove(p)
                        self.remove_widget(p)

                    # Plane das endgültige Entfernen des Gegners und den Todeseffekt
                    Clock.schedule_once(partial(self.kill_enemy, enemy), 0.1)

                    break # Das Projektil kann nur einen Gegner treffen

    def kill_enemy(self, enemy, dt):
        """Entfernt einen Gegner und erzeugt einen Todeseffekt."""
        if enemy in self.enemies:
            self.dispatch('on_enemy_killed')
            # Erzeuge einen größeren Todeseffekt
            vfx = VFX(pos=enemy.center, size=(enemy.width*2, enemy.height*2), animation_path='assets/vfx/explosion')
            self.add_widget(vfx)

            self.enemies.remove(enemy)
            self.remove_widget(enemy)

# Definition der verschiedenen Screens der App
class GameScreen(Screen):
    """Screen, der das Haupt-Spielfeld (GameWidget) enthält."""
    pass

class HeroScreen(Screen):
    """Screen, der den Skillbaum und Helden-Stats anzeigt."""
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app # Referenz zur Haupt-App

        # Haupt-Layout für den Skillbaum, das Zoom/Pan ermöglicht
        scatter = ScatterLayout(do_rotation=False, scale_min=0.5, scale_max=3.0)

        # FloatLayout, um die Skills an absoluten Positionen zu platzieren
        skill_tree_layout = FloatLayout(size=(2000, 1000))

        self.skill_nodes = {skill['id']: skill for skill in SKILL_TREE}
        self.skill_buttons = {}

        # Zeichne die Verbindungslinien
        with skill_tree_layout.canvas.before:
            Color(0.5, 0.5, 0.5, 1) # Graue Linien
            for skill in self.skill_nodes.values():
                for dep_id in skill['dependencies']:
                    if dep_id in self.skill_nodes:
                        start_pos = self.skill_nodes[dep_id]['position']
                        end_pos = skill['position']
                        Line(points=[start_pos[0] + 75, start_pos[1] + 25, end_pos[0] + 75, end_pos[1] + 25], width=1.5)

        # Erstelle die Skill-Buttons
        for skill_id, skill in self.skill_nodes.items():
            button = Button(
                size_hint=(None, None),
                size=(150, 60),
                pos=skill['position'],
                halign='center'
            )
            button.skill_id = skill_id
            button.bind(on_press=self.app.upgrade_skill)
            self.skill_buttons[skill_id] = button
            skill_tree_layout.add_widget(button)

        scatter.add_widget(skill_tree_layout)
        self.add_widget(scatter)
        self.update_button_states()

    def update_button_states(self):
        """Aktualisiert die Texte und Farben der Buttons basierend auf dem Skill-Level."""
        for skill_id, button in self.skill_buttons.items():
            skill = self.skill_nodes[skill_id]
            current_level = self.app.skill_levels.get(skill_id, 0)

            # Aktualisiere den Button-Text
            if current_level > 0:
                button.text = f"{skill['name']}\n(Lv: {current_level}/{skill['max_level']})"
            else:
                button.text = f"{skill['name']}\n(Unlock)"

            # Aktualisiere die Button-Farbe
            is_max_level = current_level >= skill['max_level']
            if is_max_level:
                button.background_color = (0.2, 0.8, 1, 1)  # Blau für Max-Level
                continue

            cost = skill['base_cost'] + current_level
            dependencies_met = all(dep in self.app.skill_levels for dep in skill['dependencies'])
            can_afford = self.app.skill_points >= cost

            if current_level > 0: # Bereits freigeschaltet
                button.background_color = (0, 1, 0, 1) if can_afford else (0.5, 0.5, 0.5, 1) # Grün / Grau
            elif dependencies_met and can_afford: # Kann freigeschaltet werden
                button.background_color = (1, 1, 0, 1) # Gelb
            else: # Gesperrt
                button.background_color = (1, 0, 0, 1) # Rot

class IdleHordeSlayerApp(App):
    # Dies ist die Hauptklasse unserer Kivy-Anwendung.
    def build(self):
        # Spieler-Daten
        self.skill_levels = {"base_attack": 1} # Speichert das Level jedes freigeschalteten Skills
        self.gold = 0
        self.gems = 0
        self.score = 0
        self.skill_points = 10 # Start-Punkte zum Testen

        # Haupt-Layout mit vertikaler Ausrichtung
        root_layout = BoxLayout(orientation='vertical')

        # 1. Obere Statusleiste (Top Bar) - bleibt global sichtbar
        top_bar = BoxLayout(size_hint_y=None, height=100, padding=10, spacing=20)
        with top_bar.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            top_bar.rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_background, pos=self._update_background)

        self.gold_label = Label(text=f"Gold: {self.gold}")
        self.gems_label = Label(text=f"Gems: {self.gems}")
        self.score_label = Label(text=f"Kills: {self.score}")
        self.skill_point_label = Label(text=f"Skill Points: {self.skill_points}")

        top_bar.add_widget(self.gold_label)
        top_bar.add_widget(self.gems_label)
        top_bar.add_widget(self.score_label)
        top_bar.add_widget(self.skill_point_label)

        # 2. ScreenManager für den mittleren, wechselbaren Bereich
        self.screen_manager = ScreenManager()

        # Erstelle den GameScreen und füge das GameWidget hinzu
        game_screen = GameScreen(name='game')
        game_widget = GameWidget()
        game_widget.bind(on_enemy_killed=self.update_stats)
        game_screen.add_widget(game_widget)
        self.screen_manager.add_widget(game_screen)

        # Erstelle den HeroScreen und übergebe eine Referenz zur App
        hero_screen = HeroScreen(name='hero', app=self)
        self.screen_manager.add_widget(hero_screen)

        # 3. Untere Navigationsleiste (Bottom Bar) - bleibt global sichtbar
        bottom_bar = BoxLayout(size_hint_y=None, height=150, spacing=10, padding=10)
        with bottom_bar.canvas.before:
            Color(0.1, 0.1, 0.1, 1)
            bottom_bar.rect = Rectangle(size=bottom_bar.size, pos=bottom_bar.pos)
        bottom_bar.bind(size=self._update_background, pos=self._update_background)

        # Definiere die Buttons und die zugehörigen Screens
        button_map = {
            "Game": "game",
            "Hero": "hero",
            "Upgrades": "upgrades",
            "Shop": "shop",
        }
        for button_text, screen_name in button_map.items():
            # Erstelle automatisch leere Screens für noch nicht implementierte Features
            if not self.screen_manager.has_screen(screen_name):
                screen = Screen(name=screen_name)
                screen.add_widget(Label(text=f"{button_text} Screen\n(Coming Soon)"))
                self.screen_manager.add_widget(screen)

            button = Button(text=button_text)
            # Binde den Button, um beim Klick den entsprechenden Screen zu zeigen
            button.bind(on_press=partial(self.change_screen, screen_name))
            bottom_bar.add_widget(button)

        # Füge die drei Hauptbereiche zum Root-Layout hinzu
        root_layout.add_widget(top_bar)
        root_layout.add_widget(self.screen_manager)
        root_layout.add_widget(bottom_bar)

        self.calculate_total_stats() # Berechne die initialen Stats beim Start
        return root_layout

    def change_screen(self, screen_name, *args):
        # Wechselt den aktuellen Screen im ScreenManager
        self.screen_manager.current = screen_name
        # Aktualisiere die Button-Zustände, wenn wir zum Hero-Screen wechseln
        if screen_name == 'hero':
            self.screen_manager.get_screen('hero').update_button_states()

    def upgrade_skill(self, button):
        """Bearbeitet das Freischalten und Aufleveln eines Skills."""
        skill_id = button.skill_id
        skill_data = self.screen_manager.get_screen('hero').skill_nodes[skill_id]
        current_level = self.skill_levels.get(skill_id, 0)

        if current_level >= skill_data['max_level']:
            print(f"Skill '{skill_data['name']}' ist bereits auf maximalem Level.")
            return

        # Kostenberechnung (Beispiel: Kosten steigen pro Level)
        cost = skill_data['base_cost'] + current_level

        if self.skill_points < cost:
            print(f"Nicht genügend Skill-Punkte für '{skill_data['name']}'.")
            return

        # Wenn der Skill neu ist, überprüfe die Abhängigkeiten
        if current_level == 0:
            dependencies_met = all(dep in self.skill_levels for dep in skill_data['dependencies'])
            if not dependencies_met:
                print(f"Abhängigkeiten für '{skill_data['name']}' nicht erfüllt.")
                return

        # Alles in Ordnung, führe das Upgrade durch
        self.skill_points -= cost
        self.skill_levels[skill_id] = current_level + 1
        print(f"Skill '{skill_data['name']}' auf Level {self.skill_levels[skill_id]} verbessert!")

        # Aktualisiere die UI
        self.skill_point_label.text = f"Skill Points: {self.skill_points}"
        self.screen_manager.get_screen('hero').update_button_states()
        self.calculate_total_stats()

    def calculate_total_stats(self):
        """Berechnet die Gesamtstatistiken des Charakters basierend auf den Skill-Leveln."""
        # Setze die Basis-Werte
        self.character_stats = {
            'attack_damage': 0,
            'attack_speed_percent': 0,
            'crit_chance_percent': 0,
            'hero_speed': 100 # Basis-Geschwindigkeit in Pixel/Sekunde
        }

        skill_definitions = self.screen_manager.get_screen('hero').skill_nodes
        for skill_id, level in self.skill_levels.items():
            skill_data = skill_definitions.get(skill_id)
            if not skill_data:
                continue

            for stat_bonus in skill_data['stats']:
                stat_type = stat_bonus['type']
                value_per_level = stat_bonus['value']

                # Berechne den Bonus für den aktuellen Stat
                if stat_type in self.character_stats:
                    self.character_stats[stat_type] += value_per_level * level
                else:
                    # Fallback für Stats, die nicht im Basis-Dict sind (sollte nicht passieren bei korrekter Def)
                    self.character_stats[stat_type] = value_per_level * level

        print("Charakter-Stats aktualisiert:", self.character_stats)


    def update_stats(self, instance, *args):
        # Wird aufgerufen, wenn ein Gegner besiegt wird
        self.score += 1
        self.gold += 1 # Vorerst 1 Gold pro Kill

        # Regel: 1 Skill-Punkt alle 10 Kills
        if self.score > 0 and self.score % 10 == 0:
            self.skill_points += 1

        # Aktualisiere die Text-Labels
        self.score_label.text = f"Kills: {self.score}"
        self.gold_label.text = f"Gold: {self.gold}"
        self.skill_point_label.text = f"Skill Points: {self.skill_points}"

    def _update_background(self, instance, value):
        # Aktualisiert den Hintergrund eines Widgets, wenn sich Größe oder Position ändern
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

if __name__ == '__main__':
    IdleHordeSlayerApp().run()