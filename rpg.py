from abc import ABC, abstractmethod

class BattleScene:
  def __init__(self, player, enemies):
    self.player = player
    self.enemies = enemies
    self.timeline = Timeline()
    
  def turn(self):
    for e in self.enemies:
      action = e.choose_action()
      e.action(action)
      action.current_speed = e.speed

class Timeline(list):
  def sort(self):
    def key(action):
      return action.current_speed
    super().sort(key=key)

class Charactor:
  def __init__(self):
    self.lv = 0
    self.name = 0
    self.assaults = []
    self.magic = []
    # 基本ステ
    self.base_assault_atk = 0
    self.base_assault_dfn = 0
    self.base_magic_atk = 0
    self.base_magic_dfn = 0
    # 戦闘時変数
    self.assault_atk = 0
    self.assault_dfn = 0
    self.magic_atk = 0
    self.magic_dfn = 0
    self.speed = 0

  def battle_start(self):
    self.assault_atk = 0
    self.assault_dfn = 0
    self.magic_atk = 0
    self.magic_dfn = 0
    self.speed = 0

class Action(ABC):
  
  @property
  @abstractmethod
  def speed_cost(self):
    ...

  @property
  @abstractmethod
  def text(self):
    ...

  @abstractmethod
  def __call__(self):
    ...

class Assault(Action):
  ...

class Magic(Action):
  ...
    
  
  