<<<<<<< HEAD
import random
from UI import *
from Action import *

class Charactor(ABC):
  def __init__(self, ui: UI, name, random=False, 
               base_hp=0, base_atk=0, base_dfn=0,
               base_sp_atk=0, base_sp_dfn=0, base_speed=0):
    self.ui = ui
    self.name = name
    self.base_hp = base_hp
    self.base_atk = base_atk
    self.base_dfn = base_dfn
    self.base_sp_atk = base_sp_atk
    self.base_sp_dfn = base_sp_dfn
    self.base_speed = base_speed
    self.lv = 1
    self.attack_slot = ActionSlot("攻撃スキル", ui, 6)
    self.magic_slot = ActionSlot("魔法スキル", ui, 6)
    self.item_slot = ActionSlot("アイテム", ui, 6)

    if random:
      self.set_random()

    # 戦闘時変数
    self.hp = 0
    self.atk = 0
    self.dfn = 0
    self.sp_atk = 0
    self.sp_dfn = 0
    self.speed = 0
    self.pre_speed = 0 # 予知用
      
  def set_random(self):
    def get_gauss():
      # 最低保証 5 最大 255
      return max(5, min(int(random.gauss(130,40)), 255))
    self.base_hp = get_gauss()
    self.base_atk = get_gauss()
    self.base_dfn = get_gauss()
    self.base_sp_atk = get_gauss()
    self.base_sp_dfn = get_gauss()
    self.base_speed = get_gauss()
    self.attack_slot.append(Attacks.actions[0])
    
  def set_battle_status(self):
    # [{(種族値×2＋個体値＋努力値/4)×Lv/100}＋5]×性格補正(1.1,1.0,0.9)
    self.atk = int(self.base_atk*2*self.lv/100 + 25)
    self.dfn = int(self.base_dfn*2*self.lv/100 + 25)
    self.sp_atk = int(self.base_sp_atk*2*self.lv/100 + 25)
    self.sp_dfn = int(self.base_sp_dfn*2*self.lv/100 + 25)
    # 変動するもの
    self.heal_sp()
    self.heal_pre_sp()
    self.heal_hp()
  
  def heal_sp(self, n: int=10000):
    # 成長しない 50 - 150程度
    max_speed = int(self.base_speed/10 + 50)
    self.speed = min(max_speed, self.speed+n)

  def heal_pre_sp(self, n: int=10000):
    # 成長しない 50 - 150程度
    max_speed = int(self.base_speed/10 + 50)
    self.pre_speed = min(max_speed, self.pre_speed+n)
  
  def heal_hp(self, n: int=10000):
    # {(種族値×2＋個体値＋努力値/4)×Lv/100}＋10＋Lv
    max_hp = int(self.base_hp*2*self.lv/100 + 50 + self.lv*4)
    self.hp = min(max_hp, self.hp+n)
  
  async def damage(self, damage):
    self.hp = max(0, self.hp - damage)
    await self.ui.output(f"{self.name}に{damage}ダメージ！ (残りHP:{self.hp})")

  def is_alive(self):
    return self.hp != 0

  async def order_actions(self, timeline, enemies):
    ok = False
    while not ok:
      ok = await self.select_action(timeline, enemies) 

  @abstractmethod
  async def select_action(self, timeline, enemies) -> bool:
      ...
  
