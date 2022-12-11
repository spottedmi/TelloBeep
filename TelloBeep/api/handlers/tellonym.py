from queue import Queue
import time, random, json, os, sys

from TelloBeep.api import Tellonym_api
from TelloBeep.config import conf
from TelloBeep.notify import Notify


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
					raise e

					# content = self.tello.run()
					time.sleep(10)




			if len(content) > 0:
				conf['logger'].info(f"new Tellonyms: {len(content)}")
				# print(f"fetched: {content[0].tell} ")


			for elem in content:	
				conf['logger'].info(f"loop of tellonyms")
				

				# tm , date = elem.created_at.rsplit("T")
				# y, M, d = tm.rsplit("-")
				# if len(M) == 1: M = f"0{M}"
				# date, mil = date.rsplit(".")
				
				# h,m,s = date.rsplit(":")

				# if len(h) == 1: h = f"0{h}"
				# if len(m) == 1: m = f"0{m}"
				# if len(s) == 1: s = f"0{s}"
		
				# if h == 24:
				# 	conf['logger'].info(f"24 hour detected")
				# 	h = "00"

				# title = f"{y}{M}{d}{h}{m}{s}_{elem.id}"
				conf['logger'].info(f"title: {elem.title}")
				
				# req = {
				# 	"text": elem.tell,
				# 	"title": title,
				# 	"metadata":elem,
				# 	"send": False,
				# 	"censure_flag": elem.flag,
				# 	"users_ip": elem.users_ip,
				# }
				# conf['logger'].info(f"{req}")
				conf['logger'].info(f"{elem}")

				q = self.q_list.get("2gen")
				Notify(q_list=self.q_list, error=f"new tellonym ({elem})")
				conf["logger"].info("pushed to queue")

				q.put(elem)
			time.sleep(5)

				