import pygame, math, copy, settings


class Triangle:
    def __init__(self, pos, angle):
        self.pos = pos
        self.angle = angle
        self.angle2 = self.angle
        self.rect = pygame.Rect(self.pos[0]-35, self.pos[1]-35, 70, 70)
        self.type = 't'
        self.health = 1
        self.bullets = []
        self.shoott = 100-settings.DIFFICULTY*10

    def shoot(self):
        self.bullets.append([math.cos(math.radians(self.angle))*40, math.sin(math.radians(self.angle))*40, math.cos(math.radians(self.angle)), math.sin(math.radians(self.angle)), copy.deepcopy(self.pos)])

    def die(self, score):
        score[0] += 20
        settings.spawn.append("t")

    def draw(self):
        if self.health > 0:
            x1 = math.cos(math.radians(self.angle)) * 40
            y1 = math.sin(math.radians(self.angle)) * 40
            x2 = math.cos(math.radians(self.angle - 120)) * 40 
            y2 = math.sin(math.radians(self.angle - 120)) * 40
            x3 = math.cos(math.radians(self.angle + 120)) * 40
            y3 = math.sin(math.radians(self.angle + 120)) * 40
            if settings.NEON:
                c = 1
                for i in range(16, 2, -2):
                    pygame.draw.line(pygame.display.get_surface(), (10*c, 10*c, 10*c),
                                     (x1 + self.pos[0], y1 + self.pos[1]), (x2 + self.pos[0], y2 + self.pos[1]), i)
                    pygame.draw.line(pygame.display.get_surface(), (10*c, 10*c, 10*c),
                                     (x2 + self.pos[0], y2 + self.pos[1]), (x3 + self.pos[0], y3 + self.pos[1]), i)
                    pygame.draw.line(pygame.display.get_surface(), (10*c, 10*c, 10*c),
                                     (x3 + self.pos[0], y3 + self.pos[1]), (x1 + self.pos[0], y1 + self.pos[1]), i)
                    c += 1

            pygame.draw.circle(pygame.display.get_surface(), (225, 255, 225), (x1 + self.pos[0], y1 + self.pos[1]), 3)

            pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x1 + self.pos[0], y1 + self.pos[1]),
                             (x2 + self.pos[0], y2 + self.pos[1]), 2)
            pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x2 + self.pos[0], y2 + self.pos[1]),
                             (x3 + self.pos[0], y3 + self.pos[1]), 2)
            pygame.draw.line(pygame.display.get_surface(), (255, 255, 255), (x3 + self.pos[0], y3 + self.pos[1]),
                             (x1 + self.pos[0], y1 + self.pos[1]), 2)

        for i in range(0, len(self.bullets)):
            if self.bullets[i] is None:
                continue
            pos = self.bullets[i][4]
            if settings.NEON:
                c = 1
                for t in range(20, 5, -1):
                    pygame.draw.line(pygame.display.get_surface(), (8 * c, 4 * c, 4 * c),
                                     (self.bullets[i][0] + pos[0], self.bullets[i][1] + pos[1]),
                                     (self.bullets[i][0] + self.bullets[i][2] * 10 + pos[0],
                                      self.bullets[i][1] + self.bullets[i][3] * 10 + pos[1]), t)
                    c += 1
            pygame.draw.line(pygame.display.get_surface(), (255, 200, 200),
                             (self.bullets[i][0] + pos[0], self.bullets[i][1] + pos[1]),
                             (self.bullets[i][0] + self.bullets[i][2] * 10 + pos[0],
                              self.bullets[i][1] + self.bullets[i][3] * 10 + pos[1]), 3)

            self.bullets[i][0] += self.bullets[i][2] * 5
            self.bullets[i][1] += self.bullets[i][3] * 5
            if not pygame.Rect(0, 0, pygame.display.get_surface().get_width(),
                               pygame.display.get_surface().get_height()).collidepoint(self.bullets[i][0] + pos[0],
                                                                                       self.bullets[i][1] + pos[1]):
                self.bullets[i] = None

    def update(self, bullets, score, ppos):
        if self.health > 0:
            if self.shoott > 0:
                self.shoott -= 1
            else:
                self.shoot()
                self.shoott = 75
            angle = int(math.degrees(math.atan2(abs(ppos[1]-self.pos[1]), abs(ppos[0]-self.pos[0]))))
            if ppos[0] > self.pos[0] and ppos[1] > self.pos[1]:
                self.angle2 = angle
            elif ppos[0] < self.pos[0] and ppos[1] > self.pos[1]:
                self.angle2 = angle+90
            elif ppos[0] < self.pos[0] and ppos[1] < self.pos[1]:
                self.angle2 = angle+180
            elif ppos[0] > self.pos[0] and ppos[1] < self.pos[1]:
                self.angle2 = angle-90
            for i in range(0, 6):
                if self.angle < self.angle2:
                    self.angle += 1
                elif self.angle > self.angle2:
                    self.angle -= 1
            for i in range(0, len(bullets)):
                if bullets[i] is None:
                    continue
                pos = bullets[i][4]
                if self.rect.collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                    self.health -= 1
                    pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), self.rect)
                    bullets[i] = None
                    if self.health == 0:
                        score[0] += 20
                        settings.spawn.append("t")
