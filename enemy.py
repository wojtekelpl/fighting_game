import random

class Enemy:
    """Klasa reprezentująca przeciwnika"""
    
    def __init__(self, name, max_hp, attack, defense, color, exp_reward, gold_reward):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.color = color
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def is_alive(self):
        """Sprawdź czy przeciwnik żyje"""
        return self.current_hp > 0
    
    def take_damage(self, damage):
        """Otrzymaj obrażenia"""
        self.current_hp -= damage
        if self.current_hp < 0:
            self.current_hp = 0
    
    def attack_player(self, player):
        """Atakuj gracza"""
        base_damage = self.attack + random.randint(-3, 3)
        damage = max(1, base_damage - player.defense)
        actual_damage = player.take_damage(damage)
        return actual_damage
    
    @staticmethod
    def create_random_enemy(player_level):
        """Stwórz losowego przeciwnika dostosowanego do poziomu gracza"""
        
        # Definicje typów przeciwników
        enemy_types = [
            {
                "name": "Szkielet",
                "color": (200, 200, 200),
                "hp_multiplier": 0.8,
                "attack_multiplier": 0.9,
                "defense_multiplier": 0.7,
                "exp_multiplier": 1.0,
                "gold_multiplier": 0.8
            },
            {
                "name": "Goblin",
                "color": (100, 150, 100),
                "hp_multiplier": 1.0,
                "attack_multiplier": 0.8,
                "defense_multiplier": 0.8,
                "exp_multiplier": 1.0,
                "gold_multiplier": 1.0
            },
            {
                "name": "Ork",
                "color": (150, 100, 100),
                "hp_multiplier": 1.2,
                "attack_multiplier": 1.1,
                "defense_multiplier": 0.9,
                "exp_multiplier": 1.2,
                "gold_multiplier": 1.2
            },
            {
                "name": "Troll",
                "color": (100, 100, 150),
                "hp_multiplier": 1.5,
                "attack_multiplier": 1.0,
                "defense_multiplier": 1.2,
                "exp_multiplier": 1.5,
                "gold_multiplier": 1.3
            },
            {
                "name": "Demon",
                "color": (150, 50, 50),
                "hp_multiplier": 1.3,
                "attack_multiplier": 1.3,
                "defense_multiplier": 1.0,
                "exp_multiplier": 1.8,
                "gold_multiplier": 1.5
            },
            {
                "name": "Smok",
                "color": (200, 100, 0),
                "hp_multiplier": 2.0,
                "attack_multiplier": 1.5,
                "defense_multiplier": 1.3,
                "exp_multiplier": 2.5,
                "gold_multiplier": 2.0
            },
            {
                "name": "Nekromanta",
                "color": (80, 50, 80),
                "hp_multiplier": 1.1,
                "attack_multiplier": 1.4,
                "defense_multiplier": 0.8,
                "exp_multiplier": 2.0,
                "gold_multiplier": 1.8
            },
            {
                "name": "Golem",
                "color": (120, 120, 120),
                "hp_multiplier": 1.8,
                "attack_multiplier": 0.9,
                "defense_multiplier": 1.5,
                "exp_multiplier": 1.6,
                "gold_multiplier": 1.4
            },
            {
                "name": "Władca Cieni",
                "color": (50, 50, 50),
                "hp_multiplier": 1.4,
                "attack_multiplier": 1.6,
                "defense_multiplier": 1.1,
                "exp_multiplier": 3.0,
                "gold_multiplier": 2.5
            },
            {
                "name": "Archanioł Upadły",
                "color": (200, 200, 50),
                "hp_multiplier": 2.2,
                "attack_multiplier": 1.7,
                "defense_multiplier": 1.4,
                "exp_multiplier": 4.0,
                "gold_multiplier": 3.0
            }
        ]
        
        # Wybierz typ przeciwnika na podstawie poziomu gracza
        max_enemy_index = min(len(enemy_types) - 1, (player_level - 1) // 2 + 2)
        enemy_type = random.choice(enemy_types[:max_enemy_index + 1])
        
        # Bazowe statystyki skalowane do poziomu gracza
        base_hp = 80 + (player_level * 15)
        base_attack = 15 + (player_level * 3)
        base_defense = 8 + (player_level * 2)
        base_exp = 30 + (player_level * 10)
        base_gold = 10 + (player_level * 5)
        
        # Zastosuj modyfikatory typu przeciwnika
        final_hp = int(base_hp * enemy_type["hp_multiplier"])
        final_attack = int(base_attack * enemy_type["attack_multiplier"])
        final_defense = int(base_defense * enemy_type["defense_multiplier"])
        final_exp = int(base_exp * enemy_type["exp_multiplier"])
        final_gold = int(base_gold * enemy_type["gold_multiplier"])
        
        # Dodaj losową wariację ±20%
        variation = 0.2
        final_hp = int(final_hp * (1 + random.uniform(-variation, variation)))
        final_attack = int(final_attack * (1 + random.uniform(-variation, variation)))
        final_defense = int(final_defense * (1 + random.uniform(-variation, variation)))
        final_exp = int(final_exp * (1 + random.uniform(-variation, variation)))
        final_gold = int(final_gold * (1 + random.uniform(-variation, variation)))
        
        # Upewnij się, że wartości są dodatnie
        final_hp = max(1, final_hp)
        final_attack = max(1, final_attack)
        final_defense = max(0, final_defense)
        final_exp = max(1, final_exp)
        final_gold = max(1, final_gold)
        
        # Czasami stwórz "elitarnego" przeciwnika
        if random.random() < 0.1:  # 10% szansy
            elite_name = f"Elitarny {enemy_type['name']}"
            final_hp = int(final_hp * 1.5)
            final_attack = int(final_attack * 1.3)
            final_defense = int(final_defense * 1.2)
            final_exp = int(final_exp * 2.0)
            final_gold = int(final_gold * 1.8)
            # Zmień kolor na złoty dla elitarnych przeciwników
            elite_color = (255, 215, 0)
            
            return Enemy(elite_name, final_hp, final_attack, final_defense, elite_color, final_exp, final_gold)
        
        return Enemy(
            enemy_type["name"], 
            final_hp, 
            final_attack, 
            final_defense, 
            enemy_type["color"], 
            final_exp, 
            final_gold
        )
    
    @staticmethod
    def create_boss_enemy(player_level):
        """Stwórz bossa dostosowanego do poziomu gracza"""
        boss_types = [
            {
                "name": "Król Szkieletów",
                "color": (150, 150, 150),
                "hp_multiplier": 3.0,
                "attack_multiplier": 2.0,
                "defense_multiplier": 1.5
            },
            {
                "name": "Smocza Królowa",
                "color": (200, 0, 0),
                "hp_multiplier": 4.0,
                "attack_multiplier": 2.5,
                "defense_multiplier": 2.0
            },
            {
                "name": "Władca Otchłani",
                "color": (100, 0, 100),
                "hp_multiplier": 5.0,
                "attack_multiplier": 3.0,
                "defense_multiplier": 2.5
            }
        ]
        
        boss_index = min(len(boss_types) - 1, player_level // 10)
        boss_type = boss_types[boss_index]
        
        # Statystyki bossa są znacznie wyższe niż zwykłych przeciwników
        base_hp = 200 + (player_level * 50)
        base_attack = 30 + (player_level * 8)
        base_defense = 20 + (player_level * 5)
        base_exp = 200 + (player_level * 50)
        base_gold = 100 + (player_level * 25)
        
        final_hp = int(base_hp * boss_type["hp_multiplier"])
        final_attack = int(base_attack * boss_type["attack_multiplier"])
        final_defense = int(base_defense * boss_type["defense_multiplier"])
        final_exp = int(base_exp * 3.0)  # Bossowie dają dużo exp
        final_gold = int(base_gold * 2.5)  # I dużo złota
        
        return Enemy(
            boss_type["name"],
            final_hp,
            final_attack, 
            final_defense,
            boss_type["color"],
            final_exp,
            final_gold
        )