import discord
from RPG import *
from UI import discordUI


class MO:

  async def __call__(self):
    rpg = RPG(CUI())
    await rpg.start()


class discordMO:

  def __init__(self, client: discord.Client):
    self.users: dict[str, RPG] = {}
    self.client: discord.Client = client
    self.channels: list[discord.TextChannel] = self.get_channels("rpg-test")

  def get_channels(self, name: str):
    channels = []
    for g in self.client.guilds:
      for c in g.channels:
        if c.name == name and c.type == discord.ChannelType.text:
          channels.append(c)
    return channels

  async def __call__(self, message: discord.Message):
    print(message.content)
    if message.author.id not in self.users and message.channel in self.channels:

      rpg = RPG(discordUI(self.client, message.channel, message.author.id))
      self.users[message.author.id] = rpg
      await rpg.start()


if __name__ == "__main__":
  mo = MO()
  loop = asyncio.new_event_loop()
  loop.run_until_complete(mo())
