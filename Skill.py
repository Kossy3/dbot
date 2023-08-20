from Action import *
from Charactor import *

@Attacks.create("びんた", 2, "小ダメージを与える")
async def test(self: Attack, to: Charactor, by: Charactor):
  damage = self.calc_damage(to, by, 10)
  await to.damage(damage)

@Attacks.create("でこぴん", 10, "大ダメージを与える")
async def test(self: Attack, to: Charactor, by: Charactor):
  damage = self.calc_damage(to, by, 50)
  await to.damage(damage)