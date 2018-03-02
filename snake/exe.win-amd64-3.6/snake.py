import pygame
import sys
import random
import time

pygame.init()                                                      #take some rgb color
background = (96,57,198)
foodColor = (255,0,0)
buttonHover =  (102,156,75)
headColor = (219,214,4)
snakeColor1 = (51,138,21)
snakeColor2 = (191,128,255)
buttonColor=(128,128,64)
fontColor = (0,162,232)

display = pygame.display.set_mode((456,456))          #display size
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

foodSound = pygame.mixer.Sound('eat.wav')
dieSound = pygame.mixer.Sound('snakeDie.wav')
snakeImg = pygame.image.load("snake.png")
snakeBody=[]

def Intro():                                          #Itroduction Page with 'play' button
	namefont = pygame.font.SysFont("comicsansms",15)
	nametext = namefont.render("Credit: Md Tomal Hossain",True,fontColor)
	display.fill(background)
	display.blit(snakeImg,(0,0))
	display.blit(nametext,(260,420))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
		Button("Exit",50,300,80,60,QuiteGame)
		Button("Play >>",250,300,100,60,MainGame)
		pygame.display.update()
		clock.tick(15)

def Button(name,x,y,h,w,action=None):                          #button function
	pos = pygame.mouse.get_pos()                               #take mouse current position
	click = pygame.mouse.get_pressed()                         #if mouse is clicked then a variable will be stored in click

	if x<pos[0]<x+h and y<pos[1]<y+w:
		pygame.draw.rect(display,buttonHover,[x,y,h,w])
		if click[0]==1 and action!=None:
			action()
	else:
		pygame.draw.rect(display,buttonColor,[x,y,h,w])
	font = pygame.font.SysFont("comicsansms",20)
	text = font.render(name,True,fontColor)
	display.blit(text,(x+15,y+15))

def newFood():                                                  #Food Generating fumction
	global Body
	Apple = [12*(random.randrange(0,36)),12*(random.randrange(0,36))]
	flag = True
	while flag:
		for pos in Body:
			if pos == Apple:
				Apple = [12*(random.randrange(0,36)),12*(random.randrange(0,36))]
				newFood()
		flag = False
	return Apple

def BonusFood():
	pos = newFood();
	return pos;

def ScoreBoard(score):                                         # function for score update
	font = pygame.font.SysFont('comicsansms',18)
	text = font.render('Score: '+str(score),True,fontColor)
	display.blit(text,(5,5))

def QuiteGame():                                               # function for Quite Game
	pygame.quit()
	sys.exit()

def start():
	start = pygame.time.get_ticks()
	return start
def GameOver():                                                # Game Over Menu
	pygame.mixer.Sound.play(dieSound)
	font = pygame.font.SysFont("comicsansms",60)
	text = font.render("Game Over",True,fontColor)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

		display.blit(text,(60,150))
		Button("Quit",50,300,80,60,QuiteGame)
		Button("Play Again",250,300,150,60,MainGame)
		pygame.display.update()
		clock.tick(15)

def MainGame(speed=12):                                                # Main Games starts from here
	global Body
	Bonus = [-10,-10]
	Body = [[96,108],[84,108],[72,108],[60,108],[48,108]]
	Head = [96,108]
	Apple = [12*(random.randrange(0,36)),12*(random.randrange(0,36))]
	b=-1;
	score = 0
	seconds = 0
	direction = 'right'
	change = direction
	exit = False
	while not exit:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit = True
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					change = 'up'
				if event.key == pygame.K_DOWN:
					change = 'down'
				if event.key == pygame.K_RIGHT:
					change = 'right'
				if event.key == pygame.K_LEFT:
					change = 'left'
		if direction == 'right' and not change == 'left':
			direction = change
		if direction == 'left' and not change == 'right':
			direction =change
		if direction == 'up' and not change == 'down':
			direction = change
		if direction == 'down' and not change == 'up':
			direction =change

		if direction == 'right':
			Head[0] += 12
		if direction == 'left':
			Head[0] -= 12
		if direction == 'up':
			Head[1] -= 12
		if direction == 'down':
			Head[1] += 12

		if Head[0]<0:
			 Head[0] = 444
		if Head[0]>444:
			Head[0] = 0
		if Head[1]<0:
			Head[1] = 444
		if Head[1]>444:
			Head[1] = 0
		Body.insert(0,list(Head))

		if Head[0] == Apple[0] and Head[1] == Apple[1]:
			pygame.mixer.Sound.play(foodSound)
			score += 5
			if score>0 and score%20==0:
				speed += 1
				Bonus = BonusFood();
				b = 0
				st = start()
			Apple=newFood()	
		else:
			Body.pop()
		
		if (Head[0] == Bonus[0] and Head[1] == Bonus[1]) or (Head[0] == Bonus[0]+12 and Head[1] == Bonus[1]+12):
			pygame.mixer.Sound.play(foodSound)
			score += 10
			b = -1
			Bonus = [-10,-10]
		for pos in Body[1:]:
			if pos == Head:
				GameOver()
		display.fill(background)
		pygame.draw.rect(display,headColor,[Head[0],Head[1],12,12])

		for pos in Body[1::2]:
			pygame.draw.rect(display,snakeColor2,[pos[0],pos[1],12,12])
		for pos in Body[2::2]:
			pygame.draw.rect(display,snakeColor1,[pos[0],pos[1],12,12])
		pygame.draw.rect(display,foodColor,[Apple[0],Apple[1],12,12])
		if(b is not -1):
			pygame.draw.rect(display,headColor,[Bonus[0],Bonus[1],24,24])
			seconds=int(5-((pygame.time.get_ticks()-st)/1000))
		if seconds<=0:
			b=-1
			Bonus = [-10,-10]
		ScoreBoard(score)
		pygame.display.update()
		clock.tick(speed)
Intro()
pygame.quit()
sys.exit()
