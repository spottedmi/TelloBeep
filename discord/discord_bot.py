from discord.ext import commands
import discord
import datetime
import asyncio


time = datetime.datetime.now

from config import conf

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
	def __init__(self, q_list):
		

		print("INIT: DISCORD")
		self.q_list = q_list
		conf['logger'].info(f"discord bot init")

		self.bot = commands.Bot(command_prefix='!')

		self.bot.loop.create_task(self.load_from_thread())
		self.bot.run(conf['DISCORD_TOKEN'])


	async def load_from_thread(self):
		await self.bot.wait_until_ready()
		channel = self.bot.get_channel(int(conf['DISCORD_CHANNEL_ID']))
		msg_sent = False

		queue = self.q_list.get("2main_thread")

		while True:
			res = queue.get()
			if res.get("filename"):
				try:
					x = f"{conf['out_image_path']}/{res.get('filename')}"
					with open(x, 'rb') as f:
						picture = discord.File(f)
				except:
					x = f"{conf['out_image_path_BACKUP']}/{res.get('filename')}"
					with open(x, 'rb') as f:
						picture = discord.File(f)

				await channel.send(f"{res.get('bot_comment')[0:1000]}", file=picture)
				conf['logger'].info(f"discord post send with picture, {res.get('bot_comment')}, {conf['out_image_path']}/{res.get('filename')}")

			else:
				await channel.send(f"{res.get('bot_comment')[0:1000]}")
				conf['logger'].info(f"discord post send {res.get('bot_comment')}")


			await asyncio.sleep(1)






if __name__ == "__main__":
	
	bot = commands.Bot(command_prefix='!')
	bot.loop.create_task(timer())
	print("loop 1 ")
	bot.run('')

