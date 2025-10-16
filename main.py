# main.py (Komplett neu aufgebauter, sauberer Zustand)

import random
import os
from functools import partial
import math

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.floatlayout import FloatLayout

from src.entities import Hero, Enemy, Projectile, VFX, XPCrystal, CRYSTAL_TYPES
from src.skills import SKILL_TREE
from src.cards import UPGRADE_CARDS

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_enemy_killed')
        self.app = App.get_running_app()
        self.hero = Hero()
        self.add_widget(self.hero)
        self.enemies = []
        self.projectiles = []
        self.xp_crystals = []
        self.attack_cooldown = 0
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.spawn_enemy, 2.0)

    def on_enemy_killed(self, enemy_instance):
        pass

    def spawn_enemy(self, dt):
        enemy = Enemy()
        enemy.x = random.randint(0, self.width - enemy.width)
        enemy.y = random.randint(self.height // 2, self.height - enemy.height)
        self.enemies.append(enemy)
        self.add_widget(enemy)

    def attack(self):
        for ability in self.hero.active_abilities:
            if ability == "default_attack":
                self.default_attack()
            elif ability == "whirlwind":
                self.whirlwind_attack()

    def default_attack(self):
        projectile = Projectile()
        projectile.pos = (self.hero.center_x - projectile.width / 2, self.hero.top)
        self.projectiles.append(projectile)
        self.add_widget(projectile)

    def whirlwind_attack(self):
        num_projectiles = 8
        for i in range(num_projectiles):
            angle = (360 / num_projectiles) * i
            projectile = Projectile(angle=angle)
            projectile.center = self.hero.center
            self.projectiles.append(projectile)
            self.add_widget(projectile)

    def update(self, dt):
        base_speed = self.app.character_stats.get('hero_speed', 100)
        speed_multiplier = 1 + (self.app.character_stats.get('hero_speed_percent', 0) / 100.0)
        hero_speed = base_speed * speed_multiplier
        self.hero.x += hero_speed * dt
        if self.hero.right > self.width: self.hero.x = 0

        self.attack_cooldown -= dt
        if self.attack_cooldown <= 0:
            self.attack()
            attack_speed_stat = 1 + (self.app.character_stats.get('attack_speed_percent', 0) / 100.0)
            self.attack_cooldown = 1.0 / max(0.1, attack_speed_stat)

        for p in self.projectiles[:]:
            p.move(dt)
            if p.top < 0 or p.bottom > self.height or p.left < 0 or p.right > self.width:
                self.projectiles.remove(p)
                self.remove_widget(p)
                continue
            for enemy in self.enemies[:]:
                if p.collide_widget(enemy):
                    enemy.on_hit()
                    if p in self.projectiles:
                        self.projectiles.remove(p)
                        self.remove_widget(p)
                    Clock.schedule_once(partial(self.kill_enemy, enemy), 0.1)
                    break

        for crystal in self.xp_crystals[:]:
            if self.hero.collide_point(*crystal.center):
                 crystal.move_towards(self.hero.center, dt)
            if self.hero.collide_widget(crystal):
                self.app.add_xp(crystal.value)
                self.xp_crystals.remove(crystal)
                self.remove_widget(crystal)

    def kill_enemy(self, enemy, dt):
        if enemy in self.enemies:
            self.dispatch('on_enemy_killed', enemy)

    def spawn_crystal(self, crystal_type, pos):
        new_crystal = XPCrystal(crystal_type=crystal_type, center=pos)
        type_data = new_crystal.type_data
        if type_data["merges_to"]:
            nearby_crystals = [c for c in self.xp_crystals if c.crystal_type == new_crystal.crystal_type and c.collide_point(*new_crystal.center, 50)]
            if len(nearby_crystals) >= type_data["merge_count"] - 1:
                crystals_to_remove = nearby_crystals[:type_data["merge_count"] - 1]
                for c in crystals_to_remove:
                    self.xp_crystals.remove(c)
                    self.remove_widget(c)
                self.spawn_crystal(type_data["merges_to"], pos)
                return
        self.xp_crystals.append(new_crystal)
        self.add_widget(new_crystal)

class GameScreen(Screen): pass
class HeroScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        scatter = ScatterLayout(do_rotation=False, scale_min=0.5, scale_max=3.0)
        skill_tree_layout = FloatLayout(size=(2000, 1000))
        self.skill_nodes = {skill['id']: skill for skill in SKILL_TREE}
        self.skill_buttons = {}
        with skill_tree_layout.canvas.before:
            Color(0.5, 0.5, 0.5, 1)
            for skill in self.skill_nodes.values():
                for dep_id in skill['dependencies']:
                    if dep_id in self.skill_nodes:
                        start_pos = self.skill_nodes[dep_id]['position']
                        end_pos = skill['position']
                        Line(points=[start_pos[0] + 75, start_pos[1] + 25, end_pos[0] + 75, end_pos[1] + 25], width=1.5)
        for skill_id, skill in self.skill_nodes.items():
            button = Button(size_hint=(None, None), size=(150, 60), pos=skill['position'], halign='center')
            button.skill_id = skill_id
            button.bind(on_press=self.app.upgrade_skill)
            self.skill_buttons[skill_id] = button
            skill_tree_layout.add_widget(button)
        scatter.add_widget(skill_tree_layout)
        self.add_widget(scatter)
        self.update_button_states()
    def update_button_states(self):
        for skill_id, button in self.skill_buttons.items():
            skill = self.skill_nodes[skill_id]
            current_level = self.app.skill_levels.get(skill_id, 0)
            if current_level > 0: button.text = f"{skill['name']}\n(Lv: {current_level}/{skill['max_level']})"
            else: button.text = f"{skill['name']}\n(Unlock)"
            is_max_level = current_level >= skill['max_level']
            if is_max_level:
                button.background_color = (0.2, 0.8, 1, 1); continue
            cost = skill['base_cost'] + current_level
            dependencies_met = all(dep in self.app.skill_levels for dep in skill['dependencies'])
            can_afford = self.app.skill_points >= cost
            if current_level > 0: button.background_color = (0, 1, 0, 1) if can_afford else (0.5, 0.5, 0.5, 1)
            elif dependencies_met and can_afford: button.background_color = (1, 1, 0, 1)
            else: button.background_color = (1, 0, 0, 1)

class CardSelectionScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=50)
        self.add_widget(self.layout)
    def show_card_options(self):
        self.layout.clear_widgets()
        self.layout.add_widget(Label(text="Level Up! Choose an Upgrade:", font_size='24sp'))
        options = random.sample(UPGRADE_CARDS, 3)
        for card_data in options:
            btn = Button(text=f"{card_data['name']}\n({card_data['description']})", size_hint_y=None, height=100)
            btn.card_data = card_data
            btn.bind(on_press=self.select_card)
            self.layout.add_widget(btn)
    def select_card(self, instance):
        self.app.apply_card_upgrade(instance.card_data)
        self.app.change_screen('game')

