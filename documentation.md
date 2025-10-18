# Projektdokumentation: Idle Horde Slayer

Dieses Dokument bietet einen technischen Überblick über die Struktur und die Kernkomponenten des Spiels "Idle Horde Slayer".

## 1. Projektstruktur

Das Projekt ist modular aufgebaut und befindet sich hauptsächlich im `game`-Paket.

- `main.py`: Enthält die Kivy-App-Klasse (`IdleHordeSlayerApp`), die den `ScreenManager` initialisiert und die zentrale `calculate_stats`-Logik enthält.
- `game/`: Das Hauptpaket für die Spiellogik.
  - `screens.py`: Definiert alle Bildschirme der App (`GameScreen`, `SkillTreeScreen`, `CityScreen`, `ShopScreen`, `EquipmentScreen`, `SettingsScreen`).
  - `entities.py`: Enthält Klassen für alle Spielobjekte wie `Hero`, `Enemy`, `Projectile` und Sammelitems (`GoldCoin`, `SoulEssence`, `LootDrop`).
  - `widget.py`: Definiert das `GameWidget`, das die Haupt-Gameplay-Schleife und die Kollisionserkennung steuert.
  - `player_data.py`: Verwaltet das Speichern und Laden aller permanenten Spielerdaten (`player_save.json`).
  - `item_data.py`: Definiert alle Ausrüstungsgegenstände und ihre Boni.
  - `config.py`: Enthält Konfigurationen für Wellen, In-Run-Upgrades und Shop-Upgrades.
- `assets/`: Beinhaltet alle visuellen Ressourcen.

## 2. Gameplay-Systeme

### Meta-Progression

Das Spiel verfügt über mehrere ineinandergreifende Systeme für die langfristige Spielerprogression.

#### a) Währungen

- **Gold:** Eine häufige Währung, die von den meisten Gegnern fallen gelassen wird. Wird für permanente Upgrades im Shop verwendet.
- **Seelenessenz:** Eine seltene Währung, die nur gelegentlich von Gegnern fallen gelassen wird. Ihre Verwendung ist für zukünftige Features (z.B. Crafting) geplant.
- **Skill-Punkte:** Werden durch Gameplay-Erfolge (Mechanik noch zu definieren) erlangt und im Skill-Tree ausgegeben.

#### b) Skill-Tree (`SkillTreeScreen`)

- Ein umfangreicher, passiver Skill-Tree zur permanenten Verbesserung von Charakterwerten.
- **Navigation:** Der Baum ist frei scroll- und zoombar, implementiert mit einem `ScatterLayout`.
- **Knotentypen:** Knoten sind visuell nach ihrer Wertigkeit unterschieden (`start`, `minor`, `notable`, `keystone`).
- **Tooltips:** Beim Überfahren eines Knotens mit der Maus werden dessen Name, Beschreibung und Kosten angezeigt.

#### c) Ausrüstung & Loot (`EquipmentScreen`)

- Gegner haben eine geringe Chance, Ausrüstungsgegenstände fallen zu lassen (`LootDrop`).
- Aufgesammelte Items landen im **Inventar** des Spielers.
- Im `EquipmentScreen` können Spieler Items aus dem Inventar in spezifische **Ausrüstungsslots** (`weapon`, `helmet`, `chest`, etc.) legen.
- Angelegte Ausrüstung gewährt permanente Boni, die in die `calculate_stats`-Logik einfließen.

#### d) Permanenter Upgrade-Shop (`ShopScreen`)

- In der "Stadt" kann der Spieler einen Händler besuchen.
- Im Shop kann Gold für dauerhafte, prozentuale Boni ausgegeben werden (z.B. "+X% mehr Gold-Drops", "+Y% mehr XP-Gewinn").
- Die Kosten für Shop-Upgrades steigen mit jedem gekauften Level exponentiell an.

### In-Run-Progression (XP und Level-Up)

- Besiegte Gegner lassen `XPCrystal`-Objekte fallen.
- **Kristall-Fusion:** 5 oder mehr Kristalle derselben Stufe fusionieren zu einem Kristall der nächsthöheren Stufe, der mehr XP wert ist.
- Bei einem Level-Up wird der `CardSelectionScreen` angezeigt, auf dem der Spieler aus drei zufälligen, temporären Upgrades für den aktuellen Run wählen kann.

### Statistik-System (`calculate_stats` in `main.py`)

- Dies ist die zentrale Methode zur Berechnung der finalen Spielerwerte.
- Sie aggregiert Boni aus drei permanenten Quellen:
  1.  Freigeschaltete Knoten im **Skill-Tree**.
  2.  Angelegte **Ausrüstung**.
  3.  Gekaufte Upgrades im **Shop**.
- Anschließend werden temporäre Boni aus der In-Run-Progression auf diese permanenten Werte aufgeschlagen.
- Das Ergebnis wird an das `GameWidget` und den `Hero` übergeben, um das Gameplay direkt zu beeinflussen.

## 3. Speicherstands-Verwaltung (`SettingsScreen`)

- Um das Übertragen von Spielständen zwischen Geräten zu ermöglichen, wurde eine manuelle Export/Import-Funktion implementiert.
- **Export:** Kopiert die `player_save.json` in einen leicht zugänglichen `exported_save/`-Ordner.
- **Import:** Überschreibt die lokale `player_save.json` mit der aus dem Export-Ordner und lädt die Daten neu, um die Änderungen sofort zu übernehmen.