class Player(Charactor):
  async def select_action(self, timeline, enemies):
      select_action_cmd = Commands()

      @select_action_cmd.command(help="攻撃")
      async def atk(no: int):
        if len(self.attack_slot) >= no > 0:
          await self.ui.output(f"攻撃スキル No.{no}：{self.attack_slot[no-1].name}")
          return self.attack_slot[no-1]
        await self.ui.output(f"No.{no}：攻撃スキルがありません")
        return None
      
      @select_action_cmd.command(help="魔法")
      async def mgc(no: int):
        if len(self.magic_slot) >= no > 0:
          await self.ui.output(f"魔法スキル No.{no}：{self.magic_slot[no-1].name}")
          return self.magic_slot[no-1]
        await self.ui.output(f"No.{no}：魔法スキルがありません")
        return None
      
      @select_action_cmd.command(help="アイテム")
      async def item(no:int):
        if len(self.item_slot) >= no > 0:
          await self.ui.output(f"アイテム No.{no}：{self.item_slot[no-1].name}")
          return self.item_slot[no-1]
        await self.ui.output(f"No.{no}：アイテムがありません")
        return None

      @select_action_cmd.command(help="完了")
      async def ok():
        return "ok"
      
      await self.ui.output(f"行動を選択してください。残りSP:{self.pre_speed} (atk int, mgc int, item int, ok)")
      await self.attack_slot.show()
      await self.magic_slot.show()
      await self.item_slot.show()
      action = None
      while not action:
        action = await self.ui.wait_commands(timeout=60, commands=select_action_cmd)
        if action == "ok":
          return True
        elif action and action.cost > self.pre_speed:
          await self.ui.output("SPが足りません")
          return False
      
      select_target_cmd = Commands()

      @select_target_cmd.command(help="対象の番号")
      async def to(no: int):
        if len(enemies) >= no > 0:
          await self.ui.output(f"対象 No.{no}：{enemies[no-1].name}")
          return enemies[no-1]
        await self.ui.output(f"対象 No.{no}：存在しません")
        return None
      
      await self.ui.output("対象を選択してください。(to int)")
      await enemies.show()
      target = None
      while not target:
        target = await self.ui.wait_commands(timeout=60, commands=select_target_cmd)

      timeline.set(action, target, self)
      return False


class Enemy(Charactor):
  async def select_action(self, timeline, enemies):
    action_slot = random.choice([self.attack_slot])
    valid_actions = action_slot.get(self.pre_speed)
    if len(valid_actions) == 0:
      return True
    action = random.choice(valid_actions)
    target = random.choice(enemies)
    timeline.set(action, target, self)
    return False



=======
import random
from UI import *
from Action import *

class Charactor(ABC):
  def __init__(self, ui: UI, name, random=False, 
               base_hp=0, base_atk=0, base_dfn=0,
               base_sp_atk=0, base_sp_dfn=0, base_speed=0):
    self.ui = ui
    self.name = name
    self.base_hp = base_hp
    self.base_atk = base_atk
    self.base_dfn = base_dfn
    self.base_sp_atk = base_sp_atk
    self.base_sp_dfn = base_sp_dfn
    self.base_speed = base_speed
    self.lv = 1
    self.attack_slot = ActionSlot("攻撃スキル", ui, 6)
    self.magic_slot = ActionSlot("魔法スキル", ui, 6)
    self.item_slot = ActionSlot("アイテム", ui, 6)

    if random:
      self.set_random()

    # 戦闘時変数
    self.hp = 0
    self.atk = 0
    self.dfn = 0
    self.sp_atk = 0
    self.sp_dfn = 0
    self.speed = 0
    self.pre_speed = 0 # 予知用
      
  def set_random(self):
    def get_gauss():
      # 最低保証 5 最大 255
      return max(5, min(int(random.gauss(130,40)), 255))
    self.base_hp = get_gauss()
    self.base_atk = get_gauss()
    self.base_dfn = get_gauss()
    self.base_sp_atk = get_gauss()
    self.base_sp_dfn = get_gauss()
    self.base_speed = get_gauss()
    self.attack_slot.append(Attacks.actions[0])
    self.attack_slot.append(Attacks.actions[1])
    
  def set_battle_status(self):
    # [{(種族値×2＋個体値＋努力値/4)×Lv/100}＋5]×性格補正(1.1,1.0,0.9)
    self.atk = int(self.base_atk*2*self.lv/100 + 25)
    self.dfn = int(self.base_dfn*2*self.lv/100 + 25)
    self.sp_atk = int(self.base_sp_atk*2*self.lv/100 + 25)
    self.sp_dfn = int(self.base_sp_dfn*2*self.lv/100 + 25)
    # 変動するもの
    self.heal_sp()
    self.heal_pre_sp()
    self.heal_hp()

  def get_max_sp(self):
    max_speed = int(self.base_speed/20 + 10)
    return max_speed
  
  def heal_sp(self, n: int=10000):
    # 成長しない 10 - 30程度 平均16.5
    self.speed = min(self.get_max_sp(), self.speed+n)

  def heal_pre_sp(self, n: int=10000):
    # 成長しない 50 - 150程度
    self.pre_speed = min(self.get_max_sp(), self.pre_speed+n)
  
  def heal_hp(self, n: int=10000):
    # {(種族値×2＋個体値＋努力値/4)×Lv/100}＋10＋Lv
    max_hp = int(self.base_hp*2*self.lv/100 + 50 + self.lv)
    self.hp = min(max_hp, self.hp+n)
  
  async def damage(self, damage):
    self.hp = max(0, self.hp - damage)
    await self.ui.output(f"{self.name}に{damage}ダメージ! (残りHP:{self.hp})")
    if not self.is_alive():
      await self.ui.output(f"{self.name}は気絶した!")

  def is_alive(self):
    return self.hp != 0

  async def order_actions(self, timeline, players, enemies):
    ok = False
    while not ok:
      ok = await self.select_action(timeline, players, enemies) 

  @abstractmethod
  async def select_action(self, timeline, enemies) -> bool:
      ...
  
