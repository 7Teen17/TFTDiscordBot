from discord.ext import commands
from main import admin_command

class Purge(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  @admin_command()
  async def purge(self, ctx, number: int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=number)
    await ctx.send(f"Deleted {number} messages.", delete_after=3)
    
async def setup(bot):
  await bot.add_cog(Purge(bot))