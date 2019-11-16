import os,sys
import neat
import pickle
import pygame
import GameClass

DISPLAY = None
SCORE = 0
FPS = 30
WIN_WIDTH = 288
WIN_HEIGHT = 512

BACKGROUND = pygame.image.load('IMAGES/bg.png')

def gameBeta(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAY  = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    SCORE = 0

    bird = GameClass.Bird(DISPLAY)
    pipe1 = GameClass.Pipe(DISPLAY, WIN_WIDTH+100)
    pipe2 = GameClass.Pipe(DISPLAY, WIN_WIDTH+100+(WIN_WIDTH/2))

    pipeGroup = pygame.sprite.Group()
    pipeGroup.add(pipe1.upperBlock)
    pipeGroup.add(pipe2.upperBlock)
    pipeGroup.add(pipe1.lowerBlock)
    pipeGroup.add(pipe2.lowerBlock)

    moved = False
	
    time = 0

    while True:

        DISPLAY.blit(BACKGROUND,(0,0))

        if (pipe1.x < pipe2.x and pipe1.behindBird==0) or (pipe2.x < pipe1.x and pipe2.behindBird==1):
            input = (bird.y,pipe1.x, pipe1.upperY, pipe1.lowerY)
            centerY = (pipe1.upperY + pipe1.lowerY)/2
        elif (pipe1.x < pipe2.x and pipe1.behindBird==1) or (pipe2.x < pipe1.x and pipe2.behindBird==0):
            input = (bird.y,pipe2.x, pipe2.upperY, pipe2.lowerY)
            centerY = (pipe2.upperY + pipe2.lowerY)/2

        vertDist = (((bird.y - centerY)**2)*100)/(512*512)
        time += 1
		
        fitness = SCORE - vertDist + (time/10.0)

        t = pygame.sprite.spritecollideany(bird,pipeGroup)

        if t!=None or (bird.y== 512 - bird.height) or (bird.y == 0):
            return(fitness)
			
        output = net.activate(input)
		
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
                 
        if output[0]>=0.5:
            bird.move("UP")
            moved = True

        if moved == False:
            bird.move(None)
        else:
            moved = False

        pipe1Pos = pipe1.move()
        if pipe1Pos[0] <= int(WIN_WIDTH * 0.2):
            if pipe1.behindBird == 0:
                pipe1.behindBird = 1
                SCORE += 10
                print("SCORE IS %d"%(SCORE))

        pipe2Pos = pipe2.move()
        if pipe2Pos[0] <= int(WIN_WIDTH * 0.2):
            if pipe2.behindBird == 0:
                pipe2.behindBird = 1
                SCORE += 10
                print("SCORE IS %d"%(SCORE))
		
        pygame.display.update()
        FPSCLOCK.tick(FPS)
    
    
def gameAlpha(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    genomeFile = 'BestOfBest.txt'
    genome = pickle.load(open(genomeFile,'rb'))
    
    fitnessScores = []
    global SCORE
    for i in range(10):
        fitness = gameBeta(genome, config)
        SCORE = 0
        print('Fitness is %f'% fitness)
        fitnessScores.append(fitness)
    

def game(Display):
    global DISPLAY
    DISPLAY = Display
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    gameAlpha(config_path)