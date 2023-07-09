import random
import pygame
import time

pygame.init()

WIDTH, HEIGHT = 800, 600

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT + 1

TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
TEXT_COLOR = (255, 255, 255)
COLOR = (255, 0, 0)  # red color

class Target:
    MAX_SIZE = 50  # max font size
    MIN_SIZE = 20  # starting font size (set to desired normal size)
    GROWTH_RATE = 1  # speed of growth
    FALL_RATE = 2  # speed of falling

    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char
        self.size = self.MIN_SIZE
        self.alpha = 255

    def update(self):
        # Target falls down
        self.y += self.FALL_RATE

        # Target grows in size
        if self.size + self.GROWTH_RATE < self.MAX_SIZE:
            self.size += self.GROWTH_RATE

        # Calculate the transparency based on y-coordinate
        self.alpha = max(0, 255 - ((self.y / HEIGHT) * 255))

    def draw(self, win):
        font = pygame.font.Font(None, int(self.size))  # Create a font of current size
        text_surface = font.render(self.char, True, COLOR).convert_alpha()
        text_surface.fill((255, 255, 255, self.alpha), special_flags=pygame.BLEND_RGBA_MULT)
        win.blit(text_surface, (self.x, self.y))
        return text_surface.get_height()

def draw(win, targets, score, misses, start_time):
    win.fill(BG_COLOR)

    for target in list(targets):  # Create a copy for iteration
        text_height = target.draw(win)
        if target.y + text_height > HEIGHT:  # If target goes beyond the screen height
            targets.remove(target)

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
        clock.tick(60)  # set FPS to 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                char = random.choice(chars)
                target = Target(x, 0, char)
                targets.append(target)

            if event.type == pygame.KEYDOWN:
                if event.unicode.upper() in [t.char for t in targets]:
                    for target in list(targets):  # Create a copy for iteration
                        if target.char == event.unicode.upper():
                            targets.remove(target)
                            score += 1
                            break
                else:
                    misses += 1

        for target in targets:
            target.update()

        draw(WIN, targets, score, misses, start_time)

    pygame.quit()

if __name__ == "__main__":
    main()
