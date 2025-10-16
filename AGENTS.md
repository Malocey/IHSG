# Agent Instructions

This document provides guidelines for AI agents working on the Idle Horde Slayer project.

## Core Conventions

1.  **Language:**
    *   All Python code (variables, functions, class names, etc.) must be written in **English**.
    *   All code comments must be written in **German** (`Deutsch`).

2.  **Framework:**
    *   The project is built using the **Kivy** framework in Python. All UI and application logic should be compatible with Kivy.

3.  **Project Structure:**
    *   `main.py`: The main entry point of the application.
    *   `src/`: Contains core source code, such as game entities (`entities.py`) and data definitions (`skills.py`).
    *   `assets/`: For all static assets like images (`.png`) and sounds.
    *   `docs/`: For design documents and other project documentation.

4.  **Code Style:**
    *   Follow standard Python PEP 8 guidelines.
    *   Ensure code is well-structured and readable. Separate concerns into different classes and modules where appropriate.

## Development Goals

*   **Primary Goal:** Develop an Idle Horde Slayer game with deep progression systems (skills, items, etc.).
*   **Visual Target:** Aim for a high-quality visual presentation, inspired by "HD-2D" games like Octopath Traveler and visually rich action games like Vampire Survivors. This includes implementing particle effects, shaders, and other advanced graphical features.
*   **Platform Target:** The final application should be buildable as a Windows executable (`.exe`) and an Android package (`.apk`).