import pygame
import sys
import random
from entities import Hero, Slime, SkeletonArcher
from ui import Button # Importiert die neue Button-Klasse

# -- Konstanten --
# Legt die Dimensionen des Spielfensters fest.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Legt die maximale Bildwiederholrate (Frames pro Sekunde) fest.
FPS = 60

# Definiert Farben für die spätere Verwendung.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# -- Spiel-Initialisierung --
# Initialisiert alle Pygame-Module, die für das Spiel benötigt werden.
pygame.init()

# Erstellt das Hauptfenster für das Spiel.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# Setzt den Titel des Fensters.
pygame.display.set_caption("Idle Horde Slayer")

# Erstellt ein Clock-Objekt, um die Bildwiederholrate zu kontrollieren.
clock = pygame.time.Clock()

# Erstellt ein Font-Objekt für die Textdarstellung.
font = pygame.font.SysFont(None, 50)

# -- Spielzustands-Management --
# Definiert die verschiedenen Zustände, die das Spiel haben kann.
game_state = "MAIN_MENU" # Mögliche Zustände: "MAIN_MENU", "VILLAGE", "IN_GAME", "SHOP_MENU"

# Erstellt eine Instanz des Helden.
hero = Hero(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
# Erstellt eine Liste, um alle aktiven Gegner zu speichern.
enemies = []
# Verfolgt die aktuelle Welle.
current_wave = 1

def start_new_run():
    # -- Setzt den Zustand für einen neuen Run zurück --
    global game_state, current_wave
    hero.x = SCREEN_WIDTH / 2
    hero.y = SCREEN_HEIGHT / 2
    hero.rect.topleft = (hero.x, hero.y)
    hero.health = 100
    current_wave = 1
    spawn_wave(current_wave)
    game_state = "IN_GAME"

def return_to_village():
    # -- Kehrt zum Dorf zurück --
    global game_state
    # Setzt die Position des Helden zurück, wenn er ins Dorf geht.
    hero.x = SCREEN_WIDTH / 2
    hero.y = SCREEN_HEIGHT / 2
    hero.rect.topleft = (hero.x, hero.y)
    game_state = "VILLAGE"

def open_shop():
    # -- Öffnet das Shop-Menü --
    global game_state
    game_state = "SHOP_MENU"

def upgrade_damage():
    # -- Verbessert den Schaden des Helden, wenn genug Gold vorhanden ist --
    cost = 10 # Kosten für das Upgrade
    if hero.gold >= cost:
        hero.gold -= cost
        hero.damage += 5
        print(f"Schaden verbessert! Neuer Schaden: {hero.damage}. Gold übrig: {hero.gold}")
    else:
        print("Nicht genug Gold für ein Schadens-Upgrade!")

# --- Button-Definitionen ---
village_buttons = [
    Button(300, 250, 200, 50, "Start Run", GREEN, (0, 200, 0), font, action=start_new_run),
    Button(300, 320, 200, 50, "Shop", BLUE, (0, 0, 200), font, action=open_shop)
]
ingame_buttons = [
    Button(SCREEN_WIDTH - 160, SCREEN_HEIGHT - 60, 150, 50, "To Village", RED, (200, 0, 0), font, action=return_to_village)
]
shop_buttons = [
    Button(300, 250, 200, 50, "Upgrade Dmg (10g)", GREEN, (0, 200, 0), font, action=upgrade_damage),
    Button(300, 320, 200, 50, "Back", RED, (200, 0, 0), font, action=return_to_village)
]

def spawn_wave(wave_number):
    # -- Erstellt Gegnerwellen --
    enemies.clear() # Entfernt alte Gegner
    print(f"Spawne Welle {wave_number}")
    if wave_number == 1:
        # Welle 1: 5 Slimes
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH - 16)
            y = random.randint(0, SCREEN_HEIGHT - 16)
            enemies.append(Slime(x, y))
    elif wave_number == 2:
        # Welle 2: 8 Slimes und 1 Bogenschütze
        for _ in range(8):
            x = random.randint(0, SCREEN_WIDTH - 16)
            y = random.randint(0, SCREEN_HEIGHT - 16)
            enemies.append(Slime(x, y))
        x = random.randint(0, SCREEN_WIDTH - 16)
        y = random.randint(0, SCREEN_HEIGHT - 16)
        enemies.append(SkeletonArcher(x, y))

