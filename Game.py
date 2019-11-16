import pygame
import GameIntro
pygame.init()

WIN_WIDTH = 288
WIN_HEIGHT = 512

def main():
    DISPLAY  = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    GameIntro.game_intro(DISPLAY)
    pygame.quit()

if __name__ == "__main__":
    main()