import pygame

from models import Asteroid, Spaceship, NPC
from user import User
from utils import get_random_position, load_sprite, print_text, print_healthcheck1, print_healthcheck2, \
    print_healthcheck3

import pygame
import math
import random
from pygame.math import Vector2
import sys


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()
        # current_w = 1680, current_h = 1050
        self.screen = pygame.display.set_mode((1024, 768))
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.background = load_sprite("space", False)

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.message_healthcheck1 = ""
        self.message_healthcheck2 = ""
        self.message_healthcheck3 = ""

        self.asteroids = []
        self.bullets = []
        self.users = []

        self.user1 = User()
        self.user2 = User()
        self.user3 = User()
        self.user1.addPlayer(1, "scott")
        self.user2.addPlayer(2, "miller")
        self.user3.addPlayer(3, "nickolas")

        self.users.append(self.user1)
        self.users.append(self.user2)
        self.users.append(self.user3)
        self.spaceship_one = Spaceship(
            (self.width // 2, self.height // 2), self.bullets.append, "space_ship_40x40", self.user1
        )

        self.spaceship_two = Spaceship(
            (self.width // -10, self.height // 5), self.bullets.append, "space_ship2_40x40", self.user2
        )

        self.spaceship_three = Spaceship(
            (self.width, self.height // -8), self.bullets.append, "space_ship3_40x40", self.user3
        )

        self.started = True

        for _ in range(10):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceship_one.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

                if (
                        position.distance_to(self.spaceship_two.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

                if (
                        position.distance_to(self.spaceship_three.position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

            self.asteroids.append(Asteroid(position, self.asteroids.append))

    def main_loop(self):
        while True:
            self._handle_input()
            if self.started:
                self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            if (
                    self.spaceship_one
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceship_one.shoot()
            if (
                    self.spaceship_two
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_f
            ):
                self.spaceship_two.shoot()

            if (
                    self.spaceship_three
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_o
            ):
                self.spaceship_three.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if not self.started:
            if is_key_pressed[pygame.K_g]:
                self.started = True

        if self.spaceship_one:
            # print(f"velocity: {self.spaceship_one.velocity}")
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship_one.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship_one.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship_one.accelerate()

            if is_key_pressed[pygame.K_DOWN]:
                self.spaceship_one.accelerate(0)

        if self.spaceship_two:
            # print(f"velocity: {self.spaceship_one.velocity}")
            if is_key_pressed[pygame.K_d]:
                self.spaceship_two.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceship_two.rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceship_two.accelerate()

            if is_key_pressed[pygame.K_s]:
                self.spaceship_two.accelerate(0)

        if self.spaceship_three:
            # print(f"velocity: {self.spaceship_three.velocity}")
            if is_key_pressed[pygame.K_l]:
                self.spaceship_three.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_j]:
                self.spaceship_three.rotate(clockwise=False)
            if is_key_pressed[pygame.K_i]:
                self.spaceship_three.accelerate()

            if is_key_pressed[pygame.K_k]:
                self.spaceship_three.accelerate(0)

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship_one:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship_one):
                    self.spaceship_one = None
                    self.message = "spaceship_one lost!"
                    break

        if self.spaceship_two:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship_two):
                    self.spaceship_two = None
                    self.message = "spaceship_two lost!"
                    break

        if self.spaceship_three:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship_three):
                    self.spaceship_three = None
                    self.message = "spaceship_three lost!"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
            if self.spaceship_one and self.spaceship_one.collides_with(bullet):
                self.spaceship_one.healthcheck_one(10)
                print(self.spaceship_one.health_state_one)
                self.message_healthcheck1 = "user {} (spaceship_one) health: {} ".format(self.spaceship_one.user.name,
                                                                                         self.spaceship_one.
                                                                                         health_state_one)

                if self.spaceship_one.health_state_one == 0:
                    self.message_healthcheck1 = "spaceship_one going to kill"

            if self.spaceship_two and self.spaceship_two.collides_with(bullet):
                self.spaceship_two.healthcheck_two(10)
                print(self.spaceship_two.health_state_two)
                self.message_healthcheck2 = "user {} (spaceship_two) health: {} ".format(self.spaceship_two.user.name,
                                                                                         self.spaceship_two.
                                                                                         health_state_two)

                if self.spaceship_two.health_state_two == 0:
                    message_healthcheck2 = "spaceship_two going to kill"

            if self.spaceship_three and self.spaceship_three.collides_with(bullet):
                self.spaceship_three.healthcheck_three(10)
                print(self.spaceship_three.health_state_three)
                self.message_healthcheck3 = "user {} (spaceship_three) health: {}".format(
                    self.spaceship_three.user.name,
                    self.spaceship_three.
                    health_state_three)

                if self.spaceship_three.health_state_three == 0:
                    self.message_healthcheck3 = "spaceship_three going to kill"

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship_one:
            self.message = "spaceship_one won!"

        if not self.asteroids and self.spaceship_two:
            self.message = "spaceship_two won!"

        if not self.asteroids and self.spaceship_three:
            self.message = "spaceship_three won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        self.screen.fill((0, 0, 0))

        for game_object in self._get_game_objects():
            # print(game_object)
            game_object.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)

        if self.message_healthcheck1:
            print_healthcheck1(self.screen, self.message_healthcheck1, pygame.font.Font(None, 30))

        if self.message_healthcheck2:
            print_healthcheck2(self.screen, self.message_healthcheck2, pygame.font.Font(None, 30))

        if self.message_healthcheck3:
            print_healthcheck3(self.screen, self.message_healthcheck3, pygame.font.Font(None, 30))

        pygame.display.flip()
        self.clock.tick(60)

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship_one:
            game_objects.append(self.spaceship_one)

        if self.spaceship_two:
            game_objects.append(self.spaceship_two)

        if self.spaceship_three:
            game_objects.append(self.spaceship_three)

        return game_objects
