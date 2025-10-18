# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-10-18

### Added
- **Skill Tree Overhaul:**
  - The skill tree is now scrollable and zoomable.
  - Nodes are visually distinct based on their type (start, minor, notable, keystone).
  - Added tooltips to show node details on hover.
  - Massively expanded the tree with over 20 new nodes, including new paths and a keystone.
- **Meta-Gameplay Loop:**
  - Implemented a "City" screen as a central hub for meta-progression.
  - Added a permanent upgrade shop where players can spend Gold.
  - Introduced two new currencies: Gold (common) and Soul Essence (rare), which drop from enemies.
- **Equipment & Loot System:**
  - Created a basic loot system where enemies can drop equipment.
  - Implemented a player inventory and equipment screen to manage items.
  - Stats from equipped items are now correctly applied to the player.
- **Save Game Management:**
  - Added a settings screen with options to manually export and import the `player_save.json` file.

### Changed
- Refactored `PlayerData` to store new currencies, shop upgrade levels, inventory, and equipment.
- The main `calculate_stats` method now integrates bonuses from the skill tree, shop, and equipment.

## [0.1.0] - 2025-10-16

### Added
- Initial project setup with a basic Kivy application structure.
- Simple gameplay loop: a hero moves and shoots, and a single enemy type spawns.
- Build scripts (`build.spec`, `build_windows.bat`) for creating a Windows executable.
- `README.md` with setup and build instructions.
- `requirements.txt` for dependency management.

### Fixed
- Restored project to a simple, functional state after an accidental reset.
- Provided a clear list of required assets and instructions for setting them up.