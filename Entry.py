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
    await self.ui.output(
f"""{message.content} さんを登録
HP:{player.hp} SP:{player.speed}
Atk:{player.atk} Dfn:{player.dfn}
Sp.Atk:{player.sp_atk} Sp.Dfn:{player.sp_dfn}""")
    player.base_speed = 10
    return player

