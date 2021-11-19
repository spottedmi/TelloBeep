#! /usr/bin/python3
from backend.server import setup

import os

os.mkdir("imgs")
os.mkdir("backend/static/thumbnails")
setup()
