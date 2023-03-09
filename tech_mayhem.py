#Author: Guillermo Ochoa
#Last update: 23/12/2015 dd/mm/yyyy
#  V 0.8

#TODO###########################################################
"""
Stuff
"""
################################################################

import math, pygame, os, sys
from random import randint
from pygame.locals import *

WIDTH = 1024
HEIGHT = 768

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)

def load_image(name, colorkey=None):
	fullname = resource_path(os.path.join('data', name))
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
			image.set_colorkey(colorkey, RLEACCEL)
	return image
	
#Objects###########################################################

class Celestia(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.fly = []
		self.fly.append(load_image("sprite_1.png", -1))
		self.fly.append(load_image("sprite_2.png", -1))
		self.image = load_image("sprite_1.png", -1)
		self.fly[0] = pygame.transform.scale(self.fly[0], (150, 71))
		self.fly[1] = pygame.transform.scale(self.fly[1], (150, 71))
		self.image = self.fly[0]
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.counter = 0
		self.health = 100
		
		#actions
		self.left = False
		self.right = False
		self.up = False
		self.down = False

	def update(self):
		if self.up:
			self.rect.y -= 6
			
		if self.down:
			self.rect.y += 6
			
		if self.left:
			self.rect.x -= 6
			
		if self.right:
			self.rect.x += 6
			
		if self.counter == 30:
			self.image = self.fly[0]
			self.counter = 0
			
		elif self.counter == 15:
			self.image = self.fly[1]

		self.counter += 1

class Missile(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y, s):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("missile.png", -1)
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.speed = s
		self.health = 100
		
	def update(self):
		self.rect.x -= self.speed

class Bullet(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.destroyed = False
		self.image = pygame.Surface((20, 3))
		self.image.fill((255, 255, 0))
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		
	def update(self):
		self.rect.x += 20
		
#Animations########################################################

class Flash(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.images.append(load_image("gun_1.png", -1))
		self.images.append(load_image("gun_2.png", -1))
		self.images.append(load_image("gun_3.png", -1))
		self.images.append(load_image("gun_4.png", -1))
		self.images.append(load_image("gun_5.png", -1))
		for i in range(len(self.images)):
			self.images[i] = pygame.transform.scale(self.images[i], (64, 36))
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.counter = 0
		
	def update(self, x, y):
		self.rect.x = x
		self.rect.y = y
		if self.index == len(self.images):
			self.kill()
		else:
			if self.counter == 1:
				self.image = self.images[self.index]
				self.index += 1
				self.counter = 0
			self.counter += 1

class Explotion(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.images.append(load_image("b1.png", -1))
		self.images.append(load_image("b2.png", -1))
		self.images.append(load_image("b3.png", -1))
		self.images.append(load_image("b4.png", -1))
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = init_x - 70
		self.rect.y = init_y - 10
		self.counter = 0
		
	def update(self):
		if self.index == len(self.images):
			self.kill()
		else:
			if self.counter == 3:
				self.image = self.images[self.index]
				self.index += 1
				self.counter = 0
			self.counter += 1

class Hit(pygame.sprite.Sprite):
	def __init__(self, init_x, init_y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.images.append(pygame.Surface((4, 4)))
		self.images.append(pygame.Surface((8, 8)))
		self.images.append(pygame.Surface((15, 15)))
		self.images[0].fill((255, 255, 0))
		self.images[1].fill((100, 100, 100))
		self.images[2].fill((200, 200, 200))
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.x = init_x
		self.rect.y = init_y
		self.counter = 0
		
	def update(self):
		if self.index == len(self.images):
			self.kill()
		else:
			if self.counter == 7:
				self.image = self.images[self.index]
				self.index += 1
				self.counter = 0
			self.counter += 1

#Main Game#########################################################			
def main():
	#initialize
	pygame.init()
	pygame.font.init()
	font = pygame.font.Font(resource_path(os.path.join('data', "Righteous.ttf")), 40)
	screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption("Technolestia's Mayhem")
	pygame.display.flip()
	clock = pygame.time.Clock()
	
	score = 0
	spawn_time = 150
	firing = False
	next_shot = 10
	game_over = False
	time = 150
	level = 0
	
	#background/images
	background = pygame.Surface(screen.get_size())
	background.fill((100, 100, 150))
	
	health = pygame.Surface((200, 20))
	health.fill((255, 0, 0))
	
	health_bar = pygame.Surface((200, 20))
	health_bar.fill((0, 255, 0))
	
	#content
	player = Celestia(50, HEIGHT/2)
	missiles = pygame.sprite.Group()
	fire = pygame.sprite.Group()
	explotions = pygame.sprite.Group()
	bullets = pygame.sprite.Group()
	hits = pygame.sprite.Group()
	tia = pygame.sprite.Group()
	tia.add(player)

	#game loop
	while 1:
		time_passed = clock.tick(60)
		
		#INPUT handler
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
				
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == K_LEFT:
					player.left = True
				if event.key == K_RIGHT:
					player.right = True
				if event.key == K_UP:
					player.up = True
				if event.key == K_DOWN:
					player.down = True
				if event.key == K_SPACE:
					firing = True
				if event.key == K_RETURN:
					game_over = False
					missiles.empty()
					bullets.empty()
					bullets.empty()
					hits.empty()
					explotions.empty()
					background.fill((100, 100, 150))
					player.rect.x = 50
					player.rect.y = HEIGHT/2
					score = 0
					player.health = 100

			if event.type == KEYUP:
				if event.key == K_LEFT:
					player.left = False
				if event.key == K_RIGHT:
					player.right = False
				if event.key == K_UP:
					player.up = False
				if event.key == K_DOWN:
					player.down = False
				if event.key == K_SPACE:
					firing = False
					
		if game_over == False:
			#LEVELS
			if score == 0:
				time = 150
				level = 0
				
			if score % 500 == 0:
				if time > 10:
					time -= 20
					level += 1
					score += 20
				else:
					time = 10
				
			#Handle Sprites
			spawn_time -= 1
			if spawn_time == 0:
				missiles.add(Missile(WIDTH, randint(1, HEIGHT - 50), randint(4, 6)))
				spawn_time = time
				
			if player.rect.x > WIDTH - 150:
				player.rect.x = WIDTH - 150
				
			if player.rect.x < 0:
				player.rect.x = 0
				
			if player.rect.y > HEIGHT - 71:
				player.rect.y = HEIGHT - 71
				
			if player.rect.y < 0:
				player.rect.y = 0
				
			#Collisions
			for missile in missiles:
				if missile.rect.x == -200:
					missiles.remove(missile)
				
				for i in pygame.sprite.spritecollide(missile, bullets, False):
					missile.health -= 25
					score += 20
				
				for i in pygame.sprite.spritecollide(missile, tia, False):
					player.health -= 10
					explotions.add(Explotion(missile.rect.x + 50, missile.rect.y - 50))
					missiles.remove(missile)
				
				if missile.health == 0:
					explotions.add(Explotion(missile.rect.x + 50, missile.rect.y - 50))
					missiles.remove(missile)
					
			for bullet in bullets:
				if bullet.rect.x >= WIDTH:
					bullets.remove(bullet)
					
				for i in pygame.sprite.spritecollide(bullet, missiles, False):
					hits.add(Hit(bullet.rect.x + 6, bullet.rect.y))
					bullets.remove(bullet)
			
			#EVENTS
			if firing:
				if next_shot == 0:
					fire.add(Flash(player.rect.x + 150, player.rect.y + 28))
					bullets.add(Bullet(player.rect.x + 150, player.rect.y + 45))
					next_shot = 8
				next_shot -= 1
			
			if player.health == 0:
				game_over = True
				
				
			#Draw EEERRRRYTHING
			player.update()
			fire.update(player.rect.x + 150, player.rect.y + 28)
			bullets.update()
			missiles.update()
			explotions.update()
			hits.update()

			screen.blit(background, (0, 0))
			explotions.draw(screen)
			fire.draw(screen)
			tia.draw(screen)
			missiles.draw(screen)
			bullets.draw(screen)
			hits.draw(screen)
			screen.blit(health, (10, 10))
			screen.blit(health_bar, (10, 10), pygame.Rect(0, 0, player.health * 2, 20))
			screen.blit(font.render("Score: " + str(score - 20), 1, (255, 255, 255)), (WIDTH/2 + 50, 10))
			screen.blit(font.render("Level: " + str(level), 1, (255, 255, 255)), (WIDTH/2 - 150, 10))
			pygame.display.update()
			
		else:
			missiles.empty()
			bullets.empty()
			bullets.empty()
			hits.empty()
			explotions.empty()
			
			background.fill((0, 0, 0))
			screen.blit(background, (0, 0))
			screen.blit(font.render("Score: " + str(score - 20), 1, (255, 255, 255)), (WIDTH/2 - 80, HEIGHT/2))
			screen.blit(font.render("Game Over", 1, (255, 255, 255)), (WIDTH/2 - 80, HEIGHT/2 - 150))
			screen.blit(font.render("Press ENTER to restart", 1, (255, 255, 255)), (WIDTH/2 - 150, HEIGHT/2 + 150))
			pygame.display.update()

if __name__ == '__main__': main()