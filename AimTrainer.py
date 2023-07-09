import math
import random
import time
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
TEXT_COLOR = (255, 255, 255)  # white color

font = pygame.font.Font(None, 36)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = (255, 0, 0)  # red color
    SECOND_COLOR = (255, 255, 255)  # white color

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
        self.create_time = time.time()

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
            if self.size < 0:
                self.size = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def check_point(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2) <= self.size

def draw(win, targets, hits, misses, avg_response_time):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    stats_text = f'Hits: {hits} Misses: {misses} Average Response Time: {avg_response_time:.2f}s'
    text_surface = font.render(stats_text, True, TEXT_COLOR)
    win.blit(text_surface, (10, 10))

    pygame.display.update()

def main():
    run = True
    hits = 0
    misses = 0
    total_response_time = 0
    targets = []
    clock = pygame.time.Clock()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:
        clock.tick(60)
        avg_response_time = total_response_time / hits if hits else 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                hit = False
                for target in targets[:]:
                    if target.check_point(x, y):
                        hit_time = time.time() - target.create_time
                        total_response_time += hit_time
                        targets.remove(target)
                        hits += 1
                        hit = True
                        break

                if not hit:
                    misses += 1

        for target in targets:
            target.update()
            if target.size == 0:  # remove target if it has disappeared
                targets.remove(target)

        draw(WIN, targets, hits, misses, avg_response_time)

    pygame.quit()

if __name__ == "__main__":
    main()
