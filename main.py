import kivy
kivy.require('2.3.0') # Ensure compatibility

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from game.screens import GameScreen, CardSelectionScreen

class IdleHordeSlayerApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        game_screen = GameScreen(name='game')
        self.screen_manager.add_widget(game_screen)

        card_selection_screen = CardSelectionScreen(name='card_selection')
        self.screen_manager.add_widget(card_selection_screen)

        # Die Referenz auf das GameWidget speichern, um darauf zugreifen zu können
        self.game_widget = game_screen.game_widget

        self.calculate_stats()
        return self.screen_manager

    def calculate_stats(self):
        """
        Berechnet die finalen Spielerstatistiken basierend auf permanenten und temporären Boni.
        Diese Funktion wird aufgerufen, wenn sich Werte ändern (z.B. durch Upgrades).
        """
        # Platzhalter für Boni aus dem Skill-Tree und In-Run-Upgrades
        permanent_damage_bonus = 0
        permanent_speed_bonus = 0
        temp_damage_bonus = 0
        temp_speed_bonus = 0

        # Basiswerte
        base_attack_damage = 10
        base_hero_speed = 100
        base_attack_speed = 0.5  # Sekunden pro Schuss

        # Berechnung der finalen Werte
        self.attack_damage = base_attack_damage + permanent_damage_bonus + temp_damage_bonus
        self.hero_speed = base_hero_speed + permanent_speed_bonus + temp_speed_bonus

        # Angriffsgeschwindigkeit wird als Cooldown berechnet (weniger ist besser)
        attack_speed_percent_bonus = 0 # z.B. 0.1 für 10% schneller
        self.attack_cooldown = base_attack_speed / (1 + attack_speed_percent_bonus)

        # Aktualisiert die Werte im Spiel
        self.game_widget.update_hero_stats(
            damage=self.attack_damage,
            speed=self.hero_speed,
            attack_cooldown=self.attack_cooldown
        )

if __name__ == '__main__':
    IdleHordeSlayerApp().run()