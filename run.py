#! /usr/bin/python3
from queue import Queue
import time, random, json, os, sys

from TelloBeep.image_generation.make_img import Make_img
from TelloBeep.backend.server import back_server

from TelloBeep.api import Tellonym_api
from TelloBeep.api import Questionmi_api
from TelloBeep.api import Instagram_api
# from api.Instagram_Api import Instagram_api

from instagrapi.exceptions import PleaseWaitFewMinutes, RateLimitError
from TelloBeep.config import conf

# from discord.discord_bot import Discord_bot
# from discord.notifications import Notify
from TelloBeep.notify import Discord_bot
from TelloBeep.notify import Notify


from TelloBeep.logs.logger import Logger
import multiprocessing
#_____________________________________________________________
#
#               INSTAGRAM API
#_____________________________________________________________

class Insta_api():
	def __init__(self, q_list):
		
		
		print("instaapi")

		"this is only a makeshift"
		"fetching api function's going to replace this"

		self.q_list = q_list
		self.insta = Instagram_api(q_list=self.q_list)

		delay = 10
		while True:
			try:
				self.insta.login()
				break
			except PleaseWaitFewMinutes :
				Notify(q_list=self.q_list, error="PLEASE_WAIT_FEW_MINUTES")
				conf['logger'].warning(f"PLEASE_WAIT_FEW_MINUTES instagram login delay: {delay}")

				time.sleep(delay)
			except RateLimitError:
				Notify(q_list=self.q_list, error="RATE_LIMIT_ERROR")
				conf['logger'].warning(f"RATE_LIMIT_ERROR instagram login delay: {delay}")

				# time.sleep(delay)

			except Exception as e:
				print(e)
				Notify(q_list=self.q_list, error="INSTAGRAM_ERROR")
			
			time.sleep(delay)
			delay += 2 * delay





		self.recv_mgs()

	def recv_mgs(self) -> None:
		q = self.q_list.get("2insta")

		while 1 :
			content = q.get()
			# print(f"INSTAGRAM {content['title']}")

			path = f"{conf['out_image_path']}/{content['filename']}"

			if conf['CAPTION'] != "":
				pass
				self.insta.upload_post(path, caption=conf['CAPTION'])
			else:
				pass
				self.insta.upload_post(path)
			# print("instagram sent")

			time.sleep(0.1)

#_____________________________________________________________
#
#               Tello API
#_____________________________________________________________

class Tello_api():
	"send txt to generating thread"
	def __init__(self, q_list, fetch_class):
		
		"fetching api function's going to replace this"
		conf['logger'].info(f"Tello_api init, fetch_class: {fetch_class}")

		self.fetch_class = fetch_class


		# time.sleep(10)

		self.q_list = q_list
		# self.tello = Tellonym_api(q_list=self.q_list)
		self.send_msg()
		

	def send_msg(self) -> None:
		"put message to the generating queue"
		
		while 1:
			
			delay = 10
			while 1:
				try:
					self.tello = self.fetch_class(q_list=self.q_list)
					
					content = self.tello.run()
					
					# print(f"content {content}")
					conf['logger'].info(f"new fetch: {content}")
					break

				except Exception as e:
					conf['logger'].info(f"exception when fetching {self.fetch_class}: {e}, delay: {delay}")
					time.sleep(delay)
					delay+=delay
					del self.tello
					conf['logger'].info(f"tellonym user deleted")

					print(f"fetch: error: {e}")

					# content = self.tello.run()
					time.sleep(10)




			if len(content) > 0:
				conf['logger'].info(f"new Tellonyms: {len(content)}")
				# print(f"fetched: {content[0].tell} ")


			for elem in content:	
				conf['logger'].info(f"loop of tellonyms")
				#generate file name
				if "." not in elem.created_at:
					elem.created_at += ".00Z"
				tm , date = elem.created_at.rsplit("T")
				y, M, d = tm.rsplit("-")
				if len(M) == 1: M = f"0{M}"
				date, mil = date.rsplit(".")
				
				h,m,s = date.rsplit(":")
				h = str(int(h) + conf['TIMEZONE'])

				if len(h) == 1: h = f"0{h}"
				if len(m) == 1: m = f"0{m}"
				if len(s) == 1: s = f"0{s}"
		
				if h == 24:
					conf['logger'].info(f"24 hour detected")
					h = "00"

				title = f"{y}{M}{d}{h}{m}{s}_{elem.id}"
				conf['logger'].info(f"title: {title}")
				req = {
					"text": elem.tell,
					"title": title,
					"metadata":elem,
					"send": False,
					"censure_flag": elem.flag,
					"users_ip": elem.users_ip,
				}
				conf['logger'].info(f"{req}")

				q = q_list.get("2gen")
				Notify(q_list=self.q_list, error=f"new tellonym ({elem.tell})")
				conf["logger"].info("pushed to queue")

				q.put(req)
			time.sleep(5)

				

class StartUp():
	def __init__(self):
		Logger()
		pid = os.getpid()
		
		os.popen(f"prlimit -n524288 -p {pid}")
		# os.popen(f"prlimit -n4 -p {pid}")
		# print(f"prlimit -n524288 -p {pid}")
		conf["logger"].critical("_____Tellobeep INIT___________________________________")
		conf["logger"].info("prlimit set")



if __name__ == "__main__":
	# Config()
	manager = multiprocessing.Manager()

	q_list = {
		"2gen": manager.Queue(),
		"2flask": manager.Queue(),
		"2tello": manager.Queue(),
		"2insta": manager.Queue(),
		"2main_thread": manager.Queue(),
	}
	
	
	start = StartUp()
	
	#generating images
	t1 = multiprocessing.Process(target = Make_img, kwargs={"q_list":q_list})
	t1.daemon = True
	t1.start()
	
	#backend
	t2 = multiprocessing.Process(target = back_server, kwargs={"q_list":q_list})
	t2.daemon = True
	t2.start()
	
	#insta thread
	t3 = multiprocessing.Process(target = Insta_api, kwargs={"q_list":q_list})
	t3.daemon = True
	t3.start()
	
	#teloym thread
	# t4 = multiprocessing.Proces(target = Tello_api, kwargs={"q_list":q_list, "fetch_class":Tellonym_api}).start()
	t4 = multiprocessing.Process(target = Tello_api, kwargs={"q_list":q_list, "fetch_class":Questionmi_api})
	t4.daemon = True
	t4.start()
	
	# #discord notifications
	# t5 = Thread(target = Discord_bot, kwargs={"q_list":q_list}).start()

	while 1:		
		try:
			Discord_bot(q_list)

		except OSError:
			conf['logger'].critical(f"closing... OSError Too many open files")
			for elem in multiprocessing.active_children():
				elem.terminate()
			conf['logger'].critical(f"all processes killed, exiting main thread")

			sys.exit(0)

		except Exception as e:
			print("cannot log into bot")
			time.sleep(10)




