from Charactor import *
import random
from test_enemy_names import data as enemy_names

class Team(list[Charactor]):
  def __init__(self,ui: UI, name: str, *args: Charactor):
    self.name = name
    self.ui = ui
    for arg in args:
      self.append(arg)
      arg.team = self

  async def our_turn(self):
    for c in self:
      await c.my_turn()

  def is_alive(self):
    for c in self:
      if c.is_alive():
        return True 
    else:
      return False
    
  def random_enemies(self, lv):
    rnd = random.randrange(1, 6)
    rnd_name = enemy_names
    for i in range(rnd):
      e = Enemy(self.ui, f"{random.choice(rnd_name, )['label'].replace('+', '')}Lv.{lv}", random=True)
      e.lv = int(lv)
      e.team = self
      self.append(e)
  
  def full_sp(self):
    for c in self:
      c.heal_sp()
      c.heal_pre_sp()

  async def order_actions(self, timeline, enemies):
    for c in self:
      await c.order_actions(timeline, self, enemies)

  async def show(self):
    await self.ui.output(f"ーー【{self.name}一覧】ーー")
    for i, v in enumerate(self):
      await self.ui.output(f"{i+1}: {v.name}")
    await self.ui.output(f"ーーー{''.join(['ー' for i in self.name])}ーーーーー")

  def battle_init(self):
    for c in self:
      c.set_battle_status()

  def remove_dead(self):
    for c in self:
      if not c.is_alive():
        self.remove(c)
