from operator import truediv
from pickle import TRUE
from textwrap import fill
from turtle import color, distance, left
import pygame, sys, time, math, random
from button import Button
from pygame import mixer

#initiate the mae
pygame.init()
mixer.init()

#set the size of window
screen = pygame.display.set_mode((1280,720))

#title and icon of the game
pygame.display.set_caption("Good old Tanks")
icon = pygame.image.load('assets/tank icon.png')
pygame.display.set_icon(icon)

background=pygame.image.load('assets/background main.jpg')

block1 = pygame.Rect(440,520,100,240)
block2 = pygame.Rect(540,600,80,200)
block3 = pygame.Rect(620,530,120,250)
block4 = pygame.Rect(740,500,100,220)
block1img = pygame.image.load('assets/building1.png')
block2img = pygame.image.load('assets/building2.png')
block3img = pygame.image.load('assets/building3.png')
block4img = pygame.image.load('assets/building4.png')
block1img = pygame.transform.scale(block1img, (100, 240))
block2img = pygame.transform.scale(block2img, (120, 200))
block3img = pygame.transform.scale(block3img, (190, 250))
block4img = pygame.transform.scale(block4img, (100, 220))

def get_font(size):
	return pygame.font.Font("assets/font.ttf",size)

def gameover(winner):
	if winner == 0:
		player = "RED TANK"
		color = (255,0,0)
	else:
		player = "GREEN TANK"
		color = (0,255,0)

	text = get_font(45).render(player + " WON !", True, color)
	screen.blit(text, [280, 150])

	while True:
		HELP_MOUSE_POS = pygame.mouse.get_pos()

		MAIN_MENU = Button(image=None, pos=(640, 320), 
		text_input="MAIN MENU", font=get_font(20), base_color="Black", hovering_color="#7c887e")
		
		PLAY_AGAIN = Button(image=None, pos=(640, 360), 
		text_input="PLAY AGAIN", font=get_font(20), base_color="Black", hovering_color="#7c887e")

		MAIN_MENU.changeColor(HELP_MOUSE_POS)
		MAIN_MENU.update(screen)

		PLAY_AGAIN.changeColor(HELP_MOUSE_POS)
		PLAY_AGAIN.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if MAIN_MENU.checkForInput(HELP_MOUSE_POS):
					main_menu()
				if PLAY_AGAIN.checkForInput(HELP_MOUSE_POS):
					play()	
		pygame.display.update()

