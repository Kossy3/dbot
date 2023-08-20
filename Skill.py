from Action import *

@Attacks.create("とっしん", 10, "敵にとっしんし、ダメージを与える")
async def test(self: Attack, to, by):
  damage = self.calc_damage(to, by, 10)
  await to.damage(damage)