from discord.ext import commands
import discord
from main import botcommands_command
import aiohttp
import json


class TaylorSwift(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.current_quote = ""
        self.availible = True
        self.current_user = ""
        self.total_correct = 0
        self.counter_eligible = True
        self.cooldowns = {}
        self.is_album = False
        with open("data/ts.json", "r") as f:
            self.total_correct = json.load(f)["correct"]

    @commands.command()
    @botcommands_command()
    async def taylorquote(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.is_album = False
                embed = discord.Embed(title="What Taylor Swift song is this from?", description=response["quote"])
                await ctx.send(embed=embed)


    @commands.command()
    @botcommands_command()
    async def tayloralbum(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.is_album = True
                embed = discord.Embed(title="What Taylor Swift album is this from?", description=response["quote"])
                await ctx.send(embed=embed)

    @commands.command()
    @botcommands_command()
    async def tayloracronym(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.is_album = False
                acronym = ""
                for i in response["song"].split(" "):
                    acronym = acronym + i[0]
                embed = discord.Embed(title="What Taylor Swift song has this acronym?", description=acronym.upper())
                await ctx.send(embed=embed)
    

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if not message.reference.cached_message.author.bot:
                return
        except AttributeError:
            return
        if self.availible:
            return
        #if not message.author.name == self.current_user:
            #return
        if not self.is_album:
            if "".join(filter(lambda x: x.isalnum(), message.content.lower())) != "".join(filter(lambda x: x.isalnum(), self.current_quote["song"].lower())):
                await message.reply("Incorrect!")
                self.counter_eligible = False
                return
        else:
            if "".join(filter(lambda x: x.isalnum(), message.content.lower())) != "".join(filter(lambda x: x.isalnum(), self.current_quote["album"].lower())):
                await message.reply("Incorrect!")
                self.counter_eligible = False
                return
        if self.counter_eligible:
            with open("data/ts.json", "r") as f:
                self.total_correct = json.load(f)["correct"] + 1
            with open("data/ts.json", "w") as f:
                json.dump({"correct": self.total_correct}, f, indent=4)
            
        await message.reply("Correct!")
        self.availible = True
        self.counter_eligible = True

    @commands.command()
    @botcommands_command()
    async def tsanswer(self, ctx):
        if self.availible:
            await ctx.send("A Taylor Swift quote is not being guessed!")
            return
        #if ctx.author.name != self.current_user:
            #await ctx.send("You are not the one that generated the quote!")
            #return
        self.availible = True
        await ctx.send(f"**Correct Answer:** {self.current_quote['song']}\n**Album:** {self.current_quote['album']}")

    @commands.command()
    @botcommands_command()
    async def tscorrect(self, ctx):
        with open("data/ts.json", "r") as f:
                self.total_correct = json.load(f)["correct"]
        await ctx.send(f"Taylor Swift quotes identified correctly: {self.total_correct}")
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TaylorSwift(bot))