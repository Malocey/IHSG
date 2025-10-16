# src/skills.py
# Definiert die Datenstruktur für den Skillbaum.
import random
import math

def generate_skill_tree(node_count=500):
    """Generiert prozedural einen großen, netzartigen Skillbaum."""
    skills = []
    positions = set()

    # Startknoten
    start_node = {
        "id": "start", "name": "Start", "description": "Der Beginn deiner Reise.",
        "base_cost": 0, "max_level": 1, "dependencies": [],
        "position": (1000, 500), "stats": [], "type": "start"
    }
    skills.append(start_node)
    positions.add(start_node["position"])

    # Generiere Hauptpfade und bemerkenswerte Knoten
    notable_skills = [
        {"name": "Art of the Gladiator", "stats": [{"type": "attack_speed_percent", "value": 10}, {"type": "dexterity", "value": 20}]},
        {"name": "Might of the Bear", "stats": [{"type": "strength", "value": 20}, {"type": "max_health", "value": 50}]},
        {"name": "Mind of the Scholar", "stats": [{"type": "intelligence", "value": 20}, {"type": "max_mana", "value": 50}]},
        {"name": "Path of the Assassin", "stats": [{"type": "crit_chance_percent", "value": 5}, {"type": "crit_damage_percent", "value": 50}]},
    ]

    for i in range(1, node_count):
        is_notable = i % 50 == 0

        # Wähle einen zufälligen existierenden Knoten als Ankerpunkt
        anchor_node = random.choice(skills)

        # Finde eine neue Position in der Nähe des Ankerpunkts
        while True:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.randint(80, 150)
            new_pos = (
                int(anchor_node["position"][0] + distance * math.cos(angle)),
                int(anchor_node["position"][1] + distance * math.sin(angle))
            )
            if new_pos not in positions:
                positions.add(new_pos)
                break

        node_id = f"node_{i}"

        if is_notable:
            notable = random.choice(notable_skills)
            node = {
                "id": node_id, "name": notable["name"], "description": "Ein mächtiger Bonus.",
                "base_cost": 5, "max_level": 1, "dependencies": [anchor_node["id"]],
                "position": new_pos, "stats": notable["stats"], "type": "notable"
            }
        else:
            stat_type = random.choice(["strength", "dexterity", "intelligence"])
            node = {
                "id": node_id, "name": f"+10 {stat_type.capitalize()}", "description": f"Erhöht {stat_type}.",
                "base_cost": 1, "max_level": 1, "dependencies": [anchor_node["id"]],
                "position": new_pos, "stats": [{"type": stat_type, "value": 10}], "type": "minor"
            }

        skills.append(node)

    return skills

SKILL_TREE = generate_skill_tree()