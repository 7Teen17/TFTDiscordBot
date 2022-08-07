from discord.ext import commands
import time
from main import botcommands_command

class WhoAsked(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.last_asked = time.time() - 61
    with open('data/whoasked.txt', "r") as f:
      try:
        self.who_asked_counter = int(f.readline().rstrip())
      except ValueError:
        self.who_asked_counter = 0
  
  @commands.command()
  @botcommands_command()
  async def whoasked(self, ctx):
    await ctx.send(f"Total who/when/what responses: {self.who_asked_counter}")
    
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.content.lower() == "who?" or message.content.lower() == "who":
      if time.time() - self.last_asked < 60.0:
        #await self.bot.process_commands(message)
        return
      self.last_asked = time.time()
      await message.channel.send("asked")
      self.who_asked_counter += 1
      with open("data/whoasked.txt", "w") as f:
        f.write(str(self.who_asked_counter))

    elif message.content.lower() == "when?" or message.content.lower() == "when":
      if time.time() - self.last_asked < 60.0:
        return
      self.last_asked = time.time()
      await message.channel.send("did I ask")
      self.who_asked_counter += 1
      with open("data/whoasked.txt", "w") as f:
        f.write(str(self.who_asked_counter))

    elif message.content.lower() == "what?" or message.content.lower() == "what":
      if time.time() - self.last_asked < 60.0:
        return
      self.last_asked = time.time()
      await message.channel.send("ever")
      self.who_asked_counter += 1
      with open("data/whoasked.txt", "w") as f:
        f.write(str(self.who_asked_counter))

    elif message.content.lower() == "you know what that sounds like" or message.content.lower() == "you know what that sounds like?":
      if time.time() - self.last_asked < 60.0:
        return
      self.last_asked = time.time()
      await message.channel.send("A SKILL ISSUE")

async def setup(bot):
  await bot.add_cog(WhoAsked(bot))