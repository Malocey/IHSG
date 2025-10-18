# AGENTS.md - Guidelines for AI Agents

This document provides instructions for AI agents working on the "Idle Horde Slayer" codebase. Adhering to these guidelines is crucial for maintaining code quality, consistency, and alignment with the project's vision.

## 1. Core Principles

1.  **Language and Comments**:
    *   **Code**: All new variables, functions, classes, and method names **must** be in **English**.
    *   **Comments**: All new code comments and documentation strings (`"""Docstrings"""`) **must** be in **German**. This is a specific user request. Maintain this convention strictly.

2.  **Architectural Style**:
    *   The project uses the Kivy framework. All UI and game logic should be built upon Kivy's widgets and event-driven architecture.
    *   The project is structured into a `game` package. New logic should be added to the appropriate module (e.g., UI elements in `screens.py`, game objects in `entities.py`).

3.  **Asset Handling**:
    *   When adding new characters or animations, assume the use of sprite sheets where animation frames are laid out horizontally.
    *   Do not add new, single-image assets for animation frames. If new assets are required, inform the user that they need to be provided.

## 2. Code Structure & Key Modules

- `main.py`: The entry point of the application. Contains the `IdleHordeSlayerApp` class, which initializes the `ScreenManager` and holds the central `calculate_stats` method.
- `game/screens.py`: Defines all UI screens (`GameScreen`, `CityScreen`, `ShopScreen`, `EquipmentScreen`, etc.).
- `game/widget.py`: Contains the `GameWidget`, which manages the core gameplay loop, entity updates, and collision detection.
- `game/entities.py`: Defines all interactive game objects (`Hero`, `Enemy`, `Projectile`, `GoldCoin`, `LootDrop`).
- `game/player_data.py`: Handles saving and loading of all permanent player data to `player_save.json`, including currency, skills, inventory, and equipment.
- `game/config.py`: A central place for game balance and configuration, such as `WAVE_CONFIG`, `CARD_UPGRADES`, and `SHOP_UPGRADES`.
- `game/item_data.py`: Defines the master list of all equipment, including their stats, type, and rarity.
- `game/animation.py`: Contains the `SpriteManager` and `AnimatedSprite` classes for handling sprite sheet animations.
- `game/ui.py`: Contains reusable UI components like `HealthBar` and `DamageNumber`.
- `game/effects.py`: Contains visual effects like `ParticleSystem`.

## 3. Gameplay Systems

*   **Statistics (`calculate_stats` in `main.py`)**: This is the single source of truth for all player stats. When adding new bonuses (from skills, items, etc.), ensure they are aggregated here. Do not modify player stats directly elsewhere. The method should calculate the final stats and then push them to the relevant game objects.
*   **Item & Loot System**:
    - New items must be defined in `game/item_data.py`.
    - Dropped items are represented by the `LootDrop` class in `game/entities.py`.
    - Player inventory and equipment are managed in `game/player_data.py`.
*   **Progression Systems**:
    - **In-Run (Temporary)**: Handled by `XPCrystal` drops and the `CardSelectionScreen`. Effects should modify temporary bonus variables in `IdleHordeSlayerApp`.
    - **Skill Tree (Permanent)**: Data is in `game/skill_tree_data.py`. Unlocked nodes are stored in `PlayerData`.
    - **Shop (Permanent)**: Data is in `game/config.py`. Purchased levels are stored in `PlayerData`.
    - **Equipment (Permanent)**: Items are defined in `game/item_data.py`. Inventory and equipped items are stored in `PlayerData`.

## 4. Finalizing Your Work

*   **Documentation**: After implementing a new feature, you **must** update the relevant documentation files (`CHANGELOG.md`, `documentation.md`, `FAQ.md`, `AGENTS.md`) to reflect the changes. This is a critical step.
*   **Run Tests**: Run existing tests to ensure no regressions were introduced.
*   **Verify UI**: If you make visual changes, attempt to verify them by generating a screenshot. Acknowledge if the process fails, but still proceed with code review.
*   **Code Review**: Always request a code review before submitting. Address the feedback provided.
*   **Clean Up**: Before submitting, remove any temporary files or directories (like `jules-scratch` or `test`).