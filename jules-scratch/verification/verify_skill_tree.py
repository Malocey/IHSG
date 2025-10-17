import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"
os.environ["KIVY_NO_FILELOG"] = "1"
os.environ['KIVY_WINDOW'] = 'egl_rpi'

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from game.screens import GameScreen, SkillTreeScreen, CardSelectionScreen
from game.player_data import PlayerData
from kivy.core.window import Window
from kivy.clock import Clock
from main import IdleHordeSlayerApp
import time

class TestApp(IdleHordeSlayerApp):
    def on_start(self):
        self.screen_manager.current = 'skill_tree'
        Clock.schedule_once(self.take_screenshot, 10)

    def take_screenshot(self, dt):
        Window.screenshot(name='jules-scratch/verification/verification.png')
        self.stop()

if __name__ == '__main__':
    TestApp().run()