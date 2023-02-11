import pacMan
import pygame


# button class
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


pygame.init()

# create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# game variables
menu_state = 'main'

# define fonts
font = pygame.font.SysFont("arialblack", 40)

# define colours
TEXT_COL = (255, 255, 255)

# load button images
play_img = pygame.image.load("asserts/buttons/play.png").convert_alpha()
quit_img = pygame.image.load("asserts/buttons/QUIT.png").convert_alpha()
back_img = pygame.image.load("asserts/buttons/back.png").convert_alpha()
easy_img = pygame.image.load('asserts/buttons/easy.png').convert_alpha()
medium_img = pygame.image.load('asserts/buttons/MEDIUM.png').convert_alpha()
hard_img = pygame.image.load('asserts/buttons/hard.png').convert_alpha()

# create button instances
play_button = Button(250, 125, play_img, 1)
quit_button = Button(250, 300, quit_img, 1)
easy_button = Button(250, 75, easy_img, 1)
hard_button = Button(250, 200, hard_img, 1)
medium_button = Button(250, 325, medium_img, 1)
back_button = Button(250, 450, back_img, 1)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# game loop
run = True
while run:

    screen.fill((2, 44, 67))

    # check menu state
    if menu_state == 'main':
        # draw pause screen buttons
        if play_button.draw(screen):
            menu_state = 'difficulties'
        if quit_button.draw(screen):
            run = False
    # check if the options menu is open
    if menu_state == 'difficulties':
        if easy_button.draw(screen):
            pacMan.start_pacman(0)
        if medium_button.draw(screen):
            pacMan.start_pacman(1)
        if hard_button.draw(screen):
            pacMan.start_pacman(2)
        if back_button.draw(screen):
            menu_state = 'main'

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
