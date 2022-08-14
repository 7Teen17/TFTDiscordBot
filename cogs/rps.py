from discord.ext import commands
import discord


class RPS(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot
        self.message1 = 17
        self.player1 = 17
        self.player2 = 17
        self.message2 = 17
        self.messageI = 17
        self.player1ans = 17
        self.player2ans = 17

    @commands.command()
    async def rps(self, ctx, other: discord.Member):
        rpsembed = discord.Embed(title="**Here are your options!**", description="**Rock, Paper, and Scissors**")
        self.message1 = await ctx.author.send(embed=rpsembed)
        self.player1 = ctx.author
        await self.message1.add_reaction('🪨')
        await self.message1.add_reaction('📜')
        await self.message1.add_reaction('💀')
        self.message2 = await other.send(embed=rpsembed)
        self.player2 = other
        await self.message2.add_reaction('🪨')
        await self.message2.add_reaction('📜')
        await self.message2.add_reaction('💀')
        self.messageI = ctx

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.user_id == 989023558623690782:
            return
        try:
            if reaction.message_id == self.message1.id:
                if str(reaction.emoji) == "🪨":
                    self.player1ans = "rock"
                elif str(reaction.emoji) == "📜":
                    self.player1ans = "paper"
                elif str(reaction.emoji) == "💀":
                    self.player1ans = "scissors"
            elif reaction.message_id == self.message2.id:
                if str(reaction.emoji) == "🪨":
                    self.player2ans = "rock"
                elif str(reaction.emoji) == "📜":
                    self.player2ans = "paper"
                elif str(reaction.emoji) == "💀":
                    self.player2ans = "scissors"
            if self.player1ans != 17 and self.player2ans != 17:
                winner = find_winner(self.player1ans, self.player2ans)
                print(winner)
                self.player1ans = 17
                self.player2ans = 17
                if winner == "tie":
                    await self.messageI.send(f"It was a tie.")
                elif winner == "p1":
                    await self.messageI.send(f"{self.player1.mention} wins!")
                else:
                    await self.messageI.send(f"{self.player2.mention} wins!")
        except AttributeError:
            pass

def find_winner(player1, player2):
    if player1 == player2:
        return "tie"
    elif player1 == "rock":
        if player2 == "scissors":
            return "p1"
        else:
            return "p2"
    elif player1 == "paper":
        if player2 == "rock":
            return "p1"
        else:
            return "p2"
    elif player1 == "scissors":
        if player2 == "paper":
            return "p1"
        else:
            return "p2"


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(RPS(bot))