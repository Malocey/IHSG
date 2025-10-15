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
from src.entities import Hero, Enemy
from src.skills import SKILL_TREE

class GameWidget(Widget):
    # Dieses Widget wird das Haupt-Widget für unser Spiel sein.
    # Hier werden wir die Spiellogik und die Darstellung implementieren.

    # Definiere ein neues Event für das Besiegen von Gegnern.
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_enemy_killed')

        # Erstelle eine Instanz des Helden.
        self.hero = Hero()
        self.hero.pos = (self.width / 2, 50)
        self.add_widget(self.hero)

        # Liste, um alle Gegner zu speichern.
        self.enemies = []

        # Starte die Spiel-Schleife (update-Methode) 60 mal pro Sekunde.
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        # Erzeuge alle 2 Sekunden einen neuen Gegner.
        Clock.schedule_interval(self.spawn_enemy, 2.0)

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

    def update(self, dt):
        # Diese Methode wird kontinuierlich aufgerufen.
        hero_speed = 100
        self.hero.x += hero_speed * dt
        if self.hero.right > self.width:
            self.hero.x = 0

        # Überprüfe Kollisionen zwischen Held und Gegnern.
        for enemy in self.enemies[:]:
            if self.hero.collide_widget(enemy):
                self.dispatch('on_enemy_killed')
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
                text=f"{skill['name']}\n(Cost: {skill['cost']})",
                size_hint=(None, None),
                size=(150, 60),
                pos=skill['position'],
                halign='center'
            )
            button.skill_id = skill_id
            button.bind(on_press=self.app.unlock_skill)
            self.skill_buttons[skill_id] = button
            skill_tree_layout.add_widget(button)

        scatter.add_widget(skill_tree_layout)
        self.add_widget(scatter)
        self.update_button_states()

    def update_button_states(self):
        """Aktualisiert die Farben der Buttons basierend auf dem Freischalt-Status."""
        for skill_id, button in self.skill_buttons.items():
            skill = self.skill_nodes[skill_id]
            is_unlocked = skill_id in self.app.unlocked_skills

            # Überprüfe, ob alle Abhängigkeiten erfüllt sind
            dependencies_met = all(dep in self.app.unlocked_skills for dep in skill['dependencies'])
            can_unlock = self.app.skill_points >= skill['cost'] and dependencies_met

            if is_unlocked:
                button.background_color = (0, 1, 0, 1)  # Grün für freigeschaltet
            elif can_unlock:
                button.background_color = (1, 1, 0, 1)  # Gelb für verfügbar
            else:
                button.background_color = (1, 0, 0, 1)  # Rot für gesperrt

class IdleHordeSlayerApp(App):
    # Dies ist die Hauptklasse unserer Kivy-Anwendung.
    def build(self):
        # Spieler-Daten
        self.unlocked_skills = {"base_attack"} # Start-Skill ist immer freigeschaltet
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

        return root_layout

    def change_screen(self, screen_name, *args):
        # Wechselt den aktuellen Screen im ScreenManager
        self.screen_manager.current = screen_name
        # Aktualisiere die Button-Zustände, wenn wir zum Hero-Screen wechseln
        if screen_name == 'hero':
            self.screen_manager.get_screen('hero').update_button_states()

    def unlock_skill(self, button):
        """Versucht, einen Skill freizuschalten, wenn der zugehörige Button geklickt wird."""
        skill_id = button.skill_id
        skill = self.screen_manager.get_screen('hero').skill_nodes[skill_id]

        # Überprüfe, ob der Skill bereits freigeschaltet ist
        if skill_id in self.unlocked_skills:
            print(f"Skill '{skill['name']}' ist bereits freigeschaltet.")
            return

        # Überprüfe die Kosten
        if self.skill_points < skill['cost']:
            print(f"Nicht genügend Skill-Punkte für '{skill['name']}'.")
            return

        # Überprüfe die Abhängigkeiten
        dependencies_met = all(dep in self.unlocked_skills for dep in skill['dependencies'])
        if not dependencies_met:
            print(f"Abhängigkeiten für '{skill['name']}' nicht erfüllt.")
            return

        # Alles in Ordnung, schalte den Skill frei
        self.skill_points -= skill['cost']
        self.unlocked_skills.add(skill_id)
        print(f"Skill '{skill['name']}' freigeschaltet!")

        # Aktualisiere die UI
        self.skill_point_label.text = f"Skill Points: {self.skill_points}"
        self.screen_manager.get_screen('hero').update_button_states()

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