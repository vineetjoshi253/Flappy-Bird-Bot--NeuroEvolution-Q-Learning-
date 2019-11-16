#Add Score
#Speed


import pygame
import GameClass
import sys

FPS = 30
WIN_WIDTH = 288
WIN_HEIGHT = 512
BACKGROUND = pygame.image.load('IMAGES/bg.png')

def game(DISPLAY):
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    SCORE = 0

    bird = GameClass.Bird(DISPLAY)
    pipe1 = GameClass.Pipe(DISPLAY, WIN_WIDTH+50)
    pipe2 = GameClass.Pipe(DISPLAY, WIN_WIDTH+50+(WIN_WIDTH/2))
    
    pipeGroup = pygame.sprite.Group()
    pipeGroup.add(pipe1.upperBlock)
    pipeGroup.add(pipe2.upperBlock)
    pipeGroup.add(pipe1.lowerBlock)
    pipeGroup.add(pipe2.lowerBlock)

    moved = False
    pause =0

    while True:

        DISPLAY.blit(BACKGROUND,(0,0))

        t = pygame.sprite.spritecollideany(bird,pipeGroup)

        if t!=None or (bird.y== 512 - bird.height) or (bird.y == 0):
            print("GAME OVER")
            print("FINAL SCORE IS %d"%SCORE)
            return(SCORE)
			
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE )):
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                bird.move("UP")
                moved = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m :
                pause=1

        if moved == False:
            bird.move(None)
        else:
            moved = False

		
        pipe1Pos = pipe1.move()
        if pipe1Pos[0] <= int(WIN_WIDTH * 0.2) - int(bird.rect.width/2):
            if pipe1.behindBird == 0:
                pipe1.behindBird = 1
                SCORE += 1
                print("SCORE IS %d"%SCORE)

        pipe2Pos = pipe2.move()
        if pipe2Pos[0] <= int(WIN_WIDTH * 0.2) - int(bird.rect.width/2):
            if pipe2.behindBird == 0:
                pipe2.behindBird = 1
                SCORE += 1
                print("SCORE IS %d"%SCORE)
		
        if pause==0:
            pygame.display.update()

        FPSCLOCK.tick(FPS)
