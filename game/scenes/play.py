import pygame

from ..utils import blit_center, blit_center_rel, scale_rel
from ..base import TransitionableScene

import os
import re
import time
import logging
from math import floor

logger = logging.getLogger("RHYTHMATICA")


class Circle:
    SIZE = 0.225
    LOCX = ((3/8), (5/8))
    LOCY = ((3/16), (8/16), (13/16))
    COLORS = (
        pygame.Color("red"), pygame.Color("gold"),
        pygame.Color("forestgreen"), pygame.Color("darkturquoise"),
        pygame.Color("blue"), pygame.Color("darkviolet")
    )

    def __init__(self, num, maxsize=None):
        if maxsize is None:
            maxsize = pygame.display.get_window_size()
        self.maxw, self.maxh = maxsize

        rw, rh = (self.LOCX[num % 2], self.LOCY[floor(num / 2)])

        self.loc = (self.maxw * rw, self.maxh * rh)
        self.radius = self.maxh * self.SIZE / 2
        self.color = pygame.Color(self.COLORS[num])

        logger.debug((self.loc, self.radius))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.loc, self.radius)


class CircleEdge(Circle):
    EDGELEN = 1/10
    RADIUS_INCREMENT = 1.1

    def __init__(self, num, maxsize=None):
        super().__init__(num, maxsize)
        self.color = pygame.Color("gray50")
        self.edge = round(self.radius * self.EDGELEN)
        self.radius_big = self.radius * self.RADIUS_INCREMENT

    def draw(self, surface, big=False):
        radius = self.radius_big if big else self.radius
        pygame.draw.circle(surface, self.color, self.loc, radius, self.edge)


class Note(CircleEdge):
    RADIUS_INCREMENT = 2.5

    def __init__(self, num, time_, speed, bpm, maxsize=None):
        super(CircleEdge, self).__init__(num, maxsize)

        self.color.r = max(0, self.color.r - 50)
        self.color.g = max(0, self.color.g - 50)
        self.color.b = max(0, self.color.b - 50)

        self.edge = round(self.radius * self.EDGELEN)
        self.radius_big = self.radius * self.RADIUS_INCREMENT

        spb = 1 / bpm * 60
        self.speed = (self.radius - self.radius_big) / spb * speed
        self.started_time = time_ - spb / speed
        self.time = time_

    @property
    def elapsed_time(self):
        return time.perf_counter() - self.started_time

    @property
    def is_showing(self):
        return self.elapsed_time > 0

    @property
    def is_gone(self):
        # logger.debug("%f, %f", time.perf_counter(), self.time + 0.2)
        return time.perf_counter() > self.time + 0.2

    def draw(self, surface):
        radius = self.get_radius()
        if not radius:
            return self.is_gone
        pygame.draw.circle(surface, self.color, self.loc, radius, self.edge)
        return False

    def judge(self):
        diff = abs(self.time - time.perf_counter())
        logger.debug("%f", diff)
        if diff > 0.5:
            return False, None
        elif diff > 0.4:
            return True, False
        else:
            return True, True

    def get_radius(self):
        return self._get_radius(self.elapsed_time)

    def _get_radius(self, time_):
        if not self.is_showing or self.is_gone:
            return 0
        return self.radius_big + self.speed * time_


def parse_a3(data):
    return [[float(y) for y in x.split()] for x in data.split("/")[1:7]]


def parse_a4(data):
    logger.debug("called")
    logger.debug(data)
    notelist = [list() for _ in range(6)]

    spb = 0
    division = 0
    offset = 0

    i = 0

    for line in data.split()[1:]:
        logger.debug("%d %s", i, line)
        if line[0] in ('b', 'd', 'w'):
            if line[0] == 'b':
                spb = 1 / float(line[1:]) * 60
                logger.debug("bpm detected, %f", spb)
            elif line[0] == 'd':
                division = int(line[1:])
                logger.debug("division detected, %d", division)
            elif line[0] == 'w':
                offset = float(line[1:])
                logger.debug("offset detected, %f", offset)

        elif line[0] == '/':
            logger.debug("skip the beat %s times", line[1:])
            i += int(line[1:])

        else:
            logger.debug("%f %d %f", spb, division, offset)
            time_ = offset + (spb / division) * i
            logger.debug("Adding note in %s at %d", line, time_)
            for num in line:
                notelist[int(num)-1].append(time_)

            i += 1

    return notelist


