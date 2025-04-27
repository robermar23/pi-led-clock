import pygame

class Cloud:
    def __init__(self, x, y, w, h, alpha, speed_x=0.1):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.alpha = alpha
        self.speed_x = speed_x  # slow horizontal movement

    def update(self, width):
        self.x += self.speed_x
        if self.x > width:
            self.x = -self.w  # wrap around to left

    def draw(self, surface):
        color = (100, 100, 120, self.alpha)
        pygame.draw.ellipse(surface, color, (self.x, self.y, self.w, self.h))
