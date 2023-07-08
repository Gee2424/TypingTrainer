import random
import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
TEXT_COLOR = (255, 255, 255)
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

def draw(win, targets, score, misses, start_time):
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

    # Display the score
    font = pygame.font.Font(None, 30)  # Create a font for score display
    text_surface = font.render(f"Score: {score}  Misses: {misses}  Speed: {(score*60)/(time.time()-start_time):.2f} CPM", True, TEXT_COLOR)
    win.blit(text_surface, (10, 10))

    pygame.display.update()

def main():
    run = True
    targets = []
    score = 0
    misses = 0
    clock = pygame.time.Clock()


    # Include all the characters that can appear on the screen
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    start_time = time.time()

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

            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() in [t.char for t in targets]:
                    for target in targets:
                        if target.char == event.unicode.upper():
                            targets.remove(target)
                            score += 1
                            break
                else:
                    misses += 1

        for target in targets:
            target.update()
            if target.size == target.MIN_SIZE and not target.grow:  # remove target if it has disappeared
                targets.remove(target)
                misses += 1

        draw(WIN, targets, score, misses, start_time)

    pygame.quit()

if __name__ == "__main__":
    main()
