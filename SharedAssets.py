import pygame as pg
import pg_extended as pgx
import argparse

app: pgx.Window = None

config: dict = None

dbStructure: dict = None

db: dict = None

dbAssets: dict[str, pg.Surface] = {}

args: argparse.Namespace = None
