from Action import *
from Charactor import *

@Attacks.create("びんた", 2, "小ダメージを与える", select_to=1)
async def test(self: Attack, to: list[Charactor], by: Charactor):
  damage = self.calc_damage(to[0], by, 10)
  await to[0].damage(damage)

@Attacks.create("でこぴん", 10, "大ダメージを与える", select_to=1)
async def test(self: Attack, to: list[Charactor], by: Charactor):
  damage = self.calc_damage(to[0], by, 50)
  await to[0].damage(damage)

@Attacks.create("ちょっぷ", 3, "小ダメージを与える", select_to=1)
async def test(self: Attack, to: list[Charactor], by: Charactor):
  damage = self.calc_damage(to[0], by, 15)
  await to[0].damage(damage)

@Attacks.create("いかく", 10, "敵全員に小ダメージを与える", select_to=0)
async def test(self: Attack, to: list[Charactor], by: Charactor):
  for e in to:
    damage = self.calc_damage(e, by, 10)
    await e.damage(damage)

@Items.create("回復薬", 0, "最大HPの30%回復する。回数限定。", select_to=0)
async def test(self: Item, by: Charactor):
  self.use(by)
  before_hp = by.hp
  by.heal_hp(int(by.get_max_hp()*0.3))
  await by.ui.output(f"        {by.name} に{by.hp - before_hp} の回復!")