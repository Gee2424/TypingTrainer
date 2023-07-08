import random
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)

COLOR = (255, 0, 0)  # red color

class Target:
    MAX_SIZE = 50  # max font size
    MIN_SIZE = 10  # min font size
    GROWTH_RATE = 1  # speed of growth/shrink

    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.size = self.MIN_SIZE
        self.grow = True

    def update(self):
        if self.grow and self.size + self.GROWTH_RATE > self.MAX_SIZE:
            self.grow = False
        elif not self.grow and self.size - self.GROWTH_RATE < self.MIN_SIZE:
            self.grow = True

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        font = pygame.font.Font(None, int(self.size))  # Create a font of current size
        text_surface = font.render(self.char, True, COLOR)
        win.blit(text_surface, (self.x, self.y))

def draw(win, targets):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    pygame.display.update()

def main():
    run = True
    targets = []
    clock = pygame.time.Clock()

    # Include all the characters that can appear on the screen
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:

        clock.tick(60)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING, HEIGHT - TARGET_PADDING)
                char = random.choice(chars)
                target = Target(x, y, char)
                targets.append(target)

        for target in targets:
            target.update()
            if target.size == target.MIN_SIZE and not target.grow:  # remove target if it has disappeared
                targets.remove(target)

        draw(WIN, targets)

    pygame.quit()

if __name__ == "__main__":
    main()
