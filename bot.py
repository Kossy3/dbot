import asyncio, os


class Bot:

  def __init__(self):
    self.GUILD_ID = int(os.getenv("GUILD_ID"))
    self.client = None
    self.guild = None
    self.text_ch = None
    self.image_ch = None
    self.loop = asyncio.get_event_loop()

  def __del__(self):
    self.loop.close()

  def set_client(self, client):
    self.client = client

  def get_channel(self, name):
    for c in self.get_guild().channels:
      if c.name == name:
        return c

  def get_guild(self):
    for g in self.client.guilds:
      if g.id == self.GUILD_ID:
        self.guild = g
    return self.guild

  def send(self, ch_name, text, *args, **kwargs):
    ch = self.get_channel(ch_name)
    if ch:
      self.client.loop.create_task(ch.send(text))
