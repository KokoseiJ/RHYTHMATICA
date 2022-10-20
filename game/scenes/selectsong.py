import pygame

from .play import Play
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
    def __init__(self, game, path, name, artist, bpm, notes, notedata, img,
                 preview, music):
        self.game = game
        self.path = path
        self.name = name
        self.artist = artist
        self.bpm = bpm
        self.notes = notes
        self.notedata = notedata
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
            True, "black", background="grey"
        )

        self.guide = scale_rel(text_multiline(
            self.game.fonts['bold'],
            "Press T, Y to change note speed.\n"
            "Press G, H to change songs.\n"
            "Press N to start the game.",
            True, "black"
        ), 1 / 9, fullsize)

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
            with open(os.path.join(path, "note.txt")) as f:
                notedata = f.read()

            img = pygame.image.load(os.path.join(path, "img.png"))
            preview = pygame.mixer.Sound(os.path.join(path, "pre.wav"))
            music = pygame.mixer.Sound(os.path.join(path, "song.wav"))

        except FileNotFoundError:
            logger.exception("Failed to load from %s.", path)
            return None

        return cls(game, path, name, artist, float(bpm), int(notes), notedata,
                   img, preview, music)

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
        blit_center_rel(surface, self.info, (0.5, 0.5), (0.5, 0))
        blit_center_rel(surface, self.guide, (0.5, 1), (0.5, 1))

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
        orig = calc_center(srcsize, calc_loc_rel(full, (1, 0.5)), (0, 0.5))
        dest = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))

        self.move(orig, dest, duration, callback)

    def move_left_out(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))
        dest = calc_center(srcsize, calc_loc_rel(full, (0, 0.5)), (1, 0.5))

        self.move(orig, dest, duration, callback)

    def move_right(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0, 0.5)), (1, 0.5))
        dest = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))

        self.move(orig, dest, duration, callback)

    def move_right_out(self, duration, callback=None):
        fullw, fullh = full = self.game.screen.get_size()
        srcsize = self.img_small.get_size()
        orig = calc_center(srcsize, calc_loc_rel(full, (0.5, 0.25)))
        dest = calc_center(srcsize, calc_loc_rel(full, (1, 0.5)), (0, 0.5))

        self.move(orig, dest, duration, callback)


class SongSelect(TransitionableScene):
    def __init__(self, fadein_surface=None):
        super().__init__()

        self.fade_surface = fadein_surface

        self.songs = []
        self.current_preview = None

        self.current_song = 0
        self.speed = 1.00

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

        if self.current_song >= len(self.songs):
            logger.warning("current_song bigger than available songs!")
            self.current_song = 0

        pygame.mixer.music.load(os.path.join("res", "sound", "nextsong.mp3"))

        if self.fade_surface is not None:
            self.game.add_task(self.fade_task, (
                self.fade_surface, True, lambda _:  self.play_preview()
            ))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            logger.warning("Q pressed, exiting")
            self.game.stop()
            return

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

                pygame.mixer.music.play()

            elif event.key == pygame.K_t and self.speed > 0.25:
                self.speed -= 0.25

            elif event.key == pygame.K_y and self.speed < 5:
                self.speed += 0.25

            elif event.key == pygame.K_n:
                self.current_preview.stop()
                pygame.mixer.music.load(
                    os.path.join("res", "sound", "start.mp3"))
                pygame.mixer.music.play()
                self.game.add_task(self.fade_task, (
                    self.fade_surface, False, self.fadeout_callback))

    def fadeout_callback(self, _):
        logger.info("SongSelect fadeout finished, starting Play Scene")

        song = self.songs[self.current_song]

        logger.info("Song: %s, Speed: %f", song.name, self.speed)
        next_scene = Play(song, self.speed, self, self.fade_surface)
        self.game.set_scene(next_scene)

    def task(self):
        if self.is_moving.is_set():
            self.game.screen.fill("white")
        else:
            self.songs[self.current_song].blit_full(self.game.screen)

        speed = scale_rel(
            self.game.fonts['regular'].render(
                f"Speed: {str(self.speed).ljust(4, '0')}x",
                True,
                "black"
            ), 1 / 18
        )

        blit_center_rel(self.game.screen, speed, (1, 1), (1, 1))
