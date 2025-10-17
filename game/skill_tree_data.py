SKILL_TREE_DATA = {
    # Start-Knoten
    'start_node': {
        'id': 'start_node', 'name': 'Ausgangspunkt', 'description': 'Der Startpunkt deiner Reise.',
        'node_type': 'start', 'cost': 0, 'connections': ['strength_1', 'dexterity_1']
    },

    # Stärke-Pfad (Minor Nodes)
    'strength_1': {
        'id': 'strength_1', 'name': '+10 Stärke', 'description': '+10 zu Stärke',
        'node_type': 'minor', 'bonus_type': 'strength', 'value': 10, 'cost': 1,
        'connections': ['start_node', 'strength_2']
    },
    'strength_2': {
        'id': 'strength_2', 'name': '+10 Stärke', 'description': '+10 zu Stärke',
        'node_type': 'minor', 'bonus_type': 'strength', 'value': 10, 'cost': 1,
        'connections': ['strength_1', 'art_of_the_gladiator', 'life_1']
    },

    # Geschicklichkeits-Pfad (Minor Nodes)
    'dexterity_1': {
        'id': 'dexterity_1', 'name': '+10 Geschicklichkeit', 'description': '+10 zu Geschicklichkeit',
        'node_type': 'minor', 'bonus_type': 'dexterity', 'value': 10, 'cost': 1,
        'connections': ['start_node', 'dexterity_2']
    },
    'dexterity_2': {
        'id': 'dexterity_2', 'name': '+10 Geschicklichkeit', 'description': '+10 zu Geschicklichkeit',
        'node_type': 'minor', 'bonus_type': 'dexterity', 'value': 10, 'cost': 1,
        'connections': ['dexterity_1', 'art_of_the_gladiator']
    },

    # Notable-Knoten
    'art_of_the_gladiator': {
        'id': 'art_of_the_gladiator', 'name': 'Kunst des Gladiators',
        'description': '+10% Angriffsgeschwindigkeit\n+10% Trefferwertung\n+20 Geschicklichkeit',
        'node_type': 'notable', 'cost': 3,
        'bonuses': [
            {'type': 'attack_speed_percent', 'value': 0.10},
            {'type': 'accuracy_percent', 'value': 0.10},
            {'type': 'dexterity', 'value': 20}
        ],
        'connections': ['strength_2', 'dexterity_2']
    },

    # Leben-Pfad (Minor Node)
    'life_1': {
        'id': 'life_1', 'name': '+20 Leben', 'description': '+20 zu maximalem Leben',
        'node_type': 'minor', 'bonus_type': 'max_health', 'value': 20, 'cost': 1,
        'connections': ['strength_2', 'life_2']
    },
    'life_2': {
        'id': 'life_2', 'name': '+30 Leben', 'description': '+30 zu maximalem Leben',
        'node_type': 'minor', 'bonus_type': 'max_health', 'value': 30, 'cost': 1,
        'connections': ['life_1', 'vitality_1']
    },
    # Notable im Lebens-Pfad
    'vitality_1': {
        'id': 'vitality_1', 'name': 'Vitalitätsschub', 'description': '+5% maximales Leben\n+1 Lebensregeneration pro Sekunde',
        'node_type': 'notable', 'cost': 3,
        'bonuses': [
            {'type': 'max_health_percent', 'value': 0.05},
            {'type': 'health_regen', 'value': 1}
        ],
        'connections': ['life_2', 'keystone_bulwark']
    },

    # Intelligenz-Pfad (neu)
    'intelligence_1': {
        'id': 'intelligence_1', 'name': '+10 Intelligenz', 'description': '+10 zu Intelligenz',
        'node_type': 'minor', 'bonus_type': 'intelligence', 'value': 10, 'cost': 1,
        'connections': ['start_node', 'intelligence_2']
    },
    'intelligence_2': {
        'id': 'intelligence_2', 'name': '+10 Intelligenz', 'description': '+10 zu Intelligenz',
        'node_type': 'minor', 'bonus_type': 'intelligence', 'value': 10, 'cost': 1,
        'connections': ['intelligence_1', 'mana_1']
    },
    'mana_1': {
        'id': 'mana_1', 'name': '+20 Mana', 'description': '+20 zu maximalem Mana',
        'node_type': 'minor', 'bonus_type': 'max_mana', 'value': 20, 'cost': 1,
        'connections': ['intelligence_2', 'arcane_potency']
    },
    'arcane_potency': {
        'id': 'arcane_potency', 'name': 'Arkane Potenz', 'description': '+10% Zauberschaden\n+20 Intelligenz',
        'node_type': 'notable', 'cost': 3,
        'bonuses': [
            {'type': 'spell_damage_percent', 'value': 0.10},
            {'type': 'intelligence', 'value': 20}
        ],
        'connections': ['mana_1']
    },

    # Kritischer Treffer-Pfad (neu)
    'crit_chance_1': {
        'id': 'crit_chance_1', 'name': '+2% Krit-Chance', 'description': '+2% auf kritische Trefferchance',
        'node_type': 'minor', 'bonus_type': 'crit_chance_percent', 'value': 0.02, 'cost': 1,
        'connections': ['dexterity_2', 'crit_damage_1']
    },
    'crit_damage_1': {
        'id': 'crit_damage_1', 'name': '+15% Krit-Schaden', 'description': '+15% auf kritischen Trefferschaden',
        'node_type': 'minor', 'bonus_type': 'crit_damage_percent', 'value': 0.15, 'cost': 1,
        'connections': ['crit_chance_1', 'lethal_precision']
    },
    'lethal_precision': {
        'id': 'lethal_precision', 'name': 'Tödliche Präzision', 'description': '+5% Krit-Chance\n+30% Krit-Schaden',
        'node_type': 'notable', 'cost': 3,
        'bonuses': [
            {'type': 'crit_chance_percent', 'value': 0.05},
            {'type': 'crit_damage_percent', 'value': 0.30}
        ],
        'connections': ['crit_damage_1']
    },

    # Verteidigungs-Pfad (neu)
    'armor_1': {
        'id': 'armor_1', 'name': '+50 Rüstung', 'description': '+50 zu Rüstung',
        'node_type': 'minor', 'bonus_type': 'armor', 'value': 50, 'cost': 1,
        'connections': ['strength_2', 'elemental_resistance_1']
    },
    'elemental_resistance_1': {
        'id': 'elemental_resistance_1', 'name': '+10% Elementarwiderstand', 'description': '+10% auf alle Elementarwiderstände',
        'node_type': 'minor', 'bonus_type': 'elemental_resistance_percent', 'value': 0.10, 'cost': 1,
        'connections': ['armor_1', 'shield_mastery']
    },
    'shield_mastery': {
        'id': 'shield_mastery', 'name': 'Schildmeisterschaft', 'description': '+15% Blockchance\n+100 Rüstung',
        'node_type': 'notable', 'cost': 3,
        'bonuses': [
            {'type': 'block_chance_percent', 'value': 0.15},
            {'type': 'armor', 'value': 100}
        ],
        'connections': ['elemental_resistance_1', 'keystone_bulwark']
    },

    # Zusätzliche Minor Nodes
    'attack_speed_1': {'id': 'attack_speed_1', 'name': '+5% Angriffsgeschw.', 'node_type': 'minor', 'bonus_type': 'attack_speed_percent', 'value': 0.05, 'cost': 1, 'connections': ['art_of_the_gladiator']},
    'movement_speed_1': {'id': 'movement_speed_1', 'name': '+5% Bewegungsgeschw.', 'node_type': 'minor', 'bonus_type': 'movement_speed_percent', 'value': 0.05, 'cost': 1, 'connections': ['dexterity_1']},
    'mana_regen_1': {'id': 'mana_regen_1', 'name': '+0.5 Mana/sek', 'node_type': 'minor', 'bonus_type': 'mana_regen', 'value': 0.5, 'cost': 1, 'connections': ['intelligence_2']},
    'evasion_1': {'id': 'evasion_1', 'name': '+5% Ausweichen', 'node_type': 'minor', 'bonus_type': 'evasion_percent', 'value': 0.05, 'cost': 1, 'connections': ['lethal_precision']},
    'area_of_effect_1': {'id': 'area_of_effect_1', 'name': '+10% Wirkungsbereich', 'node_type': 'minor', 'bonus_type': 'aoe_percent', 'value': 0.10, 'cost': 1, 'connections': ['arcane_potency']},
    'all_attributes_1': {'id': 'all_attributes_1', 'name': '+5 Alle Attribute', 'node_type': 'minor', 'bonus_type': 'all_attributes', 'value': 5, 'cost': 2, 'connections': ['art_of_the_gladiator']},

    # Keystone-Knoten
    'keystone_bulwark': {
        'id': 'keystone_bulwark', 'name': 'Unerschütterliches Bollwerk',
        'description': 'Verdoppelt den Rüstungswert. Reduziert die Bewegungsgeschwindigkeit um 20%. Immunität gegen Betäubung.',
        'node_type': 'keystone', 'cost': 5,
        'bonuses': [
            {'type': 'armor_multiplier', 'value': 2.0},
            {'type': 'movement_speed_percent', 'value': -0.20},
            {'type': 'stun_immunity', 'value': 1}
        ],
        'connections': ['vitality_1', 'shield_mastery']
    }
}