def play():
	def barrier():
		global block1, block2, block3, block4

		#pygame.draw.rect(screen,('#1c222e'),block1)
		#pygame.draw.rect(screen,('#1c222e'),block2)
		#pygame.draw.rect(screen,('#1c222e'),block3)
		#pygame.draw.rect(screen,('#1c222e'),block4)
		screen.blit(block1img,(440,520))
		screen.blit(block3img,(590,530))
		screen.blit(block2img,(520,600))
		screen.blit(block4img,(740,500))
	
	def powerDisplay(power,posx):
		text = get_font(18).render("Power: " + str(power) + "%", True, ("#726870"))
		screen.blit(text, [posx, 40])
	
	def turnDisplay(posx):
		if turn == 0:
			player=('GREEN TANK')
			color=('#0a6522')
			text = get_font(24).render(player + " TURN", True, color)
			screen.blit(text, [posx, 60])
		else:
			player='RED TANK'
			color=('#710c04')
			text = get_font(24).render(player + " TURN", True, color)
			screen.blit(text, [posx + 30, 60])
	
	def angleDisplay(angle,posx):
		text = get_font(18).render("Angle: " + str(angle) + "º", True, ("#726870"))
		screen.blit(text, [posx, 60])
	
	def distanceDisplay(distance,posx):
		text = get_font(18).render("Fuel: " + str(100 - distance) + "%", True, ("#726870"))
		screen.blit(text, [posx, 80])

	def healthDisplay(health,posx):
		text = get_font(18).render("Health: " + str(health) + "%", True, ("#726870"))
		screen.blit(text, [posx, 100])	

	def shootAnimation(tankx,tanky,enemyx,enemyy,facing,angle,power,enemy,option):
		global block1, block2, block3, block4

		explosion_tank=pygame.image.load('assets/explosion tank.png')
		explosion_terrain=pygame.image.load('assets/explosion terrain.png')
		explosion_nuke = pygame.image.load('assets/explosion nuke.png')
		nukeUP=pygame.image.load('assets/nuke up.png')
		nukeDOWN=pygame.image.load('assets/nuke down.png')
		enemyHitbox = pygame.Rect(enemy.x,enemy.y+15,64,34)

		fire = True
		damage = 0
		if option == 0:
			if facing == -1:
				x = tankx
				y = tanky+16
			else:
				x = tankx+54
				y = tanky+16

			power*=1.5
			time = 0
			newx=x
			newy=y

			while fire:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				redrawScreen()
				pygame.draw.circle(screen,(0,0,0),(newx,newy),4)
				bulletHitbox = (newx-4, newy-4,8,8)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox,1)
				pygame.display.update()

				time+=0.09


				if(newy >= 695 ):
					screen.blit(explosion_terrain,(newx - 32,newy - 64))
					hitSound()
					pygame.display.update()
					pygame.time.wait(500)
					fire=False		
				if(newx >= 1280 or newx <= 0):
					fire = False	

				if block1.colliderect(bulletHitbox) or block2.colliderect(bulletHitbox) or block3.colliderect(bulletHitbox) or block4.colliderect(bulletHitbox):
					fire = False
					screen.blit(explosion_tank,(newx - 16,newy - 16))
					hitSound()
					pygame.display.update()
					pygame.time.wait(500)
				
				if enemyHitbox.colliderect(bulletHitbox):
					fire = False
					screen.blit(explosion_tank,(newx - 16,newy - 16))
					hitSound()	
					pygame.display.update()		
					pygame.time.wait(500)	
					if newx >= enemyx+16 and newx <=enemyx+48:
						damage=50
					else:
						damage=25
					return damage		
				newx=x+(power*time*math.cos(math.radians(angle)))*facing
				newy=y-power*time*math.sin(math.radians(angle))+0.5*9.81*(time)**2

		if option == 1:
			y=tanky
			if facing == -1:
				x=tankx+40
			else:
				x=tankx+24
			
			time = 0
			newx=x
			newy=y
			while fire:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				redrawScreen()

				screen.blit(nukeUP,(newx-12,newy-12))


				bulletHitbox = (newx-12, newy-12,24,24)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox,1)
				pygame.display.update()		


				time+=0.09
				newy=y-(80*time)

				if newy <= 0:
					fire = False
				
			fire  = True	
			newx = enemyx+32
			time = 0
			while fire:	
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				redrawScreen()

				screen.blit(nukeDOWN,(newx-12,newy-12))
				bulletHitbox = (newx-12, newy-12,24,24)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox,1)
				pygame.display.update()	

				time+=0.09
				newy=(90*time)

				if enemyHitbox.colliderect(bulletHitbox):
					fire = False
					screen.blit(explosion_nuke,(newx - 16,newy - 16))	
					hitNukeSound()
					pygame.display.update()		
					pygame.time.wait(500)	
					damage = 10
					return damage		
				
		if option == 2:
			if facing == -1:
				x = tankx
				y = tanky+16
			else:
				x = tankx+54
				y = tanky+16

			power*=1.5
			time = 0
			newx1=x
			newy1=y
			newx2=x
			newy2=y
			newx3=x
			newy3=y

			fire1 =True
			fire2 =True
			fire3 =True

			while fire1 or fire2 or fire3:
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
						sys.exit()

				redrawScreen()
				pygame.draw.circle(screen,(0,0,0),(newx1,newy1),4)
				pygame.draw.circle(screen,(0,0,0),(newx2,newy2),4)
				pygame.draw.circle(screen,(0,0,0),(newx3,newy3),4)
				bulletHitbox1 = (newx1-4, newy1-4,8,8)
				bulletHitbox2 = (newx2-4, newy2-4,8,8)
				bulletHitbox3 = (newx3-4, newy3-4,8,8)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox1,1)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox2,1)
				#pygame.draw.rect(screen,(255,0,0), bulletHitbox3,1)
				pygame.display.update()

				time+=0.09
				if fire1:
					if(newy1 >= 695 ):
						screen.blit(explosion_terrain,(newx1 - 32,newy1 - 64))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
						fire1=False		
					if(newx1 >= 1280 or newx1 <= 0):
						fire1 = False	

					if block1.colliderect(bulletHitbox1) or block2.colliderect(bulletHitbox1) or block3.colliderect(bulletHitbox1) or block4.colliderect(bulletHitbox1):
						fire1 = False
						screen.blit(explosion_tank,(newx1 - 16,newy1 - 16))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
					if enemyHitbox.colliderect(bulletHitbox1):
						fire1 = False
						screen.blit(explosion_tank,(newx1 - 16,newy1 - 16))
						hitSound()	
						pygame.display.update()		
						pygame.time.wait(500)	
						if newx1 >= enemyx+16 and newx1 <=enemyx+48:
							damage+=25
						else:
							damage+=15
					newx1=x+(power*time*math.cos(math.radians(angle+3)))*facing
					newy1=y-power*time*math.sin(math.radians(angle+3))+0.5*9.81*(time)**2						
				if fire2:
					if(newy2 >= 695 ):
						screen.blit(explosion_terrain,(newx2 - 32,newy2 - 64))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
						fire2=False		
					if(newx2 >= 1280 or newx2 <= 0):
						fire2 = False	
					if block1.colliderect(bulletHitbox2) or block2.colliderect(bulletHitbox2) or block3.colliderect(bulletHitbox2) or block4.colliderect(bulletHitbox2):
						fire2 = False
						screen.blit(explosion_tank,(newx2 - 16,newy2 - 16))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
					if enemyHitbox.colliderect(bulletHitbox2):
						fire2 = False
						screen.blit(explosion_tank,(newx2 - 16,newy2 - 16))
						hitSound()	
						pygame.display.update()		
						pygame.time.wait(500)	
						if newx2 >= enemyx+16 and newx2 <=enemyx+48:
							damage+=25
						else:
							damage+=15
					newx2=x+(power*time*math.cos(math.radians(angle)))*facing
					newy2=y-power*time*math.sin(math.radians(angle))+0.5*9.81*(time)**2
				if fire3:
					if(newy3 >= 695 ):
						screen.blit(explosion_terrain,(newx3 - 32,newy3 - 64))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
						fire3=False		
					if(newx3 >= 1280 or newx3 <= 0):
						fire3 = False	
					if block1.colliderect(bulletHitbox3) or block2.colliderect(bulletHitbox3) or block3.colliderect(bulletHitbox3) or block4.colliderect(bulletHitbox3):
						fire3 = False
						screen.blit(explosion_tank,(newx3 - 16,newy3 - 16))
						hitSound()
						pygame.display.update()
						pygame.time.wait(500)
					if enemyHitbox.colliderect(bulletHitbox3):
						fire3 = False
						screen.blit(explosion_tank,(newx3 - 16,newy3 - 16))
						hitSound()	
						pygame.display.update()		
						pygame.time.wait(500)	
						if newx3 >= enemyx+16 and newx3 <=enemyx+48:
							damage+=25
						else:
							damage+=15
					newx3=x+(power*time*math.cos(math.radians(angle-3)))*facing
					newy3=y-power*time*math.sin(math.radians(angle-3))+0.5*9.81*(time)**2
				if (not(fire1) and not(fire2) and not(fire3)):
					return damage

	def shootSound():
		sound = pygame.mixer.Sound('assets/shoot.ogg')
		sound.play()

	def hitSound():
		sound = pygame.mixer.Sound('assets/hit.ogg')
		sound.play()

	def hitNukeSound():
		sound = pygame.mixer.Sound('assets/hit-nuke.ogg')
		sound.play()

	def chooseAmmo():
		text = get_font(35).render("CHOOSE AMMO:", True, "Black")
		screen.blit(text, [450, 250])

		while True:
			HELP_MOUSE_POS = pygame.mouse.get_pos()

			BASIC = Button(image=None, pos=(640, 320), 
			text_input="BASIC", font=get_font(20), base_color="Black", hovering_color="#7c887e")
			
			NUKE = Button(image=None, pos=(640, 360), 
			text_input="NUKE", font=get_font(20), base_color="Black", hovering_color="#7c887e")

			TRIPLE = Button(image=None, pos=(640, 400), 
			text_input="TRIPLE", font=get_font(20), base_color="Black", hovering_color="#7c887e")

			BASIC.changeColor(HELP_MOUSE_POS)
			BASIC.update(screen)

			NUKE.changeColor(HELP_MOUSE_POS)
			NUKE.update(screen)

			TRIPLE.changeColor(HELP_MOUSE_POS)
			TRIPLE.update(screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if BASIC.checkForInput(HELP_MOUSE_POS):
						return 0
					if NUKE.checkForInput(HELP_MOUSE_POS):
						return 1	
					if TRIPLE.checkForInput(HELP_MOUSE_POS):
						return 2	
			pygame.display.update()

	rightTankImg = pygame.image.load('assets/tank R.png')
	leftTankImg = pygame.image.load('assets/tank L.png')

	battlefieldBG=pygame.image.load('assets/background play.png')
	screen.blit(battlefieldBG, (0, 0))

	PLAY_BACK = Button(image=None, pos=(35, 20), 
						text_input="BACK", font=get_font(15), base_color="Black", hovering_color="Red") #726870

	class Stats():
		def __init__(self,power,angle,distance,health):
			self.power=power
			self.angle=angle
			self.distance=distance
			self.health=health

	class Tank():
		def __init__(self,x,y,img):
			self.x=x
			self.y=y
			self.vel=5
			self.img=img
			self.hitbox = (self.x, self.y+15,64,34)
		
		def draw(self, screen):
			screen.blit(self.img,(self.x, self.y))

			self.hitbox = (self.x, self.y+15,64,34)
			#pygame.draw.rect(screen,(255,0,0), self.hitbox,1)

	leftTank=Tank(136,650,leftTankImg)
	rightTank=Tank(1080,650,rightTankImg)

	def redrawScreen():
		screen.blit(battlefieldBG,(0,0))
		PLAY_BACK.changeColor(PLAY_MOUSE_POS)
		PLAY_BACK.update(screen)
		
		barrier()
		rightTank.draw(screen)
		leftTank.draw(screen)	
		powerDisplay(leftStats.power,50)
		angleDisplay(leftStats.angle,50)
		distanceDisplay(leftStats.distance,50)
		healthDisplay(leftStats.health,50)
		powerDisplay(rightStats.power,1030)
		angleDisplay(rightStats.angle,1030)
		distanceDisplay(rightStats.distance,1030)
		healthDisplay(rightStats.health,1030)
		turnDisplay(450)

		if rightStats.distance >= 100 or leftStats.distance >= 100 :
			text = get_font(25).render("YOU NEED TO SHOOT !", True, ("Black"))
			screen.blit(text, [420, 150])

		pygame.display.update()

	rightStats = Stats(10,0,0,100)
	leftStats = Stats(10,0,0,100)

	turn =0

	while True:
		
		if leftStats.health <=0:
			gameover(1)
		elif rightStats.health <=0:
			gameover(0)

		pygame.time.delay(60)
		PLAY_MOUSE_POS = pygame.mouse.get_pos()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
					main_menu()


		keys = pygame.key.get_pressed()
		if turn==0:
			if keys[pygame.K_LEFT] and rightTank.x > 840:
				if rightStats.distance<100:
					rightTank.x-=rightTank.vel
					rightStats.distance+=rightTank.vel

			elif keys[pygame.K_RIGHT] and rightTank.x < 1280 - 56 - rightTank.vel:
				if rightStats.distance<100:
					rightTank.x+=rightTank.vel
					rightStats.distance+=rightTank.vel

			if keys[pygame.K_UP] and rightStats.angle<90:
				rightStats.angle+=5
			elif keys[pygame.K_DOWN] and rightStats.angle>0:
				rightStats.angle-=5

			if keys[pygame.K_KP8] and rightStats.power<100:
				rightStats.power+=2
			elif keys[pygame.K_KP2] and rightStats.power>10:
				rightStats.power-=2

			if keys[pygame.K_RSHIFT]:
				option = chooseAmmo()
				shootSound()
				damage = shootAnimation(rightTank.x,rightTank.y,leftTank.x,leftTank.y,-1,rightStats.angle,rightStats.power,leftTank, option)
				if damage:
					leftStats.health-=damage
				turn=1
				rightStats.distance=0

		else:
			if keys[pygame.K_a] and leftTank.x > leftTank.vel - 10:
				if leftStats.distance<100:
					leftTank.x-=leftTank.vel
					leftStats.distance+=rightTank.vel

			elif keys[pygame.K_d] and leftTank.x < 384:
				if leftStats.distance<100:
					leftTank.x+=leftTank.vel
					leftStats.distance+=rightTank.vel
			
			if keys[pygame.K_w] and leftStats.angle<90:
				leftStats.angle+=5
			elif keys[pygame.K_s] and leftStats.angle>0:
				leftStats.angle-=5

			if keys[pygame.K_e] and leftStats.power<100:
				leftStats.power+=2
			elif keys[pygame.K_q] and leftStats.power>10:
				leftStats.power-=2

			if keys[pygame.K_LSHIFT]:
				option = chooseAmmo()
				shootSound()
				damage = shootAnimation(leftTank.x,leftTank.y,rightTank.x,rightTank.y,1,leftStats.angle,leftStats.power,rightTank,option)
				if damage:	
					rightStats.health-=damage
				turn=0
				leftStats.distance=0

		redrawScreen()


    
def help():
	while True:
		HELP_MOUSE_POS = pygame.mouse.get_pos()

		helpBG=pygame.image.load('assets/background help1.jpg')
		screen.blit(helpBG,(0,0))

		HELP_TEXT = get_font(65).render("HOW TO PLAY", True, "#bab79f")
		HELP_RECT = HELP_TEXT.get_rect(center=(640, 80))
		screen.blit(HELP_TEXT, HELP_RECT)

		PLAYER_TEXT = get_font(25).render("PLAYER 1", True, "#bab79f")
		PLAYER_RECT = PLAYER_TEXT.get_rect(center=(640, 180))
		screen.blit(PLAYER_TEXT, PLAYER_RECT)

		MOVEMENT_TEXT = get_font(20).render("← & → . . . . . move left/right", True, "#bab79f")
		MOVEMENT_RECT = MOVEMENT_TEXT.get_rect(center=(640, 220))
		screen.blit(MOVEMENT_TEXT, MOVEMENT_RECT)

		AIM_TEXT = get_font(20).render("↑ & ↓ . . . . . . . aim up/down", True, "#bab79f")
		AIM_RECT = AIM_TEXT.get_rect(center=(640, 260))
		screen.blit(AIM_TEXT, AIM_RECT)

		POWER_TEXT = get_font(20).render("K_8 & K_2 . . . . power up/down", True, "#bab79f")
		POWER_RECT = AIM_TEXT.get_rect(center=(640, 300))
		screen.blit(POWER_TEXT, POWER_RECT)

		SHOOT_TEXT = get_font(20).render("R-SHIFT . . . . . . . . . shoot", True, "#bab79f")
		SHOOT_RECT = SHOOT_TEXT.get_rect(center=(640, 340))
		screen.blit(SHOOT_TEXT, SHOOT_RECT)

		PLAYER_TEXT = get_font(25).render("PLAYER 2", True, "#bab79f")
		PLAYER_RECT = PLAYER_TEXT.get_rect(center=(640, 400))
		screen.blit(PLAYER_TEXT, PLAYER_RECT)

		MOVEMENT_TEXT = get_font(20).render("A & D . . . . . move left/right", True, "#bab79f")
		MOVEMENT_RECT = MOVEMENT_TEXT.get_rect(center=(640, 440))
		screen.blit(MOVEMENT_TEXT, MOVEMENT_RECT)

		AIM_TEXT = get_font(20).render("W & S . . . . . . . aim up/down", True, "#bab79f")
		AIM_RECT = AIM_TEXT.get_rect(center=(640, 480))
		screen.blit(AIM_TEXT, AIM_RECT)

		POWER_TEXT = get_font(20).render("E & Q . . . . . . power up/down", True, "#bab79f")
		POWER_RECT = AIM_TEXT.get_rect(center=(640, 520))
		screen.blit(POWER_TEXT, POWER_RECT)

		SHOOT_TEXT = get_font(20).render("L-SHIFT . . . . . . . . . shoot", True, "#bab79f")
		SHOOT_RECT = SHOOT_TEXT.get_rect(center=(640, 560))
		screen.blit(SHOOT_TEXT, SHOOT_RECT)

		HELP_BACK = Button(image=None, pos=(640, 640), 
		text_input="BACK", font=get_font(45), base_color="#bab79f", hovering_color="#7c887e")

		HELP_BACK.changeColor(HELP_MOUSE_POS)
		HELP_BACK.update(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if HELP_BACK.checkForInput(HELP_MOUSE_POS):
					main_menu()

		pygame.display.update()

def main_menu():
    while True:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("GOOD OLD TANKS", True, "#c2b399")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#1c222e", hovering_color="#9e9a75")
        HELP_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 400), 
                            text_input="HELP", font=get_font(75), base_color="#1c222e", hovering_color="#9e9a75")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#1c222e", hovering_color="#9e9a75")
                           

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, HELP_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if HELP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    help()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()