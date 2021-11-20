#! /usr/bin/python3
from queue import Queue
from threading import Thread
import time, random, json

from make_img import Make_img
from backend.server import back_server

from TellonymApi import Tellonym_api

from config import Config

#_____________________________________________________________
#
#               INSTAGRAM API
#_____________________________________________________________

class Insta_api(object):
	def __init__(self, q_list):
		"this is only a makeshift"
		"fetching api function's going to replace this"
		self.q_list = q_list
		
		self.TEXT_tmp = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum """
		self.recv_mgs()


	def recv_mgs(self) -> None:
		q = q_list.get("2insta")

		while 1 :
			content = q.get()
			print(f"INSTAGRAM {content['title']}")
			time.sleep(0.1)

#_____________________________________________________________
#
#               Tello API
#_____________________________________________________________

class Tello_api(Config):
	"send txt to generating thread"
	def __init__(self, q_list):
		super().__init__()
		"fetching api function's going to replace this"
		self.q_list = q_list
		self.tello = Tellonym_api()
		self.send_msg()

	def send_msg(self) -> None:
		"put message to the generating queue"
		while 1:
			content = self.tello.run()

			delay = 10

			while isinstance(content, str):
				print(f"ERROR >>>>>> {content}")
				self.tello = Tellonym_api()
				content = self.tello.run()
				print(f"	---------- delay: {delay}")
				time.sleep(delay)
				delay += delay
			print(f"fetched: {content}")

			for elem in content:
				#generate file name
				tm , date = elem.created_at.rsplit("T")
				y, M, d = tm.rsplit("-")
				date, mil = date.rsplit(".")
				h,m,s = date.rsplit(":")
				h = int(h) + self.TIMEZONE

				print(h)
				print(h)
				print(h)

				if h == 24:
					h = "00"

				title = f"{y}{M}{d}{h}{m}{s}_{elem.id}"
				
				req = {
					"text": elem.tell,
					"title": title,
					"metadata":elem,
					"send": False
				}

				q = q_list.get("2gen")
				q.put(req)

			time.sleep(3)



if __name__ == "__main__":
	q_list = {
		"2gen": Queue(),
		"2flask": Queue(),
		"2tello": Queue(),
		"2insta": Queue(),
	}

	
	
	#generating images
	t1 = Thread(target = Make_img, kwargs={"q_list":q_list}).start()

	#backend
	t2 = Thread(target = back_server, kwargs={"q_list":q_list}).start()
	
	#insta thread
	t3 = Thread(target = Insta_api, kwargs={"q_list":q_list}).start()
	
	#teloym thread
	t4 = Thread(target = Tello_api, kwargs={"q_list":q_list}).start()


	while 1 :		
		time.sleep(1)


