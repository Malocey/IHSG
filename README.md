# Idle Horde Slayer

This is a simple idle game where a hero automatically fights off waves of enemies. The player can upgrade the hero's abilities and unlock new features.

## Getting Started

This project is built with the Kivy framework in Python. To get it running on your local machine, follow these steps.

### 1. Prerequisites

*   Python 3.7+
*   pip (Python package installer)

### 2. Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd IdleHordeSlayer
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. Required Assets

The game requires a few image assets to display the characters and effects. **You will need to download these files and place them in the `assets` directory according to the specified paths.**

Create the following folder structure inside your project's root directory:
```
/assets
|-- /hero
|-- /enemy
|-- /projectile
```

Here are the links to download the required sprites.

*   **Hero (24x24):**
    *   **Source:** [Universal LPC Sprite Sheet Character Generator](https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/)
    *   **Instructions:**
        1.  Use the generator to create a character.
        2.  Select the "Walk" animation.
        3.  Click "Download image pack with credits and JSON (ZIP)".
        4.  From the downloaded ZIP, find a single frame of the walking animation (e.g., `walkcycle_e_0.png`).
        5.  Rename it to `hero.png` and place it in the `assets/hero/` directory.
    *   **License:** CC-BY-SA 3.0 or similar (Credit the artists as listed on the generator page).

*   **Enemy (16x16):**
    *   **Source:** [Pixel Crawler Free Asset Pack by Anokolisa](https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites)
    *   **Instructions:**
        1.  Download the `Pixel Crawler - Free Pack 2.0.4.zip`.
        2.  Inside the zip, navigate to `Pixel Crawler - Free Pack 2.0.4/Enemies/Orc/Idle`.
        3.  Take any of the `*.png` files (e.g., `Orc_Idle_1.png`).
        4.  Rename it to `enemy.png` and place it in `assets/enemy/`.
    *   **License:** Free to use, but the author requests that you rate the asset pack on itch.io.

*   **Projectile:**
    *   **Source:** Also from the [Pixel Crawler Free Asset Pack](https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites).
    *   **Instructions:**
        1.  In the same downloaded ZIP, navigate to `Pixel Crawler - Free Pack 2.0.4/Weapons/Wood/`.
        2.  Find the `Arrow.png` file.
        3.  Rename it to `projectile.png` and place it in `assets/projectile/`.
    *   **License:** Same as the enemy asset.


### 4. Running the Game

You can run the game directly from the source code:

```bash
python main.py
```

### 5. Building the Executable (Windows)

To package the game into a standalone `.exe` file on Windows, simply run the provided build script:

```bash
build_windows.bat
```

The script will handle the dependency installation and the PyInstaller process. The final executable will be located in the `dist/IdleHordeSlayer` folder.

---
*This project is currently under development.*