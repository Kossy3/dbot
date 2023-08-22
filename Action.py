import types
from abc import ABC, abstractmethod
from UI import *
from UI import types

class Action:
  def __init__(self, func: types.FunctionType, name: str, cost: int, text: str, select_to: int=1):
      self.func: types.FunctionType = func
      self.name = name
      self.text = text
      self.cost = cost
      self.select_to = select_to
  
  async def __call__(self, to, by):
      await self.func(self=self, to=to, by=by)


class Attack(Action):
  def calc_damage(self, to, by, factor:int):
    return int((by.atk/to.dfn*50 + to.lv*2/5+ 2)*factor/50 + 2)
    
class Magic(Action):
  def calc_damage(self, to, by, factor:int):
    return int((by.sp_atk/to.sp_dfn + to.lv/2)*factor)

class Item(Action):
  def use(self, by):
    by.item_slot.remove(self)

class Actions(ABC):
  @abstractmethod
  def create(*args, **kwargs):
    ...
  
class Attacks(Actions):
  actions :list[Action] = []
  def create(name: str, cost: int, text: str="", select_to: int=1):
    def deco(func: types.FunctionType):
        func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        async def new_func(**kwargs):
            await func(**{k:kwargs[k] for k in func_args})
        Attacks.actions.append(Attack(new_func, name, cost, text, select_to))
        return new_func
    return deco

class Magics(Actions):
  ...
   
class Items(Actions):
  actions :list[Action] = []
  def create(name: str, cost: int, text: str="", select_to: int=0):
    def deco(func: types.FunctionType):
        func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
        async def new_func(**kwargs):
            await func(**{k:kwargs[k] for k in func_args})
        Items.actions.append(Item(new_func, name, cost, text, select_to))
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