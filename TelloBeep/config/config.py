import json
import os, sys
from TelloBeep.logs.logger import logger

# logger = logger(name="config_setup")

# def make_absolute_path(filepath):
	
	
# 	if os.path.isabs(filepath):
# 		return filepath
	
# 	path  = os.path.dirname(os.path.dirname(__file__))
# 	path = f"{path}/{filepath}"
# 	# print(f"{__package__}")

# 	if os.name == "nt":
# 		filepath = filepath.replace("/", "\\")
# 	return path



# def load_json():
# 	if os.getenv("CONFIG_FILE"):
# 		with open(os.getenv("CONFIG_FILE"), "r") as f:
# 			config = f.read()
# 			conf = json.loads(config)
# 			logger.info("load config file path from env var")
# 		return conf


# 	if os.name == "posix":
# 		logger.info("detected system: posix (linux-like)")

# 		if os.path.exists(f"/etc/tellobeep/config.json"):
# 			logger.info("absolute path in /etc/tellobeep found")

# 			with open(f"/etc/tellobeep/config.json", "r") as f:
# 				config = f.read()
# 				conf = json.loads(config)
# 			return conf

# 		elif os.path.exists(f"{os.path.dirname(__file__)}/config.json"):
# 			logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")
# 			with open(f"{os.path.dirname(__file__)}/config.json", "r") as f:
# 				config = f.read()
# 				conf = json.loads(config)
# 			return conf
		
# 		else:

# 			print("--------	NO CONFIGURATION FILE---------\n put config file in /etc/tellobeep/config.json")
# 			return False

# 	elif os.name == "nt":
# 		logger.info("detected system: windows")

# 		APPDATA = os.getenv('APPDATA')


# 		if os.path.exists(f"{APPDATA}\\tellobeep\\config.json"):
# 			logger.info(f"absolute path in {APPDATA}\\tellobeep\\ found")

# 			with open(f"{APPDATA}\\tellobeep\\config.json", "r") as f:
# 				config = f.read()
# 				config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep")
# 				config = config.replace("/", "\\")
# 				conf = json.loads(config)
# 			return conf

# 		elif os.path.exists(f"{os.path.dirname(__file__)}\\config.json"):
# 			logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")

# 			with open(f"{os.path.dirname(__file__)}\\config.json", "r") as f:
				
# 				config = f.read()
# 				config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep/")
# 				config = config.replace("/", "\\")
# 				config = config.replace("\\", "\\\\")
				
# 				conf = json.loads(config)
# 				for elem in conf.keys():
# 					if isinstance(conf.get(elem), str):
# 						if "\\\\" in conf.get(elem):
# 							conf[elem] = conf[elem].replace("\\\\", "\\")
# 			return conf

# 		else:
# 			print("--------	NO CONFIGURATION FILE---------\n put config file in %appdata%\\tellobeep\\config.json")
# 			return False

# conf = load_json()
# if not conf:
# 	logger.critical("config file load failed")
# 	sys.exit(0)



# conf['token_file_tellonym'] = make_absolute_path(conf['token_file_tellonym'])
# conf['BAD_WORDS'] = make_absolute_path(conf['BAD_WORDS'])
# conf['thumb_path'] = make_absolute_path(conf['thumb_path'])
# conf['out_image_path'] = make_absolute_path(conf['out_image_path'])
# conf['INSTAGRAM_SESSION'] = make_absolute_path(conf['INSTAGRAM_SESSION'])
# conf['LOG_FILE'] = make_absolute_path(conf['LOG_FILE'])

# conf['fontname'] = make_absolute_path(conf['fontname'])
# conf['font_footer_name'] = make_absolute_path(conf['font_footer_name'])
# conf['font_header_name'] = make_absolute_path(conf['font_header_name'])
# conf['db_name'] = make_absolute_path(conf['db_name'])

# conf['image_path'] = make_absolute_path(conf['image_path'])
# conf['out_image_path_BACKUP'] = make_absolute_path(conf['out_image_path_BACKUP'])
# conf['out_image_name'] = make_absolute_path(conf['out_image_name'])
# conf['logger'] = None

# env = dict(os.environ)
# for elem in env:
# 	logger.info(f"use variable from environmental variables:  {elem}")
# 	conf[elem] = env[elem]




def dump_json(self):
	f = open("config.json", "w+")
	json.dump(conf, fp=f, indent=4)
	f.close()

