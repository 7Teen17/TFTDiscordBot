from discord.ext import commands
import json
from main import admin_command, botcommands_command

class Counting(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    with open("data/database.json", "r") as f:
      self.number = json.load(f)["counting"][0]

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.channel.id == 1000212818064310374:
      try:
        new_number = int(message.content)
        with open("data/database.json", "r") as f:
          self.number = json.load(f)["counting"][0]
        if new_number == self.number + 1:
          with open("data/database.json", "r") as f:
            data = json.load(f)
          if data["counting"][1] != message.author.name:
            await message.add_reaction("✅")
            self.number += 1
            with open("data/database.json", "r") as f:
              data = json.load(f)
            data["counting"] = [self.number, message.author.name]
            with open('data/database.json', 'w') as f:
              json.dump(data, f, indent=4)
          else:
            await message.delete()
        else:
          await message.delete()
      except ValueError:
        await message.delete()

  @commands.command()
  @admin_command()
  @botcommands_command()
  async def countingnumber(self, ctx, number: int):
    self.number = number
    with open("data/database.json", "r") as f:
      data = json.load(f)
    data["counting"][0] = self.number
    with open('data/database.json', 'w') as f:
      json.dump(data, f, indent=4)
    await ctx.send(f"Successfully set the current number to {number}.")
    

async def setup(bot):
  await bot.add_cog(Counting(bot))