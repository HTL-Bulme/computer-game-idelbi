import pygame, sys
from pygame.locals import *
import random
import math

pygame.init()

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("fonts/font.ttf", size)

screen_width = 840
screen_height = 840
i = 0

font = pygame.font.SysFont('Bauhaus 93',60)
white = (255,0,0)
	

def draw_text(text, font, text_col, x, y):
	img5 = font.render(text, True, text_col)
	screen.blit(img5,(x,y))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('FLAPPING BALL')
bg = pygame.image.load('img/bg.png')
bg_width = bg.get_width()
fotos = math.ceil(screen_width /bg_width ) + 1
def play():

	clock = pygame.time.Clock()
	fps = 120
	
	
	#variables
	scroll_speed = 0
	flying = False
	game_over = False
	log_gap = 150
	log_frequency = 1000 #ms
	last_log = pygame.time.get_ticks() - log_frequency
	bg_scroll = 0
	score = 0
	pass_log = False
	




	pygame.mixer.music.load('sounds/music2.mp3')
	pygame.mixer.music.play(-1)
	flapp =  pygame.mixer.Sound('sounds/wing.mp3')
	

	





	class Bird(pygame.sprite.Sprite):
		def __init__(self, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.images = []
			self.index = 0
			self.counter = 0
			for num in range(1, 4):
				img = pygame.image.load(f'img/ball{num}.png')
				self.images.append(img)
			self.image = self.images[self.index]
			self.rect = self.image.get_rect()
			self.rect.center = [x, y]
			self.vel = 0
			self.clicked = False

		def update(self):

			if flying == True:
				#gravity
				self.vel += 0.5
				
				if self.vel > 8:
					self.vel = 8
				if self.rect.bottom < 768:
					self.rect.y += int(self.vel)

			if game_over == False:
				#jump
				if not self.clicked and pygame.key.get_pressed()[pygame.K_SPACE]:
					self.clicked = True
					self.vel = -10
					flapp.play()
				if not pygame.key.get_pressed()[pygame.K_SPACE]:
					self.clicked = False

				#handle the animation
				self.counter += 1
				flap_cooldown = 5

				if self.counter > flap_cooldown:
					self.counter = 0
					self.index += 1
					if self.index >= len(self.images):
						self.index = 0
				self.image = self.images[self.index]

				#rotate the bird
				self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
			else:
				self.image = pygame.transform.rotate(self.images[self.index], -90)



	class log(pygame.sprite.Sprite):
		def __init__(self, x, y, position):
			pygame.sprite.Sprite.__init__(self)
			self.image = pygame.image.load('img/log.png')
			self.rect = self.image.get_rect()
			#position 1 is from the top, -1 is from the bottom
			if position == 1:
				self.image = pygame.transform.flip(self.image, False, True)
				self.rect.bottomleft = [x, y - int(log_gap / 2)]
			if position == -1:
				self.rect.topleft = [x, y + int(log_gap / 2)]

		def update(self):
			self.rect.x -= scroll_speed
			if self.rect.right < 0:
				self.kill()



	bird_group = pygame.sprite.Group()
	log_group = pygame.sprite.Group()

	flappy = Bird(100, int(screen_height / 2))

	bird_group.add(flappy)



	run = True
	while run:
		PLAY_MOUSE_POS = pygame.mouse.get_pos()

		clock.tick(fps)
		
		#draw background
		for i in range(0, fotos):
			screen.blit(bg, (i* bg_width + bg_scroll,0))
		bg_scroll -= scroll_speed
		if abs(bg_scroll) > bg_width:
			bg_scroll = 0

		bird_group.draw(screen)
		bird_group.update()
		log_group.draw(screen)

		if len(log_group) > 0:
			if (bird_group.sprites()[0].rect.left > log_group.sprites()[0].rect.right) and (not pass_log):
				score += 1
				pass_log = True
			elif bird_group.sprites()[0].rect.right < log_group.sprites()[0].rect.left:
				pass_log = False


		draw_text(str(score), font, white, int(screen_width / 2), 20)
		
					
			


			
		



		BACK = Button(image=pygame.image.load("img/Play Rect.png"), pos= (420, 460),text_input="Menu", font = get_font(75), base_color= "Blue", hovering_color="White") 
		
		
		

		#look for collision
		if pygame.sprite.groupcollide(bird_group, log_group, False, False) or flappy.rect.top < 0:
			game_over = True
			scroll_speed = 0
			pygame.mixer.music.stop()
			

			

		#check if bird has hit the ground
		if flappy.rect.bottom >= 768:
			game_over = True
			flying = False
			scroll_speed = 0
			BACK.changeColor(PLAY_MOUSE_POS)
			BACK.update(screen)
			pygame.mixer.music.stop()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if BACK.checkForInput(PLAY_MOUSE_POS):
					main_menu()
			
			


		if game_over == False and flying == True:

			#generate new logss
			time_now = pygame.time.get_ticks()
			if time_now - last_log > log_frequency:
				log_height = random.randint(-100, 100)
				btm_log = log(screen_width, int(screen_height / 2) + log_height, 1)
				
				top_log = log(screen_width, int(screen_height / 2) + log_height, -1)
				log_group.add(btm_log)
				log_group.add(top_log)
				
				last_log = time_now


			

			log_group.update()

		#score
		


		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				run = False
			
			if event.type == pygame.KEYDOWN:
				
				if event.key == pygame.K_w:
					
					pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() - 0.1)
				if event.key == pygame.K_q:
					
					pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() + 0.1)

				if event.key == pygame.K_e:
					
					pygame.mixer.music.play()


				if event.key == pygame.K_SPACE and not flying and not game_over:
					scroll_speed = 4
					flying = True
					
				

		pygame.display.update()

	pygame.quit()

def main_menu():
    while True:
        screen.blit(bg, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "Green")
        MENU_RECT = MENU_TEXT.get_rect(center=(420, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(420, 250), 
                            text_input="PLAY", font=get_font(75), base_color="Blue", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(420, 550), 
                            text_input="QUIT", font=get_font(75), base_color="Blue", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    
                    sys.exit()

        pygame.display.update()

main_menu()
	