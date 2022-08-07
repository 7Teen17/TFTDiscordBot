from discord.ext import commands
from main import me_command
import os

class Reload(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @me_command()
  async def reload(self, ctx, name):
    await ctx.send("Reloading cog." + name)
    await self.bot.reload_extension("cogs." + name)
    await ctx.send("Done.")

  @commands.command()
  @me_command()
  async def reloadall(self, ctx):
    for i in os.listdir("cogs"):
        if i[-3:] == ".py" and not "-" in i and i != "reload.py":
          print(f"Reloading cogs.{i[:-3]} ...")
          await self.bot.reload_extension(f"cogs.{i[:-3]}")
          print("Done.")
  
  @commands.command()
  @me_command()
  async def addcog(self, ctx, name):
    await ctx.send("Adding cog." + name)
    await self.bot.load_extension("cogs." + name)
    await ctx.send("Done.")

  @commands.command()
  @me_command()
  async def removecog(self, ctx, name):
    await ctx.send("Removing cog." + name)
    await self.bot.unload_extension("cogs." + name)
    await ctx.send("Done.")

async def setup(bot):
  await bot.add_cog(Reload(bot))