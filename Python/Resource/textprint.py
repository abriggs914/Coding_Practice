import pygame
import datetime

#	Class to print text to a pygame window.
#	Borrowed from:
#	https://stackoverflow.com/questions/49887874/pygame-xbox-one-controller
#	Version............1.0
#	Date........2022-03-05
#	Author....Avery Briggs

pygame.init()


BLACK = pygame.Color('black')
WHITE = pygame.Color('white')

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):

	def __init__(self):
		self.reset()
		self.font = pygame.font.Font(None, 20)

	def tprint(self, screen, textString):
		new_line_split = textString.split("\n")
		for new_line in new_line_split:
			tab_split = new_line.split("\t")
			for line in tab_split:
				if line or 1:
					textBitmap = self.font.render(line, True, BLACK)
					screen.blit(textBitmap, (self.x, self.y))
					width = textBitmap.get_width()
					if len(line) == 0:
						self.x += width
					self.indent()
			self.new_line()
			for i in range(len(tab_split)):
				self.unindent()

	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15

	def indent(self):
		self.x += 10

	def unindent(self):
		self.x -= 10
		
	def new_line(self):
		self.y += self.line_height
		
if __name__ == "__main__":
	# Set the width_canvas and height_canvas of the screen (width_canvas, height_canvas).
	screen = pygame.display.set_mode((500, 700))
	
	pygame.display.set_caption("My Game")
	
	# Loop until the user clicks the close button.
	done = False
	
	# Used to manage how fast the screen updates.
	clock = pygame.time.Clock()
	
	# Get ready to print.
	textPrint = TextPrint()
	
	while not done:
		#
		# EVENT PROCESSING STEP
		#
		# Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
		# JOYBUTTONUP, JOYHATMOTION
		for event in pygame.event.get(): # User did something.
			if event.type == pygame.QUIT: # If user clicked close.
				done = True # Flag that we are done so we exit this loop.

		#
		# DRAWING STEP
		#
		# First, clear the screen to white. Don't put other drawing commands
		# above this, or they will be erased with this command.
		screen.fill(WHITE)
		textPrint.reset()
		
		textPrint.tprint(screen, f"new line string: {datetime.datetime.now()}\nTesting new line")
		textPrint.new_line()
		textPrint.tprint(screen, f"new tab string: {datetime.datetime.now()}\tTesting tab")
		textPrint.new_line()
		textPrint.indent()
		textPrint.tprint(screen, f"new split tab string: {datetime.datetime.now()}\nhere's the new line\tfollowed by tab")
		textPrint.tprint(screen, f"new split tab string: {datetime.datetime.now()}\n\n\n\t\tTricky Test:\n1\t-\tTab\n2\t-\tTab")

		pygame.display.flip()
		
		# Limit to 20 frames per second.
		clock.tick(20)
	
	