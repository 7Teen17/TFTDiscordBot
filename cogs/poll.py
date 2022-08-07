import discord
from discord.ext import commands
numbers = {
  1: ["one", "1️⃣"],
  2: ["two", "2️⃣"],
  3: ["three", "3️⃣"],
  4: ["four", "4️⃣"],
  5: ["five", "5️⃣"],
  6: ["six", "6️⃣"],
  7: ["seven", "7️⃣"],
  8: ["eight", "8️⃣"],
  9: ["nine", "9️⃣"],
  10: ["ten", "🔟"]
}
class Poll(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  @commands.command(name='poll', description='Creates a poll to vote on')
  async def poll(self, ctx, title, *args):
    if args == None or len(args) > 10:
      await ctx.send("ERROR: Either no options or too many.")
    else:
      description = ""
      for count, arg in enumerate(args):
        if count == 0:
          description = description + f":{numbers[count+1][0]}: {arg},"
        elif count == len(args) - 1:
          description = description + f" :{numbers[count+1][0]}: {arg}"
        else:
          description = description + f" :{numbers[count+1][0]}: {arg},"
      embed = discord.Embed(title=title, description=description, color=discord.Color.blue())
      embed.set_author(name=ctx.author, icon_url=str(ctx.author.avatar))
      message = await ctx.send(embed=embed)
      for i in range(len(args)):
        await message.add_reaction(numbers[i+1][1])


async def setup(bot):
  await bot.add_cog(Poll(bot))