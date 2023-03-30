#! /usr/bin/python3
from queue import Queue
import time, random, json, os, sys
import multiprocessing

from TelloBeep.image_generation.make_img import Make_img
from TelloBeep.backend.server import back_server
from TelloBeep.notify import Discord_bot

from TelloBeep.api.handlers.insta import Insta_api
from TelloBeep.api.handlers.tellonym import Tello_api
from TelloBeep.api.handlers.fetching import Fetching_api

from TelloBeep.config import conf
from TelloBeep.logs.logger import logger



class StartUp():
	def __init__(self):
		global conf
		# Logger()
		self.logger = logger(__name__)
		pid = os.getpid()

		os.popen(f"prlimit -n524288 -p {pid}")
		# os.popen(f"prlimit -n4 -p {pid}")
		# print(f"prlimit -n524288 -p {pid}")
		self.logger.critical("_____Tellobeep INIT___________________________________")
		self.logger.info("prlimit set")

class Start():

	def __init__(self):	
		# Config()
		self.logger = logger(__name__)

		manager = multiprocessing.Manager()

		q_list = {
			"2gen": manager.Queue(),
			"2flask": manager.Queue(),
			"2tello": manager.Queue(),
			"2insta": manager.Queue(),
			"2main_thread": manager.Queue(),
		}
		
		

		print(self.logger)
		print("---------------AFTER")
		start = StartUp()
		print(self.logger)

		processes = {}
		apps = [Make_img, back_server, Insta_api, Fetching_api, Discord_bot]

		n = 0
		for app in apps:
			self.logger.info(f"__init process__ {app}")
			p = multiprocessing.Process(target = app, kwargs={"q_list": q_list})
			p.daemon = True
			p.start()

			processes[n] = (p, app) # Keep the process and the app to monitor or restart
			n += 1
			self.logger.info(f"process run, status ok")




		while 1 :
			while len(processes) > 0:
				for n in processes.keys():
					(p, a) = processes[n]
					time.sleep(0.5)

					if not p.is_alive():
						print(f"class {a} returned error, {p}")

						self.logger.warning(f"process {a} raised an error {p.exitcode}, restarting...")

						p = multiprocessing.Process(target = a, kwargs={"q_list": q_list})
						p.daemon = True 
						p.start()
						
						processes[n] = (p, a)

			time.sleep(5)


if __name__ == "__main__":
	Start()