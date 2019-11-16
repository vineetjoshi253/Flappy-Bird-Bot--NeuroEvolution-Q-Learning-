import pygame
import neat
import os
import GameClass
import pickle

DISPLAY = None
FPS = 100
WIN_WIDTH = 288
WIN_HEIGHT = 512
BACKGROUND = pygame.image.load('IMAGES/bg.png')
SCORE = 0
GENERATION = 0
MAX_FITNESS = 0
BEST_GENOME = 0

def gameBeta(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    DISPLAY  = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('Flappy Bird')

    global SCORE

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
        
        if output[0]>=0.5:
            bird.move("UP")
            moved = True
		

        if moved == False:
            bird.move(None)
        else:
            moved = False

		
        pipe1Pos = pipe1.move()
        if pipe1Pos[0] <= int(WIN_WIDTH * 0.2) - int(bird.rect.width/2):
            if pipe1.behindBird == 0:
                pipe1.behindBird = 1
                SCORE += 10
                print("SCORE IS %d"%(SCORE+vertDist))

        pipe2Pos = pipe2.move()
        if pipe2Pos[0] <= int(WIN_WIDTH * 0.2) - int(bird.rect.width/2):
            if pipe2.behindBird == 0:
                pipe2.behindBird = 1
                SCORE += 10
                print("SCORE IS %d"%(SCORE+vertDist))
		
		


        pygame.display.update()
        FPSCLOCK.tick(FPS)


def eval_genomes(genomes, config):
    i = 0
    global SCORE
    global GENERATION, MAX_FITNESS, BEST_GENOME

    GENERATION += 1
    for genome_id, genome in genomes:
		
        genome.fitness = gameBeta(genome, config)
        #print("Gen : %d Genome # : %d  Fitness : %f Max Fitness : %f"%(GENERATION,i,genome.fitness, MAX_FITNESS))
        if genome.fitness >= MAX_FITNESS:
            MAX_FITNESS = genome.fitness
            BEST_GENOME = genome
            SCORE = 0
        i+=1
    print(GENERATION)
def gameAlpha(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    
    winner = pop.run(eval_genomes, 100)
    print(type(winner))
    
    outputFile = open('BestOfBest.txt','wb')
    pickle.dump(winner, outputFile)

    
def game(Display):
    global DISPLAY
    DISPLAY = Display
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    gameAlpha(config_path)
