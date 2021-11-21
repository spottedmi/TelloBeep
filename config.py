import json, os

class Config(object):
	def __init__(self):

		#____________________________________
		#
		#			make_img
		#____________________________________

		# #footer
		# self.TEXT_footer = """#FOOTER_TEXT_FOOTER_TEXT"""

		# #metadata
		# self.out_image_name = "image.png"
		# self.out_image_path = "imgs"
		# self.extension = "png"

		# #thumbnails
		# self.thumb_path = "backend/static/thumbnails"
		# self.thumb_res = (300, 300)

		# #margins
		# self.margin = {
		# 	"top":20,
		# 	"right":20,
		# 	"bottom":20,
		# 	"left":20
		# }
		# self.height = 0
		# self.width = 0
		# self.img_object = None

		# #fonts
		# self.fontname = "/usr/share/fonts/TTF/Arial.TTF"
		# self.fontsize = 31
		# self.font = None

		# #footer config
		# self.font_footer_name = "./Anton.ttf"
		# self.font_footer_size = 65
		# self.font_footer = None
		# self.footer_height = 100
		# #footer image config
		# self.image_path = "./LogoTemplate.png"
		# self.image_size = (250, 250)

		# #header 
		# self.DATE = None

		# #colors
		# self.colorBackground= "#1C1936"
		# self.colorOutline = "#ffffff"
		# self.colorText  = "#ffffff"

		# #text config
		# self.word_break = 10


		# #outline
		# self.outline_thickness = 4

		# #instagram resolution
		# self.insta_res = (1080, 1080)
		# # self.insta_res = (1350, 1080)
		# # self.insta_res = (1608, 1080)

		# #db config
		# self.db_name = "db.sqlite"
		# self.db_tables = {
		# 	"posts": "posts",
		# 	"users": "users"
		# }

		# self.BAD_WORDS = 'swears_list.txt'



		# #____________________________________
		# #
		# #			censorship
		# #____________________________________
		# self.swears_list = None

		# #____________________________________
		# #
		# #			TellonymApi
		# #____________________________________

		# self.user = None
		# self.tells = []
		# self.token_file = "token.txt"

		# # LOGIN = None
		# # PASSWORD = None

		# self.LOGIN = "asdf"
		# self.PASSWORD = "asf"


		# self.headers = {
		# 		'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
		# 		'content-type': 'application/json;charset=utf-8',
		# 		'Host': 'api.tellonym.me',
		# 		'Origin': 'https://tellonym.me',
		# 		'Sec-Fetch-Dest': 'empty',
		# 		'Sec-Fetch-Mode': 'cors',
		# 		'Sec-Fetch-Site': 'same-site',
		# 		'Sec-GPC': '1',
		# 		'TE': 'trailers',
		# 		'tellonym-client': 'web:0.59.4',
		# 		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
		# 	}

	
		print("CONFIG INIT")
		
		self.load_locals()
		self.make_absolute_path(self.token_file)
		self.make_absolute_path(self.BAD_WORDS)
		self.make_absolute_path(self.thumb_path)
		self.make_absolute_path(self.out_image_path)

	def make_absolute_path(sefl, path):
		absolute_path = os.path.abspath(__file__)
		path = os.path.dirname(absolute_path) + "/"
		path = f"{path}/{path}"
		return path



		

	def dump_json(self):
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
		f = open(path + "config.json", "r")
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






if __name__ == "__main__":
	c = Config()
