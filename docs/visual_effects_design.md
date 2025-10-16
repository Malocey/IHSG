# Design Document: Visual Effects (VFX)

This document outlines the vision and technical approach for the visual effects in the Idle Horde Slayer game.

## Core Vision

The game aims for a high-quality, visually engaging combat experience. The primary inspirations are the rich particle effects of games like *Vampire Survivors* and the "HD-2D" aesthetic of games like *Octopath Traveler*. This means combining retro pixel art with modern, high-fidelity effects.

## Key VFX Categories

The following categories of visual effects are planned for implementation.

### 1. Projectiles
This covers all forms of attacks that travel across the screen.
- **Simple Projectiles:** Basic arrows, magic bolts. Simple, fast-moving sprites.
- **Advanced Projectiles:**
    - **Laser Beams:** Continuous, wide beams of light. Can be implemented using dynamically generated meshes or shaders.
    - **Homing Missiles:** Projectiles that track a target.
    - **Piercing Shots:** Projectiles that travel through multiple enemies.
- **Technical Approach:** Animated sprites, potentially with particle trails. Shaders can be used for glowing and distortion effects.

### 2. Explosions & Area of Effect (AoE)
These effects cover a specific area on the screen.
- **Standard Explosions:** Bursts of fire, light, or energy upon impact.
- **Lingering AoE:** Persistent ground effects like a field of fire or a pool of poison.
- **Technical Approach:** This is the primary use case for **Particle Systems**. A single explosion could consist of hundreds of particles for fire, sparks, and smoke, each with its own lifecycle (color, size, velocity over time).

### 3. Auras
Persistent visual effects attached to characters.
- **Stat Buff Auras:** A subtle glow or circling particles to indicate a temporary boost (e.g., increased attack speed).
- **Damage Auras:** A visible, damaging field around the player (e.g., a holy aura).
- **Technical Approach:** Animated sprites parented to the character, combined with shaders for glow and transparency.

### 4. Status Effects
Visual indicators on enemies or the player.
- **Burning:** A small, continuous fire particle effect on the target.
- **Frozen:** The target is tinted blue and has a frost/ice shader effect applied.
- **Poisoned:** The target drips green particles.
- **Stunned:** Swirling stars or electrical sparks above the target's head.
- **Technical Approach:** A combination of attaching small particle emitters to characters and applying color/shader overlays.

### 5. Hit Effects
Instantaneous feedback when an attack connects.
- **Impact Sparks:** A quick burst of sparks at the point of collision.
- **Damage Numbers:** Floating, animated numbers showing the damage dealt. Can have different colors/sizes for critical hits.
- **Screen Shake:** A brief, subtle shake of the camera to emphasize powerful hits.
- **Technical Approach:** Spawning short-lived particle effects or animated sprites at the impact location.

## "HD-2D" Implementation Strategy

To achieve the Octopath Traveler-inspired look, the following technical steps are planned:
1.  **3D Scene:** The game world will be rendered as a 3D scene.
2.  **2D Sprites:** Characters, enemies, and objects will be 2D sprites billboarded to always face the camera.
3.  **Orthographic Camera:** The camera will be mostly orthographic but can be slightly tilted to create a sense of depth.
4.  **Post-Processing Shaders:** A shader pipeline will be used to apply effects to the final rendered image, including:
    - **Bloom:** For intense light and glow effects.
    - **Depth of Field:** To blur the foreground and background.
    - **Vignetting:** To darken the screen edges for a cinematic feel.
    - **God Rays:** Volumetric light shafts.