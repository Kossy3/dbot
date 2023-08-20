from Action import *
from Charactor import *

@Attacks.create("とっしん", 10, "敵にとっしんし、ダメージを与える")
async def test(self: Attack, to: Charactor, by: Charactor):
  damage = self.calc_damage(to, by, 10)
  await to.damage(damage)