#! /usr/bin/python3
from queue import Queue
from threading import Thread
import time, random, json, os

from make_img import Make_img
from backend.server import back_server

from TellonymApi import Tellonym_api
from QuestionmiApi import Questionmi_api
from Instagram_Api import Instagram_api
from discord_bot import Discord_bot
from instagrapi.exceptions import PleaseWaitFewMinutes, RateLimitError
from config import Config
from notifications import Notify

#_____________________________________________________________
#
#               INSTAGRAM API
#_____________________________________________________________

class Insta_api(Config):
	def __init__(self, q_list):
		super().__init__(child_class=__class__.__name__)
		
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
				time.sleep(delay)
				delay += 2*delay
			except RateLimitError:
				Notify(q_list=self.q_list, error="RATE_LIMIT_ERROR")
				time.sleep(60)
			except Exception as e:
				# print(e)
				Notify(q_list=self.q_list, error="INSTAGRAM_ERROR")




		self.recv_mgs()

	def recv_mgs(self) -> None:
		q = self.q_list.get("2insta")

		while 1 :
			content = q.get()
			# print(f"INSTAGRAM {content['title']}")

			path = f"{self.out_image_path}/{content['filename']}"

			if self.CAPTION != "":
				pass
				self.insta.upload_post(path, caption=self.CAPTION)
			else:
				pass
				self.insta.upload_post(path)
			# print("instagram sent")

			time.sleep(0.1)

#_____________________________________________________________
#
#               Tello API
#_____________________________________________________________

class Tello_api(Config):
	"send txt to generating thread"
	def __init__(self, q_list, fetch_class):
		super().__init__(child_class=__class__.__name__)
		"fetching api function's going to replace this"
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
					# self.logger.info(f"new fetch: {content}")

					break
				except Exception as e:
					time.sleep(delay)
					delay+=delay
					print(f"fetch: error: {e}")

					# content = self.tello.run()

			time.sleep(5)



			if len(content) > 0:
				self.logger.info(f"new Tellonyms: {len(content)}")
				# print(f"fetched: {content[0].tell} ")


			for elem in content:

				#generate file name
				if "." not in elem.created_at:
					elem.created_at += ".00Z"
				tm , date = elem.created_at.rsplit("T")
				y, M, d = tm.rsplit("-")
				if len(M) == 1: M = f"0{M}"
				date, mil = date.rsplit(".")
				
				h,m,s = date.rsplit(":")
				h = str(int(h) + self.TIMEZONE)

				if len(h) == 1: h = f"0{h}"
				if len(m) == 1: m = f"0{m}"
				if len(s) == 1: s = f"0{s}"
		
				if h == 24:
					h = "00"

				title = f"{y}{M}{d}{h}{m}{s}_{elem.id}"
				
				req = {
					"text": elem.tell,
					"title": title,
					"metadata":elem,
					"send": False,
					"censure_flag": elem.flag
				}

				q = q_list.get("2gen")
				Notify(q_list=self.q_list, error=f"new tellonym ({elem.tell})")


				q.put(req)
				



if __name__ == "__main__":
	q_list = {
		"2gen": Queue(),
		"2flask": Queue(),
		"2tello": Queue(),
		"2insta": Queue(),
		"2main_thread": Queue(),
	}
	
	class StartUp(Config):
		def __init__(self):
			super().__init__(self.__class__.__name__)
			pid = os.getpid()
			
			os.popen(f"prlimit -n524288 -p {pid}")
			# os.popen(f"prlimit -n4 -p {pid}")
			# print(f"prlimit -n524288 -p {pid}")
			self.logger.critical("_____Tellobeep INIT___________________________________")


	
	start = StartUp()
	
	#generating images
	t1 = Thread(target = Make_img, kwargs={"q_list":q_list}).start()

	#backend
	t2 = Thread(target = back_server, kwargs={"q_list":q_list}).start()
	
	#insta thread
	t3 = Thread(target = Insta_api, kwargs={"q_list":q_list}).start()
	
	#teloym thread
	t4 = Thread(target = Tello_api, kwargs={"q_list":q_list, "fetch_class":Questionmi_api}).start()
	# t4 = Thread(target = Tello_api, kwargs={"q_list":q_list, "fetch_class":Tellonym_api}).start()
	
	# #discord notifications
	# t5 = Thread(target = Discord_bot, kwargs={"q_list":q_list}).start()


	while 1 :		

		try:
			Discord_bot(q_list)
		except OSError:
			start.logger.critical("closing OSError Too many open files")
			sys.exit(0)

		except Exception as e:
			print("cannot log into bot")
			t3 = Thread(target = Insta_api, kwargs={"q_list":q_list}).start()
			time.sleep(10)



