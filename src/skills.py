# src/skills.py
# Definiert die Datenstruktur für den Skillbaum.

# Jeder Skill ist ein Dictionary mit den folgenden Schlüsseln:
# - id: Eindeutiger Bezeichner für den Skill.
# - name: Name des Skills, der im UI angezeigt wird.
# - description: Kurze Beschreibung, was der Skill bewirkt.
# - base_cost: Die Grundkosten in Skill-Punkten für das erste Level.
# - max_level: Die maximale Stufe, die dieser Skill erreichen kann.
# - dependencies: Eine Liste von Skill-IDs, die zuerst freigeschaltet werden müssen.
# - position: Ein Tupel (x, y) für die Position im Skillbaum-Layout.
# - stats: Eine Liste von Boni, die dieser Skill pro Level gewährt.
#   Jeder Bonus ist ein Dictionary mit 'type' (z.B. 'attack_damage') und 'value'.

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
            {"type": "attack_damage", "value": 1} # Startwert
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