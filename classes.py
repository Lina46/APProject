import pygame
from pygame.locals import *


class Ball:
    def __init__(self, surface, x, y, r = 10, color = (255, 255, 255)):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.r = r
        self.color = color
        self.screen = surface
        self.friction = 0.01

    def move(self):
        if self.vel.magnitude() < 0.1:
            self.vel.xy = (0, 0)
        else:
            fricVec = self.vel.normalize() * - self.friction
            self.vel += fricVec
            self.pos += self.vel

    def draw(self):
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(self.screen, self.color, (x,y), self.r)

    def accelerate(self, a):
        self.vel += a
        if self.vel.magnitude() > self.r:
            self.vel.scale_to_length(self.r)
        
    def bounce(self, walls):
        for wall in walls:
            x, y = self.pos.xy
            left, top, right, bottom = wall.rect.topleft + wall.rect.bottomright
            centerx, centery = wall.rect.center

            if wall.orientation == "vertical":
                # left wall
                if y > top and y < bottom and x < centerx and x + self.r >= left:
                    self.pos.x = left - self.r
                    self.vel.x *= -1

                # right wall
                elif y > top and y < bottom and x > centerx and x - self.r <= right:
                    self.pos.x = right + self.r
                    self.vel.x *= -1

            elif wall.orientation == "horizontal":
                # top wall
                if x > left and x < right and y < centery and y + self.r >= top:
                    self.pos.y = top - self.r
                    self.vel.y *= -1

                # bottom wall
                elif x > left and x < right and y > centery and y - self.r <= bottom:
                    self.pos.y = bottom + self.r
                    self.vel.y *= -1

class Wall:
    def __init__(self, surface, x, y, orientation, length, thick=10, color=(255, 100, 0)):
        if orientation == "vertical":
            width = thick
            height = length
        elif orientation == "horizontal":
            width = length
            height = thick
        self.rect = Rect(x, y, width, height)
        self.orientation = orientation
        self.color = color
        self.screen = surface

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        
class Goal:
    def __init__(self, surface, x, y, r = 10, color = (0,0,0)):
        self.pos = pygame.math.Vector2(x,y)
        self.r = r
        self.color = color
        self.screen = surface
    
    def draw(self):
        x = int(self.pos.x)
        y = int(self.pos.y)
        pygame.draw.circle(self.screen, self.color, (x,y), self.r)
        
    def hit(self,ball):
        #has to return True if the ball is touching the target
        #Roy: But now, I tried to do it in an if-statement in the game code
        #Roy: However, this doesn't work very well
        return
        
class scoreSheet():
    def __init__(self):
        self.finalScore = None
        self.strokes = []
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.width = 250
        self.height = 510
        self.font = pygame.font.Font('arial', 22)
        self.bigFont = pygame.font.Font('arial', 30)

    def getScore(self):
        return self.strokes

    def getStrokes(self):
        return sum(self.strokes)

    def drawSheet(self, score=0):
        self.strokes.append(score)
        grey = (220, 220, 220)

        text = self.bigFont.render('Score: ' + str(sum(self.strokes)), 1, grey)
        blit(text, (800, 330))

        startx = self.screenWidth / 2 - self.width / 2
        starty = self.screenHeight / 2 - self.height / 2
        pygame.draw.rect(grey, (startx, starty, self.width, self.height))
        for i in range(1,4):
            pygame.draw.line((0,0,0), (startx + (i * (self.width/3)), starty), (startx + (i * (self.width/3)), starty + self.height), 2)
        for i in range(1, 11):
            if i == 1:
                columnLevel = self.font.render('Level', 2, (0,0,0))
                blit(columnLevel, (startx + 40, starty + 10))
                columnScore = self.font.render('Score', 2, (0,0,0))
                blit(columnScore, (startx + 295, starty + 10))
            else:
                blit = self.font.render(str(i - 1), 1, (128,128,128))
                blit(blit, (startx + 56, starty + 10 + ((i - 1) * (self.height/10))), (0,0,0))
                try:
                    blit = self.font.render(str(self.strokes[i - 2]), 1, grey)
                    blit(blit, ((startx + 60 + 266, starty + 10 + ((i - 1) * (self.height/10)))))
                except:
                    blit = self.font.render('-', 1, (128,128,128))
                    blit(blit, (startx + 62 + 266, starty + 10 + ((i - 1) * (self.height/10))))
            pygame.draw.line((0,0,0), (startx, starty + (i * (self.height/10))), (startx + self.width, starty + (i * (self.height / 10))), 2)
