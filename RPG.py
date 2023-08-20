from Entry import *
from Battle import *
from Commands import *
import Skill
import asyncio

class RPG:

  def __init__(self, ui):
    self.player: Charactor
    self.ui: UI = ui
    self.login = True

  async def start(self):
    entry = Entry(self.ui)
    self.player = await entry()
    await self.wait_commands()

  async def wait_commands(self):
    cmd = Commands()
    @cmd.command(help="HPを表示")
    async def show_hp():
      await self.ui.output(f"hp: {self.player.hp}")

    @cmd.regix_command(regix="aa")
    async def greet(message):
      await self.ui.output(f"{message.content} hello")

    @cmd.command(help="戦闘シーンのテストを開始します")
    async def test(message):
      battle = Battle(self.ui, Team(self.ui, self.player.name, self.player), random_enemies=True)
      await battle()
    
    while self.login:
      await self.ui.wait_commands(60, commands=cmd)
  