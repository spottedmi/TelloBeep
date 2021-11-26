#!/usr/bin/python3
#by RandomGuy90 A.D.2021

from PIL import Image, ImageDraw, ImageFont
import random, time, sys

from queue import Queue
import _thread

from censorship import Censorship
from db_connector import Db_connector

from notifications import Notify

class Make_img(Censorship, Db_connector):
	def __init__(self, q_list=None):
		super().__init__(q_list=q_list)

		self.FIRST_POST = None
		self.HOURS_PASSED = 0
		self.ALERT_SEND = False
		self.WARNING_SEND = False
		

		if q_list:
			self.q_list = q_list
			self.load_from_threads()

	def gen(self) -> None:
		"generate image"

		self.prepare_text()
		try:
			self.get_fonts()
		except:
			Notify(q_list=self.q_list, error="FONT_NOT_FOND")
			sys.exit(1)
		self.get_size_txt()
		self.set_margins()

		# img = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.colorBackground))
		self.get_bg_color()
		self.img_object = Image.new('RGB', (self.width, self.height), self.hex_to_rgb(self.bg_color))
		d = ImageDraw.Draw(self.img_object)
		
		#text 
		
		coords =(self.margin["left"] ,self.margin["top"])
		
		d.text(coords, self.TEXT, fill=self.hex_to_rgb(self.colorText), font=self.font)

		d.rectangle((0, 0, self.width-self.outline_thickness, self.height-self.outline_thickness),width= self.outline_thickness, fill=None, outline=self.hex_to_rgb(self.colorOutline))

		#header
		self.create_header()

		#footer
		self.create_footer()

		img = Image.open(self.image_path, "r")
		img = img.resize(self.image_size, Image.ANTIALIAS)
		img = img.convert("RGBA")

		coords = (int(self.insta_res[1]*self.logo_X_ratio), int(self.insta_res[0]*self.logo_Y_ratio))

		self.img_object.paste(img, coords, img)

		#resizing and prepare to save
		img = img.convert("RGB")
		self.save_img()
		self.save_tumbnail()
		
		self.db_add_img()

		insta = self.q_list.get("2insta")
		self.req = {
			"filename": f"{self.out_image_name}.{self.extension}",
			"title": self.TEXT,
			"send": False
		}

		if self.AUTORUN and not self.censor_flag:
			self.req["send"] = True
			print("SENDING TO INSTA")
			print(f"autorun: {self.AUTORUN}")
			insta.put(self.req)
			self.SENT = True

		self.edit_ratio()
		print(f"POSTS RATIO:	{self.POST_RATIO} PER HOUR")
		print(f"POSTS COUNT:	{self.POST_COUNT} ")
		

		# if self.AUTORUN:
		# 	self.db_set_approved()

		# d = self.q_list.get("2main_thread")
		# self.req["bot_comment"] = "New post added"
		# d.put(self.req)

		



	def save_img(self):
		self.img_object = self.img_object.resize(self.insta_res, Image.ANTIALIAS)
		self.filename = f"{self.out_image_path}/{self.out_image_name}.{self.extension}"
		try:
			self.img_object.save(self.filename)
		except FileNotFoundError:
			Notify(q_list=self.q_list,error="CANT_SAVE_IMG")
			try:
				self.filename = f"{self.out_image_path_BACKUP}/{self.out_image_name}.{self.extension}"

				self.img_object.save(self.filename)
			except FileNotFoundError:
				Notify(q_list=self.q_list,error="CANT_SAVE_IMG_BACK")
				sys.exit(1)




	def save_tumbnail(self):
		self.img_object = self.img_object.resize(self.thumb_res, Image.ANTIALIAS)
		self.img_object.save(f"{self.thumb_path}/{self.out_image_name}_thumbnail.{self.extension}")
		
	def get_bg_color(self):
		if isinstance(self.colorBackground, list):
			x = random.randrange(0, len(self.colorBackground)-1)
			self.bg_color = self.colorBackground[x]
		else:
			self.bg_color = self.colorBackground

	def edit_ratio(self):
		# self.POST_RATIO += 1
		self.POST_COUNT += 1

		if self.FIRST_POST == None:
			self.FIRST_POST = int(time.time())

		self.HOURS_PASSED = int(time.time()) 
		self.HOURS_PASSED = ( self.HOURS_PASSED - self.FIRST_POST )/ 3600

		# if self.HOURS_PASSED:
		if self.HOURS_PASSED > 1:
			self.POST_RATIO = int(self.POST_COUNT / self.HOURS_PASSED)
		else:
			self.POST_RATIO = int(self.POST_COUNT / 1)

		if self.AUTORUN:
			if self.POST_RATIO >= self.POST_RATIO_ALERT:
				print('-------------  TO MAY POSTS, AUTO RUN OFF')
				self.db_set_approved(state=None)

				if self.ALERT_SEND == False:
					# d.put(self.req)
					Notify(q_list=self.q_list,error="POST_RATIO_ALERT", img=self.req.get("filename"))
					self.ALERT_SEND = True


			elif self.POST_RATIO >= self.POST_RATIO_WARNING:
				print("POSTS ALERT ALERTTTT!!!!")
				

				if self. WARNING_SEND == False:
					# d.put(self.req)
					Notify(q_list=self.q_list ,error="POST_RATIO_WARNING", img=self.req.get("filename"))
					self.WARNING_SEND = True


		# if (self.FIRST_POST - time.time()) > 3600000:
		# 	self.HOURS_PASSED +=1


	def get_size_txt(self)-> None:
		"get size of text object"

		testImg = Image.new('RGB', (1, 1))
		testDraw = ImageDraw.Draw(testImg)
		width, height = testDraw.textsize(self.TEXT, self.font)
		self.heightTXT = height
		self.widthTXT = width
		
		# self.width = height if height > width else width
		# self.height = width if width > height else height

		self.width = self.insta_res[0]
		self.height = self.insta_res[1]

	def hex_to_rgb(self, value) -> tuple:
		"convert hex value to rgb"

		value = value.lstrip('#')
		lv = len(value)
		return tuple(int(value[i:i+lv//3], 16) for i in range(0, lv, lv//3))

	def get_fonts(self) -> None:
		"import fonts"
		
		self.font = ImageFont.truetype(self.fontname, self.fontsize)
		self.font_footer = ImageFont.truetype(self.font_footer_name, self.font_footer_size)
		self.font_header = ImageFont.truetype(self.font_header_name, self.header_font_size)

	def set_margins(self) -> None:
		"margins"

		self.margin["top"] = (self.height - self.heightTXT) / 2 
		self.margin["left"] = (self.width * 5) / 100
		
		self.width = int(self.width+(self.margin["left"]*2))
	
	def create_footer(self) -> None:
		"creating image's footer"

		ftr = ImageDraw.Draw(self.img_object)
		footer_coords = (self.margin["left"], self.insta_res[1]*self.footer_position_ratio)
		# print(footer_coords)
		ftr.text(footer_coords, self.TEXT_footer, fill=self.hex_to_rgb(self.colorText), font=self.font_footer)

	def create_header(self) -> None:
		"creating footer with posting date"
		self.create_data()
		header = ImageDraw.Draw(self.img_object)
		header_coords = (self.margin["left"], self.insta_res[1]*self.header_position_ratio)
		header.text(header_coords, self.DATE, fill=self.hex_to_rgb(self.colorText), font=self.font_header)

		
	def create_data(self) -> None:
		"create data if not specified for header"
		if self.DATE == None:
			date = time.localtime()
			yr = date.tm_year
			month  = str(date.tm_mon) if len(str(date.tm_mon)) == 2 else f"0{date.tm_mon}"
			day  = str(date.tm_mday) if len(str(date.tm_mday)) == 2 else f"0{date.tm_mday}"
			hour  = str(date.tm_hour) if len(str(date.tm_hour)) == 2 else f"0{date.tm_hour}"
			minutes  = str(date.tm_min) if len(str(date.tm_min)) == 2 else f"0{date.tm_min}"
			mil = int(round(time.time() * 1000))
			self.DATE = f"{hour}:{minutes} {day}/{month}/{yr}"



	def prepare_text(self) -> str:
		"cut text and prepare to show"

		txt = self.TEXT.rsplit(" ")
		res_txt = ""
		words = self.word_break
		i = 0 
		for elem in txt:
			i+=1
			# res_txt.append(elem)
			res_txt = res_txt +" "+ elem
			#print(res_txt)
			if not i%words:
				res_txt = res_txt + "\n"

		self.TEXT = str(res_txt)
		


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

			data = res["text"]
			print(f"data: {data}")
			self.out_image_name = res["title"]
			t = res["title"]
			self.censor_flag = res["censure_flag"]

			#2021 10 22 11 03 53
			self.DATE = f"{t[8]}{t[9]}:{t[10]}{t[11]} {t[6]}{t[7]}/{t[4]}{t[5]}/{t[0:4]}"

			self.TEXT_tmp = data
			if data:
				self.TEXT = data
		
				self.gen()
			if res.get("send") and not self.SENT:
				res = {
				"title": self.out_image_name,
				"filename": f"{self.out_image_name}.{self.extension}"
				}

				insta.put(res)
				 
			else:
				pass
			


			time.sleep(0.01)
			



if __name__ == '__main__':

	asd = Make_img()
	asd.gen("LOREM IPSUM")
