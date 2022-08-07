from discord.ext import commands
from discord import app_commands
import discord
from main import me_command
from PIL import Image
from enum import Enum
from random import choice

game = 17
'''
example piece dict
{
    "color": Color.RED,
    "id": 1
}

example space dict
{
    "location": (17, 17),
    "piece": {"color": Color.RED, "id": 1},
}
'''

#TODO: test and fill in space data
space_data = {
    0: (16,0),
    1: (96, 0),
    2: (256, 0),
    3: (),
    4: ()

}



# game state enum?
class GameState(Enum):
    AWAIT_ACCEPT = 1
    PLAYERONE_TURN = 2
    PLAYERTWO_TURN = 3
    PLAYERTHREE_TURN = 4
    PLAYERFOUR_TURN = 5
    GAME_OVER = 6

class Color(Enum):
    RED = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4

images = {
    "board": Image.open("data/sorryimages/base_board.png"),
    Color.RED: Image.open("data/sorryimages/red_piece.png"),
    Color.BLUE: Image.open("data/sorryimages/blue_piece.png"),
    Color.GREEN: Image.open("data/sorryimages/green_piece.png"),
    Color.YELLOW: Image.open("data/sorryimages/yellow_piece.png")
}

class Game():
    
    def __init__(self, playerlist, message_id):
        self.playerlist = playerlist
        self.gamestate = GameState.AWAIT_ACCEPT
        self.board = {}
        self.current_card = 5
        self.message_id = message_id
        #TODO: figure this out
        for key, value in space_data.items():
            self.board[key] = {"location": value, "piece": {"color": Color.GREEN, "id": 1}}
        self.board[0] = {"location": (304,0), "piece": {"color": Color.GREEN, "id": 1}}

    def get_player_by_user(self, user: discord.User):
        for player in self.playerlist:
            if player.user == user:
                return player
        return None

    def players_all_ready(self):
        for player in self.playerlist:
            if not player.ready:
                return False
        return True

    def initialize(self):
        
        #random color attribution

        availible_colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]

        #OPTION 1: always give green to me
        tempplayers = [i for i in self.playerlist]
        for player in tempplayers:
            if player.user.id == 743939387334721607:
                player.color = Color.GREEN
                availible_colors.remove(Color.GREEN)
                tempplayers.remove(player)
        for player in tempplayers:
            player.color = choice(availible_colors)
            availible_colors.remove(player.color)

        #OPTION 2: actually random
        #for player in self.playerlist:
            #player.color = choice(availible_colors)
            #availible_colors.remove(player.color)

        generate_board(self)


        for player in self.playerlist:
            print(player.user.name, player.color)


def generate_board(game):
    board = images["board"].copy()
    for key, space in game.board.items():
        try:
            board.paste(images[space["piece"]["color"]], space["location"], images[space["piece"]["color"]])
        except TypeError:
            print("type error")
    board.save("current_frame.png")

#basically a data class
class Player():

    def __init__(self, user):
        self.user = user
        self.ready = False
        self.color = None

class Sorry(commands.Cog):
    bot: commands.Bot

    def __init__(self, bot):
        self.bot = bot

    # OTHER FUNCTIONS GROUP

    async def display_board(game, channel):
        pass


    # COMMANDS GROUP

    #Base Sorry command
    @me_command()
    @commands.group()
    async def sorry(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send("Please use valid sub-command!")
    
    #create a sorry board
    @sorry.command()
    async def create(self, ctx, playercount: int, player2: discord.User, player3: discord.User = None, player4: discord.User = None):
        global game
        playerlist = [Player(i) for i in [ctx.author, player2, player3, player4] if i != None]
        if game != 17:
            await ctx.send("A game is currently in progress!")
            return
        if ctx.author in [player2, player3, player4]:
            await ctx.send("You can't invite yourself, silly!")
            return
        with open("data/sorryimages/start_screen.png", "rb") as f:
            picture = discord.File(f)
            if len(playerlist) == 2:
                message = await ctx.send(f"**Hey {player2.mention}, {ctx.author.mention} invited you to a game of Sorry! React with ✅ to enter!**", file=picture)
                await message.add_reaction("✅")
                messageid = message.id
            elif len(playerlist) == 3:
                message = await ctx.send(f"**Hey {player2.mention} and {player3.mention}, {ctx.author.mention} invited you to a game of Sorry! React with ✅ to enter!**", file=picture)
                await message.add_reaction("✅")
                messageid = message.id
            elif len(playerlist) == 4:
                message = await ctx.send(f"**Hey {player2.mention}, {player3.mention}, and {player4.mention}, {ctx.author.mention} invited you to a game of Sorry! React with ✅ to enter!**", file=picture)
                await message.add_reaction("✅")
                messageid = message.id
            else:
                await ctx.send("**ERROR:** Variable `playerlist` has invalid value. Please report to the developer.")
        game = Game(playerlist, messageid)


    @sorry.command()
    async def cancel(self, ctx):
        global game
        if game == 17:
            await ctx.send("No game is currently running.")
            return
        if game.get_player_by_user(ctx.author) == None:
            await ctx.send("You can't cancel a game you weren't invited to.")
            return
        if game.gamestate != GameState.AWAIT_ACCEPT:
            await ctx.send("Its too late to cancel now!")
            return
        game = 17
        await ctx.send("Successfully cancelled the current game.")
        


    # EVENTS GROUP
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if game == 17:
            return
        if reaction.message_id != game.message_id:
            return
        player = game.get_player_by_user(reaction.member)
        if player != None:
            player.ready = True
            if game.players_all_ready():
                game.initialize()
                with open("current_frame.png", "rb") as f:
                    picture = discord.File(f)
                    await self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id).send("**Heres the current board.**", file=picture)
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sorry(bot))