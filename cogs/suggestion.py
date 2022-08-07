from discord.ext import commands
import discord
from main import botcommands_command

class Suggestion(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='suggestion', description="Suggest something to be added to TFT or Matt.")
  @botcommands_command()
  async def suggestion(self, ctx, *args):
    embed = discord.Embed(title="Suggestion", description=" ".join(args), color=discord.Color.green())
    embed.set_author(name=ctx.author, icon_url=str(ctx.author.avatar))
    message = await ctx.guild.get_channel(989660038115250207).send(embed=embed)
    await message.create_thread(name=" ".join(args), reason=" ".join(args))
    await ctx.message.reply("Thank you for your suggestion. That was a great idea!")

async def setup(bot):
  await bot.add_cog(Suggestion(bot))