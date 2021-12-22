import json, os
import logging

class Config(object):
	def __init__(self, child_class=None):	
		
		self.load_locals()
		self.token_file = self.make_absolute_path(self.token_file)
		self.BAD_WORDS = self.make_absolute_path(self.BAD_WORDS)
		self.thumb_path = self.make_absolute_path(self.thumb_path)
		self.out_image_path = self.make_absolute_path(self.out_image_path)


		if child_class:

			self.logger = logging.getLogger(child_class)
			
			fh = logging.FileHandler(self.LOG_FILE)

			fh.setLevel(logging.DEBUG)
			fh.setFormatter(CustomFormatter())
			
			self.logger.addHandler(fh)

			self.logger.setLevel(logging.DEBUG)



	def make_absolute_path(sefl, filepath):
		absolute_path = os.path.abspath(__file__)
		path = os.path.dirname(absolute_path) + "/"
		path = f"{path}{filepath}"
		return path



		

	def dump_json(self):
		absolute_path = os.path.abspath(__file__)
		path = os.path.dirname(absolute_path) + "/"

		res = self.parse_locals()	
		
		f = open("config.json", "w+")
		json.dump(res, fp=f, indent=4)
		f.close()


	def parse_locals(self):
		x = dir(self)
		res = dict()
		for elem in x:
			if not elem.startswith("__") and\
			not  elem.endswith("__") and \
			not "method" in str(type(eval(f"self.{elem}"))) and\
			not "object at" in str(type(eval(f"self.{elem}")))  :
				res[elem] = eval(f"self.{elem}")

		return res

	def load_json(self):
		absolute_path = os.path.abspath(__file__)
		path = os.path.dirname(absolute_path) + "/"
		f = open("config.json", "r")
		a = f.read()
		x = json.loads(a)
		f.close()
		return x

	def load_locals(self):
		dic = self.load_json()
		self.X(dic)

	def X(self, dic):

		for elem in dic:
			try:
				elem_val = eval(f"dic.get('{elem}')")
			except:
				elem_val = eval(f'dic.get("{elem}")')	

			if str(type(elem_val)) == "<class 'str'>":
				try:
					exec(f'self.{elem} = "{elem_val}"')
				except:
					exec(f"self.{elem} = '{elem_val}'")
			else:
					exec(f"self.{elem} = {elem_val}")

	def check_err(self, err):
		self.ERROR = False
		if not isinstance(err, str):
			return self.ERROR

		for elem in self.ERRORS:
			if err in self.ERRORS[elem]:
				self.ERROR = err

		return self.ERROR
	
	def get_autorun(self):
		dic = self.load_json()
		dic = dic.get("AUTORUN")

		self.AUTORUN = dic
		return dic

	def set_autorun(self, state):
		with open("config.json", "r") as f:
			res = f.read()
			if state == False:
				res = res.replace('"AUTORUN": true,','"AUTORUN": false,')
			else:
				res = res.replace('"AUTORUN": false,','"AUTORUN": true,')

		with open("config.json", "w") as f:
			f.write(res)





class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


if __name__ == "__main__":
	c = Config()
