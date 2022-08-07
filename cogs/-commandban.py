from discord.ext import commands
import discord
from main import admin_command
import json


class CommandBan(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bans = {}

    @commands.command()
    @admin_command()
    async def commandban(self, ctx, user: discord.Member, command: str):
        with open("commandbans.json", "r") as f:
            self.bans = json.load(f)

        try:
            if command not in self.bans[str(user.id)]:
                self.bans[str(user.id)].append(command)
        except KeyError:
            self.bans[str(user.id)] = [command]

        with open('commandbans.json', 'w') as f:
            json.dump(self.bans, f)

    async def commandunban(self, ctx, user: discord.Member, command: str):
        with open("commandbans.json", "r") as f:
            self.bans = json.load(f)

        try:
            if command in self.bans[str(user.id)]:
                self.bans[str(user.id)].remove(command)
        except KeyError:
            pass

        with open('commandbans.json', 'w') as f:
            json.dump(self.bans, f)

    def me_command():
        bans = self.bans

        async def predicate(ctx):
            with open("commandbans.json", "r") as f:
                bans = json.load(f)
            return

        return commands.check(predicate)
