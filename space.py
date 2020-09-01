import sqlite3

import pygame
import sys

# Constants
DISPLAYWIDTH = 640
DISPLAYHEIGHT = 480
PLAYERWIDTH = 40
PLAYERHEIGHT = 40
ALIENWIDTH = 60
ALIENHEIGHT = 60
BULLETWIDTH = 5
BULLETHEIGHT = 5
BGCOLOR = (211, 211, 211)

# Colors
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

DIRECTIONS = {pygame.K_LEFT: (-1), pygame.K_RIGHT: 1}


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        image = pygame.image.load("spaceship.png").convert()
        self.image = pygame.transform.scale(image, (PLAYERWIDTH, PLAYERHEIGHT))
        self.rect = self.image.get_rect()
        self.name = 'PLAYER1'
        self.hp = 3

    def update(self, keys, *args):
        for key in DIRECTIONS:
            if keys[key]:
                self.rect.x += DIRECTIONS[key] * 80
        self.checkForSide()

    def checkForSide(self):
        if self.rect.right > DISPLAYWIDTH:
            self.rect.right = DISPLAYWIDTH
        elif self.rect.left < 0:
            self.rect.left = 0


class Alien(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = PLAYERWIDTH
        self.height = PLAYERHEIGHT
        image = pygame.image.load("alien.png").convert_alpha()
        self.image = pygame.transform.scale(image, (ALIENWIDTH, ALIENHEIGHT))
        self.rect = self.image.get_rect()
        self.nbMoves = 1
        self.time = pygame.time.get_ticks() - 500

    def update(self, keys, currentTime):
        if currentTime - self.time > 30:
            if (self.nbMoves // 6) % 2 == 0:
                self.rect.x += 10
                self.nbMoves += 1
            if (self.nbMoves // 6) % 2 == 1:
                self.rect.x -= 10
                self.nbMoves += 1
            if self.nbMoves % 6 == 0:
                self.rect.y += 10
            self.time = currentTime


class Bullet(pygame.sprite.Sprite):

    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.width = BULLETWIDTH
        self.height = BULLETHEIGHT
        self.color = YELLOW
        image = pygame.image.load("laser.png").convert_alpha()
        self.image = pygame.transform.scale(image, (BULLETWIDTH, BULLETHEIGHT))
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.top = rect.bottom
        self.speed = 3
        self.vectory = -1

    def update(self, *args):
        self.rect.y += self.vectory * self.speed

        if self.rect.bottom < 0:
            self.kill()

        elif self.rect.bottom > 500:
            self.kill()


class App():

    def __init__(self):
        pygame.init()
        self.displaySurf, self.displayRect = self.makeScreen()
        self.player = self.makePlayer()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.bullets = pygame.sprite.Group()
        self.aliens = self.makeAliens()
        self.allSprites = pygame.sprite.Group(self.player, self.aliens)
        self.gameOver = -1
        self.updateDb = 0
        self.start = pygame.time.get_ticks()
        self.end = 0

    def makeAliens(self):
        aliens = pygame.sprite.Group()
        for i in range(4):
            for j in range(8):
                alien = Alien()
                alien.rect.x = j * (ALIENWIDTH + 20)
                alien.rect.y = i * (ALIENHEIGHT + 5)
                aliens.add(alien)

        return aliens

    def makePlayer(self):
        player = Player()
        player.rect.centerx = self.displayRect.centerx
        player.rect.bottom = self.displayRect.bottom - 5

        return player

    def makeScreen(self):
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        displayRect = displaySurf.get_rect()
        background = pygame.image.load("background.jpg").convert()
        background = pygame.transform.scale(background, (DISPLAYWIDTH, DISPLAYHEIGHT))
        displaySurf.blit(background, (0, 0))
        displaySurf.convert()

        return displaySurf, displayRect

    def checkEvents(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.gameOver == 0:
                        bullet = Bullet(self.player.rect)
                        self.bullets.add(bullet)
                        self.allSprites.add(bullet)
                    elif self.gameOver == -1:
                        self.gameOver = 0
                    elif self.gameOver == 2:
                        self.gameOver = -1
                        self.resetGame()
                    elif self.gameOver == 1:
                        self.resetGame()
                        self.gameOver = -1
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def checkCollisions(self):
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        for a in self.aliens:
            if a.rect.bottom == DISPLAYHEIGHT:
                a.kill()
                self.player.hp -= 1

    def checkGameOver(self):
        if len(self.aliens) == 0:
            self.gameOver = 1
        if self.player.hp < 1:
            self.gameOver = 2

    def resetGame(self):
        self.player = self.makePlayer()
        self.bullets = pygame.sprite.Group()
        self.aliens = self.makeAliens()
        self.allSprites = pygame.sprite.Group(self.player, self.aliens)
        self.keys = pygame.key.get_pressed()
        self.clock = pygame.time.Clock()
        self.start = pygame.time.get_ticks()


    def winScreen(self):
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        win = pygame.image.load("win.jpg").convert()
        win = pygame.transform.scale(win, (DISPLAYWIDTH, DISPLAYHEIGHT))
        displaySurf.blit(win, (0, 0))
        displaySurf.convert()

    def loseScreen(self):
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        lose = pygame.image.load("gameover.jpg").convert()
        lose = pygame.transform.scale(lose, (DISPLAYWIDTH, DISPLAYHEIGHT))
        displaySurf.blit(lose, (0, 0))
        displaySurf.convert()

    def home(self):
        displaySurf = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))
        home = pygame.image.load("home.jpg").convert()
        home = pygame.transform.scale(home, (DISPLAYWIDTH, DISPLAYHEIGHT))
        displaySurf.blit(home, (0, 0))
        displaySurf.convert()

    def save(self, conn):
        self.end = pygame.time.get_ticks()
        print(self.start, self.end)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO result(username, score) VALUES(?, ?)""", (self.player.name, self.end - self.start))
        cursor.execute("""SELECT * FROM result""")
        users = cursor.fetchall()
        conn.commit()
        print(users)

    def mainLoop(self):
        pygame.init()
        conn = sqlite3.connect('space.db')
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS result(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, username TEXT, score INTEGER)""")
        conn.commit()
        running = True
        while running:
            if self.gameOver == -1:
                self.home()
                self.checkEvents()
                pygame.display.flip()
                self.clock.tick(60)
            elif self.gameOver == 0:
                currentTime = pygame.time.get_ticks()
                self.updateDb = 0
                self.makeScreen()
                self.checkEvents()
                self.allSprites.update(self.keys, currentTime)
                self.checkCollisions()
                self.allSprites.draw(self.displaySurf)
                pygame.display.flip()
                pygame.display.update()
                self.checkGameOver()
                self.clock.tick(60)
            elif self.gameOver == 1:
                self.checkEvents()
                self.winScreen()
                self.checkEvents()
                if self.updateDb == 0:
                    self.updateDb += 1
                    self.save(conn)
                pygame.display.flip()
                pygame.display.update()
                self.clock.tick(60)
            elif self.gameOver == 2:
                self.checkEvents()
                self.loseScreen()
                self.checkEvents()
                pygame.display.flip()
                pygame.display.update()
                self.clock.tick(60)



if __name__ == '__main__':
    pygame.init()
    app = App()
    app.mainLoop()
