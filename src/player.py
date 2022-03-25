import pygame, math, copy, time, settings
from pygame.locals import *


class Player:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.bullets = []
        self.delete = []
        self.health = 5
        self.score = [0, 3, 1]
        self.color = [8, 1, 1]
        self.evil = True
        self.switcht = 0
        self.shoott = 0
        self.time = time.time()
        self.rect = pygame.Rect(self.pos[0]-35, self.pos[1]-35, 70, 70)
        self.bullets2 = []

    def distance(self, x, y, x1, y1):
        return math.sqrt((abs(x1-x)**2)+(abs(y1-y)**2))

    def draw(self, enemies):
        x1 = math.cos(math.radians(self.angle))*40
        y1 = math.sin(math.radians(self.angle))*40
        x2 = math.cos(math.radians(self.angle-120))*40
        y2 = math.sin(math.radians(self.angle-120))*40
        x3 = math.cos(math.radians(self.angle+120))*40
        y3 = math.sin(math.radians(self.angle+120))*40
        if settings.NEON:
            c = 1
            for i in range(20, 2, -2):
                pygame.draw.line(pygame.display.get_surface(), (self.color[0]*c, self.color[1]*c, c), (x1+self.pos[0], y1+self.pos[1]), (x2+self.pos[0], y2+self.pos[1]), i)
                pygame.draw.line(pygame.display.get_surface(), (self.color[0]*c, self.color[1]*c, c), (x2+self.pos[0], y2+self.pos[1]), (x3+self.pos[0], y3+self.pos[1]), i)
                pygame.draw.line(pygame.display.get_surface(), (self.color[0]*c, self.color[1]*c, c), (x3+self.pos[0], y3+self.pos[1]), (x1+self.pos[0], y1+self.pos[1]), i)
                c += 1

        pygame.draw.circle(pygame.display.get_surface(), (225, 255, 225), (x1+self.pos[0], y1+self.pos[1]), 3)

        pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x1 + self.pos[0], y1 + self.pos[1]),(x2 + self.pos[0], y2 + self.pos[1]), 2)
        pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x2 + self.pos[0], y2 + self.pos[1]),(x3 + self.pos[0], y3 + self.pos[1]), 2)
        pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x3 + self.pos[0], y3 + self.pos[1]),(x1 + self.pos[0], y1 + self.pos[1]), 2)

        if not self.evil:
            pygame.draw.line(pygame.display.get_surface(), (200, 255, 200),
                             (self.pos[0]+x2+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y2+math.sin(math.radians(self.angle+180))*10),
                             (self.pos[0]+x3+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y3+math.sin(math.radians(self.angle+180))*10), 2)

        for i in range(0, len(self.bullets)):
            if self.bullets[i] is None:
                continue
            pos = self.bullets[i][4]
            if settings.NEON:
                c = 1
                for t in range(20, 5, -1):
                    pygame.draw.line(pygame.display.get_surface(), (4 * c, 4 * c, 8 * c),
                                     (self.bullets[i][0] + pos[0], self.bullets[i][1] + pos[1]),
                                     (self.bullets[i][0] + self.bullets[i][2] * 10 + pos[0],
                                      self.bullets[i][1] + self.bullets[i][3] * 10 + pos[1]), t)
                    c += 1
            pygame.draw.line(pygame.display.get_surface(), (200, 200, 255),
                             (self.bullets[i][0] + pos[0], self.bullets[i][1] + pos[1]),
                             (self.bullets[i][0] + self.bullets[i][2] * 10 + pos[0],
                              self.bullets[i][1] + self.bullets[i][3] * 10 + pos[1]), 3)

            self.bullets[i][0] += self.bullets[i][2] * 10
            self.bullets[i][1] += self.bullets[i][3] * 10
            if not pygame.Rect(0, 0, pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height()).collidepoint(self.bullets[i][0]+pos[0], self.bullets[i][1]+pos[1]):
                self.bullets[i] = None

        for enemy in enemies:
            if enemy.health == 0:
                continue
            if self.evil and enemy.rect.collidepoint(x1+self.pos[0], y1+self.pos[1]) or\
                    enemy.rect.collidepoint(x2+self.pos[0], y2+self.pos[1]) or\
                    enemy.rect.collidepoint(x3+self.pos[0], y3+self.pos[1]):
                    self.health -= 1
                    enemy.health = 0
                    settings.spawn.append(enemy.type)
            elif not self.evil and enemy.rect.collidepoint(x1+self.pos[0], y1+self.pos[1]):
                enemy.health = 0
                enemy.die(self.score)

            if enemy.type == "t":
                for i in range(0, len(enemy.bullets)):
                    if enemy.bullets[i] is None:
                        continue
                    pos = enemy.bullets[i][4]
                    if not self.evil:
                        buffer = 5
                        ld = self.distance(self.pos[0]+x2+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y2+math.sin(math.radians(self.angle+180))*10, self.pos[0]+x3+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y3+math.sin(math.radians(self.angle+180))*10)
                        pd1 = self.distance(pos[0]+enemy.bullets[i][0], pos[1]+enemy.bullets[i][1], self.pos[0]+x3+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y3+math.sin(math.radians(self.angle+180))*10)
                        pd2 = self.distance(pos[0]+enemy.bullets[i][0], pos[1]+enemy.bullets[i][1], self.pos[0]+x2+math.cos(math.radians(self.angle+180))*10, self.pos[1]+y2+math.sin(math.radians(self.angle+180))*10)
                        if ld-buffer <= pd1+pd2 <= ld+buffer:
                            enemy.bullets[i] = None
                            continue
                    if self.rect.collidepoint(enemy.bullets[i][0]+pos[0], enemy.bullets[i][1]+pos[1]):
                        self.health -= 1
                        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), self.rect)
                        enemy.bullets[i] = None

    def update(self):
        self.rect = pygame.Rect(self.pos[0]-35, self.pos[1]-35, 70, 70)
        for i in self.bullets:
            if i is not None:
                self.bullets2.append(i)
        self.bullets = self.bullets2
        self.bullets2 = []
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_a]:
            self.angle -= 3
        if keys[K_RIGHT] or keys[K_d]:
            self.angle += 3
        if keys[K_UP] or keys[K_w]:
            if 10 < self.pos[0]+math.cos(math.radians(self.angle))*5 < pygame.display.get_surface().get_width()-10 and\
                    10 < self.pos[1]+math.sin(math.radians(self.angle))*5 < pygame.display.get_surface().get_height()-10:
                self.pos[0] += math.cos(math.radians(self.angle))*5
                self.pos[1] += math.sin(math.radians(self.angle))*5
        if keys[K_DOWN] or keys[K_s]:
            if 10 < self.pos[0]-math.cos(math.radians(self.angle))*5 < pygame.display.get_surface().get_width()-10 and\
                    10 < self.pos[1]-math.sin(math.radians(self.angle))*5 < pygame.display.get_surface().get_height()-10:
                self.pos[0] -= math.cos(math.radians(self.angle)) * 5
                self.pos[1] -= math.sin(math.radians(self.angle)) * 5
        if self.evil and (keys[K_SPACE] or pygame.mouse.get_pressed()[0]) and self.shoott == 0:
            self.shoot()
            self.shoott = 5
            settings.sounds["LASER"].play()
        else:
            settings.sounds["LASER"].stop()
        if self.score[0] >= 50 and (keys[K_RETURN] or pygame.mouse.get_pressed()[2]) and self.switcht == 0:
            self.score[0] -= 50
            self.evil = not self.evil
            if self.color == [1, 8, 1]:
                self.color = [8, 1, 1]
            else:
                self.color = [1, 8, 1]
            self.switcht = 100
        if self.switcht > 0:
            self.switcht -= 1
        if self.shoott > 0:
            self.shoott -= 1
        if self.health < 5 and not self.evil:
            if time.time()-self.time>5:
                self.health += 1
                self.time = time.time()

    def shoot(self):
        self.bullets.append([math.cos(math.radians(self.angle))*40, math.sin(math.radians(self.angle))*40, math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)), copy.deepcopy(self.pos)])
