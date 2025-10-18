import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.scatterlayout import ScatterLayout
from game.map import MapGenerator, MapWidget

class MapTestApp(App):
    def build(self):
        # Erstelle einen Generator und eine Karte
        map_generator = MapGenerator(width=50, height=50)
        map_grid = map_generator.generate_map()

        # Erstelle das Widget, um die Karte anzuzeigen
        # Wir geben eine feste Größe, damit das ScatterLayout richtig funktioniert
        map_widget = MapWidget(map_grid, tile_size=32, size=(50*32, 50*32))

        # Füge das MapWidget zu einem ScatterLayout hinzu, um Zoom/Pan zu ermöglichen
        root = ScatterLayout(do_rotation=False)
        root.add_widget(map_widget)

        return root

if __name__ == '__main__':
    MapTestApp().run()