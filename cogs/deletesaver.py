from discord.ext import commands
from main import admin_command

class DeleteSaver(commands.Cog):
  def __init__(self, bot):
      self.bot = bot
      self.enabled = True

  @commands.Cog.listener()
  async def on_raw_message_delete(self, message):
    if not self.enabled:
      return
    try:
      if message.cached_message.channel.name == "counting" or message.cached_message.channel.name == "message-logs" or message.cached_message.content[0] == "$" or message.cached_message.author.bot:
        return
      await message.cached_message.guild.get_channel(990096838134743051).send(f"{message.cached_message.channel.mention} {message.cached_message.author.mention}** deleted:** {message.cached_message.content}")
    except AttributeError:
      await self.bot.get_guild(917800744453804043).get_channel(990096838134743051).send("**[INFO]** A message was deleted but it was not in the message cache so it was not recorded.")

  @commands.command()
  @admin_command()
  async def togglesave(self, ctx, enabled: bool):
    self.enabled = enabled
    await ctx.send("Successfully " + ("enabled" if enabled else "disabled") + " message logs.")
      

async def setup(bot):
  await bot.add_cog(DeleteSaver(bot))