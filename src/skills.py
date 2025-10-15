# src/skills.py
# Definiert die Datenstruktur für den Skillbaum.

# Jeder Skill ist ein Dictionary mit den folgenden Schlüsseln:
# - id: Eindeutiger Bezeichner für den Skill.
# - name: Name des Skills, der im UI angezeigt wird.
# - description: Kurze Beschreibung, was der Skill bewirkt.
# - cost: Wie viele Skill-Punkte das Freischalten kostet.
# - dependencies: Eine Liste von Skill-IDs, die zuerst freigeschaltet werden müssen.
# - position: Ein Tupel (x, y) für die Position im Skillbaum-Layout.
#   Die Koordinaten sind relativ, z.B. in einem 1000x1000 Gitter.

SKILL_TREE = [
    {
        "id": "base_attack",
        "name": "Base Attack",
        "description": "Grundlegender Angriffsschaden.",
        "cost": 0,  # Start-Skill, kostet nichts
        "dependencies": [],
        "position": (100, 500)
    },
    {
        "id": "attack_speed_1",
        "name": "Attack Speed I",
        "description": "Erhöht die Angriffsgeschwindigkeit um 5%.",
        "cost": 1,
        "dependencies": ["base_attack"],
        "position": (300, 400)
    },
    {
        "id": "attack_damage_1",
        "name": "Attack Damage I",
        "description": "Erhöht den Angriffsschaden um 5.",
        "cost": 1,
        "dependencies": ["base_attack"],
        "position": (300, 600)
    },
    {
        "id": "crit_chance_1",
        "name": "Crit Chance I",
        "description": "Erhöht die kritische Trefferchance um 1%.",
        "cost": 2,
        "dependencies": ["attack_damage_1"],
        "position": (500, 700)
    },
    {
        "id": "multi_shot_1",
        "name": "Multi-Shot I",
        "description": "Chance, einen zusätzlichen Pfeil abzufeuern.",
        "cost": 3,
        "dependencies": ["attack_speed_1"],
        "position": (500, 300)
    },
]