# AGENTS.md - Guidelines for AI Agents

This document provides instructions for AI agents working on the "Idle Horde Slayer" codebase. Adhering to these guidelines is crucial for maintaining code quality, consistency, and alignment with the project's vision.

## 1. Core Principles

1.  **Language and Comments**:
    *   **Code**: All new variables, functions, classes, and method names **must** be in **English**.
    *   **Comments**: All new code comments and documentation strings (`"""Docstrings"""`) **must** be in **German**. This is a specific user request. Maintain this convention strictly.

2.  **Architectural Style**:
    *   The project uses the Kivy framework. All UI and game logic should be built upon Kivy's widgets and event-driven architecture.
    *   The current structure is a single-file application (`main.py`). While this may change in the future, for now, new classes and logic should be added to this file unless a refactoring into multiple files is explicitly requested.

3.  **Asset Handling**:
    *   The game's visual assets are based on sprite sheets. The animation system (`SpriteManager`, `AnimatedSprite`) is designed to handle this.
    *   When adding new characters or animations, assume the use of sprite sheets where animation frames are laid out horizontally.
    *   Do not add new, single-image assets for animation frames. If new assets are required, inform the user that they need to be provided in a sprite sheet format.

## 2. Animation System Usage

The animation system is a core component. When working with it, follow these rules:

*   **Inherit from `AnimatedSprite`**: Any game object that needs to be animated (characters, effects, etc.) should inherit from the `AnimatedSprite` class.
*   **Use `set_animation()` for State Changes**: Do not manually manipulate textures. Use the `set_animation(name, loop, on_end)` method to control an object's visual state.
    *   For continuous animations (like walking or idle), use `loop=True`.
    *   For one-shot animations (like death, attacks, or spell casts), use `loop=False` and provide an `on_end` callback function to handle the logic that should occur after the animation finishes (e.g., removing the object, dealing damage).
*   **Load Multiple Sheets in the Constructor**: If a character has multiple, separate animation sheets (e.g., one for running, one for dying), load them within the class's `__init__` method. Create additional `SpriteManager` instances if necessary and manually add the animation frames to the primary `sprite_manager.animations` dictionary. See the `Enemy` class for an example of this pattern.

## 3. Code Modifications

*   **Verify Asset Paths**: Before implementing code that uses an asset, always verify the exact path to that asset using `list_files` or `run_in_bash_session`. Asset paths are a common source of errors.
*   **Maintain German Comments**: When modifying existing code, ensure that any new comments you add are in German. Preserve existing English code elements.
*   **Run the Game**: Although you cannot "see" the output, after making significant changes, you can attempt to run the application (`python main.py`) to check for runtime errors or crashes. This is a good practice to catch issues before finalizing your work.
*   **Follow the Plan**: Stick to the user-approved plan. If you discover a necessary deviation, update the plan using `set_plan` and notify the user.

## 4. Code Structure

The project is structured into a `game` package. Key modules include:
- `game/animation.py`: Contains `SpriteManager` and `AnimatedSprite`.
- `game/entities.py`: Contains `Hero`, `Enemy`, and `Projectile`.
- `game/ui.py`: Contains UI elements like `HealthBar` and `DamageNumber`.
- `game/widget.py`: Contains the main `GameWidget`.
- `game/screens.py`: Contains the `GameScreen` and `CardSelectionScreen`.
- `game/config.py`: Contains game configurations like `WAVE_CONFIG`.
- `game/effects.py`: Contains visual effects like `ParticleSystem`.

## 5. Gameplay Systems

*   **Wave System**: Enemy waves are defined in `game/config.py`. When adding new enemies or balancing waves, modify this configuration. The system is designed to automatically handle wave progression and difficulty scaling.
*   **Statistics**: All player stats are calculated in the `IdleHordeSlayerApp.calculate_stats()` method. Do not hardcode stat values directly in the `Hero` or `GameWidget` classes. Instead, add new base stats or bonus calculations to this central method.
*   **In-Run Progression**: The level-up logic is handled in `GameWidget.level_up()`. This method is responsible for incrementing the player's level, increasing the XP required for the next level, and switching to the `CardSelectionScreen`. When implementing card effects, ensure they modify the temporary bonus placeholders in `calculate_stats()` and then trigger a recalculation.