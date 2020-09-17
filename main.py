import pygame
import tkinter
import perlin

secret_rainbow_flag = False

letter_to_number = {
	"a": 1,
	"b": 2,
	"c": 3,
	"d": 4,
	"e": 5,
	"f": 6,
	"g": 7,
	"h": 8,
	"i": 9,
	"j": 10,
	"k": 11,
	"l": 12,
	"m": 13,
	"n": 14,
	"o": 15,
	"p": 16,
	"q": 17,
	"r": 18,
	"s": 19,
	"t": 20,
	"u": 21,
	"v": 22,
	"w": 23,
	"x": 24,
	"y": 25,
	"z": 26,

}


def get_num_from_string(string):
	"""
	converts a string into a number
	by adding each numeric value of each letters position
	"""
	output = 0
	string = string.lower()
	for char in string:
		if char in letter_to_number:
			output += letter_to_number[char]
		else:
			pass
	return output


def bsd_rand(seed=1):
	def rand(rmin, rmax):
		rand.seed = (1103515245 * rand.seed + 12345) & 0x7fffffff
		return rmin + (rand.seed % (rmax - rmin + 1))

	rand.seed = seed
	return rand


def generate_random_color(random_function):
	color = pygame.Color(0)
	hue = random_function(0, 360)
	sat = 100
	light = random_function(40, 60)
	alpha = 100
	color.hsla = hue, sat, light, alpha
	return color


def generate_similar_color(hsla, random_function):
	color = pygame.Color(0)
	light_change = random_function(-15, 15)
	hue_change = random_function(-12, 12)
	color = generate_neighbor_color(hsla, hue_change)
	h, s, l, a = color.hsla
	if l + light_change < 0 or l + light_change > 100:
		light_change = -light_change
	color.hsla = h, s, l + light_change, a
	return color


def generate_neighbor_color(hsla, offset):
	color = pygame.Color(0)
	hue, s, l, a = hsla
	if hue + offset > 360:
		hue = (hue + offset) - 360
	elif hue + offset < 0:
		hue = (hue + offset) + 360
	else:
		hue = hue + offset

	color.hsla = hue, s, l, a
	return color


def complementary_color(hsla):
	color = pygame.Color(0)
	hue, s, l, a = hsla
	if hue >= 180:
		color.hsla = hue - 180, s, l, a
		return color
	color.hsla = hue + 180, s, l, a
	return color


def generate_rects(screen, random_int_from_name, random_int_from_fav_thing, random_int_from_color):
	# create list of rectangles
	# generate rectangles in quadrants
	quadrants = [
		pygame.Rect((0, 0, screen.get_width() // 2, screen.get_height() // 2)),
		pygame.Rect((screen.get_width() // 2, 0, screen.get_width() // 2, screen.get_height() // 2)),
		pygame.Rect(
				(screen.get_width() // 2, screen.get_height() // 2, screen.get_width() // 2, screen.get_height() // 2)),
		pygame.Rect((0, screen.get_height() // 2, screen.get_width() // 2, screen.get_height() // 2))
	]

	rects = list()
	for quadrant in quadrants:
		num_of_rects = random_int_from_fav_thing(2, 5)
		for j in range(num_of_rects):
			width = random_int_from_name(25, 90)
			height = random_int_from_fav_thing(25, 90)
			x_pos = random_int_from_color(quadrant.x, quadrant.right - width)
			y_pos = random_int_from_fav_thing(quadrant.y, quadrant.bottom - height)
			new_rect = pygame.Rect((x_pos, y_pos, width, height))
			rects.append(new_rect)

	return rects


def generate_perlin(screen, random_int_from_fav_thing, random_int_from_name):
	# perlin noise for squiggles
	perlin.random.seed(random_int_from_fav_thing(2, 5) + random_int_from_name(3, 7))
	x_noise = perlin.PerlinNoiseFactory(1, octaves=5)
	y_noise = perlin.PerlinNoiseFactory(1, octaves=5)
	lines = [[], ]
	drawer_vel = pygame.Vector2()
	drawer_pos = pygame.Vector2()
	drawer_pos.x, drawer_pos.y = 200, 200
	current_line = 0
	# out of bounds flag
	oob = False

	# generate the random squigglies
	for i in range(0, 1000, 1):
		drawer_vel.x = x_noise(i / 500)
		drawer_vel.y = y_noise(i / 500)
		if drawer_vel.x != 0 or drawer_vel.y != 0:
			drawer_vel.normalize_ip()
			drawer_vel *= 5
			drawer_pos += drawer_vel
		if drawer_pos.x < 0:
			drawer_pos.x = screen.get_width()
			oob = True
		elif drawer_pos.x > screen.get_width():
			drawer_pos.x = 0
			oob = True
		elif drawer_pos.y < 0:
			drawer_pos.y = screen.get_height()
			oob = True
		elif drawer_pos.y > screen.get_height():
			drawer_pos.y = 0
			oob = True
		if oob:
			lines.append(list())
			current_line += 1
			oob = False
		lines[current_line].append((int(drawer_pos.x), int(drawer_pos.y)))
	return lines


def draw_rect(rect, surface, color, random_int_from_name):
	rect_color = pygame.Color(0)
	if secret_rainbow_flag:
		rect_color = generate_random_color(random_int_from_name)
	else:
		rect_color = generate_similar_color(color.hsla, random_int_from_name)

	# make the rect translucent for a cool effect
	rect_color.a = 240
	rectangle = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA, 32)
	rectangle.fill(rect_color)
	surface.blit(rectangle, rect)


def draw_lines(points, surface, color, random_int_from_name):
	if len(points) > 1:
		if secret_rainbow_flag:
			pygame.draw.lines(surface, generate_random_color(random_int_from_name), False, points, 4)
		else:
			pygame.draw.lines(
					surface,
					generate_similar_color(complementary_color(color.hsla).hsla, random_int_from_name),
					False, points, 4)


def main(name, age, favorite_thing, favorite_color):
	pygame.init()
	screen = pygame.display.set_mode((512, 512), pygame.SRCALPHA, 32)
	rect_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32)
	perlin_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA, 32)

	name = name.lower()
	favorite_thing = favorite_thing.lower()
	favorite_color = favorite_color.lower()

	# create functions to generate random numbers using the different user input as a seed
	random_int_from_fav_thing = bsd_rand(seed=get_num_from_string(favorite_thing))
	random_int_from_name = bsd_rand(seed=get_num_from_string(name))
	random_int_from_color = bsd_rand(seed=get_num_from_string(favorite_color))
	random_int_from_age = bsd_rand(seed=age)

	# get main colors
	main_color = 0

	if favorite_color in pygame.color.THECOLORS:
		main_color = pygame.Color(favorite_color)
	elif favorite_color == "rainbow" or favorite_color == "random" or favorite_color == "rainbows":
		main_color = pygame.Color("cyan")
		secret_rainbow_flag = True
	else:
		main_color = generate_random_color(random_int_from_color)

	rects = generate_rects(screen, random_int_from_name, random_int_from_color, random_int_from_fav_thing)
	perlin = generate_perlin(screen, random_int_from_fav_thing, random_int_from_name)

	# draw the squiggles
	for points in perlin:
		draw_lines(points, perlin_surface, main_color, random_int_from_name)

	for rect in rects:
		draw_rect(rect, rect_surface, main_color, random_int_from_name)

	screen.fill((255, 255, 255))
	screen.blit(perlin_surface, (0, 0))
	screen.blit(rect_surface, (0, 0))

	pygame.display.flip()
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				running = False

	pygame.quit()
