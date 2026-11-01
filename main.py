import pygame
import random

pygame.init()

# design the window

WIDTH = 900
HEIGHT = 700
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Racer")
clock = pygame.time.Clock()

# colors

BLACK = (5, 8, 15)
ROAD = (18, 22, 32)
ROAD_DARK = (10, 13, 22)
WHITE = (235, 245, 255)
CYAN = (30, 220, 255)
BLUE = (50, 110, 255)
RED = (255, 55, 75)
YELLOW = (255, 220, 70)
PURPLE = (190, 70, 255)
ORANGE = (255, 135, 40)
GRAY = (80, 95, 115)

# fonts 
FONT = pygame.font.SysFont("arial", 28, bold=True)
SMALL_FONT = pygame.font.SysFont("arial", 18, bold=True)
BIG_FONT = pygame.font.SysFont("arial", 56, bold=True)


# road settings

LANES = 3
ROAD_WIDTH = 600
ROAD_LEFT = (WIDTH - ROAD_WIDTH) // 2
LANE_WIDTH = ROAD_WIDTH // LANES

PLAYER_Y = HEIGHT - 135

BASE_SPEED = 6.0
BOOST_SPEED = 11.0


# build the player
class Player:
    def __init__(self):
        self.lane = 1
        self.x = self.lane_x()
        self.y = PLAYER_Y

        self.width = 62
        self.height = 105

        self.move_cooldown = 0
        self.boost = False

    def lane_x(self):
        return ROAD_LEFT + self.lane * LANE_WIDTH + LANE_WIDTH // 2

    def update(self):
        keys = pygame.key.get_pressed()

        if self.move_cooldown > 0:
            self.move_cooldown -= 1

        # lane switching
        # a cooldown prevents one key press from jumping through multiple lanes in a single second
        if self.move_cooldown == 0:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if self.lane > 0:
                    self.lane -= 1
                    self.move_cooldown = 10

            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if self.lane < LANES - 1:
                    self.lane += 1
                    self.move_cooldown = 10

        target_x = self.lane_x()

        # smooth movement between lanes
        self.x += (target_x - self.x) * 0.25

        self.boost = keys[pygame.K_SPACE]

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def draw(self):
        r = self.rect

        # neon glow
        glow = r.inflate(28, 28)
        pygame.draw.rect(
            screen,
            (15, 55, 90),
            glow,
            border_radius=18
        )

        # car body
        pygame.draw.rect(
            screen,
            BLUE,
            r,
            border_radius=16
        )

        pygame.draw.rect(
            screen,
            CYAN,
            r,
            3,
            border_radius=16
        )

        # windows
        window = pygame.Rect(
            r.x + 10,
            r.y + 16,
            r.width - 20,
            36
        )

        pygame.draw.rect(
            screen,
            (10, 25, 45),
            window,
            border_radius=9
        )

        pygame.draw.rect(
            screen,
            CYAN,
            window,
            2,
            border_radius=9
        )

        # hood
        hood = pygame.Rect(
            r.x + 13,
            r.y + 57,
            r.width - 26,
            28
        )

        pygame.draw.rect(
            screen,
            (30, 70, 145),
            hood,
            border_radius=7
        )

        # lights
        pygame.draw.rect(
            screen,
            WHITE,
            (r.x + 9, r.bottom - 19, 14, 7),
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            WHITE,
            (r.right - 23, r.bottom - 19, 14, 7),
            border_radius=3
        )

        # boost flames
        if self.boost:
            pygame.draw.polygon(
                screen,
                ORANGE,
                [
                    (r.centerx - 10, r.bottom),
                    (r.centerx, r.bottom + 32),
                    (r.centerx + 10, r.bottom)
                ]
            )

            pygame.draw.polygon(
                screen,
                YELLOW,
                [
                    (r.centerx - 5, r.bottom),
                    (r.centerx, r.bottom + 20),
                    (r.centerx + 5, r.bottom)
                ]
            )
