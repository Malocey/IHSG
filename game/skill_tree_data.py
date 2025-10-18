SKILL_TREE_DATA = {
    # Start-Knoten (Beispiel)
    'start_node': {'id': 'start_node', 'name': 'Ausgangspunkt', 'description': '', 'type': None, 'value': 0, 'connections': ['strength_1', 'dexterity_1']},

    # Stärke-Pfad
    'strength_1': {'id': 'strength_1', 'name': '+10 Stärke', 'description': '+10 zu Stärke', 'type': 'strength', 'value': 10, 'connections': ['start_node', 'strength_2']},
    'strength_2': {'id': 'strength_2', 'name': '+10 Stärke', 'description': '+10 zu Stärke', 'type': 'strength', 'value': 10, 'connections': ['strength_1', 'art_of_the_gladiator']},

    # Geschicklichkeits-Pfad
    'dexterity_1': {'id': 'dexterity_1', 'name': '+10 Geschicklichkeit', 'description': '+10 zu Geschicklichkeit', 'type': 'dexterity', 'value': 10, 'connections': ['start_node', 'dexterity_2']},
    'dexterity_2': {'id': 'dexterity_2', 'name': '+10 Geschicklichkeit', 'description': '+10 zu Geschicklichkeit', 'type': 'dexterity', 'value': 10, 'connections': ['dexterity_1', 'art_of_the_gladiator']},

    # Notable-Knoten
    'art_of_the_gladiator': {
        'id': 'art_of_the_gladiator',
        'name': 'Kunst des Gladiators',
        'description': '+10% Angriffsgeschwindigkeit\n+10% Trefferwertung\n+20 Geschicklichkeit',
        'type': 'notable',
        'bonuses': [
            {'type': 'attack_speed_percent', 'value': 0.10},
            {'type': 'accuracy_percent', 'value': 0.10},
            {'type': 'dexterity', 'value': 20}
        ],
        'connections': ['strength_2', 'dexterity_2']
    },

    # Beispiel für einen weiteren Pfad
    'life_1': {'id': 'life_1', 'name': '+20 Leben', 'description': '+20 zu maximalem Leben', 'type': 'max_health', 'value': 20, 'connections': ['strength_2']},
}