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

        self.spaceships = []

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

        self.spaceships.append(self.spaceship_one)
        self.spaceships.append(self.spaceship_two)
        self.spaceships.append(self.spaceship_three)

        print(self.spaceships[0])
        print(self.spaceships[1])
        print(self.spaceships[2])
        self.started = True

        for _ in range(10):
            while True:
                position = get_random_position(self.screen)
                if (
                        position.distance_to(self.spaceships[0].position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

                if (
                        position.distance_to(self.spaceships[1].position)
                        > self.MIN_ASTEROID_DISTANCE
                ):
                    break

                if (
                        position.distance_to(self.spaceships[2].position)
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
                    len(self.spaceships) > 0 and self.spaceships[0]
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_SPACE
            ):
                self.spaceships[0].shoot()
            if (
                    len(self.spaceships) > 1 and self.spaceships[1]
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_f
            ):
                self.spaceships[1].shoot()

            if (
                    len(self.spaceships) > 2 and self.spaceships[2]
                    and event.type == pygame.KEYDOWN
                    and event.key == pygame.K_o
            ):
                self.spaceships[2].shoot()

        is_key_pressed = pygame.key.get_pressed()

        if not self.started:
            if is_key_pressed[pygame.K_g]:
                self.started = True

        if len(self.spaceships) > 0 and self.spaceships[0]:
            # print(f"velocity: {self.spaceship_one.velocity}")
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceships[0].rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceships[0].rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceships[0].accelerate()

            if is_key_pressed[pygame.K_DOWN]:
                self.spaceships[0].accelerate(0)

        if len(self.spaceships) > 1 and self.spaceships[1]:
            # print(f"velocity: {self.spaceship_one.velocity}")
            if is_key_pressed[pygame.K_d]:
                self.spaceships[1].rotate(clockwise=True)
            elif is_key_pressed[pygame.K_a]:
                self.spaceships[1].rotate(clockwise=False)
            if is_key_pressed[pygame.K_w]:
                self.spaceships[1].accelerate()

            if is_key_pressed[pygame.K_s]:
                self.spaceships[1].accelerate(0)

        if len(self.spaceships) > 2 and self.spaceships[2]:
            # print(f"velocity: {self.spaceship_three.velocity}")
            if is_key_pressed[pygame.K_l]:
                self.spaceships[2].rotate(clockwise=True)
            elif is_key_pressed[pygame.K_j]:
                self.spaceships[2].rotate(clockwise=False)
            if is_key_pressed[pygame.K_i]:
                self.spaceships[2].accelerate()

            if is_key_pressed[pygame.K_k]:
                self.spaceships[2].accelerate(0)

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if len(self.spaceships) > 0 and self.spaceships[0]:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceships[0]):
                    self.spaceships[0] = None
                    self.message = "spaceship_one lost!"
                    break

        if len(self.spaceships) > 1 and self.spaceships[1]:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceships[1]):
                    self.spaceships[1] = None
                    self.message = "spaceship_two lost!"
                    break

        if len(self.spaceships) > 2 and self.spaceships[2]:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceships[2]):
                    self.spaceships[2] = None
                    self.message = "spaceship_three lost!"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break
            if len(self.spaceships) > 0 and self.spaceships[0] and self.spaceships[0].collides_with(bullet):
                self.spaceships[0].healthcheck_one(10)
                print(self.spaceships[0].health_state_one)
                self.message_healthcheck1 = "user {} (spaceship_one) health: {} ".format(self.spaceships[0].user.name,
                                                                                         self.spaceships[0].
                                                                                         health_state_one)

                if self.spaceships[0].health_state_one == 0:
                    self.message_healthcheck1 = "spaceship_one is destroyed"
                    self.spaceships.remove(self.spaceships[0])

            if len(self.spaceships) > 1 and self.spaceships[1] and self.spaceships[1].collides_with(bullet):
                self.spaceships[1].healthcheck_two(10)
                print(self.spaceships[1].health_state_two)
                self.message_healthcheck2 = "user {} (spaceship_two) health: {} ".format(self.spaceships[1].user.name,
                                                                                         self.spaceships[1].
                                                                                         health_state_two)

                if self.spaceships[1].health_state_two == 0:
                    self.message_healthcheck2 = "spaceship_two is destroyed"
                    self.spaceships.remove(self.spaceships[1])

            if len(self.spaceships) > 2 and self.spaceships[2] and self.spaceships[2].collides_with(bullet):
                self.spaceships[2].healthcheck_three(10)
                print(self.spaceships[2].health_state_three)
                self.message_healthcheck3 = "user {} (spaceship_three) health: {}".format(
                    self.spaceships[2].user.name,
                    self.spaceships[2].
                    health_state_three)

                if self.spaceships[2].health_state_three == 0:
                    self.message_healthcheck3 = "spaceship_three is destroyed"
                    self.spaceships.remove(self.spaceships[2])

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceships[0]:
            self.message = "spaceship_one won!"

        if not self.asteroids and self.spaceships[1]:
            self.message = "spaceship_two won!"

        if not self.asteroids and self.spaceships[2]:
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

        if len(self.spaceships) > 0 and self.spaceships[0]:
            game_objects.append(self.spaceships[0])

        if len(self.spaceships) > 1 and self.spaceships[1]:
            game_objects.append(self.spaceships[1])
        print("size of the spaceships    ")
        print(len(self.spaceships))
        if len(self.spaceships) > 2 and self.spaceships[2]:
            game_objects.append(self.spaceships[2])

        return game_objects