class IdleHordeSlayerApp(App):
    def build(self):
        self.skill_levels = {"base_attack": 1}
        self.gold = 0; self.score = 0; self.skill_points = 10
        self.character_stats = {}; self.run_level = 1; self.run_xp = 0; self.xp_to_next_level = 5; self.run_stats = {}
        root_layout = BoxLayout(orientation='vertical')
        top_bar = BoxLayout(size_hint_y=None, height=100, padding=10, spacing=20)
        with top_bar.canvas.before: Color(0.1, 0.1, 0.1, 1); top_bar.rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_background)
        self.gold_label = Label(text=f"Gold: {self.gold}"); self.score_label = Label(text=f"Kills: {self.score}"); self.skill_point_label = Label(text=f"Skill Points: {self.skill_points}"); self.run_level_label = Label(text=f"Level: {self.run_level} (XP: {self.run_xp}/{self.xp_to_next_level})")
        top_bar.add_widget(self.gold_label); top_bar.add_widget(self.score_label); top_bar.add_widget(self.skill_point_label); top_bar.add_widget(self.run_level_label)
        self.screen_manager = ScreenManager()
        game_screen = GameScreen(name='game'); game_widget = GameWidget(); game_widget.bind(on_enemy_killed=self.on_enemy_killed)
        game_screen.add_widget(game_widget); self.screen_manager.add_widget(game_screen)
        hero_screen = HeroScreen(name='hero', app=self); self.screen_manager.add_widget(hero_screen)
        card_screen = CardSelectionScreen(name='card_selection', app=self); self.screen_manager.add_widget(card_screen)
        bottom_bar = BoxLayout(size_hint_y=None, height=150, spacing=10, padding=10)
        with bottom_bar.canvas.before: Color(0.1, 0.1, 0.1, 1); bottom_bar.rect = Rectangle(size=bottom_bar.size, pos=bottom_bar.pos)
        bottom_bar.bind(size=self._update_background)
        button_map = {"Game": "game", "Hero": "hero", "Upgrades": "upgrades", "Shop": "shop"}
        for button_text, screen_name in button_map.items():
            if not self.screen_manager.has_screen(screen_name):
                screen = Screen(name=screen_name); screen.add_widget(Label(text=f"{button_text} Screen\n(Coming Soon)")); self.screen_manager.add_widget(screen)
            button = Button(text=button_text); button.bind(on_press=partial(self.change_screen, screen_name)); bottom_bar.add_widget(button)
        root_layout.add_widget(top_bar); root_layout.add_widget(self.screen_manager); root_layout.add_widget(bottom_bar)
        self.calculate_total_stats(); return root_layout
    def on_enemy_killed(self, instance, enemy):
        self.score += 1; self.gold += 1
        if self.score > 0 and self.score % 10 == 0: self.skill_points += 1
        self.score_label.text = f"Kills: {self.score}"; self.gold_label.text = f"Gold: {self.gold}"; self.skill_point_label.text = f"Skill Points: {self.skill_points}"
        instance.spawn_crystal("blue", enemy.center)
        if enemy in instance.enemies: instance.enemies.remove(enemy); instance.remove_widget(enemy)
    def add_xp(self, amount):
        self.run_xp += amount
        if self.run_xp >= self.xp_to_next_level:
            self.run_level += 1; self.run_xp -= self.xp_to_next_level; self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
            self.screen_manager.get_screen('card_selection').show_card_options(); self.change_screen('card_selection')
        self.run_level_label.text = f"Level: {self.run_level} (XP: {self.run_xp}/{self.xp_to_next_level})"
    def apply_card_upgrade(self, card_data):
        card_type = card_data['type']
        if card_type == 'stat_boost':
            stat = card_data['bonus']['stat']; base_value = card_data['bonus']['value']
            related_skill_id = stat.replace('_percent', '') + '_1'
            skill_level = self.skill_levels.get(related_skill_id, 0)
            multiplier = 1 + (skill_level * 0.1); final_value = base_value * multiplier
            self.run_stats[stat] = self.run_stats.get(stat, 0) + final_value
        elif card_type == 'new_ability':
            ability_id = card_data['bonus']['ability_id']
            game_widget = self.screen_manager.get_screen('game').children[0]
            if ability_id not in game_widget.hero.active_abilities: game_widget.hero.active_abilities.append(ability_id)
        self.calculate_total_stats()
    def change_screen(self, screen_name, *args):
        self.screen_manager.current = screen_name
        if screen_name == 'hero': self.screen_manager.get_screen('hero').update_button_states()
    def upgrade_skill(self, button):
        skill_id = button.skill_id; skill_data = self.screen_manager.get_screen('hero').skill_nodes[skill_id]
        current_level = self.skill_levels.get(skill_id, 0)
        if current_level >= skill_data['max_level']: return
        cost = skill_data['base_cost'] + current_level
        if self.skill_points < cost: return
        if current_level == 0:
            dependencies_met = all(dep in self.skill_levels for dep in skill_data['dependencies'])
            if not dependencies_met: return
        self.skill_points -= cost; self.skill_levels[skill_id] = current_level + 1
        self.skill_point_label.text = f"Skill Points: {self.skill_points}"
        self.screen_manager.get_screen('hero').update_button_states(); self.calculate_total_stats()
    def calculate_total_stats(self):
        self.character_stats = {'attack_damage': 0, 'attack_speed_percent': 0, 'crit_chance_percent': 0, 'hero_speed': 100, 'max_health': 100}
        if hasattr(self, 'screen_manager') and self.screen_manager.has_screen('hero'):
            skill_definitions = self.screen_manager.get_screen('hero').skill_nodes
            for skill_id, level in self.skill_levels.items():
                skill_data = skill_definitions.get(skill_id)
                if not skill_data: continue
                for stat_bonus in skill_data['stats']:
                    stat_type = stat_bonus['type']; value_per_level = stat_bonus['value']
                    self.character_stats[stat_type] = self.character_stats.get(stat_type, 0) + (value_per_level * level)
        for stat, value in self.run_stats.items():
            self.character_stats[stat] = self.character_stats.get(stat, 0) + value
        print("Charakter-Stats aktualisiert:", self.character_stats)
    def _update_background(self, instance, value):
        instance.rect.pos = instance.pos; instance.rect.size = instance.size
if __name__ == '__main__':
    IdleHordeSlayerApp().run()