import pygame
import GameHuman,GameNEAT,NEATTest


WIN_WIDTH = 288
WIN_HEIGHT = 512
BACKGROUND = pygame.image.load('IMAGES/bg.png')

Display = None

def text_objects(text, font,color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,width,height,col1,col2,action):
    global Display
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(Display, col2,(x,y,width,height))
        if click[0] == 1 :
            action(Display) 
    else:
        pygame.draw.rect(Display, col1,(x,y,width,height))

    smallText = pygame.font.SysFont('Comic Sans MS', 15)
    textSurf, textRect = text_objects(msg, smallText,(0,0,0))
    textRect.center = ( (x+(width/2)), (y+(height/2)) )
    Display.blit(textSurf, textRect)
    
def game_intro(DISPLAY):
    global Display
    Display = DISPLAY
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
           
        Display.blit(BACKGROUND,(0,0))
        largeText = pygame.font.SysFont('Comic Sans MS', 22)
        TextSurf, TextRect = text_objects("Flappy Bird (MT19012/20)", largeText,(0,118,0))
        TextRect.center = ((WIN_WIDTH/2),(WIN_HEIGHT/4))
        Display.blit(TextSurf, TextRect)
        
        button("MAKE IT JUMP!",75,310,150,50,(0,255,0),(0,137,0),GameHuman.game)
        #button("NEAT!",75,380,150,50,(0,255,0),(0,137,0),GameNEAT.game)
        #button("TEST NEAT!",75,450,150,50,(0,255,0),(0,137,0),NEATTest.game)
        pygame.display.update()
        pygame.time.Clock().tick(15)