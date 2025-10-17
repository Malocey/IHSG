import kivy
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.animation import Animation

class HealthBar(Widget):
    """
    Eine einfache Lebensanzeige für Spiel-Entitäten.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        with self.canvas:
            # Hintergrund der Lebensanzeige (z.B. in Rot)
            Color(1, 0, 0, 0.8)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            # Vordergrund, der die aktuellen Lebenspunkte darstellt (z.B. in Grün)
            Color(0, 1, 0, 0.8)
            self.fg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.fg_rect.pos = self.pos
        # The width of the fg_rect is updated separately based on health percentage.

    def set_health_percent(self, percent):
        """
        Aktualisiert die Breite der Lebensanzeige basierend auf einem Prozentsatz (0.0 bis 1.0).
        """
        self.fg_rect.size = (self.width * max(0, percent), self.height)

class DamageNumber(Label):
    """
    Eine Zahl, die auf dem Bildschirm erscheint und verblasst, um Schaden anzuzeigen.
    """
    def __init__(self, damage, **kwargs):
        super().__init__(text=str(damage), **kwargs)
        self.font_size = '20sp'
        self.bold = True
        self.color = (1, 1, 0, 1)  # Gelbe Farbe für Schaden

        # Animation: Nach oben bewegen und verblassen
        anim = Animation(y=self.y + 50, opacity=0, duration=0.8)
        anim.bind(on_complete=self.on_animation_complete)
        anim.start(self)

    def on_animation_complete(self, *args):
        """
        Entfernt das Widget, nachdem die Animation abgeschlossen ist.
        """
        if self.parent:
            self.parent.remove_widget(self)

# Farben für verschiedene Kristall-Stufen
CRYSTAL_COLORS = [
    (0.2, 0.8, 1, 0.9),  # Stufe 0 (Cyan)
    (0.5, 1, 0.5, 0.9),  # Stufe 1 (Hellgrün)
    (1, 1, 0.5, 0.9),  # Stufe 2 (Gelb)
    (1, 0.5, 0.5, 0.9),  # Stufe 3 (Rot)
    (1, 0.5, 1, 0.9),  # Stufe 4 (Magenta)
]

class XPCrystal(Widget):
    """
    Ein XP-Kristall, der von Gegnern fallen gelassen und vom Helden eingesammelt wird.
    """
    def __init__(self, tier=0, **kwargs):
        super().__init__(**kwargs)
        self.tier = tier
        self.xp_value = 5 ** tier
        self.size = (15 + tier * 3, 15 + tier * 3) # Größer mit jeder Stufe
        self.velocity = (0, 0)
        with self.canvas:
            color = CRYSTAL_COLORS[self.tier % len(CRYSTAL_COLORS)]
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos