
from TelloBeep.email.email_fetcher import Mail_fetcher
from TelloBeep.logs.logger import logger

from TelloBeep.config import conf

import subprocess, time

class Bypass_email():
	def __init__(self):
		self.logger = logger(name = __name__)
		self.logger.warning("bypass init")

		self.comm = f'''
from instagrapi import Client\n
cl = Client()\n
i = cl.login("{conf['LOGIN_INSTAGRAM']}","{conf['PASSWORD_INSTAGRAM']}")\n
cl.dump_settings("{conf['INSTAGRAM_SESSION']}")\n
print(f"logged to the instagram account: "+ str(i))\n
'''

		self.command = f'''python -c '{self.comm}'  '''

	def run_process(self):
		self.logger.info("running process")
		self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
		self.logger.info("process runned")
		return self.process

	def check_process(self):
		self.logger.warning("check process init")
		

		self.run_process()
		self.logger.warning("process runned 2")
		it = 0
		while i<100:
			self.logger.info("while loop")
			output = ""
			while len(output) < 5:
				output = self.process.stdout.readline()
				output = output.decode("utf-8")
				self.logger.info(output)
				time.sleep(1)

			
			self.logger.debug(f"process output: {output}")
			if "logged to the instagram account: True" in output:

				self.logger.debug(f"process output: {output}")
				break
				return True
			else:
				# code = input("CODE: ")
				self.logger.warning("run mail fetcher")

				e = Mail_fetcher()
				code = e.get_code()

				self.process.stdin.write(f"{code}\n".encode())
				self.process.stdin.flush()  
				output, error = self.process.communicate()

			i+=1
			time.sleep(1)
		return False

