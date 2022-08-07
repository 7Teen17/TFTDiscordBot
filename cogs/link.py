import discord
from discord.ext import commands
from main import botcommands_command

class Link(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='link', description="Returns the rickroll link.")
  @botcommands_command()
  async def link(self, ctx):
    await ctx.send(
  	    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  	)


async def setup(bot):
  await bot.add_cog(Link(bot))