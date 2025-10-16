# src/cards.py
# Definiert die Datenstruktur für die Upgrade-Karten, die man während eines Runs erhält.

UPGRADE_CARDS = [
    {
        "id": "dmg_boost_1",
        "name": "Damage Boost I",
        "description": "Increases Attack Damage.",
        "type": "stat_boost",
        "bonus": {"stat": "attack_damage", "value": 10}
    },
    {
        "id": "speed_boost_1",
        "name": "Attack Speed Boost I",
        "description": "Increases Attack Speed.",
        "type": "stat_boost",
        "bonus": {"stat": "attack_speed_percent", "value": 5}
    },
    {
        "id": "crit_boost_1",
        "name": "Crit Chance Boost I",
        "description": "Increases Critical Hit Chance.",
        "type": "stat_boost",
        "bonus": {"stat": "crit_chance_percent", "value": 2}
    },
    {
        "id": "health_boost_1",
        "name": "Health Boost I",
        "description": "Increases Max Health.",
        "type": "stat_boost",
        "bonus": {"stat": "max_health", "value": 20}
    },
    {
        "id": "whirlwind_ability",
        "name": "New Ability: Whirlwind",
        "description": "Unleash a spinning attack around the hero.",
        "type": "new_ability",
        "bonus": {"ability_id": "whirlwind"}
    }
]