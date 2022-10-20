import pygame

from ..base import TransitionableScene
from ..utils import (
    SmoothMoveXY, calc_loc_rel, calc_center, scale_rel, blit_center_rel,
    text_multiline
)

import os
import logging
from threading import Event

logger = logging.getLogger("RHYTHMATICA")


class SongPack:
    def __init__(
            self, game, path, name, artist, bpm, notes, img, preview, music):
        self.game = game
        self.path = path
        self.name = name
        self.artist = artist
        self.bpm = bpm
        self.notes = notes
        self.img = img.convert_alpha()
        self.preview = preview
        self.music = music

        notepersec = int(notes) / self.music.get_length()

        if notepersec < 3:
            self.difficulty = "EASY"
        elif 3 <= notepersec < 6:
            self.difficulty = "MEDIUM"
        elif 6 <= notepersec < 10:
            self.difficulty = "HARD"
        else:
            self.difficulty = "EXTREME"

        self.mover = None

        fullsize = self.game.screen.get_size()

        self.img_big = scale_rel(self.img, 1, fullsize)
        self.img_big.set_alpha(128)
        self.img_small = scale_rel(self.img, 0.5, fullsize)

        self.info = text_multiline(
            self.game.fonts['regular'],
            f"{self.name}\nArtist: {self.artist}\n"
            f"BPM: {self.bpm}\nDifficulty: {self.difficulty}",
            True, "black", None
        )
        info_x = (fullsize[0] - self.info.get_size()[0]) / 2
        info_y = fullsize[1] / 2
        self.info_pos = (info_x, info_y)

        self.guide = scale_rel(text_multiline(
            self.game.fonts['bold'],
            "Press T, Y to change note speed.\n"
            "Press G, H to change songs.\n"
            "Press N to start the game.",
            True, "black"
        ), 1 / 9, fullsize)

        guide_x = (fullsize[0] - self.guide.get_size()[0]) / 2
        guide_y = fullsize[1] - self.guide.get_size()[1]
        self.guide_pos = (guide_x, guide_y)

    @classmethod
    def from_path(cls, game, path):
        folder_name = path.rstrip("/").rsplit("/")[-1]
        logger.info("Loading %s...", folder_name)
        try:
            with open(os.path.join(path, "info.txt")) as f:
                try:
                    name, artist, bpm, notes = [
                        x.strip() for x in f.readlines()[:4]]
                except ValueError:
                    logger.exception(
                        "Failed to load a song from %s.", folder_name)
                    return None

            img = pygame.image.load(os.path.join(path, "img.png"))
            preview = pygame.mixer.Sound(os.path.join(path, "pre.wav"))
            music = pygame.mixer.Sound(os.path.join(path, "song.wav"))

        except FileNotFoundError:
            logger.exception("Failed to load from %s.", path)
            return None

        return cls(game, path, name, artist, bpm, notes, img, preview, music)

    @classmethod
    def load_bulk(cls, game, path):
        return [
            cls.from_path(game, os.path.join(path, folder))
            for folder in os.listdir(path)
            if os.path.isdir(os.path.join(path, folder))
        ]

    def blit_full(self, surface):
        surface.fill("white")

        blit_center_rel(surface, self.img_big, (0.5, 0.5))
        blit_center_rel(surface, self.img_small, (0.5, 0.25))
        surface.blit(self.info, self.info_pos)
        surface.blit(self.guide, self.guide_pos)

    def blit_small(self, surface, left=True):
        loc = (-0.1 if left else 1.1, 0.5)
        blit_center_rel(surface, self.img_small, loc)

    def move_task(self, game, mover, callback):
        mover.draw(game.screen)
        if mover.is_running:
            self.game.add_task(self.move_task, (mover, callback))
        else:
            if callable(callback):
                callback()

    def move(self, orig, dest, duration, callback=None):
        mover = SmoothMoveXY(self.img_small, orig, dest, duration)
        mover.start()
        self.game.add_task(self.move_task, (mover, callback))

    def move_left(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (1, 0.5)))
        orig = (fullw, orig[1])
        dest = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))

        self.move(orig, dest, duration, callback)

    def move_left_out(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))
        dest = calc_center(srcsize, calc_loc_rel(full, (0, 0.5)))
        dest = (-srcsize[0], dest[1])

        self.move(orig, dest, duration, callback)

    def move_right(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0, 0.5)))
        orig = (-srcsize[0], orig[1])
        dest = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))

        self.move(orig, dest, duration, callback)

    def move_right_out(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))
        dest = calc_center(srcsize, calc_loc_rel(full, (1, 0.5)))
        dest = (fullw, dest[1])

        self.move(orig, dest, duration, callback)


class SongSelect(TransitionableScene):
    def __init__(self, fadein_surface=None):
        super().__init__()

        self.fadein_surface = fadein_surface

        self.songs = []
        self.current_preview = None

        self.current_song = 0

        self.is_moving = Event()

    @property
    def prev(self):
        return self.current_song - 1 \
            if self.current_song > 0 else len(self.songs) - 1

    @property
    def next(self):
        return self.current_song + 1 \
            if self.current_song < len(self.songs) - 1 else 0

    def play_preview(self):
        self.current_preview = self.songs[self.current_song].preview.play()

    def start(self):
        self.songs = [
            x for x in SongPack.load_bulk(self.game, os.path.join("soundpack"))
            if x is not None]

        if not self.songs:
            logger.error("No songs are found??? Exiting game...")
            self.game.stop()

        if self.fadein_surface is not None:
            self.game.add_task(self.fade_task, (
                self.fadein_surface, True, lambda _:  self.play_preview()
            ))

    def handle_event(self, event):
        if self.fade_ongoing.is_set() or self.is_moving.is_set():
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_g, pygame.K_h):
                def callback():
                    self.is_moving.clear()
                    self.play_preview()

                self.current_preview.stop()
                self.is_moving.set()

                if event.key == pygame.K_g:
                    self.current_song = self.prev
                    self.songs[self.next].move_right_out(1)
                    self.songs[self.current_song].move_right(1, callback)

                elif event.key == pygame.K_h:
                    self.current_song = self.next
                    self.songs[self.prev].move_left_out(1)
                    self.songs[self.current_song].move_left(1, callback)

    def task(self):
        if self.is_moving.is_set():
            self.game.screen.fill("white")
        else:
            self.songs[self.current_song].blit_full(self.game.screen)
