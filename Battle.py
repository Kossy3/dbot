from Charactor import *
from Team import *
import random

class Battle:
  def __init__(self, ui :UI, players :Team, enemies :Team=None, random_enemies: int=0):
    self.players = players
    self.enemies = enemies
    self.ui = ui
    self.timeline = Timeline(ui)
    if random_enemies:
      self.enemies = Team(self.ui, "Enemy")
      self.enemies.random_enemies(lv=random_enemies)

  async def __call__(self):
    order: list[Team] = [self.players, self.enemies]
    i = 1 # random.randrange(2)
    j = (i+1)%2
    [await t.show() for t in order]
    [t.battle_init() for t in order]
    winner = None
    while not winner:
      self.timeline.clear()
      [t.full_sp() for t in order]
      [t.remove_dead() for t in order]
      await order[i].order_actions(self.timeline, order[j])
      self.timeline.time_sort()
      await self.timeline.show()
      await order[j].order_actions(self.timeline, order[i])
      self.timeline.time_sort()
      # await self.timeline.show()
      await self.timeline.excute()
      
      winner = self.get_winner()
    await self.ui.output("戦闘終了")
    if winner == self.players:
      await self.ui.output("＞＞＞勝利＜＜＜")
    else:
      await self.ui.output("ーーー敗北ーーー")

  def get_winner(self):
    if not self.players.is_alive():
      return self.enemies
    elif not self.enemies.is_alive():
      return self.players
    else:
      return None
      

class Timeline(list):
  class Task:
    def __init__(self, action: Action, to: list[Charactor], by: Charactor):
      self.action = action
      self.to = to
      self.by = by
      self.time = int(by.pre_speed)
      self.sousai = False

  def __init__(self, ui: UI):
    self.ui = ui

  def set(self, action: Action, to: list[Charactor], by: Charactor, cost_factor: float=1):
    self.append(Timeline.Task(action, to, by))
    by.pre_speed -= int(action.cost*cost_factor)

  def time_sort(self):
    def key(task: Timeline.Task):
      return task.time
    self.sort(key=key, reverse=True)

  async def show(self):
    await self.ui.output(f"ーータイムラインーー")
    for i in self:
      await self.ui.output(f"[SP:{i.time}] {i.action.name} to {', '.join([v.name for v in i.to])} by {i.by.name}")
    await self.ui.output(f"ーーーーーーーーーー")

  def is_sousai(self, time:int):
    teams = set()
    for v in self:
      if v.time == time and v.by.is_alive():
        teams.add(v.by.team.name)
    return len(teams) >= 2

  async def excute(self):
    sousai_time = 10000
    for v in self:
      if sousai_time == v.time:
        continue
      if self.is_sousai(v.time):
        sousai_time = v.time
        await self.ui.output(f"[SP:{v.time:02}] ＞＞相殺＜＜")
      elif v.by.is_alive():
        await self.ui.output(f"[SP:{v.time:02}] {v.by.name} の {v.action.name} が発動!")
        await v.action(v.to, v.by)
