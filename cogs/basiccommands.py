from discord.ext import commands
from main import admin_command, botcommands_command

class BasicCommands(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @admin_command()
  async def purge(self, ctx, number: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=number)
    await ctx.send(f"Deleted {number} messages.", delete_after=3)

  @commands.command()
  @botcommands_command()
  async def source(self, ctx):
    await ctx.send("https://github.com/7Teen17/TFTDiscordBot")
    
async def setup(bot):
  await bot.add_cog(BasicCommands(bot))