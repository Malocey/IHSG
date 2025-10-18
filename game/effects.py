import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.animation import Animation
import random

class Particle(Widget):
    """
    Ein einzelnes Partikel mit einer Lebensdauer und Geschwindigkeit.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.velocity_x = random.uniform(-150, 150)
        self.velocity_y = random.uniform(-100, 200)
        self.lifespan = random.uniform(0.5, 1.2)

        # Zufällige Farbe zwischen Gelb und Orange
        r = 1.0
        g = random.uniform(0.5, 1.0)
        b = 0.0

        with self.canvas:
            self.color = Color(r, g, b, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def update(self, dt):
        """
        Aktualisiert die Position und Lebensdauer des Partikels.
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.velocity_y -= 200 * dt # Schwerkraft-Effekt
        self.lifespan -= dt

        self.color.a = max(0, self.lifespan * 2) # Verblassen

        if self.lifespan <= 0:
            Clock.unschedule(self.update)
            if self.parent:
                self.parent.remove_widget(self)

class TrailParticle(Widget):
    """
    Ein Partikel, das für den Schweif-Effekt von Projektilen verwendet wird.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (12, 12)
        with self.canvas:
            self.color = Color(1, 1, 0.5, 0.6) # Blassgelb
            self.rect = Rectangle(size=self.size, pos=self.pos)

        # Animation zum Verblassen
        anim = Animation(opacity=0, duration=0.3)
        anim.bind(on_complete=lambda *args: self.parent.remove_widget(self) if self.parent else None)
        anim.start(self)

class ParticleSystem:
    """
    Ein System zur Verwaltung von Partikeleffekten.
    """
    @staticmethod
    def create_explosion(parent, pos, num_particles=40):
        """
        Erzeugt eine Partikel-Explosion an einer bestimmten Position.
        """
        for _ in range(num_particles):
            size = random.uniform(2, 5)
            particle = Particle(center=pos, size=(size, size))
            parent.add_widget(particle)