
from TelloBeep.email.email_fetcher import Mail_fetcher
from TelloBeep.logs.logger import logger



import subprocess, time

class Bypass_email():
	def __init__(self, conf=None):
		if conf:
			self.conf = conf
		

		self.logger = logger(name=f"{self.conf.get('instance')}_{__name__}")
		
		self.logger.warning("bypass init")

		self.comm = f'''
from instagrapi import Client\n
import sys\n
cl = Client()\n
i = cl.login("{self.conf['LOGIN_INSTAGRAM']}","{self.conf['PASSWORD_INSTAGRAM']}")\n
cl.dump_settings("{self.conf['INSTAGRAM_SESSION']}")\n
print(f"logged to the instagram account: "+ str(i))\n
'''

		self.command = f'''python -c '{self.comm}'  '''
		self.logger.warning(f"{self.command}")

	def run_process(self):
		self.logger.info("running process")
		# self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		self.process = subprocess.Popen(['python', '-c', self.comm], stcdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
		
		self.logger.info("process runned")
		return self.process

	def check_process(self):
		self.logger.warning("check process init")
		

		self.run_process()
		self.logger.warning("process runned 2")
		i = 0
		while i<100:
			self.logger.info("while loop")
			output = ""
			break_crit = 0
			# while len(output) < 5 or break_crit < 200:
			# while True:
			while len(output) < 5:
				print(1)
				# output = self.process.stdout.readline()
				output = process.stdout.readline().strip()
				# print(f"output {output}")
				# if self.conf['LOGIN_INSTAGRAM'] in output:
				#     break
				print(2)
				output = output.decode("utf-8")
				print(3)
				print(len(output))
				print(4)
				self.logger.info(f"{output}")
				print(5)
				break_crit+1
				print(6)
				time.sleep(2)

			
			self.logger.debug(f"process output: {output}")
			if "logged to the instagram account: True" in output:

				self.logger.debug(f"process output: {output}")
				break
				return True
			elif "RateLimitError" in output:
				print("RateLimitError")
			elif self.conf['LOGIN_INSTAGRAM'] in output:
			# else:
				# code = input("CODE: ")
				self.logger.warning("run mail fetcher")

				e = Mail_fetcher()
				code = e.get_code()
				print(code)
				print(code)
				print(code)
				print(code)
				print(code)
				inp = f"{code}\n"
				self.process.stdin.write(inp.encode("utf-8"))
				self.process.stdin.flush()  
				output, error = self.process.communicate()

			i+=1
			time.sleep(1)
		return False

