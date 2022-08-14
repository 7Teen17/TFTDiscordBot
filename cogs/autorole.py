import discord
from discord.ext import commands
from main import me_command
import json

class Autorole(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    with open("data/autoroles.json", "r") as f:
      self.autorole_messages = json.load(f)

  @me_command()
  @commands.group()
  async def autorole(self, ctx):
    pass

  @autorole.command()
  async def create(self, ctx, role: discord.Role, title, *, description: str):
    embed = discord.Embed(title=title, description=description, color=discord.Color.og_blurple())
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")
    self.autorole_messages[str(message.id)] = role.id
    await ctx.message.delete()
    with open('data/autoroles.json', 'w') as f:
      json.dump(self.autorole_messages, f, indent=4)

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    with open("data/autoroles.json", "r") as f:
      self.autorole_messages = json.load(f)
    if str(payload.message_id) in self.autorole_messages:
      await payload.member.add_roles(self.bot.get_guild(917800744453804043).get_role(self.autorole_messages[str(payload.message_id)]))
    with open('data/autoroles.json', 'w') as f:
      json.dump(self.autorole_messages, f, indent=4)

  @commands.Cog.listener()
  async def on_raw_reaction_remove(self, payload):
    with open("data/autoroles.json", "r") as f:
      self.autorole_messages = json.load(f)
    if str(payload.message_id) in self.autorole_messages:
      await self.bot.get_guild(917800744453804043).get_member(payload.user_id).remove_roles(self.bot.get_guild(917800744453804043).get_role(self.autorole_messages[str(payload.message_id)]))
    with open('data/autoroles.json', 'w') as f:
      json.dump(self.autorole_messages, f, indent=4)

  @commands.Cog.listener()
  async def on_raw_message_delete(self, payload):
    with open("data/autoroles.json", "r") as f:
      self.autorole_messages = json.load(f)
    if str(payload.message_id) in self.autorole_messages:
      self.autorole_messages.pop(str(payload.message_id))
    with open('data/autoroles.json', 'w') as f:
      json.dump(self.autorole_messages, f, indent=4)
      

async def setup(bot):
  await bot.add_cog(Autorole(bot))
    