import pygame
from numpy.random import choice

#Parameters
WIN_WIDTH = 288
WIN_HEIGHT = 512
PIPEGAP = 160 
BASESHIFT = WIN_HEIGHT * 0.79

class Bird(pygame.sprite.Sprite):
    def __init__(self,displayScreen):
        #Init Bird As Game Object
        pygame.sprite.Sprite.__init__(self)
        #Load Bird Image
        self.image = pygame.image.load('IMAGES/bird1.png')
        
        #Initial Positions Of Birds
        self.x = int(WIN_WIDTH * 0.2)
        self.y = WIN_HEIGHT*0.5
        
        #Rectangle Bounding Box (Bird)
        self.rect = self.image.get_rect()
        self.height = self.rect.height
        
        #Where to display
        self.screen = displayScreen
        
        #Bird Parameters
        self.playerVelY = -9
        self.playerMaxVelY = 10
       	self.playerMinVelY = -8
       	self.playerAccY = 1
       	self.playerFlapAcc = -9
       	self.playerFlapped = False
        self.display(self.x, self.y)

    #Display Bird
    def display(self,x,y):
        self.screen.blit(self.image, (x,y))
        self.rect.x, self.rect.y = x,y

    #Move Input
    def move(self,input):

    	if input != None:
    		self.playerVelY = self.playerFlapAcc
    		self.playerFlapped = True

    	if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
    		self.playerVelY += self.playerAccY
    	if self.playerFlapped:
    		self.playerFlapped = False

    	self.y += min(self.playerVelY, WIN_HEIGHT - self.y - self.height)
    	self.y = max(self.y,0)
    	self.display(self.x,self.y)


class PipeBlock(pygame.sprite.Sprite):
	def __init__(self,image,upper):
		pygame.sprite.Sprite.__init__(self)
		if upper == False:
			self.image = pygame.image.load(image)
		else:
			self.image = pygame.transform.rotate(pygame.image.load(image),180)
		self.rect = self.image.get_rect()



class Pipe(pygame.sprite.Sprite):
	def __init__(self,screen,x):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.lowerBlock = PipeBlock('IMAGES/pipe.png',False)
		self.upperBlock = PipeBlock('IMAGES/pipe.png',True)
		self.pipeWidth = self.upperBlock.rect.width
		self.x = x
		heights = self.getHeight()
		self.upperY, self.lowerY = heights[0], heights[1]
		self.behindBird = 0
		self.display()


	def getHeight(self):
		randVal = choice([1,2,3,4,5,6,7,8,9], p =[0.04,0.04*2,0.04*3,0.04*4,0.04*5,0.04*4,0.04*3,0.04*2,0.04] )
		midYPos = 106 + 30*randVal
		upperPos = midYPos - (PIPEGAP/2)
		lowerPos = midYPos + (PIPEGAP/2)
		return([upperPos,lowerPos])

	def display(self):
		self.screen.blit(self.lowerBlock.image, (self.x, self.lowerY))
		self.screen.blit(self.upperBlock.image, (self.x, self.upperY - self.upperBlock.rect.height))
		self.upperBlock.rect.x, self.upperBlock.rect.y = self.x, (self.upperY - self.upperBlock.rect.height)
		self.lowerBlock.rect.x, self.lowerBlock.rect.y = self.x, self.lowerY

	def move(self):

		self.x -= 3

		if self.x <= 0:
			self.x = WIN_WIDTH
			heights = self.getHeight()
			self.upperY, self.lowerY = heights[0], heights[1]
			self.behindBird = 0

		self.display()
		return([self.x+(self.pipeWidth/2), self.upperY, self.lowerY])
