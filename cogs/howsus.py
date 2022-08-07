from discord.ext import commands
from main import botcommands_command

class HowSus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @botcommands_command()
  async def howsus(self, ctx):
    await ctx.reply("You are 69% sus. ඞ")

async def setup(bot):
  await bot.add_cog(HowSus(bot))