import json
import os

class PlayerData:
    """
    Verwaltet die permanenten Spielerdaten, wie Währungen, Upgrades und Skills.
    """
    def __init__(self, save_file='player_save.json'):
        self.save_file = save_file
        self.gold = 0
        self.soul_essence = 0
        self.skill_points = 0
        self.unlocked_nodes = {'start_node'}
        self.shop_upgrades = {}
        self.load_data()

    def load_data(self):
        """
        Lädt die Spielerdaten aus der Speicherdatei, falls sie existiert.
        """
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.gold = data.get('gold', 0)
                    self.soul_essence = data.get('soul_essence', 0)
                    self.skill_points = data.get('skill_points', 0)
                    self.shop_upgrades = data.get('shop_upgrades', {})
                    unlocked = set(data.get('unlocked_nodes', ['start_node']))
                    self.unlocked_nodes = unlocked
                    print(f"Spielerdaten geladen: {self.gold} Gold, {self.soul_essence} Seelenessenz, {self.skill_points} Punkte.")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Fehler beim Laden der Speicherdatei: {e}. Erstelle neue Speicherdatei.")
                self.save_data()
        else:
            print("Keine Speicherdatei gefunden. Erstelle neue Speicherdatei.")
            self.save_data()

    def save_data(self):
        """
        Speichert die aktuellen Spielerdaten in der Speicherdatei.
        """
        data = {
            'gold': self.gold,
            'soul_essence': self.soul_essence,
            'skill_points': self.skill_points,
            'unlocked_nodes': list(self.unlocked_nodes),
            'shop_upgrades': self.shop_upgrades
        }
        try:
            with open(self.save_file, 'w') as f:
                json.dump(data, f, indent=4)
            # Weniger ausführliches Logging beim Speichern, um die Konsole nicht zuzumüllen
            # print("Spielerdaten gespeichert.")
        except IOError as e:
            print(f"Fehler beim Speichern der Daten: {e}")

    def unlock_node(self, node_id):
        """
        Schaltet einen neuen Knoten frei, wenn genügend Punkte vorhanden sind.
        """
        if self.skill_points > 0:
            self.unlocked_nodes.add(node_id)
            self.skill_points -= 1
            self.save_data()
            return True
        return False

    def add_skill_points(self, amount):
        """
        Fügt dem Spieler Fähigkeitspunkte hinzu.
        """
        self.skill_points += amount
        self.save_data()