#! /usr/bin/python3
from queue import Queue
from threading import Thread
import time, random, json

from make_img import Make_img
from backend.server import back_server

from TellonymApi import Tellonym_api

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
			time.sleep(0.1)

#_____________________________________________________________
#
#               INSTAGRAM API
#_____________________________________________________________

class Tello_api(object):
	"send txt to generating thread"
	def __init__(self, q_list):
		"fetching api function's going to replace this"
		self.q_list = q_list
		self.tello = Tellonym_api()
		self.send_msg()

	def send_msg(self) -> None:
		"put message to the generating queue"
		while 1:
			content = self.tello.run()
			for elem in content:

				#generate file name
				t = time.localtime()
				y = f"{t.tm_year}"if len(str(t.tm_year)) == 4 else f"0{t.tm_year}"
				M = f"{t.tm_mon}" if len(str(t.tm_mon)) == 2 else f"0{t.tm_mon}"
				d = f"{t.tm_mday}"if len(str(t.tm_mday)) == 2 else f"0{t.tm_mday}"
				h = f"{t.tm_hour}"if len(str(t.tm_hour)) == 2 else f"0{t.tm_hour}"
				m = f"{t.tm_min}" if len(str(t.tm_min)) == 2 else f"0{t.tm_min}"
				s = f"{t.tm_sec}" if len(str(t.tm_sec)) == 2 else f"0{t.tm_sec}"
				mil = int(round(time.time() * 1000))
				
				# title = current date + tellonym id
				title = f"{y}{M}{d}{h}{m}{s}{mil}_{elem.id}"
				
				req = {
					"text": elem.tell,
					"title": title,
					"metadata":elem
				}
				
				q = q_list.get("2gen")
				q.put(req)

			time.sleep(1)



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


