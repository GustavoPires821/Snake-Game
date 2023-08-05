import pygame
import sys
from pygame import Vector2
import random

pygame.init()

SCREEN_WIDTH: int = 600
SCREEN_HEIGHT: int = 600

SCREEN: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

TILE: int = 30


class Main:
    def __init__(self):
        self.snake = Snake()
        self.food = Food()
        self.interface = Interface()

        self.snake_speed = 200

        # [bg_color HEX, initial_snake_color RGB, last_snake_color RGB, food_color HEX, fail[init RGB, end RGB]
        self.color_list = ["#F6F4EB", (40, 112, 181), (129, 186, 240), "#28b64e", [(230, 44, 59), (237, 135, 143)]]

        self.backcolor = self.color_list[0]
        self.snake.init_color = self.color_list[1]
        self.snake.last_color = self.color_list[2]
        self.food.food_color = self.color_list[3]

    def draw_elements(self):
        SCREEN.fill(self.backcolor)
        self.food.draw()
        self.snake.draw()
        self.interface.draw()
        if not self.snake.enable_move:
            self.fail()

    def check_food(self):
        max_score = SCREEN_WIDTH * (SCREEN_HEIGHT - 120)
        max_score //= TILE ** 2

        if self.food.pos == self.snake.body[0]:
            self.snake.grow = True
            self.interface.score += 1

            while self.food.pos in self.snake.body and len(self.snake.body) < max_score:
                self.food.randomize()

    def check_collision(self):
        # checks for walls collision
        if not 0 <= self.snake.body[0].x < SCREEN_WIDTH or not 120 <= self.snake.body[0].y < SCREEN_HEIGHT:
            self.snake.enable_move = False

        # checks for the head collision with the body
        if self.snake.body[0] in self.snake.body[1:]:
            self.snake.enable_move = False

    def fail(self):
        self.interface.death_message()
        self.backcolor = self.interface.bg_color
        self.snake.init_color = self.color_list[4][0]
        self.snake.last_color = self.color_list[4][1]

    def update(self):
        self.check_collision()
        self.check_food()
        self.draw_elements()


class Snake:
    def __init__(self):
        self.body: list = [Vector2(300, 300 + (TILE * index)) for index in range(1, 4)]
        self.direction: Vector2 = Vector2(0, -TILE)
        self.grow: bool = False
        self.init_color: tuple = (145, 200, 228)
        self.last_color: tuple = (116, 155, 194)
        self.enable_move: bool = True

    def move(self):
        if self.enable_move:
            if self.grow:
                body_copy = self.body.copy()
                self.grow = False
            else:
                body_copy = self.body[:-1]

            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy

    def draw(self):
        # creates a list with color variation divided by the lenght of the body
        rgb_comp: list = [(self.last_color[index] - self.init_color[index])/len(self.body) for index in range(3)]

        for index, square in enumerate(self.body):
            # takes the color component times the index plus the inital color
            color: list = [self.init_color[rgb_value] + (rgb_comp[rgb_value] * index) for rgb_value in range(3)]
            snake_surf = pygame.Surface((TILE, TILE))
            snake_surf.fill(color)
            snake_rect = snake_surf.get_rect(topleft=(square.x, square.y))
            SCREEN.blit(snake_surf, snake_rect)


class Food:
    def __init__(self):
        self.pos_x: int = random.randint(0, (SCREEN_WIDTH // TILE) - 1)
        self.pos_y: int = random.randint(4, (SCREEN_HEIGHT // TILE) - 1)
        self.pos: Vector2 = Vector2(self.pos_x * TILE, self.pos_y * TILE)
        self.food_color = "#4682A9"

    def draw(self):
        food_surf = pygame.Surface((TILE, TILE))
        food_surf.fill(self.food_color)
        food_rect = food_surf.get_rect(topleft=self.pos)
        SCREEN.blit(food_surf, food_rect)

    def randomize(self):
        self.pos_x: int = random.randint(0, (SCREEN_WIDTH // TILE) - 1)
        self.pos_y: int = random.randint(4, (SCREEN_HEIGHT // TILE) - 1)
        self.pos: Vector2 = Vector2(self.pos_x * TILE, self.pos_y * TILE)


class Interface:
    def __init__(self):
        self.menu_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 120)
        self.bg_color = "#4682A9"
        self.fore_color = "#F6F4EB"
        self.font = pygame.font.Font(None, 100)
        self.score = 0

    def draw(self):
        pygame.draw.rect(SCREEN, self.bg_color, self.menu_rect)

        score_surf = self.font.render(f"Score: {self.score}", True, self.fore_color)
        score_rect = score_surf.get_rect(center=(300, 60))

        SCREEN.blit(score_surf, score_rect)

    def death_message(self):
        message_surf = self.font.render("press 'R' to reset", True, self.fore_color)
        message_rect = message_surf.get_rect(midtop=(300, 300))

        SCREEN.blit(message_surf, message_rect)


SNAKE_UPDATE = pygame.USEREVENT + 1
pygame.time.set_timer(SNAKE_UPDATE, 110)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SNAKE_UPDATE:
            main_game.snake.move()
        if event.type == pygame.KEYDOWN:
            if not main_game.snake.enable_move and event.key == pygame.K_r:
                main_game = Main()
            if main_game.snake.direction.x:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    main_game.snake.direction = Vector2(0, -TILE)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    main_game.snake.direction = Vector2(0, TILE)
            elif main_game.snake.direction.y:
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    main_game.snake.direction = Vector2(TILE, 0)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    main_game.snake.direction = Vector2(-TILE, 0)

    main_game.update()
    pygame.display.flip()
    clock.tick(60)