class Player(Charactor):
  async def select_action(self, timeline, players, enemies):
      select_action_cmd = Commands()

      @select_action_cmd.command(help="攻撃")
      async def atk(no: int):
        if len(self.attack_slot) >= no > 0:
          await self.ui.output(f"攻撃スキル No.{no}：{self.attack_slot[no-1].name}")
          return self.attack_slot[no-1]
        await self.ui.output(f"No.{no}：攻撃スキルがありません")
        return None
      
      @select_action_cmd.command(help="魔法")
      async def mgc(no: int):
        if len(self.magic_slot) >= no > 0:
          await self.ui.output(f"魔法スキル No.{no}：{self.magic_slot[no-1].name}")
          return self.magic_slot[no-1]
        await self.ui.output(f"No.{no}：魔法スキルがありません")
        return None
      
      @select_action_cmd.command(help="アイテム")
      async def item(no:int):
        if len(self.item_slot) >= no > 0:
          await self.ui.output(f"アイテム No.{no}：{self.item_slot[no-1].name}")
          return self.item_slot[no-1]
        await self.ui.output(f"No.{no}：アイテムがありません")
        return None

      @select_action_cmd.command(help="完了")
      async def ok():
        return "ok"
      
      await self.ui.output(f"行動を選択してください。残りSP:{self.pre_speed} (atk int, mgc int, item int, ok)")
      await self.attack_slot.show()
      await self.magic_slot.show()
      await self.item_slot.show()
      action = None
      while not action:
        action = await self.ui.wait_commands(timeout=60, commands=select_action_cmd)
        if action == "ok":
          return True
        elif action and action.cost > self.pre_speed:
          await self.ui.output("SPが足りません")
          return False
      
      select_target_cmd = Commands()

      @select_target_cmd.command(help="対象の番号")
      async def to(no: int):
        if len(enemies) >= no > 0:
          await self.ui.output(f"対象 No.{no}：{enemies[no-1].name}")
          return enemies[no-1]
        await self.ui.output(f"対象 No.{no}：存在しません")
        return None
      
      await self.ui.output("対象を選択してください。(to int)")
      await enemies.show()
      target = None
      while not target:
        target = await self.ui.wait_commands(timeout=60, commands=select_target_cmd)

      timeline.set(action, target, self)
      return False
  

class Enemy(Charactor):
  async def select_action(self, timeline, players, enemies):
    cost_factor = len(players)
    action_slot = random.choice([self.attack_slot])
    valid_actions = action_slot.get(self.pre_speed/cost_factor)
    if len(valid_actions) == 0:
      return True
    action = random.choice(valid_actions)
    target = random.choice(enemies)
    timeline.set(action, target, self, cost_factor=cost_factor)
    return False



>>>>>>> Kossy3
