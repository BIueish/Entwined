import copy
import pygame, sys, os, random
from pygame.locals import *
pygame.mixer.init(channels=8, buffer=1024)
pygame.font.init()
from src.player import Player
import settings
settings.spawn = []
from src.circle import Circle
from src.square import Square
from src.triangle import Triangle


class Game:
    def __init__(self):
        settings.loadSettings()
        pygame.display.set_caption("Entwined")
        self.displaysurf = pygame.display.set_mode((600, 600), pygame.RESIZABLE | pygame.SRCALPHA, 32)
        self.player = Player([self.displaysurf.get_width()/2, self.displaysurf.get_height()/2], 0)
        self.clock = pygame.time.Clock()
        self.playing = False
        self.difficulty = settings.DIFFICULTY
        self.enemies = []
        self.enemies2 = []
        self.score = [0, 1]
        self.score2 = [0, 1]
        self.meter = 0
        self.menu = False
        self.currentOption = None
        self.font = pygame.font.Font(os.path.join("assets", "fonts", "Roboto-Thin.ttf"), 32)
        self.title = pygame.font.Font(os.path.join("assets", "fonts", "Roboto-Thin.ttf"), 72)

    def spawn(self, type):
        x = random.randint(0, self.displaysurf.get_width())
        y = random.randint(0, self.displaysurf.get_height())
        while True:
            valid = False
            enemyv = False
            for i in self.enemies:
                if i.rect.collidepoint(x, y):
                    enemyv = True
            if not self.player.rect.collidepoint(x, y) and not enemyv:
                valid = True
            if valid:
                break
            else:
                x = random.randint(0, self.displaysurf.get_width())
                y = random.randint(0, self.displaysurf.get_height())
        if type == "c":
            self.enemies.append(Circle([x, y]))
            settings.sounds["CIRCLE"].play()
        elif type == "s":
            self.enemies.append(Square([x, y], 60, 60))
            settings.sounds["SQUARE"].play()
        elif type == 't':
            self.enemies.append(Triangle([x, y], 0))
            settings.sounds["TRIANGLE"].play()
        for i in self.enemies:
            if i.health > 0:
                self.enemies2.append(i)
        self.enemies = copy.deepcopy(self.enemies2)
        self.enemies2 = []

    def set(self, inc):
        if self.currentOption == 0:
            settings.NEON = not settings.NEON
        elif self.currentOption == 1:
            if inc:
                settings.DIFFICULTY += 1
                self.difficulty = settings.DIFFICULTY
                if self.playing:
                    self.playing = False
                    self.menu = False
                    self.enemies = []
                    self.player.bullets = []
                    self.player.angle = 0
                    self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
            else:
                if settings.DIFFICULTY > 0:
                    settings.DIFFICULTY -= 1
                    self.difficulty = settings.DIFFICULTY
                    if self.playing:
                        self.playing = False
                        self.menu = False
                        self.enemies = []
                        self.player.bullets = []
                        self.player.angle = 0
                        self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
        elif self.currentOption == 2:
            if inc:
                if settings.VOLUME < 1.0:
                    settings.VOLUME += 0.1
            else:
                if settings.VOLUME > 0:
                    settings.VOLUME -= 0.1
        elif self.currentOption == 3:
            if inc:
                settings.FPS += 1
            elif settings.FPS > 30:
                settings.FPS -= 1

        elif self.currentOption == 4:
            if self.playing:
                self.playing = False
                self.menu = False
                self.enemies = []
                self.player.bullets = []
                self.player.angle = 0
                self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
            else:
                settings.saveSettings()
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.displaysurf.fill((0, 0, 0))
            for i in pygame.event.get():
                if i.type == QUIT:
                    settings.saveSettings()
                    pygame.quit()
                    sys.exit()
                elif i.type == KEYDOWN and i.key == K_SPACE and not self.playing and not self.menu:
                    settings.sounds["OPEN"].play()
                    self.playing = True
                    self.player.angle = 0
                    self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
                    self.enemies = []
                    for i in range(0, self.difficulty):
                        self.spawn("c")
                    for i in range(0, self.difficulty + 1):
                        self.spawn("s")
                    for i in range(0, self.difficulty + 2):
                        self.spawn("t")
                elif i.type == KEYDOWN and i.key == K_ESCAPE:
                    self.menu = not self.menu
                    self.currentOption = 0
                    settings.sounds["OPEN"].play()
                elif self.menu and i.type == KEYDOWN:
                    if i.key == K_UP or i.key == K_w:
                        if self.currentOption > 0:
                            self.currentOption -= 1
                            settings.sounds["SETTINGS"].play()
                    elif i.key == K_DOWN or i.key == K_s:
                        if self.currentOption < 4:
                            self.currentOption += 1
                            settings.sounds["SETTINGS"].play()
                    elif i.key == K_LEFT:
                        self.set(False)
                        settings.sounds["SETTING_CHANGE"].play()
                    elif i.key == K_RIGHT:
                        self.set(True)
                        settings.sounds["SETTING_CHANGE"].play()
            self.player.draw(self.enemies)
            if not self.menu:
                self.player.update()
            if self.player.health == 0:
                settings.sounds["DEATH"].play()
                self.playing = False
                self.player.evil = True
                self.player.color = [8, 1, 1]
                self.menu = False
                self.player.angle = 0
                self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
                self.player.bullets = []
                self.player.health = 5
                self.player.score[0] = 0
                if self.score[0] > settings.HIGHSCORE:
                    settings.HIGHSCORE = self.score[0]
                self.score[0] = 0
            self.player.draw(self.enemies)
            if self.playing:
                for enemy in self.enemies:
                    enemy.draw()
                    if not self.menu:
                        if enemy.type == 'c':
                            enemy.update(self.player.bullets, self.player.score)
                        elif enemy.type == 's':
                            enemy.update(self.player.bullets, self.player.score, self.player.pos)
                        elif enemy.type == 't':
                            enemy.update(self.player.bullets, self.player.score, self.player.pos)
                if self.player.score[0] > self.score2[0]:
                    self.score[0] += self.player.score[0]-self.score2[0]
                    self.score2[0] = self.player.score[0]
                elif self.player.score[0] < self.score2[0]:
                    self.score2[0] = self.player.score[0]
                if self.meter < self.score2[0]:
                    self.meter += 1
                elif self.meter > self.score2[0]:
                    self.meter -= 1
                for i in settings.spawn:
                    self.spawn(i)
                settings.spawn = []
                if settings.NEON:
                    c = 1
                    for t in range(10, 5, -2):
                        pygame.draw.rect(self.displaysurf, (8*c, 15*c, 8*c), (
                            0, self.displaysurf.get_height() - t, self.meter / 50 * self.displaysurf.get_width(), t), border_radius=t)
                        c += 1
                pygame.draw.rect(self.displaysurf, (200, 235, 200), (
                0, self.displaysurf.get_height() - 5, self.meter / 50 * self.displaysurf.get_width(), 5))

                render = self.font.render(str(self.player.health), True, (255, 220, 220))
                self.displaysurf.blit(render, (5, self.displaysurf.get_height()-render.get_height()-5))

                render = self.font.render(str(self.score[0]), True, (220, 220, 255))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, 5))
            else:
                render = self.title.render("enTWINed", True, (200, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, 150))

                render = self.font.render("[press space to start]", True, (200, 200, 255))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, self.displaysurf.get_height() - render.get_height() - 50))

                render = self.font.render("highscore: "+str(settings.HIGHSCORE), True, (200, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, self.displaysurf.get_height() - render.get_height() - 5))

                self.player.pos = [self.displaysurf.get_width() / 2, self.displaysurf.get_height() / 2]
            if self.menu:
                s = pygame.Surface((self.displaysurf.get_width(), self.displaysurf.get_height()))
                pygame.draw.rect(s, (0, 0, 0), (0, 0, self.displaysurf.get_width(), self.displaysurf.get_height()))
                s.set_alpha(220)
                self.displaysurf.blit(s, (0, 0))
                render = self.title.render("settings", True, (220, 220, 255))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, 100))
                if self.currentOption == 0:
                    render = self.font.render("neon: "+str(settings.NEON), True, (255, 255, 255))
                else:
                    render = self.font.render("neon: " + str(settings.NEON), True, (255, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width()/2-render.get_width()/2, 200))
                if self.currentOption == 1:
                    render = self.font.render("difficulty: " + str(settings.DIFFICULTY), True, (255, 255, 255))
                else:
                    render = self.font.render("difficulty: " + str(settings.DIFFICULTY), True, (255, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width() / 2 - render.get_width() / 2, 250))
                if self.currentOption == 2:
                    render = self.font.render("volume: " + str(settings.VOLUME), True, (255, 255, 255))
                else:
                    render = self.font.render("volume: " + str(settings.VOLUME), True, (255, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width() / 2 - render.get_width() / 2, 300))
                if self.currentOption == 3:
                    render = self.font.render("fps: " + str(settings.FPS), True, (255, 255, 255))
                else:
                    render = self.font.render("fps: " + str(settings.FPS), True, (255, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width() / 2 - render.get_width() / 2, 350))
                if self.currentOption == 4:
                    render = self.font.render("quit", True, (255, 255, 255))
                else:
                    render = self.font.render("quit", True, (255, 200, 200))
                self.displaysurf.blit(render, (self.displaysurf.get_width() / 2 - render.get_width() / 2, 400))
            pygame.display.update()
            self.clock.tick(settings.FPS)
