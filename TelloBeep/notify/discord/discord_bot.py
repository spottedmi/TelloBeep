import discord
from discord.ext import commands
import datetime
import asyncio
import time as tm
# commands = discord.ext.commands

time = datetime.datetime.now


from TelloBeep.logs.logger import logger


async def timer():
	await bot.wait_until_ready()
	channel = bot.get_channel("") # replace with channel ID that you want to send to
	msg_sent = False

	while True:
		if  time().minute%2 == 0:
			if not msg_sent:
				await channel.send(f"minutes is even {time().minute}")
				msg_sent = True
		else:
			msg_sent = False

	await asyncio.sleep(1)


class Discord_bot():
	def __init__(self, q_list, conf=None):
		if conf:
			self.conf = conf		
		self.logger = logger(name=f"{self.conf.get('instance')}_{__name__}")

		print("INIT: DISCORD")
		self.q_list = q_list
		self.logger.info(f"discord bot init")

		self.bot = commands.Bot(command_prefix='!')

		self.bot.loop.create_task(self.load_from_thread())
		self.bot.run(self.conf['DISCORD_TOKEN'])


	async def load_from_thread(self):
		await self.bot.wait_until_ready()
		
		msg_sent = False
		queue = self.q_list.get("2main_thread")

		while True:
			res = queue.get()
			self.logger.info(f"got discord info")
			msg = f"{res.get('bot_comment')[0:1000]}"

			if res.get("filename"):
				self.logger.info(f"discord post has filename {res.get('filename')}")
				try:
					x = f"{self.conf['out_image_path']}/{res.get('filename')}"
					with open(x, 'rb') as f:
						picture = discord.File(f)
					self.logger.info(f"picture read propertly")
				except:
					self.logger.info(f"couldn't find picture in first location, searching for backup")
					x = f"{self.conf['out_image_path_BACKUP']}/{res.get('filename')}"
					with open(x, 'rb') as f:
						picture = discord.File(f)

				# await channel.send(f"{res.get('bot_comment')[0:1000]}", file=picture)
				# self.logger.info(f"discord post send with picture, {res.get('bot_comment')}, {self.conf['out_image_path']}/{res.get('filename')}")
				await  self.send_msg(msg, picture=picture)

			else:
				# await channel.send(f"{res.get('bot_comment')[0:1000]}")
				# self.logger.info(f"discord post send {res.get('bot_comment')}")
				res = await self.send_msg(msg)

			await asyncio.sleep(1)


	async def send_msg(self, msg, picture=None) -> bool:
		tm.sleep(15)
		sleep = 1
		while True:
			try:
				await self.send_message_core(msg, picture=picture)
				return True

			except Exception as e:
				self.logger.info(f"discord connection error, cannot send msg: f{msg}, sleep: {sleep}")	

				tm.sleep(sleep)
				sleep +=2


	async def send_message_core(self, msg, picture=None) -> bool :
		channel = self.bot.get_channel(int(self.conf['DISCORD_CHANNEL_ID']))
		if picture:
			await channel.send(f"{msg}", file=picture)
			self.logger.info(f"discord post send with picture, {msg}, {picture}")	
		else:
			await channel.send(f"{msg}")
			self.logger.info(f"discord post send {msg}")

		return True





if __name__ == "__main__":
	
	bot = commands.Bot(command_prefix='!')
	bot.loop.create_task(timer())
	print("loop 1 ")
	bot.run('')

