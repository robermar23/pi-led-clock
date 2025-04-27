import random
import pygame
class Star:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.brightness = 255
        self.twinkle_direction = random.choice([-1, 1])

    def update(self):
        # Optional twinkle effect
        delta = random.randint(0, 3) * self.twinkle_direction
        self.brightness += delta
        if self.brightness > 255:
            self.brightness = 255
            self.twinkle_direction *= -1
        elif self.brightness < 180:
            self.brightness = 180
            self.twinkle_direction *= -1

    def draw(self, surface):
        c = tuple(min(255, max(0, int(channel * (self.brightness / 255)))) for channel in self.color)
        pygame.draw.circle(surface, c, (self.x, self.y), self.radius)
