from abc import ABC, abstractmethod
from Message import *
import discord
import asyncio
from Commands import *


class UI(ABC):

  @abstractmethod
  async def output(self, text: str):
    ...

  @abstractmethod
  async def wait_input(self, timeout: float) -> Message:
    ...

  async def wait_commands(self, timeout: float, commands: Commands):
    message = None
    while not message:
      message: Message = await self.wait_input(timeout=timeout)
    if message.content:
      try:
        response = await commands.call_commands(message)
        return response
      except Commands.MissingArgument:
        return None
    else:
      return None


class CUI(UI):

  async def output(self, text):
    print(text)

  async def wait_input(self, timeout):
    return Message(input())


class discordUI(UI):

  def __init__(self, client: discord.Client, channel: discord.TextChannel,
               user_id: int):
    self.client: discord.Client = client
    self.channel: discord.TextChannel = channel
    self.user_id: int = user_id
    self.texts = []

  async def output(self, text):
    self.texts.append(text)

  async def wait_input(self, timeout) -> str:
    if len(self.texts) > 0:
      self.texts.insert(0, f"<@{self.user_id}>")
      await self.channel.send("\n".join(f"```python\n{self.texts}\n```"))
      self.texts.clear()

    def check(message: discord.Message):
      return message.channel.name == self.channel.name and message.author.id == self.user_id

    try:
      message: discord.Message = await self.client.wait_for("message",
                                                            check=check,
                                                            timeout=timeout)
      return Message(message)
    except asyncio.TimeoutError:
      return None
