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


# traffic car
class TrafficCar:
    def __init__(self, lane, y, color=None):
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = float(y)

        self.width = 60
        self.height = 100

        self.color = color or random.choice([
            RED,
            ORANGE,
            PURPLE,
            (40, 210, 150)
        ])

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def update(self, speed):
        self.y += speed

    def draw(self):
        r = self.rect

        # glow
        pygame.draw.rect(
            screen,
            (65, 20, 35),
            r.inflate(24, 24),
            border_radius=18
        )

        # body
        pygame.draw.rect(
            screen,
            self.color,
            r,
            border_radius=15
        )

        # outline
        pygame.draw.rect(
            screen,
            WHITE,
            r,
            2,
            border_radius=15
        )

        # windows
        window = pygame.Rect(
            r.x + 9,
            r.y + 14,
            r.width - 18,
            35
        )

        pygame.draw.rect(
            screen,
            (15, 25, 35),
            window,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            GRAY,
            window,
            2,
            border_radius=8
        )

        # rear lights
        pygame.draw.rect(
            screen,
            RED,
            (r.x + 8, r.bottom - 18, 13, 7),
            border_radius=3
        )

        pygame.draw.rect(
            screen,
            RED,
            (r.right - 21, r.bottom - 18, 13, 7),
            border_radius=3
        )
        
        

# boost pad
class BoostPad:
    def __init__(self, lane, y):
        self.lane = lane
        self.x = ROAD_LEFT + lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = float(y)
        self.width = 105
        self.height = 50

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height
        )

    def update(self, speed):
        self.y += speed

    def draw(self):
        r = self.rect

        pygame.draw.rect(
            screen,
            (85, 70, 15),
            r,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            YELLOW,
            r,
            3,
            border_radius=8
        )

        # arrows
        for offset in (-28, 0, 28):
            pygame.draw.polygon(
                screen,
                YELLOW,
                [
                    (self.x + offset - 10, self.y + 9),
                    (self.x + offset, self.y - 10),
                    (self.x + offset + 10, self.y + 9)
                ]
            )


# road drawing

road_offset = 0


def draw_road():
    global road_offset

    screen.fill(BLACK)

    # background
    pygame.draw.rect(
        screen,
        ROAD_DARK,
        (ROAD_LEFT - 45, 0, ROAD_WIDTH + 90, HEIGHT)
    )

    # road
    pygame.draw.rect(
        screen,
        ROAD,
        (ROAD_LEFT, 0, ROAD_WIDTH, HEIGHT)
    )

    # neon road edges
    pygame.draw.line(
        screen,
        CYAN,
        (ROAD_LEFT, 0),
        (ROAD_LEFT, HEIGHT),
        5
    )

    pygame.draw.line(
        screen,
        CYAN,
        (ROAD_LEFT + ROAD_WIDTH, 0),
        (ROAD_LEFT + ROAD_WIDTH, HEIGHT),
        5
    )

    # yellow outer lights
    for y in range(-50, HEIGHT + 50, 55):
        yy = (y + int(road_offset * 1.5)) % (HEIGHT + 55) - 55

        pygame.draw.rect(
            screen,
            YELLOW,
            (ROAD_LEFT - 30, yy, 8, 30),
            border_radius=4
        )

        pygame.draw.rect(
            screen,
            YELLOW,
            (ROAD_LEFT + ROAD_WIDTH + 22, yy, 8, 30),
            border_radius=4
        )

    # lane markings
    for lane in range(1, LANES):
        x = ROAD_LEFT + lane * LANE_WIDTH

        for y in range(-80, HEIGHT + 80, 80):
            yy = (y + int(road_offset)) % (HEIGHT + 80) - 80

            pygame.draw.rect(
                screen,
                WHITE,
                (x - 3, yy, 6, 42),
                border_radius=3
            )

    # side details
    for y in range(-40, HEIGHT + 40, 65):
        yy = (y + int(road_offset * 0.7)) % (HEIGHT + 65) - 65

        pygame.draw.circle(
            screen,
            BLUE,
            (ROAD_LEFT - 18, yy),
            4
        )

        pygame.draw.circle(
            screen,
            BLUE,
            (ROAD_LEFT + ROAD_WIDTH + 18, yy),
            4
        )


# HUD(heads up display)
def draw_hud(score, speed, boost):
    score_text = FONT.render(
        f"SCORE: {score}",
        True,
        WHITE
    )

    speed_text = FONT.render(
        f"SPEED: {int(speed)}",
        True,
        CYAN
    )

    screen.blit(
        score_text,
        (25, 20)
    )

    screen.blit(
        speed_text,
        (
            WIDTH - speed_text.get_width() - 25,
            20
        )
    )

    if boost:
        boost_text = SMALL_FONT.render(
            "BOOST!",
            True,
            YELLOW
        )

        screen.blit(
            boost_text,
            (
                WIDTH // 2 - boost_text.get_width() // 2,
                HEIGHT - 42
            )
        )


# game over screen
def draw_game_over(score):
    overlay = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA
    )

    overlay.fill((0, 0, 0, 185))
    screen.blit(overlay, (0, 0))

    title = BIG_FONT.render(
        "CRASHED!",
        True,
        RED
    )

    score_text = FONT.render(
        f"Final score: {score}",
        True,
        WHITE
    )

    restart_text = SMALL_FONT.render(
        "Press R to race again  •  ESC to quit",
        True,
        WHITE
    )

    screen.blit(
        title,
        title.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 - 70)
        )
    )

    screen.blit(
        score_text,
        score_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2)
        )
    )

    screen.blit(
        restart_text,
        restart_text.get_rect(
            center=(WIDTH // 2, HEIGHT // 2 + 55)
        )
    )



# reset
def reset_game():
    player = Player()

    traffic = []
    boost_pads = []

    score = 0
    distance_score = 0

    speed = BASE_SPEED

    spawn_timer = 0
    boost_timer = 0

    game_over = False

    return (
        player,
        traffic,
        boost_pads,
        score,
        distance_score,
        speed,
        spawn_timer,
        boost_timer,
        game_over
    )


# spawn traffic
def spawn_traffic(traffic):
    # pick a lane that is not occupied near the top.
    possible_lanes = list(range(LANES))
    random.shuffle(possible_lanes)

    for lane in possible_lanes:
        blocked = any(
            car.lane == lane and car.y < 180
            for car in traffic
        )

        if not blocked:
            traffic.append(
                TrafficCar(
                    lane,
                    -120
                )
            )
            return


# spawn boost
def spawn_boost(boost_pads):
    lane = random.randrange(LANES)

    boost_pads.append(
        BoostPad(
            lane,
            -150
        )
    )

