import diplomacy_message
import discord
from discord.ext import tasks
from dotenv import load_dotenv
import os
import scraper


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll_diplomacy.start()
        # self.bg_task = self.loop.create_task(self.poll_diplomacy())

    VERBOSE = False
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
    ROLE_ID = os.getenv('DISCORD_MENTION_ROLE_ID')
    POLL_WAIT_TIME = int(os.getenv('WD_POLL_WAIT_TIME'))
    COMMS_MESSAGE = '\N{no entry sign} Communications Blackout \N{no entry sign}\n'

    @tasks.loop(seconds=POLL_WAIT_TIME)
    async def poll_diplomacy(self):
        await self.wait_until_ready()
        channel: discord.TextChannel = self.get_channel(self.CHANNEL_ID)
        message = diplomacy_message.get_status()

        if message is not None:
            embed = discord.Embed().set_image(url=message[1])
            embed.title = message[0]
            if not message[2]:
                embed.description = self.COMMS_MESSAGE

            embed.color = discord.Colour(message[3])
            embed.set_footer(text=message[4])
            await channel.send(embed=embed, content='<@&{}>'.format(self.ROLE_ID))

        print(self.POLL_WAIT_TIME)



