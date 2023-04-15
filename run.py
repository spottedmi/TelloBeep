#! /usr/bin/python3
from queue import Queue
import time, random, json, os, sys
import multiprocessing

from TelloBeep.image_generation.make_img import Make_img
# from TelloBeep.backend.server import back_server
from TelloBeep.notify import Discord_bot

from TelloBeep.api.handlers.insta import Insta_api
from TelloBeep.api.handlers.tellonym import Tello_api
from TelloBeep.api.handlers.fetching import Fetching_api

# 
from TelloBeep.config import Config
from TelloBeep.logs.logger import logger

from importlib import import_module



class StartUp():
	def __init__(self):
		# Logger()
		self.logger = logger(__name__)
		pid = os.getpid()

		os.popen(f"prlimit -n524288 -p {pid}")
		# os.popen(f"prlimit -n4 -p {pid}")
		# print(f"prlimit -n524288 -p {pid}")
		self.logger.critical("_____Tellobeep INIT___________________________________")
		self.logger.info("prlimit set")

class TelloBeep():

	def __init__(self, config=None):	
		# Config()
		print("init")
		

		config_class = Config(config_file=config)
		self.conf = config_class.get_conf()
		print(len(self.conf))

		# Make_img(conf=self.conf)

		# sys.exit(0)

		self.logger = logger(__name__)

		self.manager = multiprocessing.Manager()

		self.q_list = {
			"2gen": self.manager.Queue(),
			"2flask": self.manager.Queue(),
			"2tello": self.manager.Queue(),
			"2insta": self.manager.Queue(),
			"2main_thread": self.manager.Queue(),
		}
		
		
		start = StartUp()

	def run(self):
		print(self.conf.get("BACKEND_PORT"))
		
		
		processes = {}
		server = import_module('TelloBeep.backend.server')
		
		back_server = server.back_server
		back_server.conf = self.conf
		server.app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{self.conf['db_name']}"

		apps = [Make_img, back_server, Insta_api, Fetching_api, Discord_bot]

		n = 0
		for app in apps:
			self.logger.info(f"__init process__ {app}")
			p = multiprocessing.Process(target = app, kwargs={"q_list": self.q_list, "conf":self.conf})
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

						p = multiprocessing.Process(target = a, kwargs={"q_list": self.q_list, "conf":self.conf})
						p.daemon = True 
						p.start()
						
						processes[n] = (p, a)

			time.sleep(5)


if __name__ == "__main__":
	tellobeep = TelloBeep()
	tellobeep.run()