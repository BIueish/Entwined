import pygame, settings


class Square:
    def __init__(self, pos, w, h):
        self.pos = pos
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.pos[0]-2, self.pos[1]-2, w+4, h+4)
        self.type = 's'
        self.health = 5
        self.dir = 0

    def die(self, score):
        score[0] += 15
        settings.spawn.append("s")

    def draw(self):
        if self.health > 0:
            if settings.NEON:
                c = 1
                for i in range(20, 2, -2):
                    pygame.draw.rect(pygame.display.get_surface(), (2*c, 5*c, 8*c), (self.pos[0]-i/2, self.pos[1]-i/2, self.w+i, self.h+i), i)
                    c += 1
            pygame.draw.rect(pygame.display.get_surface(), (255, 255, 255), (self.pos[0], self.pos[1], self.w, self.h), 2)

            if self.dir == 0:
                pygame.draw.rect(pygame.display.get_surface(), (100, 160, 230), (self.pos[0]+self.w+10, self.pos[1], 1, self.h), 3)
            elif self.dir == 1:
                pygame.draw.rect(pygame.display.get_surface(), (100, 160, 230),
                                 (self.pos[0], self.pos[1]+self.h+10, self.w, 1), 3)
            elif self.dir == 2:
                pygame.draw.rect(pygame.display.get_surface(), (100, 160, 230),
                                 (self.pos[0] - 10, self.pos[1], 1, self.h), 3)
            elif self.dir == 3:
                pygame.draw.rect(pygame.display.get_surface(), (100, 160, 230),
                                 (self.pos[0], self.pos[1]-10, self.w, 1), 3)

    def update(self, bullets, score, ppos):
        if self.health > 0:
            if ppos[0] < self.pos[0]:
                self.dir = 2
            elif ppos[0] > self.pos[0]+self.w:
                self.dir = 0
            elif ppos[1] < self.pos[1]:
                self.dir = 3
            elif ppos[1] > self.pos[1]+self.h:
                self.dir = 1
            for i in range(0, len(bullets)):
                if bullets[i] is None:
                    continue
                pos = bullets[i][4]
                blocked = False
                if self.dir == 0:
                    if pygame.Rect((self.pos[0] + self.w + 5, self.pos[1], 10, self.h)).collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                        blocked = True
                elif self.dir == 1:
                    if pygame.Rect((self.pos[0], self.pos[1] + self.h + 5, self.w, 10)).collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                        blocked = True
                elif self.dir == 2:
                    if pygame.Rect((self.pos[0] - 5, self.pos[1], 10, self.h)).collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                        blocked = True
                elif self.dir == 3:
                    if pygame.Rect((self.pos[0], self.pos[1] - 5, self.w, 10)).collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                        blocked = True
                if not blocked:
                    if self.rect.collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                        self.health -= 1
                        pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0),
                                         (self.pos[0], self.pos[1], self.w, self.h), 2)
                        bullets[i] = None
                        if self.health == 0:
                            score[0] += 15
                            settings.spawn.append("s")
                else:
                    bullets[i] = None
