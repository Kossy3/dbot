import discord
from RPG import *
from UI import discordUI

class MO:
  async def __call__(self):
    rpg = RPG(CUI())
    await rpg.start()

class discordMO:
  def __init__(self, client: discord.Client):
    self.users :dict[str,RPG] = {}
    self.client :discord.Client = client
    self.channel :discord.TextChannel = self.get_channel("rpg-test")

  def get_channel(self, name: str):
    for c in self.client.get_guild().channels:
      if c.name == name and c.type == discord.ChannelType.text:
        return c
    
  async def __call__(self, message: discord.Message):
    if message.author.id in self.users and message.channel == self.channel:
      rpg = RPG(discordUI(self.client, self.channel, message.author.id))
      self.users[message.author.id] = rpg
      await rpg.start()
      

if __name__ == "__main__":
  mo = MO()
  loop = asyncio.new_event_loop()
  loop.run_until_complete(mo())