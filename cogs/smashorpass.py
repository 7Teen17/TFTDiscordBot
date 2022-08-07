from discord.ext import commands

class Smashorpass(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self, message):
    if len(message.attachments) != 0:
      if message.channel.id == 971257148522770512:
        await message.add_reaction("🔥")

      elif message.channel.id == 927081047907266570:
        await message.add_reaction("✅")
        await message.add_reaction("❌")

async def setup(bot):
  await bot.add_cog(Smashorpass(bot))