import discord
from discord.ext import commands
from main import botcommands_command

class Mcstatus(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='mcstatus', description="Returns the status of the tftgood.minehut.gg minecraft server")
  @botcommands_command()
  async def mcstatus(self, ctx):
    await ctx.send("https://mcapi.us/server/image?ip=tftgood.minehut.gg&theme=dark")


async def setup(bot):
  await bot.add_cog(Mcstatus(bot))