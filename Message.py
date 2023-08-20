import discord
from datetime import datetime

class Message:
  def __init__(self, message):
    self.content: str
    self.id: int
    self.author: str
    self.room: str
    self.to: str
    self.created: datetime
    if type(message) == discord.Message:
      self.convert_from_discord(message)
    elif type(message) == str:
      self.convert_from_str(message)
    elif type(message) == dict:
      self.convert_from_dict(message)

  def convert_from_discord(self, message: discord.Message):
    self.content = message.content
    self.id = message.id
    self.author = message.author
    self.room = message.guild.name
    self.to = "ALL"
    self.created = message.created_at
  
  def convert_from_str(self, message: str):
    self.content = message
    self.id = 0
    self.author = None
    self.room = None
    self.to = "ALL"
    self.created = datetime.now()

  def convert_from_dict(self, message: dict):
    self.content = message["message"]
    self.id = message["id"]
    self.author = message["from_user"]
    self.room = message["room_name"]
    self.to = message["to_user"]
    self.created = datetime.strptime(message["created"], '%Y-%m-%d %H:%M:%S')