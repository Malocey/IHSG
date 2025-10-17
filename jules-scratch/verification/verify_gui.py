import sys
import os
import kivy
kivy.require('2.3.0')

# Fügt das Hauptverzeichnis zum Python-Pfad hinzu, damit der Import von 'main' funktioniert
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from kivy.clock import Clock
from kivy.core.window import Window
from main import IdleHordeSlayerApp

# Sicherstellen, dass das Ausgabeverzeichnis existiert
output_dir = "jules-scratch/verification"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

class TestApp(IdleHordeSlayerApp):
    """
    Eine abgeleitete App-Klasse, die den Testablauf steuert.
    """
    def on_start(self):
        """
        Wird aufgerufen, nachdem die App gestartet und das Fenster erstellt wurde.
        """
        # Planen der Screenshots
        Clock.schedule_once(self.take_battle_screenshot, 2)
        Clock.schedule_once(self.trigger_level_up, 3)
        Clock.schedule_once(self.take_levelup_screenshot, 4)
        Clock.schedule_once(self.stop_app, 5)

    def take_battle_screenshot(self, dt):
        """
        Macht einen Screenshot vom Kampfbildschirm.
        """
        screenshot_path = os.path.join(output_dir, "battle_screen.png")
        Window.screenshot(name=screenshot_path)
        print(f"Screenshot vom Kampfbildschirm gespeichert unter: {screenshot_path}")

    def trigger_level_up(self, dt):
        """
        Löst manuell ein Level-Up aus, um den Bildschirm zu wechseln.
        """
        print("Löse Level-Up aus...")
        game_widget = self.root.get_screen('game').game_widget
        game_widget.level_up() # Direkter Aufruf für einen zuverlässigen Test

    def take_levelup_screenshot(self, dt):
        """
        Macht einen Screenshot vom Level-Up-Bildschirm.
        """
        # Sicherstellen, dass der Bildschirm gewechselt hat
        if self.root.current == 'card_selection':
            screenshot_path = os.path.join(output_dir, "level_up_screen.png")
            Window.screenshot(name=screenshot_path)
            print(f"Screenshot vom Level-Up-Bildschirm gespeichert unter: {screenshot_path}")
        else:
            print("FEHLER: Konnte nicht zum Level-Up-Bildschirm wechseln.")

    def stop_app(self, dt):
        """
        Beendet die Anwendung nach den Tests.
        """
        print("Tests abgeschlossen. App wird beendet.")
        self.stop()

if __name__ == '__main__':
    TestApp().run()