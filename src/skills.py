# src/skills.py
# Definiert die Datenstruktur für den Skillbaum.

SKILL_TREE = [
    {
        "id": "base_attack",
        "name": "Base Attack",
        "description": "Schaltet grundlegende Angriffsfähigkeiten frei.",
        "base_cost": 0,
        "max_level": 1,
        "dependencies": [],
        "position": (100, 500),
        "stats": [
            {"type": "attack_damage", "value": 1}
        ]
    },
    {
        "id": "attack_speed_1",
        "name": "Attack Speed I",
        "description": "Erhöht die Angriffsgeschwindigkeit.",
        "base_cost": 1,
        "max_level": 10,
        "dependencies": ["base_attack"],
        "position": (300, 400),
        "stats": [
            {"type": "attack_speed_percent", "value": 5}
        ]
    },
    {
        "id": "attack_damage_1",
        "name": "Attack Damage I",
        "description": "Erhöht den Angriffsschaden.",
        "base_cost": 1,
        "max_level": 10,
        "dependencies": ["base_attack"],
        "position": (300, 600),
        "stats": [
            {"type": "attack_damage", "value": 5}
        ]
    },
    {
        "id": "crit_chance_1",
        "name": "Crit Chance I",
        "description": "Erhöht die kritische Trefferchance.",
        "base_cost": 2,
        "max_level": 5,
        "dependencies": ["attack_damage_1"],
        "position": (500, 700),
        "stats": [
            {"type": "crit_chance_percent", "value": 1}
        ]
    },
    {
        "id": "hero_speed_1",
        "name": "Hero Speed I",
        "description": "Erhöht die Bewegungsgeschwindigkeit des Helden.",
        "base_cost": 3,
        "max_level": 5,
        "dependencies": ["attack_speed_1"],
        "position": (500, 300),
        "stats": [
            {"type": "hero_speed_percent", "value": 10}
        ]
    },
]