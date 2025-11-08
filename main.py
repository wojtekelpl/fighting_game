#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gra Walki z Skinami
Prosta gra 2D gdzie walczysz z przeciwnikami, zdobywasz doświadczenie i odblokowujesz nowe skiny!
"""

import pygame
import sys
from game import Game

def main():
    """Główna funkcja uruchamiająca grę"""
    pygame.init()
    
    # Ustawienia okna
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gra Walki z Skinami")
    
    # Ikona okna (opcjonalna)
    # pygame.display.set_icon(pygame.image.load("icon.png"))
    
    # Inicjalizacja gry
    game = Game(screen)
    
    # Główna pętla gry
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Przekazanie eventów do gry
            game.handle_event(event)
        
        # Aktualizacja gry
        game.update()
        
        # Rysowanie
        game.draw()
        
        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(60)  # 60 FPS
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()