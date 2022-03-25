import pygame, settings


class Circle:
    def __init__(self, pos):
        self.pos = pos
        self.health = 15
        self.rect = pygame.Rect(self.pos[0]-30, self.pos[1]-30, 60, 60)
        self.type = "c"

    def die(self, score):
        score[0] += 10
        settings.spawn.append("c")

    def draw(self):
        if self.health > 0:
            if settings.NEON:
                c = 1
                for i in range(20, 2, -2):
                    pygame.draw.circle(pygame.display.get_surface(), (10*c, 8*c, c), self.pos, 30+i/2, i)
                    c += 1
                pygame.draw.circle(pygame.display.get_surface(), (255, 200, 0), self.pos, 30, 2)

    def update(self, bullets, score):
        if self.health > 0:
            for i in range(0, len(bullets)):
                if bullets[i] is None:
                    continue
                pos = bullets[i][4]
                if self.rect.collidepoint(bullets[i][0]+pos[0], bullets[i][1]+pos[1]):
                    self.health -= 1
                    pygame.draw.circle(pygame.display.get_surface(), (0, 0, 0), self.pos, 30, 3)
                    bullets[i] = None
                    if self.health == 0:
                        score[0] += 10
                        settings.spawn.append("c")