class Config():
	def __init__(self, config_file=None, conf=None):
		self.logger = logger(name=__name__)

		if isinstance(conf, dict):
			self.conf = conf
		else:		
			self.conf = dict()

		self.conf = self.load_json(filepath=config_file)

		print(f"self.config {len(self.conf)}")

		self.load_env()

		self.parse_paths()

	def dump_json(self):
		f = open("config.json", "w+")
		json.dump(self.conf, fp=f, indent=4)
		f.close()

	def make_absolute_path(self, filepath):

		if filepath is not None and os.path.isabs(filepath):
			return filepath
		
		path  = os.path.dirname(os.path.dirname(__file__))
		path = f"{path}/{filepath}"
		# print(f"{__package__}")

		if os.name == "nt":
			filepath = filepath.replace("/", "\\")
		return path

	def parse_paths(self):
		try:
			self.conf['token_file_tellonym'] = self.make_absolute_path(self.conf['token_file_tellonym'])
			self.conf['BAD_WORDS'] = self.make_absolute_path(self.conf['BAD_WORDS'])
			self.conf['thumb_path'] = self.make_absolute_path(self.conf['thumb_path'])
			self.conf['out_image_path'] = self.make_absolute_path(self.conf['out_image_path'])
			self.conf['INSTAGRAM_SESSION'] = self.make_absolute_path(self.conf['INSTAGRAM_SESSION'])
			self.conf['LOG_FILE'] = self.make_absolute_path(self.conf['LOG_FILE'])

			self.conf['fontname'] = self.make_absolute_path(self.conf['fontname'])
			self.conf['font_footer_name'] = self.make_absolute_path(self.conf['font_footer_name'])
			self.conf['font_header_name'] = self.make_absolute_path(self.conf['font_header_name'])
			self.conf['db_name'] = self.make_absolute_path(self.conf['db_name'])

			self.conf['image_path'] = self.make_absolute_path(self.conf['image_path'])
			self.conf['out_image_path_BACKUP'] = self.make_absolute_path(self.conf['out_image_path_BACKUP'])
			self.conf['out_image_name'] = self.make_absolute_path(self.conf['out_image_name'])
			self.conf['logger'] = None
		except Exception as e:
			self.logger.warning(f"could not parse path: {e}")
			pass
		return self.conf

	def load_env(self):
		env = dict(os.environ)
		for elem in env:
			self.logger.info(f"use variable from environmental variables:  {elem}")
			self.conf[elem] = env[elem]

	def load_json(self, filepath=None):
		print(f"filepath {filepath}")

		if filepath:
			with open(os.getenv("CONFIG_FILE"), "r") as f:
				config = f.read()
				self.conf = json.loads(config)
				self.logger.info(f"load config file by passed argument {filepath}")
			return self.conf

		if os.getenv("CONFIG_FILE"):

			with open(os.getenv("CONFIG_FILE"), "r") as f:
				config = f.read()
				conf = json.loads(config)
				self.logger.info("load config file path from env var")
			return conf


		if os.name == "posix":
			self.logger.info("detected system: posix (linux-like)")

			if os.path.exists(f"/etc/tellobeep/config.json"):
				self.logger.info("absolute path in /etc/tellobeep found")

				with open(f"/etc/tellobeep/config.json", "r") as f:
					config = f.read()
					conf = json.loads(config)
				return conf

			elif os.path.exists(f"{os.path.dirname(__file__)}/config.json"):
				self.logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")
				with open(f"{os.path.dirname(__file__)}/config.json", "r") as f:
					config = f.read()
					conf = json.loads(config)
				return conf
			
			else:

				print("--------	NO CONFIGURATION FILE---------\n put config file in /etc/tellobeep/config.json")
				return False

		elif os.name == "nt":
			self.logger.info("detected system: windows")

			APPDATA = os.getenv('APPDATA')


			if os.path.exists(f"{APPDATA}\\tellobeep\\config.json"):
				self.logger.info(f"absolute path in {APPDATA}\\tellobeep\\ found")

				with open(f"{APPDATA}\\tellobeep\\config.json", "r") as f:
					config = f.read()
					config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep")
					config = config.replace("/", "\\")
					conf = json.loads(config)
				return conf

			elif os.path.exists(f"{os.path.dirname(__file__)}\\config.json"):
				self.logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")

				with open(f"{os.path.dirname(__file__)}\\config.json", "r") as f:
					
					config = f.read()
					config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep/")
					config = config.replace("/", "\\")
					config = config.replace("\\", "\\\\")
					
					conf = json.loads(config)
					for elem in conf.keys():
						if isinstance(conf.get(elem), str):
							if "\\\\" in conf.get(elem):
								conf[elem] = conf[elem].replace("\\\\", "\\")
				return conf

			else:
				print("--------	NO CONFIGURATION FILE---------\n put config file in %appdata%\\tellobeep\\config.json")
				return False

	def get_conf(self):
		return self.conf



if __name__ == "__main__":
	pass