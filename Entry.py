import random
from UI import *
from Charactor import *

class Entry:
  def __init__(self, ui :UI):
    self.ui = ui

  async def __call__(self) -> Charactor:
    await self.ui.output("名前を入力してください(7文字以内)")
    message: Message = None
    while message == None or len(message.content) > 7:
      message = await self.ui.wait_input(30)
    
    # ステータス配分がここであるかもしれない
    player = Player(self.ui, message.content, random=True)
    player.set_battle_status()
    # HP特盛
    player.base_hp *= 5
    await self.ui.output("基礎HPを5倍にします")
    await self.ui.output(
f"""{message.content} さんを登録
HP:{player.hp}({player.base_hp}) SP:{player.speed}({player.base_speed})
Atk:{player.atk}({player.base_atk}) Dfn:{player.dfn}({player.base_dfn})
Sp.Atk:{player.sp_atk}({player.base_sp_atk}) Sp.Dfn:{player.sp_dfn}({player.base_sp_dfn})
※()は基礎値""")
    return player