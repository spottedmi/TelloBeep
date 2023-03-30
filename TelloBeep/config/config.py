import json
import os, sys


def make_absolute_path(filepath):
	
	
	if os.path.isabs(filepath):
		return filepath
	
	path  = os.path.dirname(os.path.dirname(__file__))
	path = f"{path}/{filepath}"
	# print(f"{__package__}")

	if os.name == "nt":
		filepath = filepath.replace("/", "\\")
	return path




if os.name == "posix":
	if os.path.exists(f"{os.path.dirname(__file__)}/config.json"):

		with open(f"{os.path.dirname(__file__)}/config.json", "r") as f:
			config = f.read()
			conf = json.loads(config)

	elif os.path.exists(f"/etc/tellobeep/config.json"):

		with open(f"/etc/tellobeep/config.json", "r") as f:
			config = f.read()
			conf = json.loads(config)
	else:

		print("--------	NO CONFIGURATION FILE---------\n put config file in /etc/tellobeep/config.json")

elif os.name == "nt":
	APPDATA = os.getenv('APPDATA')

	if os.path.exists(f"{os.path.dirname(__file__)}\\config.json"):
		with open(f"{os.path.dirname(__file__)}\\config.json", "r") as f:

			config = f.read()
			config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep")
			config = config.replace("/", "\\")
			conf = json.loads(config)

	elif os.path.exists(f"{APPDATA}\\tellobeep\\config.json"):
		with open(f"{APPDATA}\\tellobeep\\config.json", "r") as f:
			
			config = f.read()
			config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep/")
			config = config.replace("/", "\\")
			config = config.replace("\\", "\\\\")
			
			conf = json.loads(config)
			for elem in conf.keys():
				if isinstance(conf.get(elem), str):
					if "\\\\" in conf.get(elem):
						conf[elem] = conf[elem].replace("\\\\", "\\")

	else:
		print("--------	NO CONFIGURATION FILE---------\n put config file in %appdata%\\tellobeep\\config.json")



conf['token_file_tellonym'] = make_absolute_path(conf['token_file_tellonym'])
conf['BAD_WORDS'] = make_absolute_path(conf['BAD_WORDS'])
conf['thumb_path'] = make_absolute_path(conf['thumb_path'])
conf['out_image_path'] = make_absolute_path(conf['out_image_path'])
conf['INSTAGRAM_SESSION'] = make_absolute_path(conf['INSTAGRAM_SESSION'])
conf['LOG_FILE'] = make_absolute_path(conf['LOG_FILE'])

conf['fontname'] = make_absolute_path(conf['fontname'])
conf['font_footer_name'] = make_absolute_path(conf['font_footer_name'])
conf['font_header_name'] = make_absolute_path(conf['font_header_name'])
conf['db_name'] = make_absolute_path(conf['db_name'])

conf['image_path'] = make_absolute_path(conf['image_path'])
conf['out_image_path_BACKUP'] = make_absolute_path(conf['out_image_path_BACKUP'])
conf['out_image_name'] = make_absolute_path(conf['out_image_name'])
conf['logger'] = None


# for elem in conf:
# 	print(f"{elem} {conf.get(elem)}")
# sys.exit()


def dump_json(self):
	f = open("config.json", "w+")
	json.dump(conf, fp=f, indent=4)
	f.close()


# class Config(object):
# 	def __init__(self, child_class=None):	
		
# 		self.load_locals()
# 		print(conf.get("token_file_tellonym"))
# 		print(conf.get("token_file_tellonym"))



# 		if child_class:
# 			conf["logger"] = logging.getLogger(child_class)
# 			fh = logging.FileHandler(conf['LOG_FILE'])
# 			fh.setLevel(logging.DEBUG)
# 			fh.setFormatter(CustomFormatter())
# 			conf["logger"].addHandler(fh)
# 			conf["logger"].setLevel(logging.DEBUG)




	


		

# 	def dump_json(self):
# 		absolute_path = os.path.abspath(__file__)
# 		path = os.path.dirname(absolute_path) + "/"

# 		res = self.parse_locals()	
		
# 		f = open("config.json", "w+")
# 		json.dump(res, fp=f, indent=4)
# 		f.close()


# 	def parse_locals(self):
# 		x = dir(self)
# 		res = dict()
# 		for elem in x:
# 			if not elem.startswith("__") and\
# 			not  elem.endswith("__") and \
# 			not "method" in str(type(eval(f"self.{elem}"))) and\
# 			not "object at" in str(type(eval(f"self.{elem}")))  :
# 				res[elem] = eval(f"self.{elem}")

# 		return res

# 	def load_json(self):
# 		absolute_path = os.path.abspath(__file__)
# 		path = os.path.dirname(absolute_path) + "/"
# 		f = open("config.json", "r")
# 		a = f.read()
# 		x = json.loads(a)
# 		f.close()
# 		return x

# 	def load_locals(self):
# 		dic = self.load_json()
# 		self.X(dic)

# 	def X(self, dic):

# 		for elem in dic:
# 			try:
# 				elem_val = eval(f"dic.get('{elem}')")
# 			except:
# 				elem_val = eval(f'dic.get("{elem}")')	

# 			if str(type(elem_val)) == "<class 'str'>":
# 				try:
# 					exec(f'self.{elem} = "{elem_val}"')
# 				except:
# 					exec(f"self.{elem} = '{elem_val}'")
# 			else:
# 					exec(f"self.{elem} = {elem_val}")

# 	def check_err(self, err):
# 		self.ERROR = False
# 		if not isinstance(err, str):
# 			return self.ERROR

# 		for elem in conf['ERRORS']:
# 			if err in conf['ERRORS'][elem]:
# 				self.ERROR = err

# 		return self.ERROR
	
# 	def get_autorun(self):
# 		dic = self.load_json()
# 		dic = dic.get("AUTORUN")

# 		conf['AUTORUN'] = dic
# 		return dic

# 	def set_autorun(self, state):
# 		with open("config.json", "r") as f:
# 			res = f.read()
# 			if state == False:
# 				res = res.replace('"AUTORUN": true,','"AUTORUN": false,')
# 			else:
# 				res = res.replace('"AUTORUN": false,','"AUTORUN": true,')

# 		with open("config.json", "w") as f:
# 			f.write(res)





if __name__ == "__main__":
	pass