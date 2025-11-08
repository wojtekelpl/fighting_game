import random

class Player:
    """Klasa reprezentująca gracza"""
    
    def __init__(self):
        # Podstawowe statystyki
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        self.gold = 50
        
        # Statystyki bojowe
        self.base_max_hp = 100
        self.base_attack = 20
        self.base_defense = 10
        
        self.max_hp = self.base_max_hp
        self.current_hp = self.max_hp
        self.attack = self.base_attack
        self.defense = self.base_defense
        
        # System skinów
        self.current_skin = 0
        self.available_skins = [
            {
                "name": "Podstawowy",
                "color": (100, 150, 200),
                "price": 0,
                "unlocked": True,
                "attack_bonus": 0,
                "defense_bonus": 0,
                "hp_bonus": 0
            },
            {
                "name": "Czerwony Wojownik",
                "color": (200, 50, 50),
                "price": 100,
                "unlocked": False,
                "attack_bonus": 5,
                "defense_bonus": 0,
                "hp_bonus": 0
            },
            {
                "name": "Zielony Obrońca",
                "color": (50, 200, 50),
                "price": 150,
                "unlocked": False,
                "attack_bonus": 0,
                "defense_bonus": 8,
                "hp_bonus": 20
            },
            {
                "name": "Niebieski Mag",
                "color": (50, 50, 200),
                "price": 200,
                "unlocked": False,
                "attack_bonus": 8,
                "defense_bonus": 3,
                "hp_bonus": 10
            },
            {
                "name": "Złoty Mistrz",
                "color": (255, 215, 0),
                "price": 500,
                "unlocked": False,
                "attack_bonus": 10,
                "defense_bonus": 10,
                "hp_bonus": 50
            },
            {
                "name": "Fioletowy Zabójca",
                "color": (128, 0, 128),
                "price": 300,
                "unlocked": False,
                "attack_bonus": 15,
                "defense_bonus": 2,
                "hp_bonus": 5
            },
            {
                "name": "Srebrny Rycerz",
                "color": (192, 192, 192),
                "price": 400,
                "unlocked": False,
                "attack_bonus": 7,
                "defense_bonus": 12,
                "hp_bonus": 30
            },
            {
                "name": "Czarny Ninja",
                "color": (50, 50, 50),
                "price": 600,
                "unlocked": False,
                "attack_bonus": 20,
                "defense_bonus": 5,
                "hp_bonus": 15
            },
            {
                "name": "Tęczowy Legenda",
                "color": (255, 100, 255),
                "price": 1000,
                "unlocked": False,
                "attack_bonus": 25,
                "defense_bonus": 15,
                "hp_bonus": 100
            }
        ]
        
        # Stan walki
        self.defending = False
        self.special_cooldown = 0
        
        # Aktualizacja statystyk na podstawie skina
        self.update_stats()
    
    def update_stats(self):
        """Aktualizacja statystyk na podstawie poziomu i skina"""
        # Statystyki bazowe + bonus za poziom
        level_bonus = (self.level - 1) * 5
        
        # Bonus ze skina
        current_skin_data = self.available_skins[self.current_skin]
        skin_attack_bonus = current_skin_data["attack_bonus"]
        skin_defense_bonus = current_skin_data["defense_bonus"]
        skin_hp_bonus = current_skin_data["hp_bonus"]
        
        # Obliczenie końcowych statystyk
        self.attack = self.base_attack + level_bonus + skin_attack_bonus
        self.defense = self.base_defense + (level_bonus // 2) + skin_defense_bonus
        
        old_max_hp = self.max_hp
        self.max_hp = self.base_max_hp + (level_bonus * 2) + skin_hp_bonus
        
        # Jeśli max HP się zwiększyło, dodaj różnicę do current HP
        if self.max_hp > old_max_hp:
            self.current_hp += (self.max_hp - old_max_hp)
        
        # Upewnij się, że current HP nie przekracza max HP
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
    
    def update_stats_for_level(self):
        """Aktualizacja statystyk na podstawie aktualnego poziomu (używane przy wczytywaniu gry)"""
        self.experience_to_next_level = 100 * self.level
        self.update_stats()
    
    def is_alive(self):
        """Sprawdź czy gracz żyje"""
        return self.current_hp > 0
    
    def attack_enemy(self, enemy):
        """Atakuj przeciwnika"""
        base_damage = self.attack + random.randint(-5, 5)
        damage = max(1, base_damage - enemy.defense)
        enemy.take_damage(damage)
        return damage
    
    def special_attack(self, enemy):
        """Specjalny atak (podwójne obrażenia, cooldown 5 sekund)"""
        base_damage = (self.attack * 2) + random.randint(-10, 10)
        damage = max(1, base_damage - enemy.defense)
        enemy.take_damage(damage)
        self.special_cooldown = 300  # 5 sekund przy 60 FPS
        return damage
    
    def take_damage(self, damage):
        """Otrzymaj obrażenia"""
        if self.defending:
            damage = max(1, damage // 2)  # Obrona zmniejsza obrażenia o połowę
        
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
        
        return damage
    
    def heal(self, amount):
        """Ulecz się"""
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
    
    def gain_experience(self, exp):
        """Zdobądź doświadczenie"""
        self.experience += exp
    
    def check_level_up(self):
        """Sprawdź czy gracz może awansować na wyższy poziom"""
        if self.experience >= self.experience_to_next_level:
            self.level += 1
            self.experience -= self.experience_to_next_level
            self.experience_to_next_level = 100 * self.level
            
            # Ulecz gracza przy awansie
            self.heal(self.max_hp // 2)
            
            # Aktualizuj statystyki
            self.update_stats()
            
            return True
        return False
    
    def respawn(self):
        """Odrodzenie po śmierci"""
        self.current_hp = self.max_hp // 2  # Odrodzenie z połową HP
        
        # Utrata trochę doświadczenia
        exp_loss = self.experience // 4
        self.experience = max(0, self.experience - exp_loss)
        
        # Utrata trochę złota
        gold_loss = self.gold // 10
        self.gold = max(0, self.gold - gold_loss)
    
    def get_skin_info(self):
        """Zwróć informacje o aktualnym skinie"""
        return self.available_skins[self.current_skin]