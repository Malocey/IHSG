# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documentation files: `AGENTS.md`, `README.md`, `CHANGELOG.md`, `VERSION`.
- Design document for visual effects: `docs/visual_effects_design.md`.

## [0.1.0] - 2025-10-15

This is the first functional version of the Idle Horde Slayer game, featuring a complete skill and character stat system.

### Added
- **Skill Leveling System:** Skills now have levels and can be upgraded.
- **Character Stat System:** Character stats are now calculated based on the levels of unlocked skills.
- **Gameplay Integration:** The hero's movement speed is now affected by the "Hero Speed" skill.
- **Functional Skill Tree:** A fully interactive skill tree screen where players can spend points to unlock and upgrade skills.
- **Screen Manager:** Implemented a system to switch between different game views (Game, Hero, etc.).
- **Basic UI Layout:** The application has a top status bar, a central game area, and a bottom navigation bar.
- **Initial Project Setup:** Created the basic file structure, Kivy application window, and core game loop with a moving hero and spawning enemies.
- **Player Data:** Implemented systems to track player currency (gold, gems), score, and skill points.
- **Robust Asset Loading:** Entities now have a fallback (colored rectangle) if their sprite images are not found, preventing crashes.