from flask import Flask
from threading import Thread
from bot import Bot

app = Flask('')
bot = Bot()


@app.route('/')
def home():
  return "ping"


@app.route("/send/<id>", methods=["GET"])
def send(id):
  bot.send("test", id)
  return id


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive(client):
  bot.set_client(client)
  t = Thread(target=run)
  t.start()
