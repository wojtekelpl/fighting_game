import pygame
import random
import json
import os
import sys
from player import Player
from enemy import Enemy


class Game:
    """Główna klasa gry zarządzająca wszystkimi elementami"""

    # Kolory
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)

    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Fonty
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Stan gry
        self.state = "menu"  # menu, fight, shop, stats
        self.player = Player()
        self.current_enemy = None
        self.battle_messages = []
        self.message_timer = 0
        
        # Wczytanie zapisanego stanu gry
        self.load_game()
        
    def handle_event(self, event):
        """Obsługa eventów"""
        if event.type == pygame.KEYDOWN:
            if self.state == "menu":
                self.handle_menu_input(event.key)
            elif self.state == "fight":
                self.handle_fight_input(event.key)
            elif self.state == "shop":
                self.handle_shop_input(event.key)
            elif self.state == "stats":
                self.handle_stats_input(event.key)
            elif self.state == "skins":
                self.handle_skins_input(event.key)
    
    def handle_menu_input(self, key):
        """Obsługa inputu w menu głównym"""
        if key == pygame.K_1:
            self.start_fight()
        elif key == pygame.K_2:
            self.state = "shop"
        elif key == pygame.K_3:
            self.state = "stats"
        elif key == pygame.K_4:
            self.state = "skins"
        elif key == pygame.K_ESCAPE:
            self.save_game()
            pygame.quit()
            sys.exit()
    
    def handle_fight_input(self, key):
        """Obsługa inputu podczas walki"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            if key == pygame.K_SPACE:
                self.state = "menu"
            return
            
        if key == pygame.K_1:
            self.player_attack()
        elif key == pygame.K_2:
            self.player_defend()
        elif key == pygame.K_3:
            self.player_special_attack()
    
    def handle_shop_input(self, key):
        """Obsługa inputu w sklepie"""
        if key == pygame.K_ESCAPE:
            self.state = "menu"
        elif key >= pygame.K_1 and key <= pygame.K_9:
            skin_index = key - pygame.K_1
            self.buy_skin(skin_index)
    
    def handle_stats_input(self, key):
        """Obsługa inputu w statystykach"""
        if key == pygame.K_ESCAPE:
            self.state = "menu"
    
    def handle_skins_input(self, key):
        """Obsługa inputu w menu skinów"""
        if key == pygame.K_ESCAPE:
            self.state = "menu"
        elif key >= pygame.K_1 and key <= pygame.K_9:
            skin_index = key - pygame.K_1
            self.buy_skin(skin_index)
    
    def start_fight(self):
        """Rozpocznij walkę z nowym przeciwnikiem"""
        self.state = "fight"
        self.current_enemy = Enemy.create_random_enemy(self.player.level)
        self.battle_messages = [f"Pojawił się {self.current_enemy.name}!"]
        self.message_timer = 120  # 2 sekundy przy 60 FPS
    
    def player_attack(self):
        """Atak gracza"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
            
        damage = self.player.attack_enemy(self.current_enemy)
        self.battle_messages.append(f"Zadałeś {damage} obrażeń!")
        self._handle_enemy_counter_attack()
        self.message_timer = 180  # 3 sekundy
    
    def player_defend(self):
        """Obrona gracza"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
            
        self.player.defending = True
        self.battle_messages.append("Przyjmujesz pozycję obronną!")
        
        enemy_damage = self.current_enemy.attack_player(self.player)
        self.battle_messages.append(f"{self.current_enemy.name} zadał Ci {enemy_damage} obrażeń!")
        
        self.player.defending = False
        self.message_timer = 180
    
    def player_special_attack(self):
        """Specjalny atak gracza"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
            
        if self.player.special_cooldown > 0:
            self.battle_messages.append("Specjalny atak nie jest jeszcze gotowy!")
            self.message_timer = 120
            return
            
        damage = self.player.special_attack(self.current_enemy)
        self.battle_messages.append(f"Specjalny atak! Zadałeś {damage} obrażeń!")
        self._handle_enemy_counter_attack()
        self.message_timer = 180

    def _handle_enemy_counter_attack(self):
        """Obsługa kontrataku przeciwnika lub nagrody za pokonanie"""
        if self.current_enemy.is_alive():
            enemy_damage = self.current_enemy.attack_player(self.player)
            self.battle_messages.append(f"{self.current_enemy.name} zadał Ci {enemy_damage} obrażeń!")

            if not self.player.is_alive():
                self.battle_messages.append("Zostałeś pokonany!")
                self.player.respawn()
        else:
            exp_gained = self.current_enemy.exp_reward
            gold_gained = self.current_enemy.gold_reward
            self.player.gain_experience(exp_gained)
            self.player.gold += gold_gained
            self.battle_messages.append(f"Pokonałeś {self.current_enemy.name}!")
            self.battle_messages.append(f"Zdobyłeś {exp_gained} doświadczenia i {gold_gained} złota!")

            if self.player.check_level_up():
                self.battle_messages.append(f"Awansowałeś na poziom {self.player.level}!")
    
    def buy_skin(self, skin_index):
        """Kup lub załóż skin"""
        if skin_index < len(self.player.available_skins):
            skin = self.player.available_skins[skin_index]
            if skin["unlocked"]:
                self.player.current_skin = skin_index
                self.player.update_stats()
                self.battle_messages = [f"Założyłeś skin: {skin['name']}"]
            elif self.player.gold >= skin["price"]:
                self.player.gold -= skin["price"]
                skin["unlocked"] = True
                self.player.current_skin = skin_index
                self.player.update_stats()
                self.battle_messages = [f"Kupiłeś i założyłeś skin: {skin['name']}"]
            else:
                self.battle_messages = [f"Nie masz wystarczająco złota na {skin['name']}"]
            
            self.message_timer = 120
    
    def update(self):
        """Aktualizacja stanu gry"""
        if self.message_timer > 0:
            self.message_timer -= 1
            
        if self.player.special_cooldown > 0:
            self.player.special_cooldown -= 1
    
    def draw(self):
        """Rysowanie gry"""
        self.screen.fill(self.WHITE)
        
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "fight":
            self.draw_fight()
        elif self.state == "shop":
            self.draw_shop()
        elif self.state == "stats":
            self.draw_stats()
        elif self.state == "skins":
            self.draw_skins()
    
    def draw_skins(self):
        """Rysowanie menu skinów"""
        title = self.font_large.render("KOLEKCJA SKINÓW", True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)
        
        gold_text = self.font_medium.render(f"Złoto: {self.player.gold}", True, self.YELLOW)
        self.screen.blit(gold_text, (50, 100))
        
        current_skin = self.player.available_skins[self.player.current_skin]
        current_text = self.font_medium.render(f"Aktualny skin: {current_skin['name']}", True, self.BLUE)
        self.screen.blit(current_text, (self.screen_width - 300, 100))
        
        # Rysowanie gracza z aktualnym skinem
        self.draw_player(self.screen_width//2 - 50, 150)
        
        # Lista skinów w siatce 3x3
        cols = 3
        start_x = 100
        start_y = 280
        skin_width = 200
        skin_height = 120
        
        for i, skin in enumerate(self.player.available_skins):
            if i >= 9:  # Maksymalnie 9 skinów na ekranie
                break
                
            col = i % cols
            row = i // cols
            
            x = start_x + col * (skin_width + 20)
            y = start_y + row * (skin_height + 20)
            
            # Tło skina
            bg_color = self.GREEN if skin["unlocked"] else self.GRAY
            if i == self.player.current_skin:
                bg_color = self.BLUE
            
            skin_rect = pygame.Rect(x, y, skin_width, skin_height)
            pygame.draw.rect(self.screen, bg_color, skin_rect)
            pygame.draw.rect(self.screen, self.BLACK, skin_rect, 3)
            
            # Podgląd skina - kolorowy kwadrat
            preview_rect = pygame.Rect(x + 10, y + 10, 40, 40)
            pygame.draw.rect(self.screen, skin["color"], preview_rect)
            pygame.draw.rect(self.screen, self.BLACK, preview_rect, 2)
            
            # Numer i nazwa
            number_text = self.font_medium.render(f"{i+1}", True, self.BLACK)
            self.screen.blit(number_text, (x + 60, y + 15))
            
            name_text = self.font_small.render(skin["name"], True, self.BLACK)
            self.screen.blit(name_text, (x + 10, y + 60))
            
            # Status i cena
            if skin["unlocked"]:
                if i == self.player.current_skin:
                    status_text = "AKTUALNY"
                    status_color = self.WHITE
                else:
                    status_text = "POSIADANY"
                    status_color = self.BLACK
            else:
                status_text = f"{skin['price']} złota"
                status_color = self.RED if self.player.gold < skin["price"] else self.BLACK
            
            status_render = self.font_small.render(status_text, True, status_color)
            self.screen.blit(status_render, (x + 10, y + 80))
            
            # Bonusy
            bonus = f"+{skin['attack_bonus']}ATK +{skin['defense_bonus']}DEF +{skin['hp_bonus']}HP"
            bonus_render = self.font_small.render(bonus, True, self.PURPLE)
            self.screen.blit(bonus_render, (x + 10, y + 100))
        
        # Instrukcje
        instructions = [
            "Naciśnij numer (1-9) aby kupić/założyć skin",
            "ESC - Powrót do menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, self.BLACK)
            self.screen.blit(text, (50, self.screen_height - 60 + i * 25))
        
        # Wiadomości
        if self.message_timer > 0 and self.battle_messages:
            msg_text = self.font_medium.render(self.battle_messages[-1], True, self.GREEN)
            msg_rect = msg_text.get_rect(center=(self.screen_width//2, self.screen_height - 100))
            self.screen.blit(msg_text, msg_rect)

    def draw_menu(self):
        """Rysowanie menu głównego"""
        title = self.font_large.render("GRA WALKI Z SKINAMI", True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen_width//2, 100))
        self.screen.blit(title, title_rect)
        
        # Opcje menu
        options = [
            "1. Walcz z przeciwnikiem",
            "2. Sklep ze skinami", 
            "3. Statystyki gracza",
            "4. Kolekcja skinów",
            "ESC. Zapisz i wyjdź"
        ]
        
        for i, option in enumerate(options):
            text = self.font_medium.render(option, True, self.BLACK)
            text_rect = text.get_rect(center=(self.screen_width//2, 250 + i * 60))
            self.screen.blit(text, text_rect)
        
        # Informacje o graczu
        self.draw_player_info(50, 50)
    
    def draw_fight(self):
        """Rysowanie ekranu walki"""
        # Rysowanie gracza
        self.draw_player(200, 400)
        
        # Rysowanie przeciwnika
        if self.current_enemy:
            self.draw_enemy(600, 400)
        
        # Pasek zdrowia gracza
        self.draw_health_bar(50, 50, self.player.current_hp, self.player.max_hp, "Gracz")
        
        # Pasek zdrowia przeciwnika
        if self.current_enemy:
            self.draw_health_bar(550, 50, self.current_enemy.current_hp, self.current_enemy.max_hp, self.current_enemy.name)
        
        # Opcje walki
        if self.current_enemy and self.current_enemy.is_alive():
            fight_options = [
                "1. Atakuj",
                "2. Broń się",
                f"3. Specjalny atak {'(gotowy)' if self.player.special_cooldown == 0 else f'({self.player.special_cooldown//60 + 1}s)'}"
            ]
            
            for i, option in enumerate(fight_options):
                text = self.font_small.render(option, True, self.BLACK)
                self.screen.blit(text, (50, 500 + i * 30))
        else:
            if self.current_enemy and not self.current_enemy.is_alive():
                text = self.font_medium.render("Naciśnij SPACJĘ aby wrócić do menu", True, self.BLACK)
                self.screen.blit(text, (50, 500))
        
        # Wiadomości z walki
        self.draw_battle_messages()
    
    def draw_shop(self):
        """Rysowanie sklepu"""
        title = self.font_large.render("SKLEP ZE SKINAMI", True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)
        
        gold_text = self.font_medium.render(f"Złoto: {self.player.gold}", True, self.YELLOW)
        self.screen.blit(gold_text, (50, 100))
        
        # Lista skinów
        for i, skin in enumerate(self.player.available_skins):
            y_pos = 150 + i * 60
            
            # Kolor skina
            skin_rect = pygame.Rect(50, y_pos, 40, 40)
            pygame.draw.rect(self.screen, skin["color"], skin_rect)
            pygame.draw.rect(self.screen, self.BLACK, skin_rect, 2)
            
            # Informacje o skinie
            if skin["unlocked"]:
                status = "POSIADANY" if i != self.player.current_skin else "AKTUALNY"
                color = self.GREEN if i != self.player.current_skin else self.BLUE
                text = f"{i+1}. {skin['name']} - {status}"
            else:
                text = f"{i+1}. {skin['name']} - Cena: {skin['price']} złota"
                color = self.BLACK
            
            skin_text = self.font_small.render(text, True, color)
            self.screen.blit(skin_text, (100, y_pos + 5))
            
            # Bonus skina
            bonus_text = f"Bonus: +{skin['attack_bonus']} ATK, +{skin['defense_bonus']} DEF, +{skin['hp_bonus']} HP"
            bonus_render = self.font_small.render(bonus_text, True, self.GRAY)
            self.screen.blit(bonus_render, (100, y_pos + 25))
        
        # Instrukcja
        instruction = self.font_small.render("Naciśnij numer skina aby go kupić/założyć. ESC - powrót", True, self.BLACK)
        self.screen.blit(instruction, (50, self.screen_height - 50))
        
        # Wiadomości
        if self.message_timer > 0 and self.battle_messages:
            msg_text = self.font_medium.render(self.battle_messages[-1], True, self.RED)
            msg_rect = msg_text.get_rect(center=(self.screen_width//2, self.screen_height - 100))
            self.screen.blit(msg_text, msg_rect)
    
    def draw_stats(self):
        """Rysowanie statystyk gracza"""
        title = self.font_large.render("STATYSTYKI GRACZA", True, self.BLACK)
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)
        
        # Rysowanie gracza
        self.draw_player(self.screen_width//2 - 50, 150)
        
        # Statystyki
        stats = [
            f"Poziom: {self.player.level}",
            f"Doświadczenie: {self.player.experience}/{self.player.experience_to_next_level}",
            f"Życie: {self.player.current_hp}/{self.player.max_hp}",
            f"Atak: {self.player.attack}",
            f"Obrona: {self.player.defense}",
            f"Złoto: {self.player.gold}",
            f"Aktualny skin: {self.player.available_skins[self.player.current_skin]['name']}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.font_medium.render(stat, True, self.BLACK)
            self.screen.blit(text, (50, 250 + i * 40))
        
        # Instrukcja
        instruction = self.font_small.render("Naciśnij ESC aby wrócić do menu", True, self.BLACK)
        self.screen.blit(instruction, (50, self.screen_height - 50))
    
    def draw_player_info(self, x, y):
        """Rysowanie podstawowych informacji o graczu"""
        info = [
            f"Poziom: {self.player.level}",
            f"HP: {self.player.current_hp}/{self.player.max_hp}",
            f"Złoto: {self.player.gold}"
        ]
        
        for i, line in enumerate(info):
            text = self.font_small.render(line, True, self.BLACK)
            self.screen.blit(text, (x, y + i * 25))
    
    def draw_player(self, x, y):
        """Rysowanie gracza"""
        current_skin = self.player.available_skins[self.player.current_skin]
        
        # Ciało
        pygame.draw.circle(self.screen, current_skin["color"], (x + 50, y + 30), 25)
        pygame.draw.rect(self.screen, current_skin["color"], (x + 35, y + 50, 30, 60))
        
        # Ręce
        pygame.draw.circle(self.screen, current_skin["color"], (x + 20, y + 70), 10)
        pygame.draw.circle(self.screen, current_skin["color"], (x + 80, y + 70), 10)
        
        # Nogi
        pygame.draw.circle(self.screen, current_skin["color"], (x + 35, y + 120), 12)
        pygame.draw.circle(self.screen, current_skin["color"], (x + 65, y + 120), 12)
        
        # Oczy
        pygame.draw.circle(self.screen, self.BLACK, (x + 45, y + 25), 3)
        pygame.draw.circle(self.screen, self.BLACK, (x + 55, y + 25), 3)
        
        # Obramowanie
        pygame.draw.circle(self.screen, self.BLACK, (x + 50, y + 30), 25, 2)
    
    def draw_enemy(self, x, y):
        """Rysowanie przeciwnika"""
        if not self.current_enemy:
            return
            
        enemy_color = self.current_enemy.color
        
        # Ciało przeciwnika - podobne do gracza ale w innym kolorze
        pygame.draw.circle(self.screen, enemy_color, (x + 50, y + 30), 25)
        pygame.draw.rect(self.screen, enemy_color, (x + 35, y + 50, 30, 60))
        
        # Ręce
        pygame.draw.circle(self.screen, enemy_color, (x + 20, y + 70), 10)
        pygame.draw.circle(self.screen, enemy_color, (x + 80, y + 70), 10)
        
        # Nogi
        pygame.draw.circle(self.screen, enemy_color, (x + 35, y + 120), 12)
        pygame.draw.circle(self.screen, enemy_color, (x + 65, y + 120), 12)
        
        # Czerwone oczy (wrogie)
        pygame.draw.circle(self.screen, self.RED, (x + 45, y + 25), 3)
        pygame.draw.circle(self.screen, self.RED, (x + 55, y + 25), 3)
        
        # Obramowanie
        pygame.draw.circle(self.screen, self.BLACK, (x + 50, y + 30), 25, 2)
    
    def draw_health_bar(self, x, y, current_hp, max_hp, label):
        """Rysowanie paska zdrowia"""
        bar_width = 200
        bar_height = 20
        
        # Tło paska
        pygame.draw.rect(self.screen, self.GRAY, (x, y + 20, bar_width, bar_height))
        
        # Pasek zdrowia
        if max_hp > 0:
            health_width = int((current_hp / max_hp) * bar_width)
            health_color = self.GREEN if current_hp > max_hp * 0.5 else self.YELLOW if current_hp > max_hp * 0.25 else self.RED
            pygame.draw.rect(self.screen, health_color, (x, y + 20, health_width, bar_height))
        
        # Obramowanie
        pygame.draw.rect(self.screen, self.BLACK, (x, y + 20, bar_width, bar_height), 2)
        
        # Etykieta
        label_text = self.font_small.render(label, True, self.BLACK)
        self.screen.blit(label_text, (x, y))
        
        # Wartości HP
        hp_text = self.font_small.render(f"{current_hp}/{max_hp}", True, self.BLACK)
        self.screen.blit(hp_text, (x + bar_width + 10, y + 20))
    
    def draw_battle_messages(self):
        """Rysowanie wiadomości z walki"""
        if self.message_timer > 0 and self.battle_messages:
            # Pokaż ostatnie 3 wiadomości
            messages_to_show = self.battle_messages[-3:]
            
            for i, message in enumerate(messages_to_show):
                text = self.font_small.render(message, True, self.BLACK)
                text_rect = text.get_rect(center=(self.screen_width//2, 600 + i * 25))
                self.screen.blit(text, text_rect)
    
    def save_game(self):
        """Zapisanie stanu gry"""
        save_data = {
            "player_level": self.player.level,
            "player_experience": self.player.experience,
            "player_gold": self.player.gold,
            "player_current_skin": self.player.current_skin,
            "unlocked_skins": [skin["unlocked"] for skin in self.player.available_skins]
        }
        
        try:
            with open("save_game.json", "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=4, ensure_ascii=False)
            print("Gra została zapisana!")
        except Exception as e:
            print(f"Błąd podczas zapisywania: {e}")
    
    def load_game(self):
        """Wczytanie stanu gry"""
        if os.path.exists("save_game.json"):
            try:
                with open("save_game.json", "r", encoding="utf-8") as f:
                    save_data = json.load(f)
                
                self.player.level = save_data.get("player_level", 1)
                self.player.experience = save_data.get("player_experience", 0)
                self.player.gold = save_data.get("player_gold", 0)
                self.player.current_skin = save_data.get("player_current_skin", 0)
                
                unlocked_skins = save_data.get("unlocked_skins", [])
                for i, unlocked in enumerate(unlocked_skins):
                    if i < len(self.player.available_skins):
                        self.player.available_skins[i]["unlocked"] = unlocked
                
                # Aktualizacja statystyk na podstawie poziomu
                self.player.update_stats_for_level()
                
                print("Gra została wczytana!")
            except Exception as e:
                print(f"Błąd podczas wczytywania: {e}")               