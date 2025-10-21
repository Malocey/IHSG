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
        self.velocity_x = random.uniform(-50, 50)
        self.velocity_y = random.uniform(50, 150)
        self.lifespan = random.uniform(0.3, 0.8)

        with self.canvas:
            self.color = Color(1, 1, 0, 1) # Gelbe Partikel
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

class ParticleSystem(Widget):
    """
    Ein System zur Verwaltung von Partikeleffekten, das jetzt ein Widget ist.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.particles = []

    def create_explosion(self, pos, num_particles=20):
        """
        Erzeugt eine Partikel-Explosion an einer bestimmten Position.
        """
        for _ in range(num_particles):
            particle = Particle(center=pos, size=(3, 3))
            self.particles.append(particle)
            self.add_widget(particle)

    def update(self, dt):
        # The particles update themselves, but we could add system-wide logic here if needed.
        # For now, this method is a placeholder to be called from the main game loop.
        pass