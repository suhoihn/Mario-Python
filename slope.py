#
# 2d platformer slope platform demo
# written to try to to help out someone on IRC
# 
# controls: 
# - left and right keyboard cursor keys: horizontal walking movement
# - up arrow cursor keyboard key: jump
#
# blockeduser
# Tue Dec 24 15:03:09 EST 2013
#
# See also: https://sites.google.com/site/bl0ckeduserssoftware/tricks,
# gives a drawing explaining a slightly different technique i used
# in an old platformer project circa 2009.
#
# better techniques may exist but this is a pretty
# straightforward one
#

import pygame	# somewhat convoluted SDL python binding...

import sys	# unix exit()

from pygame.locals import *		# mystery sauce

pygame.init()		# mandatory

# get a window with a fancy title and a font and a "clock"
win = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Slope Demo')
fpsClock = pygame.time.Clock()

# setup some colors for further use
black = pygame.Color(0, 0, 0)
blue = pygame.Color(0, 0, 255)
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)

# Variables: are the movement keys down ?
left_key_down = False
right_key_down = False

# Variables: player in-game coordinates
player_x = 10.0
player_y = 10.0

# Variable: player Y velocity
player_yvel = 0.0

#
#	CONSTANTS
#

player_w = 80.0		# player width
player_h = 80.0		# player height

yaccel = 1.0		# player Y accelearation
max_yvel = 20.0		# player max Y velcoity

slope_x1 = 10.0
slope_y1 = 200.0

slope_x2 = 640.0
slope_y2 = 70.0

on_slope = False

x_move_vel = 10.0

while True:
	# player horizontal movement
	moving_x = 0
	if left_key_down:
		moving_x = -x_move_vel
	if right_key_down:
		moving_x = +x_move_vel

	# adjust the Y-coordinates of the player if he walks
	# along the slope
	if on_slope and moving_x != 0:
		player_y += moving_x * ((slope_y2 - slope_y1) / (slope_x2 - slope_x1))

	# player Y acceleration
	if player_yvel < max_yvel:
		player_yvel += yaccel
	player_y += player_yvel

	# player X movement
	player_x += moving_x

	# player slope hit check
	on_slope = False
	# within the horizontal confines of slope ?
	if slope_x1 <= player_x + player_w <= slope_x2: #- player_w:
		# find out the Y-coordinate of the slope's intersection
		# to the player's current X-coordinate, and check
		# if the player's bottom Y position trespasses that.
		# if so, set the `on_slope' flag and zero the player's
		# Y velocity
		proj_y = slope_y1 + (player_x - slope_x1) * ((slope_y2 - slope_y1) / (slope_x2 - slope_x1))
		if player_y + player_h >= proj_y:
			player_y = proj_y - player_h
			player_yvel = 0
			on_slope = True	

	# draw white background
	pygame.draw.rect(win, white, (0,0, 640, 480))

	# draw player
	pygame.draw.rect(win, black, (player_x, player_y, player_w, player_h))

	# draw slope
	pygame.draw.line(win, red, (slope_x1, slope_y1), (slope_x2, slope_y2), 2)

	# flip the videobuffers
	pygame.display.update()

	# deal with keyboard events and quit events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit(0)
		elif event.type == KEYDOWN:
			if event.key == K_LEFT:
				left_key_down = True
			elif event.key == K_RIGHT:
				right_key_down = True
			elif event.key == K_UP:
				# jumping -- give a velocity pulse
				# only allowed if on the slope
				if on_slope:
					player_yvel = -10.0
		elif event.type == KEYUP:
			if event.key == K_LEFT:
				left_key_down = False
			elif event.key == K_RIGHT:
				right_key_down = False

	fpsClock.tick(20)

