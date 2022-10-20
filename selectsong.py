import pygame

from base import TransitionableScene
from utils import scale_rel, blit_center_rel, text_multiline

import os
import logging

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

        self.img_big = scale_rel(self.img, 1, self.game.screen.get_size())
        self.img_big.set_alpha(128)
        self.img_small = scale_rel(self.img, 0.5, self.game.screen.get_size())

        self.info = text_multiline(
            self.game.fonts['regular'],
            f"{self.name}\nArtist: {self.artist}\n"
            f"BPM: {self.bpm}\nDifficulty: {self.difficulty}",
            True, "black", None
        )
        info_x = (self.game.screen.get_size()[0] - self.info.get_size()[0]) / 2
        info_y = self.game.screen.get_size()[1] / 2
        self.info_pos = (info_x, info_y)

        self.guide = scale_rel(text_multiline(
            self.game.fonts['bold'],
            "Press T, Y to change speed.\n"
            "Press G, H to change songs.\n"
            "Press N to start the game.",
            True, "black"
        ), 1 / 9, self.game.screen.get_size())

        guide_x = (self.game.screen.get_size()[0] - self.guide.get_size()[0])/2
        guide_y = self.game.screen.get_size()[1] - self.guide.get_size()[1]
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


class SongSelect(TransitionableScene):
    def __init__(self, fadein_surface):
        super().__init__()

        self.fadein_surface = fadein_surface

        self.songs = []
        self.current_preview = None

        self.current_song = 0

    def start(self):
        self.songs = [
            x for x in SongPack.load_bulk(self.game, os.path.join("soundpack"))
            if x is not None]

        if not self.songs:
            logger.error("No songs are found??? Exiting game...")
            self.game.stop()

    def task(self):
        self.songs[self.current_song].blit_full(self.game.screen)
