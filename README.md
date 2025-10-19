# Idle Horde Slayer

Ein prozedural generiertes Idle-Spiel, bei dem ein Held automatisch Horden von Gegnern bekämpft. Der Spieler verbessert den Helden durch einen umfangreichen Skill-Tree, sammelt Loot, rüstet Gegenstände aus und kauft permanente Upgrades in einer Stadt.

## Features

-   **Prozedurale Karten:** Jede Runde findet in einer zufällig generierten Dungeon-Karte statt.
-   **Automatischer Kampf:** Der Held bewegt sich und greift selbstständig an.
-   **Tiefes Progressionssystem:**
    -   Temporäre Upgrades während eines Runs.
    -   Ein permanenter, passiver Skill-Tree.
    -   Ein Loot-System mit Ausrüstungs-Slots.
    -   Ein Shop in der Stadt für permanente Meta-Upgrades.
-   **Visuelle Effekte:** Partikelexplosionen und andere Effekte für befriedigendes Gameplay-Feedback.

## Getting Started

Dieses Projekt wird mit dem Kivy-Framework in Python entwickelt.

### 1. Voraussetzungen

-   Python 3.9+
-   pip (Python package installer)
-   Git

### 2. Setup

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/No-More-Interns/IHSG.git
    cd IHSG
    ```

2.  **Virtuelle Umgebung erstellen und aktivieren (empfohlen):**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

3.  **Abhängigkeiten installieren:**
    ```bash
    pip install -r requirements.txt
    ```
    *Hinweis: Wenn es bei der Installation von Kivy zu Problemen kommt, stelle sicher, dass du die neuesten Build-Tools für deine Plattform installiert hast (z.B. Visual Studio Build Tools unter Windows).*

4.  **Assets herunterladen:**
    Das Spiel benötigt externe Sprite-Sheet-Assets. Führe die folgenden Befehle im Hauptverzeichnis des Projekts aus, um sie in den `assets`-Ordner zu klonen:
    ```bash
    git clone https://github.com/s4m-ur4i/lpc-base-assets.git assets/hero
    git clone https://github.com/s4m-ur4i/lpc-monsters.git assets/enemies
    ```

### 3. Spiel starten

Du kannst das Spiel direkt aus dem Quellcode starten:

```bash
python main.py
```

### 4. Executable erstellen (Windows)

Um das Spiel in eine eigenständige `.exe`-Datei für Windows zu verpacken, führe das mitgelieferte Build-Skript aus:

```bash
build_windows.bat
```

Das Skript kümmert sich um die Installation der Abhängigkeiten und den PyInstaller-Prozess. Die fertige Anwendung befindet sich danach im Ordner `dist/main`.

---
*Dieses Projekt befindet sich in aktiver Entwicklung.*