import discord
import os
from keep_alive import keep_alive
from MO import discordMO

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# クライアントの生成
client = discord.Client(intents=intents)
mo: discordMO

# discordと接続した時に呼ばれる
@client.event
async def on_ready():
  global mo
  mo = discordMO(client)
  print(f'We have logged in as {client.user}')



# メッセージを受信した時に呼ばれる
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  # メッセージが"$hello"で始まっていたら"Hello!"と応答
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!1.1.6')
  
  await mo(message)


@client.event
async def on_voice_state_update(member, before, after):
  ch_name = "使い捨て"
  overwrites = {
    member.guild.default_role:
    discord.PermissionOverwrite(read_messages=False),
    member: discord.PermissionOverwrite(read_messages=True),
    member.guild.me: discord.PermissionOverwrite(read_messages=True)
  }

  def get_category(channel):
    return channel.category if channel.category else channel.guild

  def get_ch_names(category):
    return [c.name for c in category.channels]

  if before.channel:
    category = get_category(before.channel)
    ch_names = get_ch_names(category)
    # チャンネル削除
    if (len(before.channel.members) == 0 and ch_name in ch_names and type(
        category.channels[ch_names.index(ch_name)]) == discord.TextChannel):
      await category.channels[ch_names.index(ch_name)].delete()

    # パーミッション更新
    else:
      await category.channels[ch_names.index(ch_name)
                              ].set_permissions(member, read_messages=False)

  if after.channel:
    category = get_category(after.channel)
    ch_names = get_ch_names(category)
    # チャンネル生成
    if (ch_name not in ch_names or type(
        category.channels[ch_names.index(ch_name)]) != discord.TextChannel):
      await member.guild.create_text_channel(ch_name,
                                             category=category,
                                             overwrites=overwrites)
    # パーミッション更新
    else:
      await category.channels[ch_names.index(ch_name)
                              ].set_permissions(member, read_messages=True)


keep_alive(client)
TOKEN = os.getenv("BOT_TOKEN")
try:
  client.run(TOKEN)
except:
  os.system("kill 1")