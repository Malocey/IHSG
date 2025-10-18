"""
Definiert die Daten für alle Ausrüstungsgegenstände im Spiel.
"""

ITEM_DATA = {
    # Waffen
    'rusty_sword': {
        'name': 'Rostiges Schwert',
        'type': 'weapon',
        'rarity': 'common',
        'bonuses': {'strength': 5}
    },
    'sharp_dagger': {
        'name': 'Scharfer Dolch',
        'type': 'weapon',
        'rarity': 'common',
        'bonuses': {'dexterity': 5}
    },
    'apprentice_wand': {
        'name': 'Lehrlingszauberstab',
        'type': 'weapon',
        'rarity': 'common',
        'bonuses': {'intelligence': 5}
    },

    # Helme
    'leather_cap': {
        'name': 'Lederkappe',
        'type': 'helmet',
        'rarity': 'common',
        'bonuses': {'max_health': 10}
    },

    # Rüstungen
    'padded_armor': {
        'name': 'Gepolsterte Rüstung',
        'type': 'chest',
        'rarity': 'common',
        'bonuses': {'armor': 20}
    },

    # Runen (Beispiele)
    'rune_of_flame': {
        'name': 'Flammenrune',
        'type': 'rune',
        'rarity': 'uncommon',
        'bonuses': {'fire_damage_percent': 0.05}
    },
    'rune_of_haste': {
        'name': 'Rune der Hast',
        'type': 'rune',
        'rarity': 'uncommon',
        'bonuses': {'attack_speed_percent': 0.03}
    }
}

# Definiert die möglichen Slots für Ausrüstung
EQUIPMENT_SLOTS = ['weapon', 'helmet', 'chest', 'boots', 'rune_1', 'rune_2']