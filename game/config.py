# Konfiguration für Gegnerwellen
WAVE_CONFIG = [
    {'duration': 30, 'enemies': ['orc'], 'max_enemies': 10, 'spawn_interval': 2.0},
    {'duration': 45, 'enemies': ['orc', 'slime'], 'max_enemies': 15, 'spawn_interval': 1.5},
    {'duration': 60, 'enemies': ['orc', 'slime', 'bat'], 'max_enemies': 20, 'spawn_interval': 1.0},
]

# Konfiguration für Karten-Upgrades beim Level-Up
CARD_UPGRADES = [
    {'text': '+15% Schaden', 'type': 'damage_percent', 'value': 0.15},
    {'text': '+10% Angriffsgeschwindigkeit', 'type': 'attack_speed_percent', 'value': 0.10},
    {'text': '+10% Bewegungsgeschwindigkeit', 'type': 'speed_percent', 'value': 0.10},
    {'text': '+20 Max. Leben', 'type': 'max_health', 'value': 20},
    {'text': '+5 Flächenschaden', 'type': 'area_damage', 'value': 5},
    {'text': 'Projektile durchschlagen 1 Gegner', 'type': 'pierce', 'value': 1},
]

# Konfiguration für permanente Shop-Upgrades
SHOP_UPGRADES = {
    'gold_find': {
        'name': 'Goldsucher',
        'description': 'Erhöht die Menge an gefundenem Gold um 2% pro Level.',
        'bonus_type': 'gold_find_percent',
        'bonus_per_level': 0.02,
        'cost_formula': lambda level: 100 * (1.5 ** level)  # Exponentielle Kosten
    },
    'xp_gain': {
        'name': 'Wissensdurst',
        'description': 'Erhöht den Gewinn von Erfahrungspunkten um 2% pro Level.',
        'bonus_type': 'xp_gain_percent',
        'bonus_per_level': 0.02,
        'cost_formula': lambda level: 120 * (1.6 ** level)
    },
    'shop_price': {
        'name': 'Feilschen',
        'description': 'Reduziert die Preise im Shop um 1% pro Level (max 20%).',
        'bonus_type': 'shop_price_percent',
        'bonus_per_level': 0.01,
        'max_level': 20,
        'cost_formula': lambda level: 200 * (1.8 ** level)
    }
}