def draw_text(text, font, color, surface, x, y):
    # Hilfsfunktion zum Zeichnen von Text auf dem Bildschirm.
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# -- Haupt-Spiel-Schleife --
# Die 'running'-Variable steuert, ob das Spiel weiterlaufen soll.
running = True
while running:
    # --- Event-Verarbeitung ---
    # Durchläuft alle Ereignisse, die seit dem letzten Frame aufgetreten sind.
    for event in pygame.event.get():
        # Überprüft, ob das Ereignis "Fenster schließen" ist.
        if event.type == pygame.QUIT:
            running = False

        # --- Zustands-spezifische Event-Verarbeitung ---
        if game_state == "MAIN_MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Im Hauptmenü reicht ein Klick, um ins Dorf zu kommen.
                return_to_village()
        elif game_state == "VILLAGE":
            for button in village_buttons:
                button.handle_event(event)
        elif game_state == "SHOP_MENU":
            for button in shop_buttons:
                button.handle_event(event)
        elif game_state == "IN_GAME":
            # Event-Verarbeitung für In-Game-Buttons
            for button in ingame_buttons:
                button.handle_event(event)

            # Verarbeitet Tastendrücke für die Heldenbewegung.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    hero.moving_up = True
                if event.key == pygame.K_s:
                    hero.moving_down = True
                if event.key == pygame.K_a:
                    hero.moving_left = True
                if event.key == pygame.K_d:
                    hero.moving_right = True
            # Verarbeitet das Loslassen von Tasten.
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    hero.moving_up = False
                if event.key == pygame.K_s:
                    hero.moving_down = False
                if event.key == pygame.K_a:
                    hero.moving_left = False
                if event.key == pygame.K_d:
                    hero.moving_right = False

    # --- Spiellogik & Bildschirm zeichnen ---
    # Füllt den Bildschirm mit Schwarz, um alte Zeichnungen zu löschen.
    screen.fill(BLACK)

    # Zeichnet unterschiedliche Inhalte basierend auf dem aktuellen Spielzustand.
    if game_state == "MAIN_MENU":
        draw_text("Main Menu", font, WHITE, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_text("Click to Start", font, GREEN, screen, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)

    elif game_state == "VILLAGE":
        draw_text("Village", font, WHITE, screen, SCREEN_WIDTH / 2, 150)
        draw_text(f"Gold: {hero.gold}", font, WHITE, screen, SCREEN_WIDTH / 2, 200)
        for button in village_buttons:
            button.draw(screen)

    elif game_state == "SHOP_MENU":
        draw_text("Shop", font, WHITE, screen, SCREEN_WIDTH / 2, 150)
        draw_text(f"Gold: {hero.gold}", font, WHITE, screen, SCREEN_WIDTH / 2, 200)
        for button in shop_buttons:
            button.draw(screen)

    elif game_state == "IN_GAME":
        # Bewegt den Helden.
        hero.move()

        # --- Kampflogik ---
        # Geht durch eine Kopie der Gegnerliste, um sie während der Iteration sicher zu verändern.
        for enemy in enemies[:]:
            # Einfache Kollisionserkennung.
            if hero.rect.colliderect(enemy.rect):
                hero.health -= enemy.damage * (1/FPS)
                enemy.health -= hero.damage * (1/FPS)

            if enemy.health <= 0:
                hero.gold += enemy.gold_reward
                enemies.remove(enemy)
                print(f"Gegner besiegt! Gold: {hero.gold}")

        # Überprüft, ob der Held besiegt wurde.
        if hero.health <= 0:
            print("Held wurde besiegt! Zurück zum Dorf.")
            return_to_village()

        # Überprüft, ob die Welle abgeschlossen ist.
        if not enemies:
            print(f"Welle {current_wave} abgeschlossen!")
            current_wave += 1
            # Hier könnte eine Logik für eine maximale Wellenanzahl eingefügt werden.
            spawn_wave(current_wave)

        # --- Zeichnen ---
        hero.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for button in ingame_buttons:
            button.draw(screen)

        # Zeigt die Lebenspunkte, Gold und aktuelle Welle an.
        draw_text(f"Health: {int(hero.health)}", font, WHITE, screen, 100, 30)
        draw_text(f"Gold: {hero.gold}", font, WHITE, screen, 700, 30)
        draw_text(f"Wave: {current_wave}", font, WHITE, screen, SCREEN_WIDTH / 2, 30)

    # --- Bildschirm aktualisieren ---
    # Zeigt den neu gezeichneten Frame auf dem Bildschirm an.
    pygame.display.flip()

    # --- Bildwiederholrate kontrollieren ---
    # Sorgt dafür, dass die Schleife nicht öfter als 'FPS' mal pro Sekunde läuft.
    clock.tick(FPS)

# -- Spiel beenden --
# Gibt alle von Pygame verwendeten Ressourcen frei.
pygame.quit()
# Beendet das Python-Skript.
sys.exit()