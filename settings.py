import os, pygame

FPS = 60
DIFFICULTY = 1
NEON = True
VOLUME = 1
HIGHSCORE = 0

sounds = {}
sounds["SETTING_CHANGE"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "change.wav"))
sounds["SETTINGS"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "setting.wav"))
sounds["OPEN"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "open.wav"))
sounds["START"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "start.wav"))
sounds["DEATH"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "death.wav"))
sounds["TRIANGLE"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "triangle.wav"))
sounds["SQUARE"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "square.wav"))
sounds["CIRCLE"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "circle.wav"))
sounds["LASER"] = pygame.mixer.Sound(os.path.join("assets", "sounds", "laser.mp3"))
sounds["SETTINGS"].set_volume(VOLUME/10)
sounds["SETTING_CHANGE"].set_volume(VOLUME/10)
sounds["OPEN"].set_volume(VOLUME/10)
sounds["DEATH"].set_volume(VOLUME/10)
sounds["TRIANGLE"].set_volume(VOLUME/10)
sounds["SQUARE"].set_volume(VOLUME/10)
sounds["CIRCLE"].set_volume(VOLUME/10)
sounds["LASER"].set_volume(0)


def loadSettings():
    global FPS, DIFFICULTY, NEON, VOLUME, HIGHSCORE
    file = open(os.path.join("assets", "config"), "r")
    lines = file.readlines()
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip('\n')
    FPS = int(lines[0])
    DIFFICULTY = int(lines[1])
    if lines[2] == "False":
        NEON = False
    else:
        NEON = True
    VOLUME = int(lines[3])
    HIGHSCORE = int(lines[4])
    file.close()


def saveSettings():
    global FPS, DIFFICULTY, NEON, VOLUME, HIGHSCORE
    file = open(os.path.join("assets", "config"), "w")
    lines = [str(FPS) + '\n', str(DIFFICULTY) + '\n', str(NEON) + '\n', str(VOLUME) + '\n', str(HIGHSCORE)+'\n']
    file.writelines(lines)
    file.close()
