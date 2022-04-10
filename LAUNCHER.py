from turtle import width
import pygame
import random

#window
FPS = 60
WIDTH = 900
HEIGHT = 600

def printing(window, text, font, size, color, x, y):
    fontName = pygame.font.match_font(font)
    fontSize = pygame.font.Font(fontName, size)
    textSurface = fontSize.render(text, True, color)
    text_rect = textSurface.get_rect()
    text_rect.center = (x, y)
    window.blit(textSurface, text_rect)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (25,255,0)
GRAY = (128, 128, 128)
VIOLET = (126, 8, 236)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREEN = (0,128,0)
CYAN = (0, 255, 255)
LIGHTGRAY = (211, 211, 211)
NAVY = (0, 0, 128)
MEDIUMSLATEBLUE = (123, 104, 238)
SKYBLUE = (0, 191, 255)
HONEYDEW = (240, 255, 240)
SNOW = (255, 250, 250)
IVORY = (255, 255, 240)
YELLOWGREEN = (154, 205, 50)
DARKGREEN = (0, 100, 0)
INDIGO = (75, 0, 130)

#player(platform) and objects
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platImg,(200,20))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2,HEIGHT-20)
    
    def update(self):
        self.speedx = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.speedx = -10
        if keys[pygame.K_d]:
            self.speedx = 10
        self.rect.x += self.speedx  

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0     

class Circle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20,20))
        self.image = pygame.transform.scale(circleImg,(20,20))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speedx = random.randint(-3,3)
        if self.speedx == 0:
            self.speedx = 2
        self.speedy = random.randint(3,7)

    def update(self):
        if self.rect.right > WIDTH:
            self.speedx = -self.speedx
            

        if self.rect.left < 0:
            self.speedx = -self.speedx
            

        if self.rect.top < 0:
            self.speedy = -self.speedy

        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((43,43))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 2
        # self.image = pygame.transform.scale(blockImg,(43,43))
        self.updTx()
    def updTx(self):
        self.image = pygame.transform.scale(blockImg[self.hp-1],(43,43))
        
    


pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('SimplePong')
clock = pygame.time.Clock()

#textures and design
platImg = pygame.image.load('player.jpg').convert()
blockImg =[ pygame.image.load('brick.jpg').convert(), pygame.image.load('player.jpg').convert()]
circleImg = pygame.image.load('circle.jpg').convert()
pygame.display.set_icon(pygame.image.load('icon.svg'))
mainbg = pygame.image.load('mainBg.jpg').convert()
mainbg = pygame.transform.scale(mainbg,(WIDTH, HEIGHT))
mainbg_rect = mainbg.get_rect()
bglv = pygame.image.load('bglv.jpg').convert()
bglv = pygame.transform.scale(bglv,(WIDTH, HEIGHT))
bglv_rect = bglv.get_rect()
menubg = pygame.image.load('menuBg.jpg').convert()
menubg = pygame.transform.scale(menubg, (WIDTH, HEIGHT))
menubg_rect = menubg.get_rect()


#objects
player = Platform()
circle = Circle()
sprites = pygame.sprite.Group()
circles = pygame.sprite.Group()
blocks = pygame.sprite.Group()
circles.add(circle)
sprites.add(player)
sprites.add(circle)

levels = [
    ['####################',
     ' # # # # # # # # # #'],

    ['####################',
     '# #### ### ### ### #'],

    ['# # # # ## # # # # #',
     '####################'],
        ]


level = 0
for i in range(20):
    for j in range(len(levels[level])):
        if levels[level][j][i] == '#':
            block = Block(i*45, j*45)
            sprites.add(block)
            blocks.add(block)

