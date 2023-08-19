import types
from abc import ABC, abstractmethod
from UI import *
#from charactor import Charactor

class Action:
  def __init__(self, func: types.FunctionType, name: str, cost: int, text: str):
      self.func: types.FunctionType = func
      self.name = name
      self.text = text
      self.cost = cost
  
  async def __call__(self, to, by):
      await self.func(self=self, to=to, by=by)


class Attack(Action):
    def calc_damage(self, to, by, factor:int):
        return int((by.atk/to.dfn + to.lv/2)*factor)


class Attacks(list):
  
  attacks :list[Attack] = []

  def create(name: str, cost: int, text: str=""):
    def deco(func: types.FunctionType):
        func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        async def new_func(**kwargs):
            await func(**{k:kwargs[k] for k in func_args})
        Attacks.attacks.append(Attack(new_func, name, cost, text))
        return new_func
    return deco


class ActionSlot(list):
    def __init__(self, name: str, ui: UI, limit: int):
      self.limit = limit
      self.ui = ui
      self.name = name
    
    async def show(self, max_cost=1000):
      await self.ui.output(f"ーー【{self.name}一覧】ーー")
      for i, v in enumerate(self):
        if v.cost <= max_cost:
          await self.ui.output(f"{i+1}: {v.name} {v.cost}")
      await self.ui.output(f"ーーー{''.join(['ー' for i in self.name])}ーーーーー")

    def get(self, max_cost):
       return [a for a in self if a.cost <= max_cost]

    async def set(self, action: Action):
      if len(self) == self.limit:
        await self.ui.output(f"スロットに空きがありません。破棄する{self.name}を選択してください。(番号を入力)")
        self.show()
        text = None
        while not text or (text.isdecimal() and int(text) <= len(self)):
          res: Message = await self.ui.wait_input()
          text = res.content
        removed_action = self.pop(int(text)-1)
        await self.ui.output(f"{removed_action.name} を破棄しました。")
      self.append(action)
      await self.ui.output(f"{action.name} を追加しました。")

  
@Attacks.create("とっしん", 10, "敵にとっしんし、ダメージを与える")
async def test(self: Attack, to, by):
  damage = self.calc_damage(to, by, 10)
  await to.damage(damage)
  

class Magic:
  def __init__(self):
    ...
'''
magic = Magic()

@magic.main(name="ファイアーボール", cost=20, 
text="""敵に100ダメージ""")
def fireball(to, by):
  to.damage(100, by)


def main():
  output = Output()
  player = Charactor(output, "")
  Battle()


if __name__ == "__main__":
  main()
'''