# Projektdokumentation: Idle Horde Slayer

Dieses Dokument bietet einen technischen Überblick über die Struktur und die Kernkomponenten des Spiels "Idle Horde Slayer".

## 1. Projektstruktur

Das Projekt ist in einer einzigen Python-Datei (`main.py`) organisiert, die alle Spiel-Logik enthält. Die visuellen Assets sind im `assets`-Verzeichnis untergebracht.

- `main.py`: Enthält die Kivy-App, die Spiel-Widgets und die gesamte Logik für Charaktere, Gegner und Animationen.
- `assets/`: Beinhaltet alle visuellen Ressourcen wie Sprite-Sheets für Helden, Gegner und Umgebungsobjekte.
- `requirements.txt`: Listet alle notwendigen Python-Bibliotheken auf.
- `build.spec` / `build_windows.bat`: Skripte zur Erstellung einer ausführbaren Windows-Datei.

## 2. Das Animationssystem

Das Herzstück der visuellen Darstellung ist ein flexibles, auf Sprite-Sheets basierendes Animationssystem. Es besteht aus zwei Hauptklassen:

### `SpriteManager`

Diese Klasse ist für das Laden und Verwalten von Sprite-Sheets verantwortlich.

- **Konstruktor (`__init__`)**: Nimmt den Pfad zu einem Sprite-Sheet sowie die Breite und Höhe eines einzelnen Frames entgegen.
- **`_slice_sheet()`**: Eine interne Methode, die das Sheet automatisch in einzelne, speicheroptimierte Kivy-Texturen (`TextureRegion`) zerlegt. Dies geschieht nur einmal beim Laden, um die Performance zu maximieren.
- **`add_animation()`**: Ermöglicht die Definition einer benannten Animation (z.B. 'walk', 'idle', 'death') durch die Angabe einer Sequenz von Frame-Indizes und einer Abspielgeschwindigkeit (`frame_rate`).

### `AnimatedSprite`

Dies ist die Basisklasse für alle animierten Objekte im Spiel (wie `Hero` und `Enemy`).

- **Konstruktor (`__init__`)**: Erstellt eine Instanz des `SpriteManager`, um die Animationsdaten zu verwalten.
- **`set_animation(name, loop, on_end)`**: Wechselt die aktive Animation.
  - `loop` (bool): Bestimmt, ob die Animation in einer Schleife abgespielt wird.
  - `on_end` (callable): Eine optionale Callback-Funktion, die am Ende einer nicht-loopenden Animation ausgeführt wird. Dies ist entscheidend für Zustandsübergänge, wie z.B. das Entfernen eines Gegners nach seiner Todesanimation.
- **`update_animation(dt)`**: Diese Methode wird in jedem Frame des Spiels aufgerufen und aktualisiert den aktuellen Frame der Animation basierend auf der vergangenen Zeit (`dt`). Sie steuert das Timing und die Logik für Looping und Callbacks.

## 3. Spiel-Entitäten

### `Hero` und `Enemy`

Beide Klassen erben von `AnimatedSprite` und sind somit animierbar.

- Im Konstruktor jeder Klasse werden die spezifischen Sprite-Sheets geladen und die jeweiligen Animationen (z.B. Laufen, Sterben) definiert.
- Die `Enemy`-Klasse verfügt über eine `die()`-Methode, die die Todesanimation startet und sicherstellt, dass das Objekt erst nach Abschluss der Animation aus dem Spiel entfernt wird.

### `GameWidget`

Das Haupt-Widget, das die gesamte Spiellogik steuert.

- **`update(dt)`-Methode**: Ruft `update_animation(dt)` für alle aktiven animierten Objekte auf.
- **Kollisionserkennung**: Löst die `die()`-Methode eines Gegners aus, anstatt ihn sofort zu entfernen, um einen sauberen visuellen Übergang zu gewährleisten.
- **`on_enemy_death(enemy)`**: Eine Callback-Methode, die von der `AnimatedSprite`-Klasse aufgerufen wird, um das Gegnerobjekt endgültig aus dem Speicher und von der Anzeige zu entfernen.

## 4. Gameplay-Systeme

### Wellen-System (`game/config.py`)

- Die Gegner erscheinen in Wellen, die in der `WAVE_CONFIG`-Konstante definiert sind.
- Jede Welle hat eine Dauer, eine Liste von möglichen Gegnertypen, eine maximale Gegneranzahl und ein Spawn-Intervall.
- Die `start_next_wave()`-Methode im `GameWidget` steuert den Übergang zwischen den Wellen und erhöht den Schwierigkeitsgrad, indem die Lebenspunkte neuer Gegner mit jeder Runde durch die Konfiguration multipliziert werden.

### Statistik-System

- Die `IdleHordeSlayerApp`-Klasse enthält eine `calculate_stats()`-Methode, die als zentrale Anlaufstelle für die Berechnung aller spielrelevanten Werte dient.
- Aktuell sind die Boni noch Platzhalter, aber das System ist darauf ausgelegt, Werte aus verschiedenen Quellen (z.B. Skill-Tree, temporäre Upgrades) zu kombinieren.
- Die berechneten Werte (Schaden, Geschwindigkeit, Angriffs-Cooldown) werden an das `GameWidget` übergeben und beeinflussen direkt das Verhalten des Helden.

### In-Run-Progression (XP und Level-Up)

- Besiegte Gegner lassen `XPCrystal`-Objekte der Stufe 0 fallen.
- Kristalle bewegen sich langsam auf den Helden zu.
- **Kristall-Fusion:** Wenn 5 oder mehr Kristalle derselben Stufe nahe beieinander liegen, werden sie zu einem einzigen Kristall der nächsthöheren Stufe fusioniert. Dieser neue Kristall ist 5-mal so viel wert und wird zur besseren Erkennung größer und in einer anderen Farbe dargestellt.
- Beim Einsammeln erhält der Spieler den entsprechenden XP-Wert des Kristalls.
- Erreicht die Gesamt-XP den Schwellenwert, wird ein Level-Up ausgelöst und der `CardSelectionScreen` angezeigt.

## 5. Visuelle Effekte ("Juice")

- **`DamageNumber`**: Eine Klasse, die auf dem Bildschirm schwebende Schadenszahlen erzeugt, wenn ein Gegner getroffen wird. Sie nutzt Kivy's `Animation`-Klasse, um nach oben zu schweben und zu verblassen.
- **`screen_shake()`**: Eine Methode im `GameWidget`, die durch eine schnelle Sequenz von Positionsänderungen der gesamten Spiel-Leinwand einen Schütteleffekt erzeugt. Dieser wird ausgelöst, wenn ein Gegner stirbt, um dem Kampf mehr Wucht zu verleihen.