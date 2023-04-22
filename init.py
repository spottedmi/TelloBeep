#! /usr/bin/python3
from TelloBeep.backend.server import setup

import os
try:
	os.mkdir("TelloBeep/imgs")
except Exception as e:
	print(e)
try:
	os.mkdir("TelloBeep/backend/static/thumbnails")
except Exception as e:
	print(e)
try:
	os.remove("TelloBeep/database/db.sqlite")
except:
	pass
setup()
