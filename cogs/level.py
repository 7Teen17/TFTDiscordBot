import discord
import json
import time
from discord.ext import commands

class Level(commands.Cog):
  def __init__(self, bot):
    self.bot = bot


  async def check_new(self, users, user):
    if str(user.id) in users:
      return
    users[str(user.id)] = {
      "experience": 0,
      "total_xp": 0,
      "level": 1,
      "lvl_end": 10,
      "last_message": time.time()
    }
    with open('data/levels.json', 'w') as f:
      json.dump(users, f, indent=4)

  async def add_xp(self, users, user, xp, message):
    users[str(user.id)]["experience"] += xp
    users[str(user.id)]["total_xp"] += xp
    if users[str(user.id)]["experience"] >= users[str(user.id)]["lvl_end"]:
      users[str(user.id)]["level"] += 1
      embed = discord.Embed(title="**LEVEL UP!**", description=f"{user.mention} has leveled up to level {users[str(user.id)]['level']}!\nReward: nothing lol", color=discord.Color.random())
      embed.set_thumbnail(url=str(user.avatar))
      users[str(user.id)]["experience"] = 0
      
      users[str(user.id)]["lvl_end"] += 1
      await message.guild.get_channel(989594141275062272).send(embed=embed)
      
      
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.guild.id != 917800744453804043:
      return
    if message.author.bot or message.channel.id == 1000212818064310374:
      return
    valid = 0
    async for chat in message.channel.history(limit=3):
      if chat.author == message.author or chat.author.bot:
        valid += 1
    if valid == 3:
      return
    with open("data/levels.json", "r") as f:
      users = json.load(f)
    await self.check_new(users, message.author)
    if time.time() - users[str(message.author.id)]["last_message"] < 1.7:
      return
    
    await self.add_xp(users, message.author, 1, message)
    users[str(message.author.id)]["last_message"] = time.time()

    with open('data/levels.json', 'w') as f:
      json.dump(users, f, indent=4)


  @commands.command()
  async def level(self, ctx, member: discord.Member = None):
    if ctx.channel.name != "bot-commands":
      return
    member = member or ctx.author
    with open("data/levels.json", "r") as f:
      users = json.load(f)
    await self.check_new(users, member)
    embed = discord.Embed(title=f"{member.name}\'s Level", description=f"**Level {users[str(member.id)]['level']}\nXP:** {users[str(member.id)]['experience']}/{users[str(member.id)]['lvl_end']}\n**Total XP:** {users[str(member.id)]['total_xp']}")
    embed.set_thumbnail(url=str(member.avatar))
    await ctx.send(embed=embed)

  @commands.command()
  async def leaderboard(self, ctx):
    if ctx.channel.name != "bot-commands":
      return
    with open("data/levels.json", "r") as f:
      users = json.load(f)
    leaderboard = []
    for i in users.keys():
      leaderboard.append([users[i]["total_xp"], i, users[i]["level"]])
    leaderboard = sorted(leaderboard, key = lambda item: item[0], reverse=True)
    embed = discord.Embed(title="TFT Good Leaderboard", color=discord.Color.blurple())
    for i in range(10 if len(leaderboard) >=10 else len(leaderboard)):
      embed.add_field(name=f"**#{i+1}**: ", value=f"<@{leaderboard[i][1]}>: Level {users[str(leaderboard[i][1])]['level']}, Total XP: {users[str(leaderboard[i][1])]['total_xp']}", inline=False)
    await ctx.send(embed=embed)
    

async def setup(bot):
  await bot.add_cog(Level(bot))