playerScore = 0
state = 3 #0- game is going on, 1 - level has ended. 2 - game has ended

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if state != 0:
                    run = False
            if event.key == pygame.K_c:
                if state != 0:
                    state = 0
            if event.key == pygame.K_ESCAPE:
                if state!=1 and state!=2 and state!=3 and state!=4:
                    state = 4
            if event.key == pygame.K_e:
                if state != 0:
                    state = 0

            if event.key == pygame.K_r:
                if state != 0:
                    state = 0
                    level = 0
                    playerScore = 0
                    for i in range(20):
                        for j in range(len(levels[level])):
                            if levels[level][j][i] == '#':
                                block = Block(i*45, j*45)
                                sprites.add(block)
                                blocks.add(block)
                    circle.rect.center = (WIDTH//2, HEIGHT//2)

    hitscircle = pygame.sprite.spritecollide(player, circles, False)
    if hitscircle:
        circle.speedy = -circle.speedy

    hitsblocks = pygame.sprite.spritecollide(circle, blocks, False)
    if hitsblocks:
        circle.speedy = -circle.speedy
        for hit in hitsblocks:
            hit.hp-=1
            hit.updTx()
            if hit.hp <1: 
                hit.kill()               
                playerScore+=1

    if len(blocks.sprites()) == 0:
        level+=1
        if level == len(levels):
            state = 2 #end
        elif state!=2:
            state = 1 #level passed
            for i in range(20):
                for j in range(len(levels[level])):
                    if levels[level][j][i] == '#':
                        block = Block(i*45, j*45)
                        sprites.add(block)
                        blocks.add(block)
            circle.rect.center = (WIDTH//2, HEIGHT//2)

    if circle.rect.y > HEIGHT:
        state = 2

    if state == 0:
        window.blit(mainbg, mainbg_rect)
        sprites.draw(window)
        sprites.update()
        printing(window, 'Score: '+str(playerScore), 'Sheriff', 30, GREEN, 60, HEIGHT-70)
        pygame.display.flip()
    elif state == 1:
        window.blit(bglv, bglv_rect)
        printing(window, "You've passed the level!", 'Arial', 30, VIOLET, WIDTH//2, HEIGHT//2-20)
        printing(window, '|C| Continue', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+80)
        printing(window, '|Q| Quit', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+120)
        pygame.display.flip()
    elif state == 2:
        window.blit(bglv, bglv_rect)
        printing(window, "The End!", 'Arial', 40, VIOLET, WIDTH//2, HEIGHT//2-50)
        printing(window, '|R| Restart', 'Arial', 25, BLUE, WIDTH//2, HEIGHT//2+20)
        printing(window, '|Q| Quit', 'Arial', 25, RED, WIDTH//2, HEIGHT//2+50)
        printing(window, 'For more games you can visit our github: https://github.com/Aboba-Games', 'Arial', 20, MEDIUMSLATEBLUE, WIDTH//2, HEIGHT//2+160)
        pygame.display.flip()
    elif state == 3:
        window.blit(menubg, menubg_rect)
        printing(window, 'SimplePong', 'Sheriff', 40, GRAY, WIDTH//2, HEIGHT//2)
        printing(window, 'Version: snapshot 0.1b9.4.22', 'Sheriff', 20, RED, WIDTH//2, HEIGHT/2-20)
        printing(window, '|E|Play', 'Sheriff', 30, GREEN, WIDTH//2, HEIGHT//2+80)
        printing(window, '|Q|Exit', 'Sheriff', 30, RED, WIDTH//2, HEIGHT//2+120)
        printing(window, 'Aboba Games®', 'Arial', 25, BLUE, 90, 10)
        printing(window, 'Updated: 04/10/22', 'Arial', 25, BLUE, 790, 10)
        pygame.display.flip()
    elif state == 4:
        window.blit(menubg, menubg_rect)
        printing(window, 'Pause', 'Sheriff', 40, GRAY, WIDTH//2, HEIGHT//2-50)
        printing(window, '|C|Continue', 'Sheriff', 30, GREEN, WIDTH//2, HEIGHT//2+20)
        printing(window, '|Q|Exit', 'Sheriff', 30, RED, WIDTH//2, HEIGHT//2+50)
        pygame.display.flip()

pygame.quit()
#s01a104