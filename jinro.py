class Scene:
  
  def __init__(self):
    self.scene = "夜"

  def next(self):
    scenes = "夜", "朝"
    i = scenes.index(self.scene)
    self.scene = scenes[i+1]

class Job:
  ...

class JinroBot:
  def __init__(self, client):
    self.client = client
    self.scenes = Scene()