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
