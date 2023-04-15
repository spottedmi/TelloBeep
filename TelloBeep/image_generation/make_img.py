#!/usr/bin/python3
#by RandomGuy90 A.D.2021

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random, time, sys, json

from queue import Queue
import _thread, random

from TelloBeep.censorship.censorship import Censorship
from TelloBeep.database.db_connector import Db_connector



from TelloBeep.notify import Notify

from TelloBeep.logs.logger import logger


class Make_img(Censorship, Db_connector):
	def __init__(self, q_list=None, conf=None):
		if conf:
			self.conf = conf
		

		super().__init__(q_list=q_list, conf=self.conf)
		self.logger = logger(name=f"{conf.get('instance')}_{__name__}")
		

		

		self.FIRST_POST = None
		self.HOURS_PASSED = 0
		self.ALERT_SEND = False
		self.WARNING_SEND = False
		self.censor_flag = False
		self.tell_ip = ""
		

		if q_list:
			self.q_list = q_list
			self.load_from_threads()

	def gen(self) -> None:
		"generate image"
		xd = self.conf
		self.logger.info(f"generating new image")

	
		self.prepare_text()

		try:
			self.get_fonts()
			self.logger.error(f"fonts imported")

		except Exception as e:
			
			# Notify(q_list=self.q_list, error="FONT_NOT_FOUfND")
			self.logger.error(f"font not found error: {e}")
			

			sys.exit(1)

		self.get_size_txt()
		self.set_margins()
	
		# img = Image.new('RGB', (self.conf['width'], self.conf['height']), self.hex_to_rgb(self.conf['colorBackground']))
		self.get_bg_color()
		self.logger.error(f"image background color {self.bg_color}")

		
		self.img_object = Image.new('RGB', (self.conf['width'], self.conf['height']), self.hex_to_rgb(self.bg_color))
		rand = random.randrange(0, 50)
		self.logger.error(f"image random generating {rand} == 1")


		if rand == 1:
		# print(rand)
		# if rand > 1:
			self.img_object = self.gen_gradient_img(self.conf['height'], self.conf['width'])
			self.logger.error(f"image generate special gradient")


		
		d = ImageDraw.Draw(self.img_object)

		#text 
		coords =(self.conf['margin']["left"] ,self.conf['margin']["top"])
		
		if coords[1] < 20:
			coords =(coords[0] ,130)

		self.check_height()
		d.text(coords, self.TEXT, fill=self.hex_to_rgb(self.conf['colorText']), font=self.font)
		d.rectangle((0, 0, self.conf['width']-self.conf['outline_thickness'], self.conf['height']-self.conf['outline_thickness']),width= self.conf['outline_thickness'], fill=None, outline=self.hex_to_rgb(self.conf['colorOutline']))

		#header
		self.create_header()
		self.logger.error(f"image: create header")


		#footer
		self.create_footer()

		#watermark
		if self.conf.get("watermark"):
			self.create_watermark()


		self.logger.error(f"image: create footer")

		#icon generation
		img = Image.open(self.conf['image_path'], "r")
		img = img.resize(self.conf['image_size'], Image.ANTIALIAS)
		self.logger.info(f"image: resizing")

		img = img.convert("RGBA")
		self.logger.info(f"image: converting to RGBA")

		coords = (int(self.conf['insta_res'][1]*self.conf['logo_X_ratio']), int(self.conf['insta_res'][0]*self.conf['logo_Y_ratio']))

		self.img_object.paste(img, coords, img)

		#resizing and prepare to save
		img = img.convert("RGB")
		# img = Image.alpha_composite(img, d)    
		# self.img_object = self.img_object.putalpha(d)


		
		self.save_img()
		self.logger.info(f"image: saving image")

		self.save_tumbnail()
		self.logger.info(f"image: saving thumbnail")

		self.db_add_img()
		self.logger.info(f"image: adding to database")

	

		insta = self.q_list.get("2insta")  if self.q_list else None
		self.req = {
			"filename": f"{self.conf['out_image_name']}.{self.conf['extension']}",
			"title": self.TEXT,
			"send": False
		}

		self.edit_ratio()

		if self.conf['AUTORUN'] and not self.censor_flag:
			self.req["send"] = True

			if insta: insta.put(self.req)
			self.logger.info(f"image send automatically, {self.req['filename']}")
			self.SENT = True


	
	def check_height(self):
		if self.TEXT.count("\n") > 20:
			x = self.TEXT.split("\n")
			ret = ""
			for index, elem in enumerate(x):
				ret = ret+elem+"\n"
				if index > 20:
					self.TEXT = ret
					break

		self.TEXT = self.TEXT[0:1000]



	def save_img(self):
		self.img_object = self.img_object.resize(self.conf['insta_res'], Image.ANTIALIAS)
		self.filename = f"{self.conf['out_image_path']}/{self.conf['out_image_name']}.{self.conf['extension']}"
		try:
			self.img_object.save(self.filename)
		except FileNotFoundError:
			Notify(q_list=self.q_list,error="CANT_SAVE_IMG")
			self.logger.error(f" couldn't save image, {self.filename}")

			try:
				self.filename = f"{self.conf['out_image_path_BACKUP']}/{self.conf['out_image_name']}.{self.conf['extension']}"

				self.img_object.save(self.filename)
			except FileNotFoundError:
				Notify(q_list=self.q_list,error="CANT_SAVE_IMG_BACK")
				self.logger.critical(f" couldn't save image in backup location, {self.filename}")

				sys.exit(1)




	def save_tumbnail(self):
		self.img_object = self.img_object.resize(self.conf['thumb_res'], Image.ANTIALIAS)
		self.img_object.save(f"{self.conf['thumb_path']}/{self.conf['out_image_name']}_thumbnail.{self.conf['extension']}")
		
	def get_bg_color(self):
		if isinstance(self.conf['colorBackground'], list):
			x = random.randrange(0, len(self.conf['colorBackground'])-1)
			self.bg_color = self.conf['colorBackground'][x]
		else:
			self.bg_color = self.conf['colorBackground']

	def edit_ratio(self):
		# self.conf['POST_RATIO'] += 1
		self.conf['POST_COUNT'] += 1

		if self.FIRST_POST == None:
			self.FIRST_POST = int(time.time())
			self.logger.warning(f"first post {self.FIRST_POST}")		


		self.HOURS_PASSED = int(time.time()) 
		self.HOURS_PASSED = ( self.HOURS_PASSED - self.FIRST_POST )/ 3600
		# self.HOURS_PASSED = self.HOURS_PASSED * 40
		self.logger.warning(f"HOURS_PASSED {self.HOURS_PASSED} ({self.HOURS_PASSED*60})")		


		self.conf['POST_RATIO'] = int(self.conf['POST_COUNT'] / 1)
		# if self.HOURS_PASSED:
		if self.HOURS_PASSED > 1:	
			self.FIRST_POST = int(time.time())
			self.conf['POST_COUNT'] = 1
			self.conf['POST_RATIO'] = 1


		# 	self.conf['POST_RATIO'] = int(self.conf['POST_COUNT'] / self.HOURS_PASSED)
		# 	# self.conf['POST_RATIO'] = self.conf['POST_RATIO'] * 100
		# else:
		# 	# self.HOURS_PASSED = 1.1
		# 	self.conf['POST_RATIO'] = int(self.conf['POST_COUNT'] / 1)


		self.logger.warning(f"post ratio: {self.conf['POST_RATIO']} posts: {self.conf['POST_COUNT']} hours: {self.HOURS_PASSED}")		

		
		if self.conf['POST_RATIO'] >= self.conf['POST_RATIO_ALERT']:
			self.logger.warning(f" post ratio alert, autorun off, {self.conf['POST_RATIO']}")

			print('-------------  TO MAY POSTS, AUTO RUN OFF')
			
			self.db_set_approved(state=None)
		
			# self.set_autorun(False)
			self.conf['AUTORUN'] = False
			# self.get_autorun()

			if self.ALERT_SEND == False:
				# d.put(self.req)
				Notify(q_list=self.q_list,error="POST_RATIO_ALERT", img=self.req.get("filename"))
				self.ALERT_SEND = True
				self.logger.warning(f"image: post ratio - ALERT")




		elif self.conf['POST_RATIO'] >= self.conf['POST_RATIO_WARNING']:
			print("POSTS ALERT ALERTTTT!!!!")
			self.logger.warning(f" post ratio warning, {self.conf['POST_RATIO']}")		

			if self. WARNING_SEND == False:
				# d.put(self.req)
				Notify(q_list=self.q_list ,error="POST_RATIO_WARNING", img=self.req.get("filename"))
				self.WARNING_SEND = True
		
		if self.conf['POST_RATIO'] < self.conf['POST_RATIO_ALERT']:
			self.conf['AUTORUN'] = True
			# self.set_autorun(True)

		self.logger.info(f"image: post ratio: {self.conf['POST_RATIO']} autorun: {self.conf['AUTORUN']}")



		# if (self.FIRST_POST - time.time()) > 3600000:
		# 	self.HOURS_PASSED +=1
	def gen_gradient_img(self, height, width) -> Image:
		def get_gradient_2d(start, stop, width, height, is_horizontal):
			if is_horizontal:
				return np.tile(np.linspace(start, stop, width), (height, 1))
			else:
				return np.tile(np.linspace(start, stop, height), (width, 1)).T


		def get_gradient_3d(width, height, start_list, stop_list, is_horizontal_list):
			result = np.zeros((height, width, len(start_list)), dtype=np.float64)
			for i, (start, stop, is_horizontal) in enumerate(zip(start_list, stop_list, is_horizontal_list)):
				result[:, :, i] = get_gradient_2d(start, stop, width, height, is_horizontal)
			return result

		
		array = get_gradient_3d(int(height*1.5), int(width*1.5), (255, 0, 255), (108,64,121), (True, False, False))
		# array = get_gradient_2d(512, 256, 500, 500,False)
		img = Image.fromarray(np.uint8(array))
		img = img.rotate(-75, resample=0, expand=0, center=None, translate=None, fillcolor=None)
		img = img.crop((width*0.17,height*0.2,1350,1350))

		return img


	def get_size_txt(self)-> None:
		"get size of text object"

		testImg = Image.new('RGB', (1, 1))
		testDraw = ImageDraw.Draw(testImg)
		width, height = testDraw.textsize(self.TEXT, self.font)
		self.heightTXT = height
		self.widthTXT = width
		
		# self.conf['width'] = height if height > width else width
		# self.conf['height'] = width if width > height else height

		self.conf['width'] = self.conf['insta_res'][0]
		self.conf['height'] = self.conf['insta_res'][1]

	def hex_to_rgb(self, value) -> tuple:
		"convert hex value to rgb"

		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

	def get_fonts(self) -> None:
		"import fonts"
		self.font = ImageFont.truetype(self.conf['fontname'], self.conf['fontsize'])
		self.font_footer = ImageFont.truetype(self.conf['font_footer_name'], self.conf['font_footer_size'])
		self.font_header = ImageFont.truetype(self.conf['font_header_name'], self.conf['header_font_size'])
		self.font_watermark = ImageFont.truetype(self.conf['font_footer_name'], self.conf['watermark_font_size'])


	def create_watermark(self) -> None:
		mark = ImageDraw.Draw(self.img_object)
		footer_coords = (self.conf['margin']["left"], self.conf['insta_res'][1]*0.93)
		# print(footer_coords)
		mark.text(footer_coords, self.conf['watermark'], fill=self.hex_to_rgb(self.conf['colorText']), font=self.font_watermark)



	def set_margins(self) -> None:
		"margins"
		
		self.conf['margin']["top"] = (self.conf['height'] - self.heightTXT) / 2 
		self.conf['margin']["left"] = (self.conf['width'] * 5) / 100
		self.conf['width'] = int(self.conf['width']+(self.conf['margin']["left"]*2))
	
	def create_footer(self) -> None:
		"creating image's footer"

		ftr = ImageDraw.Draw(self.img_object)
		footer_coords = (self.conf['margin']["left"], self.conf['insta_res'][1]*self.conf['footer_position_ratio'])
		# print(footer_coords)

		ftr.text(footer_coords, self.conf['TEXT_footer'], fill=self.hex_to_rgb(self.conf['colorText']), font=self.font_footer)

	def create_header(self) -> None:
		"creating footer with posting date"
		self.create_data()
		header = ImageDraw.Draw(self.img_object)
		header_coords = (self.conf['margin']["left"], self.conf['insta_res'][1]*self.conf['header_position_ratio'])
		# header.text(header_coords, self.conf['DATE'], fill=self.hex_to_rgb(self.conf['colorText']), font=self.conf['font_header'])
		header.text(header_coords, self.conf['DATE'], fill=self.hex_to_rgb(self.conf['colorText']), font=self.font_header)

		
	def create_data(self) -> None:
		"create data if not specified for header"
		if self.conf['DATE'] == None:
			date = time.localtime()
			yr = date.tm_year
			month  = str(date.tm_mon) if len(str(date.tm_mon)) == 2 else f"0{date.tm_mon}"
			day  = str(date.tm_mday) if len(str(date.tm_mday)) == 2 else f"0{date.tm_mday}"
			hour  = str(date.tm_hour) if len(str(date.tm_hour)) == 2 else f"0{date.tm_hour}"
			minutes  = str(date.tm_min) if len(str(date.tm_min)) == 2 else f"0{date.tm_min}"
			mil = int(round(time.time() * 1000))
			if day == "24":
				day = "00"
			self.conf['DATE'] = f"{hour}:{minutes} {day}/{month}/{yr}"


	def prepare_text(self) -> str:
		"cut text and prepare to show"

		self.logger.debug(f"prepare text input: {self.TEXT}" )

		# txt = self.TEXT.rsplit(" ")
		txt = self.TEXT
		self.logger.debug(f"prepare text split: {self.TEXT}" )
		
		res_txt = ""
		chars_inline = 0
		space = 0
		chars_total = 0
		for char in txt:
			chars_total+=1
			chars_inline +=1
			if char == " ":
				space += 1
			if chars_inline >= ((self.conf['characters_break']-10) + (space/2)):
				t = txt[chars_total:chars_total+20]

				# if "\n" in t:
				# 	#todo
				# 	# replace t in txt with t.replace("\n", "")
				if char == " ":
					res_txt += f"\n"
				else:
					if (len(res_txt) - res_txt.rfind(" ")) > 10:
						res_txt += f"-\n"

					else:
						index = res_txt.rfind(" ")
						res_txt = f"{res_txt[:index]}\n{res_txt[index:]}"
				
				chars_inline = 0
				space = 0

			
			res_txt += char


		self.TEXT = str(res_txt)
		self.logger.debug(f"text prepared: {self.TEXT}" )



		if self.censor_flag == True:
			self.censure_txt()

	def load_from_threads(self):

		while 1:
			self.SENT = False
			gen = self.q_list.get("2gen")
			insta = self.q_list.get("2insta")
			# q2 = self.q_list.get("2flask")
			# q2 = self.q_list.get("2tello")
			res = gen.get() 

			
			#res =  q2.get()

			# data = res["text"]
			data = res.tell
			# self.conf['out_image_name'] = res["title"]
			self.conf['out_image_name'] = res.title
			# t = res["title"]
			t = res.title
			# self.censor_flag = res["censure_flag"]
			self.censor_flag = res.flag
			# try:
			# 	self.tell_ip = res["users_ip"]
			# except:
			# 	self.tell_ip = "0.0.0.0"
			self.tell_ip = res.users_ip

			#2021 10 22 11 03 53			
			if f"{t[8]}{t[9]}" == "24":
				hour = f"00"
			else:
				hour = f"{t[8]}{t[9]}"
				
			self.conf['DATE'] = f"{hour}:{t[10]}{t[11]} {t[6]}{t[7]}/{t[4]}{t[5]}/{t[0:4]}"

			self.TEXT_tmp = data
			if data:
				self.TEXT = data
		
				self.gen()
			if res.send and not self.SENT:
				# res = {
				# "title": self.conf['out_image_name'],
				# "filename": f"{self.conf['out_image_name']}.{self.conf['extension']}"
				# }
				res.filename = f"{self.conf['out_image_name']}.{self.conf['extension']}"
	

				insta.put(res)
				 
			else:
				pass
			


			time.sleep(0.01)
			



if __name__ == '__main__':

	asd = Make_img()
	asd.TEXT = "LOREM IPSUM ąśðæżćź„"
	asd.gen()
