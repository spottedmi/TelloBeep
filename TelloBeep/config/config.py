import json
import os, sys
from TelloBeep.logs.logger import logger

logger = logger(name="config_setup")

def make_absolute_path(filepath):
	
	
	if os.path.isabs(filepath):
		return filepath
	
	path  = os.path.dirname(os.path.dirname(__file__))
	path = f"{path}/{filepath}"
	# print(f"{__package__}")

	if os.name == "nt":
		filepath = filepath.replace("/", "\\")
	return path



def load_json():
	if os.getenv("CONFIG_FILE"):
		with open(os.getenv("CONFIG_FILE"), "r") as f:
			config = f.read()
			conf = json.loads(config)
			logger.info("load config file path from env var")
		return conf


	if os.name == "posix":
		logger.info("detected system: posix (linux-like)")

		if os.path.exists(f"/etc/tellobeep/config.json"):
			logger.info("absolute path in /etc/tellobeep found")

			with open(f"/etc/tellobeep/config.json", "r") as f:
				config = f.read()
				conf = json.loads(config)
			return conf

		elif os.path.exists(f"{os.path.dirname(__file__)}/config.json"):
			logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")
			with open(f"{os.path.dirname(__file__)}/config.json", "r") as f:
				config = f.read()
				conf = json.loads(config)
			return conf
		
		else:

			print("--------	NO CONFIGURATION FILE---------\n put config file in /etc/tellobeep/config.json")
			return False

	elif os.name == "nt":
		logger.info("detected system: windows")

		APPDATA = os.getenv('APPDATA')


		if os.path.exists(f"{APPDATA}\\tellobeep\\config.json"):
			logger.info(f"absolute path in {APPDATA}\\tellobeep\\ found")

			with open(f"{APPDATA}\\tellobeep\\config.json", "r") as f:
				config = f.read()
				config = config.replace("/etc/tellobeep/", f"{APPDATA}/tellobeep")
				config = config.replace("/", "\\")
				conf = json.loads(config)
			return conf

		elif os.path.exists(f"{os.path.dirname(__file__)}\\config.json"):
			logger.info(f"absolute path not found, using local config in {os.path.dirname(__file__)}/config.json")

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

conf = load_json()
if not conf:
	logger.critical("config file load failed")
	sys.exit(0)



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

env = dict(os.environ)
for elem in env:
	logger.info(f"use variable from environmental variables:  {elem}")
	conf[elem] = env[elem]




def dump_json(self):
	f = open("config.json", "w+")
	json.dump(conf, fp=f, indent=4)
	f.close()



if __name__ == "__main__":
	pass