# FAQ - Häufig gestellte Fragen

Hier finden Sie Antworten auf häufig gestellte Fragen zum Spiel "Idle Horde Slayer".

## 1. Gameplay

**F: Was ist das Ziel des Spiels?**
A: "Idle Horde Slayer" ist ein Idle-Spiel. Der Held kämpft automatisch gegen endlose Wellen von Gegnern. Ihre Aufgabe als Spieler ist es, den Helden durch Upgrades zu verstärken, neue Fähigkeiten freizuschalten und ihn so immer mächtiger zu machen.

**F: Wie funktioniert das Upgrade-System?**
A: Das Spiel kombiniert zwei Systeme:
1.  **Permanente Upgrades:** Zwischen den Spieldurchläufen können Sie in einem Skill-Tree permanente Boni freischalten.
2.  **Temporäre Upgrades (In-Run):** Während eines Laufs sammeln Sie XP-Kristalle von besiegten Gegnern. Diese Kristalle können auf dem Spielfeld zu stärkeren Versionen fusionieren, wenn genügend von ihnen nahe beieinander liegen. Bei einem Level-Up erhalten Sie eine Auswahl von drei zufälligen Karten, die mächtige, aber nur für diesen Lauf gültige Boni gewähren.

**F: Kann ich den Helden direkt steuern?**
A: Nein, das Kernkonzept ist "Idle". Der Held bewegt und kämpft von allein. Der Fokus des Spielers liegt auf strategischen Entscheidungen bei den Upgrades.

## 2. Technik & Assets

**F: Welche Engine wird verwendet?**
A: Das Spiel wird mit dem **Kivy-Framework** in Python entwickelt. Kivy ermöglicht die plattformübergreifende Entwicklung für Windows, macOS, Linux, Android und iOS.

**F: Woher stammen die Grafiken?**
A: Die Assets sind eine Kombination aus verschiedenen frei verfügbaren Quellen, um einen "HD-2D"-ähnlichen Stil zu erzielen. Die Hauptquellen sind:
- **Held:** [Liberated Pixel Cup (LPC) Sprite Sheet Generator](https://liberatedpixelcup.github.io/Universal-LPC-Spritesheet-Character-Generator/)
- **Gegner & Umgebung:** [Pixel Crawler Asset Pack von Anokolisa](https://anokolisa.itch.io/free-pixel-art-asset-pack-topdown-tileset-rpg-16x16-sprites)

**F: Kann ich die Assets austauschen?**
A: Ja, solange die Animations-Sprite-Sheets einem ähnlichen Format folgen (alle Frames in einer Reihe), können die Pfade in den `Hero`- und `Enemy`-Klassen in `main.py` leicht angepasst werden.

## 3. Zukünftige Entwicklung

**F: Welche Features sind als Nächstes geplant?**
A: Die Roadmap umfasst unter anderem:
- Ein umfassendes, prozedural generiertes Skill-Tree-System.
- Zufällig generierte Dungeons und Landschaften.
- Ein Händler/Waffenschmied zum Kaufen und Modifizieren von Ausrüstung.
- Visuelle Effekte wie Partikelsysteme und dynamische Beleuchtung.
- Ein Koop-Modus (Shared- oder Split-Screen).

**F: Wie kann ich zur Entwicklung beitragen?**
A: Das Projekt ist derzeit in einer frühen Phase. Zukünftig könnten Beiträge aus der Community in Betracht gezogen werden. Halten Sie Ausschau nach Updates in der `README.md`.