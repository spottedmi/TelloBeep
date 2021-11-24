from discord.ext import commands
import discord
import datetime
import asyncio

time = datetime.datetime.now

from config import Config

async def timer():
    await bot.wait_until_ready()
    channel = bot.get_channel(913154344130576434) # replace with channel ID that you want to send to
    msg_sent = False

    while True:
        if  time().minute%2 == 0:
            if not msg_sent:
                await channel.send(f"minutes is even {time().minute}")
                msg_sent = True
        else:
            msg_sent = False

    await asyncio.sleep(1)


class Discord_bot(Config):
    def __init__(self, q_list):
        super().__init__()
        print("INIT: DISCORD")
        self.q_list = q_list

        self.bot = commands.Bot(command_prefix='!')

        self.bot.loop.create_task(self.load_from_thread())
        self.bot.run(self.DISCORD_TOKEN)

    async def load_from_thread(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(int(self.DISCORD_CHANNEL_ID))
        msg_sent = False

        queue = self.q_list.get("2main_thread")

        while True:
            res = queue.get()
            x = f"{self.out_image_path}/{res.get('filename')}"
            with open(x, 'rb') as f:
                picture = discord.File(f)

            await channel.send(f"{res.get('bot_comment')}", file=picture)


            await asyncio.sleep(1)






if __name__ == "__main__":
    
    bot = commands.Bot(command_prefix='!')
    print(bot)
    bot.loop.create_task(timer())
    print("loop 1 ")
    bot.run('')

