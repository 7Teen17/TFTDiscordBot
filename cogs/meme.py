from discord.ext import commands
import aiohttp

class Meme(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def megamind(self, ctx, *, caption: str):
    async with aiohttp.ClientSession() as session:
      async with session.post("https://api.imgflip.com/caption_image", data={"template_id": "370850147", "username": "7Teen", "password": "One23456789!", "text0": caption, "text1": ""}) as response:
        response = await response.json()
        if response["success" ]:
          await ctx.send(response["data"]["url"])
        else: 
          await ctx.send(response["error_message"])

async def setup(bot):
  await bot.add_cog(Meme(bot))