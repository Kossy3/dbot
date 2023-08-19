from abc import ABC, abstractmethod
from Message import *
import discord
import asyncio
from Commands import *

class UI(ABC):
  @abstractmethod
  async def output(self, text:str):
    ...

  @abstractmethod
  async def wait_input(self, timeout:float) -> Message:
    ...

  async def wait_commands(self, timeout:float, commands: Commands):
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
  def __init__(self, client: discord.Client, channel: discord.TextChannel, user_id: int):
    self.client: discord.Client = client
    self.channel: discord.TextChannel = channel
    self.user_id: int = user_id

  async def output(self, text):
    await self.channel.send(text)

  async def wait_input(self, timeout) -> str:
    def check(message: discord.Message):
      return message.channel.name == self.channel.name and message.author.id == self.user_id
    try:
      message: discord.Message = await self.channel.wait_for("message", check=check, timeout=timeout)
      return Message(message)
    except asyncio.TimeoutError:
      return None
    

      

    
