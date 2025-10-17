import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.image import Image as CoreImage

class SpriteManager:
    """
    Verwaltet das Laden und Zerschneiden von Sprite-Sheets sowie die Definition von Animationen.
    """
    def __init__(self, sheet_path, frame_width, frame_height):
        # Lädt die Textur des Sprite-Sheets.
        self.sheet_texture = CoreImage(sheet_path).texture
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.animations = {}
        self._frames = []
        self._slice_sheet()

    def _slice_sheet(self):
        """
        Zerschneidet das Sprite-Sheet in einzelne Frames basierend auf der Frame-Größe.
        """
        sheet_width, sheet_height = self.sheet_texture.size
        cols = int(sheet_width // self.frame_width)
        rows = int(sheet_height // self.frame_height)

        for row in range(rows):
            for col in range(cols):
                x = col * self.frame_width
                # Kivy-Texturen haben ihren Ursprung unten links. Die y-Koordinate muss invertiert werden.
                y = sheet_height - (row + 1) * self.frame_height
                frame = self.sheet_texture.get_region(x, y, self.frame_width, self.frame_height)
                self._frames.append(frame)

    def add_animation(self, name, frame_indices, frame_rate):
        """
        Definiert eine neue Animation durch die Angabe von Frame-Indizes und einer Abspielrate.
        - name: Name der Animation (z.B. 'walk', 'idle').
        - frame_indices: Eine Liste von Indizes, die die Reihenfolge der Frames bestimmen.
        - frame_rate: Zeit in Sekunden zwischen den Frames.
        """
        self.animations[name] = {
            'frames': [self._frames[i] for i in frame_indices],
            'frame_rate': frame_rate
        }

    def get_animation(self, name):
        """
        Gibt die Daten für eine benannte Animation zurück.
        """
        return self.animations.get(name)


class AnimatedSprite(Widget):
    """
    Ein Widget, das eine Animation aus einem Sprite-Sheet abspielen kann.
    Ersetzt die statische Sprite-Klasse für animierte Objekte.
    """
    def __init__(self, sheet_path, frame_width, frame_height, **kwargs):
        super().__init__(**kwargs)
        # Der SpriteManager kümmert sich um die Textur-Daten.
        self.sprite_manager = SpriteManager(sheet_path, frame_width, frame_height)

        self.current_animation_name = None
        self.current_animation_data = None
        self.current_frame_index = 0
        self.frame_time = 0.0 # Zähler für die Zeit seit dem letzten Frame-Wechsel
        self.animation_finished = False

        with self.canvas:
            # Startet mit dem ersten Frame als Standard-Textur.
            default_texture = self.sprite_manager._frames[0] if self.sprite_manager._frames else None
            self.rect = Rectangle(texture=default_texture, pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        """Aktualisiert die Position und Größe des Rechtecks auf der Canvas."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def add_animation(self, name, frame_indices, frame_rate=1.0/10.0):
        """
        Fügt eine Animation hinzu. Eine Hilfsmethode, die den Aufruf an den SpriteManager weiterleitet.
        """
        self.sprite_manager.add_animation(name, frame_indices, frame_rate)

    def set_animation(self, name, loop=True, on_end=None):
        """
        Wechselt die aktuell abgespielte Animation.
        - loop: Wenn False, wird die Animation nur einmal abgespielt.
        - on_end: Eine Callback-Funktion, die am Ende einer nicht-loopenden Animation aufgerufen wird.
        """
        if self.current_animation_name == name and not self.animation_finished:
            return

        anim_data = self.sprite_manager.get_animation(name)
        if anim_data:
            self.current_animation_name = name
            # Wir kopieren die Daten, um sie für diese Instanz modifizieren zu können.
            self.current_animation_data = anim_data.copy()
            self.current_animation_data['loop'] = loop
            self.current_animation_data['on_end'] = on_end
            self.current_frame_index = 0
            self.frame_time = 0.0
            self.animation_finished = False
            self.rect.texture = self.current_animation_data['frames'][0]
        else:
            print(f"Warnung: Animation '{name}' wurde nicht gefunden.")

    def update_animation(self, dt):
        """
        Wird in jeder Frame des Spiels aufgerufen, um die Animation zu aktualisieren.
        """
        if not self.current_animation_data or self.animation_finished:
            return

        self.frame_time += dt
        frame_rate = self.current_animation_data['frame_rate']

        if self.frame_time >= frame_rate:
            self.frame_time -= frame_rate
            self.current_frame_index += 1

            animation_frames = self.current_animation_data['frames']
            num_frames = len(animation_frames)

            if self.current_frame_index >= num_frames:
                if not self.current_animation_data.get('loop', True):
                    self.animation_finished = True
                    # Auf dem letzten Frame bleiben.
                    self.current_frame_index = num_frames - 1
                    # Callback ausführen, falls vorhanden.
                    if self.current_animation_data.get('on_end'):
                        self.current_animation_data['on_end']()
                    return
                else:
                    self.current_frame_index = 0

            self.rect.texture = animation_frames[self.current_frame_index]