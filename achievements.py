"""
System osiągnięć dla gry walki
"""

class Achievement:
    """Klasa reprezentująca pojedyncze osiągnięcie"""
    
    def __init__(self, name, description, condition, reward_gold=0, reward_exp=0):
        self.name = name
        self.description = description
        self.condition = condition
        self.reward_gold = reward_gold
        self.reward_exp = reward_exp
        self.unlocked = False
    
    def check_condition(self, player, game_stats):
        """Sprawdź czy warunki osiągnięcia zostały spełnione"""
        return self.condition(player, game_stats)

class AchievementManager:
    """Zarządca osiągnięć"""
    
    def __init__(self):
        self.achievements = []
        self.setup_achievements()
    
    def setup_achievements(self):
        """Konfiguracja listy osiągnięć"""
        
        # Osiągnięcia związane z poziomem
        self.achievements.append(Achievement(
            "Pierwsze Kroki",
            "Osiągnij poziom 5",
            lambda player, stats: player.level >= 5,
            reward_gold=100,
            reward_exp=50
        ))
        
        self.achievements.append(Achievement(
            "Doświadczony Wojownik", 
            "Osiągnij poziom 10",
            lambda player, stats: player.level >= 10,
            reward_gold=250,
            reward_exp=100
        ))
        
        self.achievements.append(Achievement(
            "Mistrz Walki",
            "Osiągnij poziom 20",
            lambda player, stats: player.level >= 20,
            reward_gold=500,
            reward_exp=200
        ))
        
        # Osiągnięcia związane z walkami
        self.achievements.append(Achievement(
            "Pierwsza Krew",
            "Wygraj pierwszą walkę",
            lambda player, stats: stats.get('enemies_defeated', 0) >= 1,
            reward_gold=50,
            reward_exp=25
        ))
        
        self.achievements.append(Achievement(
            "Zabójca Potworów",
            "Pokonaj 50 przeciwników",
            lambda player, stats: stats.get('enemies_defeated', 0) >= 50,
            reward_gold=300,
            reward_exp=150
        ))
        
        self.achievements.append(Achievement(
            "Legenda Areny",
            "Pokonaj 100 przeciwników",
            lambda player, stats: stats.get('enemies_defeated', 0) >= 100,
            reward_gold=600,
            reward_exp=300
        ))
        
        # Osiągnięcia związane ze skinami
        self.achievements.append(Achievement(
            "Kolekcjoner",
            "Posiadaj 3 różne skiny",
            lambda player, stats: len([s for s in player.available_skins if s['unlocked']]) >= 3,
            reward_gold=150,
            reward_exp=75
        ))
        
        self.achievements.append(Achievement(
            "Mistrz Mody",
            "Posiadaj wszystkie skiny",
            lambda player, stats: all(s['unlocked'] for s in player.available_skins),
            reward_gold=1000,
            reward_exp=500
        ))
        
        # Osiągnięcia związane ze złotem
        self.achievements.append(Achievement(
            "Bogacz",
            "Posiadaj 1000 złota naraz",
            lambda player, stats: player.gold >= 1000,
            reward_gold=200,
            reward_exp=100
        ))
        
        # Osiągnięcia związane z walką
        self.achievements.append(Achievement(
            "Nietykalny",
            "Wygraj walkę bez otrzymania obrażeń",
            lambda player, stats: stats.get('flawless_victories', 0) >= 1,
            reward_gold=200,
            reward_exp=100
        ))
        
        self.achievements.append(Achievement(
            "Mistrz Specjalistów",
            "Użyj 20 specjalnych ataków",
            lambda player, stats: stats.get('special_attacks_used', 0) >= 20,
            reward_gold=150,
            reward_exp=75
        ))
    
    def check_achievements(self, player, game_stats):
        """Sprawdź wszystkie osiągnięcia i zwróć listę nowych"""
        newly_unlocked = []
        
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.check_condition(player, game_stats):
                achievement.unlocked = True
                newly_unlocked.append(achievement)
                
                # Przyznaj nagrody
                player.gold += achievement.reward_gold
                player.experience += achievement.reward_exp
        
        return newly_unlocked
    
    def get_progress_info(self):
        """Zwróć informacje o postępie osiągnięć"""
        total = len(self.achievements)
        unlocked = len([a for a in self.achievements if a.unlocked])
        return unlocked, total
    
    def to_dict(self):
        """Konwertuj na słownik do zapisu"""
        return {
            'achievements': [
                {
                    'name': a.name,
                    'unlocked': a.unlocked
                } for a in self.achievements
            ]
        }
    
    def from_dict(self, data):
        """Wczytaj ze słownika"""
        if 'achievements' in data:
            saved_achievements = {a['name']: a['unlocked'] for a in data['achievements']}
            
            for achievement in self.achievements:
                if achievement.name in saved_achievements:
                    achievement.unlocked = saved_achievements[achievement.name]