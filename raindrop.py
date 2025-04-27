import pygame
import random
class Raindrop:
    def __init__(self, x, y, length, speed):
        self.x = x
        self.y = y
        self.length = length
        self.speed = speed
        self.color = (180, 180, 255, 100)  # soft blue with transparency

    def update(self, height):
        self.y += self.speed
        if self.y > height:
            self.y = random.randint(-50, -10)  # restart above screen

    def draw(self, surface):
        end_y = self.y + self.length
        pygame.draw.line(surface, self.color, (self.x, self.y), (self.x, end_y))