def parse_notes(data):
    version = re.search(r"ver:([A-Z0-9]+)", data).group(1)
    logger.debug(version)
    if version == "A3":
        return parse_a3(data)
    elif version == "A4":
        return parse_a4(data)
    else:
        raise RuntimeError("Unknown Chart Version!")


class Play(TransitionableScene):
    name = "Play"
    KEYS = ["t", "y", "g", "h", "b", "n"]

    def __init__(self, song, speed, prev_scene=None, fadein_surface=None):
        super().__init__()

        self.songdata = song
        self.speed = speed
        self.prev_scene = prev_scene
        self.fade_surface = fadein_surface

        self.movetime = 1 / self.songdata.bpm * 60 / speed

        self.start_time = None
        self.song_length = self.songdata.music.get_length()
        self.channel = None

        self.notedata = None
        self.notes = [list() for _ in range(6)]

        self.hit = False
        self.hit_duration = 1.5
        self.hit_blink = 0.2
        self.hit_show_until = 0

        self.hits = 0
        self.misses = 0
        self.combo = 0
        self.maxcombo = 0
        self.score = 0
        self.score_per_note = 10000 / self.songdata.notes

        self.hit_image = None
        self.miss_image = None

        self.bg_surface = None
        self.bg_circle = [list() for _ in range(6)]
        self.edges = None
        self.key_status = [
            False, False,
            False, False,
            False, False
        ]

    @property
    def elapsed_time(self):
        if self.start_time is None:
            return 0
        else:
            return time.perf_counter() - self.start_time

    @property
    def is_ongoing(self):
        return self.elapsed_time < self.song_length

    def start(self):
        self.notedata = parse_notes(self.songdata.notedata)

        screen_size = self.game.screen.get_size()

        self.hit_image = pygame.image.load(
            os.path.join("res", "image", "judge", "hit.png")).convert_alpha()
        self.miss_image = pygame.image.load(
            os.path.join("res", "image", "judge", "miss.png")).convert_alpha()

        self.hit_image = scale_rel(self.hit_image, 2 / 7, screen_size)
        self.miss_image = scale_rel(self.miss_image, 2 / 7, screen_size)

        self.bg_surface = pygame.Surface(screen_size)

        self.bg_surface.fill("white")
        self.bg_surface.blit(self.songdata.img_big, (0, 0))

        height = screen_size[1] * self.game.font_size_ratio * 2 / 3
        titletxt_bg = pygame.Surface((screen_size[0], height))
        titletxt_bg.fill("black")
        titletxt_bg.set_alpha(128)
        blit_center_rel(self.bg_surface, titletxt_bg, (0.5, 0), (0.5, 0))

        for n in range(6):
            self.bg_circle[n] = circle = Circle(n, screen_size)
            circle.draw(self.bg_surface)

        self.edges = [CircleEdge(n, screen_size) for n in range(6)]

        if self.fade_surface is not None:
            self.game.add_task(self.fade_task, (
                self.fade_surface, True, self.start_game))

    def start_game(self, _, t=None):
        if t is None:
            logger.info("Starting the game in 3 seconds...")
            t = time.perf_counter()

        if time.perf_counter() - t < 3:
            self.game.add_task(self.start_game, (t,))
        else:
            logger.info("GAME START!")
            self.start_time = time.perf_counter()
            self.channel = self.songdata.music.play()
            self.game.add_task(self.spawn_task)
            self.game.add_task(self.draw_task)
            self.game.add_task(self.show_judge_task)
            self.game.add_task(self.stop_task)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                logger.info("q pressed, exiting the game")
                self.game.stop()

            keyname = pygame.key.name(event.key)
            if keyname in self.KEYS:
                keystatus = event.type == pygame.KEYDOWN
                keyindex = self.KEYS.index(keyname)
                self.key_status[keyindex] = keystatus
                if keystatus:
                    self.handle_judge(keyindex)
                # logger.debug(self.key_status)

    def handle_judge(self, n):
        if len(self.notes[n]) == 0:
            return

        logger.debug("%d", n)

        recognized, hit = self.notes[n][0].judge()
        if recognized:
            self.notes[n].pop(0)
            self.handle_hit(hit)

    def handle_hit(self, hit=True):
        self.show_judge(hit)
        if hit:
            self.hits += 1
            self.combo += 1
            self.maxcombo = max(self.combo, self.maxcombo)
            self.score += self.score_per_note
        else:
            self.combo = 0
            self.misses += 1

    def show_judge(self, hit=True):
        self.hit = hit
        self.hit_show_until = time.perf_counter() + self.hit_duration

    def show_judge_task(self, game):
        now = time.perf_counter()
        show = bool(int(now % self.hit_blink * 10))

        if now < self.hit_show_until and show:
            img = self.hit_image if self.hit else self.miss_image
            blit_center_rel(game.screen, img, (0.5, 0.5))

        if self.is_ongoing:
            self.game.add_task(self.show_judge_task)

    def spawn_task(self, game):
        for n in range(6):
            if len(self.notedata[n]) == 0:
                continue
            if self.elapsed_time > self.notedata[n][0] - self.movetime:
                logger.debug("%f Spawned a note for %d", self.elapsed_time, n)
                self.notes[n].append(Note(
                    n, self.notedata[n].pop(0) + self.start_time, self.speed,
                    self.songdata.bpm))

        if self.is_ongoing:
            self.game.add_task(self.spawn_task)

    def draw_task(self, game):
        for n in range(6):
            offset = 0
            # logger.debug("========== %d, %d", n, len(self.notes[n]))
            for i in range(len(self.notes[n])):
                i -= offset

                # logger.debug(i)
                # logger.debug(self.notes[n])
                
                is_gone = self.notes[n][i].draw(game.screen)
                if is_gone:
                    self.notes[n].pop(i)
                    offset += 1
                    self.handle_hit(False)

        if self.is_ongoing:
            self.game.add_task(self.draw_task)

    def stop_task(self, game):
        def callback(_):
            self.game.set_scene(self.prev_scene)

        if not self.channel.get_busy():
            self.game.add_task(self.fade_task, (
                self.fade_surface, False, callback))
        else:
            self.game.add_task(self.stop_task)

    def task(self):
        self.game.screen.blit(self.bg_surface, (0, 0))
        [edge.draw(self.game.screen, self.key_status[n])
         for n, edge in enumerate(self.edges)]

        if self.elapsed_time == 0:
            for i, circle in enumerate(self.bg_circle):
                keytext = self.game.fonts['regular'].render(
                    self.KEYS[i].upper(), 1, 'white')
                blit_center(self.game.screen, keytext, circle.loc)

        titletxt = self.game.fonts['black'].render(
            f"{self.songdata.artist} - {self.songdata.name}", True, "white")
        titletxt = scale_rel(titletxt, self.game.font_size_ratio * 2 / 3)

        width_ratio = self.elapsed_time / self.song_length
        width = self.game.screen.get_width() * width_ratio

        titletxt_bg = pygame.Surface((width, titletxt.get_height()))
        titletxt_bg.fill("black")
        titletxt_bg.set_alpha(100)

        blit_center_rel(self.game.screen, titletxt_bg, (0, 0), (0, 0))
        blit_center_rel(self.game.screen, titletxt, (0.5, 0), (0.5, 0))

        scoretxt = self.game.fonts['regular'].render(
            str(round(self.score)), 1, 'black')
        blit_center_rel(self.game.screen, scoretxt, (0.5, 1), (0.5, 1))

        if self.combo >= 5:
            combotxt = self.game.fonts['black'].render(
                str(self.combo), True, "black")

            blit_center_rel(self.game.screen, combotxt, (0.5, 0.65))
