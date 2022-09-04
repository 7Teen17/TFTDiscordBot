import discord
import os
import discord.ext
from discord.ext import commands, tasks
from keep_alive import keep_alive
import asyncio
import time

last_asked = time.time()

intents = discord.Intents.all()
#intents.message_content = True
#intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.event
async def on_ready():
  game = discord.Game("Wii Sports")
  await bot.change_presence(status=discord.Status.online, activity=game)
  for i in os.listdir("cogs"):
    if i[-3:] == ".py" and i[0] != "-":
      print(f"Loading cogs.{i[:-3]} ...")
      await bot.load_extension(f"cogs.{i[:-3]}")
      print("Done.")
  print("The bot is online! Go use it.")

def me_command():
    async def predicate(ctx):
        return ctx.author.id == 743939387334721607 or ctx.author.id == 862374209309245461
    return commands.check(predicate)

def admin_command():
  async def predicate(ctx):
    return ctx.author.get_role(918698095573884938) != None or ctx.author.get_role(929144746016927795) != None
  return commands.check(predicate)

def botcommands_command():
    async def predicate(ctx):
        return ctx.channel.name == "bot-commands" or ctx.channel.name == "bot-testing"
    return commands.check(predicate)


if __name__ == "__main__":
  with open("bottoken.txt", "r") as f:
    bottoken = f.read()
  bot.run(bottoken)