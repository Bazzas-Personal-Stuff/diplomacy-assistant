import diplomacy_message
import discord
from discord.ext import tasks
from discord.ext import commands
import dotenv
import os
import scraper


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.poll_diplomacy.start()
        # self.bg_task = self.loop.create_task(self.poll_diplomacy())

    VERBOSE = False
    dotenv.load_dotenv()
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
            embed.description = ''
            if not message[2]:
                embed.description = self.COMMS_MESSAGE + '\n\n'
            embed.description += '[Game Link]({}{})'.format(scraper.GAME_URL, scraper.WD_GAME_ID)

            embed.color = discord.Colour(message[3])
            embed.set_footer(text=message[4])
            await channel.send(embed=embed, content='<@&{}>'.format(self.ROLE_ID))

        print(self.POLL_WAIT_TIME)

    bot = commands.Bot(command_prefix='$')

    @bot.command(name='setID')
    async def set_new_id(ctx, new_id):
        try:
            id_test = int(new_id)

            os.environ['WD_GAME_ID'] = new_id
            with dotenv.find_dotenv() as env:
                dotenv.set_key(env, 'WD_GAME_ID', new_id)

            diplomacy_message.update_dotenv()
            scraper.update_dotenv()

            await ctx.send("Game ID is now {}".format(os.getenv('WD_GAME_ID')))
        except ValueError:
            await ctx.send("Please enter a valid Game ID.")
