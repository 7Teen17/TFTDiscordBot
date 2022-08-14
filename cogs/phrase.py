from discord.ext import commands
import discord

is_guessed = False
class Phrase(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        global is_guessed
        if ctx.author.id == 634173087402950666:
            return
        if ctx.content.lower() == "rubiks" or ctx.content.lower() == "rubik's":
            if not is_guessed:
                is_guessed = True
                embed = discord.Embed(title=f"**BIG FAT WINNER**", description=f"You guessed the phrase correctly. NICE!")
                embed.set_thumbnail(url=str(ctx.author.avatar))
                await ctx.reply(embed=embed)
                await ctx.channel.send(discord.utils.get(ctx.guild.members, id=743939387334721607).mention)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Phrase(bot))