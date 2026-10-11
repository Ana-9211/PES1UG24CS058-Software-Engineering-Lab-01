"""
GameEngine: owns the frog and all vehicles, and runs one frame's worth
of game logic.

Features: 3 lives with respawn, score for each goal reached (win at
WIN_SCORE), a 30-second timer per attempt, and R to restart.
"""

import random

import pygame

from game.frog import Frog
from game.vehicle import Vehicle
from game.collisions import check_collision
from game.renderer import (
    GRID_COLS, GRID_ROWS, GOAL_ROW, ROAD_ROWS, START_ROW, CELL_SIZE, WIDTH, HEIGHT,
)

STARTING_LIVES = 3
ATTEMPT_SECONDS = 30
WIN_SCORE = 3          # goal reaches needed to win
FPS = 60
ATTEMPT_FRAMES = ATTEMPT_SECONDS * FPS

LANE_SPEEDS = [1.5, -2, 2, -2.5, 1.5, -2]   # one entry per road row, alternating direction


class GameEngine:
    def __init__(self):
        self._build_entities()

    def _build_entities(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.timer_frames = ATTEMPT_FRAMES
        self.state = "playing"   # "playing" | "won" | "game_over"
        start_col = GRID_COLS // 2
        self.frog = Frog(
            col=start_col, row=START_ROW,
            start_col=start_col, start_row=START_ROW,
            cols=GRID_COLS, start_row_limit=START_ROW,
        )
        frog_x_range = (start_col * CELL_SIZE, start_col * CELL_SIZE + CELL_SIZE)

        self.vehicles = []
        for i, row in enumerate(ROAD_ROWS):
            speed = LANE_SPEEDS[i % len(LANE_SPEEDS)]
            vehicle_width = 40 if i % 2 == 0 else 70   # mix of cars and wider trucks
            spacing = 300
            count = 2

            # Try a few random phases and keep the first one that doesn't
            # already overlap the frog's starting column - guarantees a
            # safe first lane instead of leaving it to chance.
            for _attempt in range(20):
                phase = random.randint(0, spacing - 1)
                positions = []
                safe = True
                for n in range(count):
                    offset = phase + n * spacing
                    x = offset if speed > 0 else WIDTH - offset - vehicle_width
                    positions.append(x)
                    if not (x + vehicle_width <= frog_x_range[0] or x >= frog_x_range[1]):
                        safe = False
                if safe:
                    break

            for x in positions:
                self.vehicles.append(Vehicle(x=x, row=row, width=vehicle_width,
                                              height=CELL_SIZE - 8, speed=speed))

    def handle_keydown(self, key):
        if key == pygame.K_r:
            self._build_entities()
            return
        if self.state != "playing":
            return
        if key == pygame.K_UP:
            self.frog.move(0, -1)
        elif key == pygame.K_DOWN:
            self.frog.move(0, 1)
        elif key == pygame.K_LEFT:
            self.frog.move(-1, 0)
        elif key == pygame.K_RIGHT:
            self.frog.move(1, 0)

    def _lose_life(self):
        self.lives -= 1
        if self.lives <= 0:
            self.state = "game_over"
        else:
            self.frog.reset()
            self.timer_frames = ATTEMPT_FRAMES

    def update(self):
        if self.state != "playing":
            return

        for v in self.vehicles:
            v.update(road_width_px=WIDTH)

        if check_collision(self.frog, self.vehicles):
            self._lose_life()
            return

        if self.frog.row == GOAL_ROW:
            self.score += 1
            if self.score >= WIN_SCORE:
                self.state = "won"
            else:
                self.frog.reset()
                self.timer_frames = ATTEMPT_FRAMES
            return

        self.timer_frames -= 1
        if self.timer_frames <= 0:
            self._lose_life()

    @property
    def seconds_left(self):
        return max(0, -(-self.timer_frames // FPS))   # ceil

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.frog, self.vehicles)
        renderer.draw_hud(surface, font, self.score, WIN_SCORE, self.lives, self.seconds_left)
        if self.state == "won":
            renderer.draw_banner(surface, font, "YOU WIN! Press R to restart")
        elif self.state == "game_over":
            renderer.draw_banner(surface, font, "GAME OVER - Press R to restart")
        else:
            renderer.draw_text(surface, font, "Arrow keys to move. R to restart.", (10, HEIGHT - 24))
