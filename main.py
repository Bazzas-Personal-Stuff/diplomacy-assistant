from discord_client import MyClient

client = MyClient(command_prefix='$', self_bot=False)
client.run(client.TOKEN)

