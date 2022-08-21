from re import M
from discord.ext import commands
from discord import app_commands
import discord
from main import botcommands_command, me_command
from PIL import Image
from enum import Enum
from random import choice

game = 17
'''

example space dict
{
    "location": (17, 17),
    "piece": {"color": Color.RED, "id": 1},
}
'''

#TODO: test and fill in space data
space_data = {
    0: (16,0),
    1: (88, 0),
    2: (160, 0),
    3: (232, 0),
    4: (304, 0),
    5: (376, 0),
    6: (448, 0),
    7: (520, 0),
    8: (592, 0),
    9: (664, 0),
    10: (736, 0),
    11: (808, 0),
    12: (880, 0),
    13: (952, 0),
    14: (1024, 0),
    15: (1096, 0),
    16: (1096, 80),
    17: (1096, 152),
    18: (1096, 224),
    19: (1096, 296),
    20: (1096, 368),
    21: (1096, 440),
    22: (1096, 512),
    23: (1096, 584),
    24: (1096, 656),
    25: (1096, 728),
    26: (1096, 800),
    27: (1096, 872),
    28: (1096, 944),
    29: (1096, 1016),
    30: (1096, 1088),
    31: (1024, 1088),
    32: (952, 1088),
    33: (880, 1088),
    34: (808, 1088),
    35: (736, 1088),
    36: (664, 1088),
    37: (592, 1088),
    38: (520, 1088),
    39: (448, 1088),
    40: (376, 1088),
    41: (304, 1088),
    42: (232, 1088),
    43: (160, 1088),
    44: (88, 1088),
    45: (16, 1088),
    46: (16, 1016),
    47: (16, 944),
    48: (16, 872),
    49: (16, 800),
    50: (16, 728),
    51: (16, 656),
    52: (16, 584),
    53: (16, 512),
    54: (16, 440),
    55: (16, 368),
    56: (16, 296),
    57: (16, 224),
    58: (16, 152),
    59: (16, 80),
    "g1": (160, 80),
    "g2": (160, 152),
    "g3": (160, 224),
    "g4": (160, 296),
    "g5": (160, 368),
    "r1": (1024, 152),
    "r2": (952, 152),
    "r3": (880, 152),
    "r4": (808, 152),
    "r5": (736, 152),
    "b1": (952, 1016),
    "b2": (952, 944),
    "b3": (952, 872),
    "b4": (952, 800),
    "b5": (952, 728),
    "y1": (88, 944),
    "y2": (160, 944),
    "y3": (232, 944),
    "y4": (304, 944),
    "y5": (376, 944),
    "gh1": (248, 96),
    "gh2": (304, 128),
    "gh3": (360, 96),
    "rh1": (1000, 240),
    "rh2": (952, 288),
    "rh3": (1000, 328),
    "bh1": (752, 960),
    "bh2": (808, 938),
    "bh3": (864, 960),
    "yh1": (112, 832),
    "yh2": (160, 792),
    "yh3": (112, 752)

}

class Card(Enum):
    ONE = 1,
    TWO = 2,
    THREE = 3,
    FOUR = -4,
    FIVE = 5,
    SEVEN = 7,
    EIGHT = 8,
    NINE = 9,
    TEN = 10,
    ELEVEN = 11,
    TWELVE = 12
    SORRY = 13

availible_cards = [
    Card.ONE,
    Card.ONE,
    Card.ONE,
    Card.ONE,
    Card.ONE,
    Card.TWO,
    Card.TWO,
    Card.TWO,
    Card.TWO,
    Card.THREE,
    Card.THREE,
    Card.THREE,
    Card.THREE,
    Card.FOUR,
    Card.FOUR,
    Card.FOUR,
    Card.FOUR,
    Card.FIVE,
    Card.FIVE,
    Card.FIVE,
    Card.FIVE,
    Card.SEVEN,
    Card.SEVEN,
    Card.SEVEN,
    Card.SEVEN,
    Card.EIGHT,
    Card.EIGHT,
    Card.EIGHT,
    Card.EIGHT,
    Card.TEN,
    Card.TEN,
    Card.TEN,
    Card.TEN,
    Card.ELEVEN,
    Card.ELEVEN,
    Card.ELEVEN,
    Card.ELEVEN,
    Card.SORRY,
    Card.SORRY,
    Card.SORRY,
    Card.SORRY
]

used_cards = []



class GameState(Enum):
    AWAIT_ACCEPT = 1
    DRAW_CARD = 2
    CHOOSE_PIECE = 3
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
    Color.YELLOW: Image.open("data/sorryimages/yellow_piece.png"),
    1: Image.open("data/sorryimages/one.png"),
    2: Image.open("data/sorryimages/two.png"),
    3: Image.open("data/sorryimages/three.png")
}

homes = {
    Color.RED: ["rh1", "rh2", "rh3"],
    Color.YELLOW: ["yh1", "yh2", "yh3"],
    Color.GREEN: ["gh1", "gh2", "gh3"],
    Color.BLUE: ["bh1", "bh2", "bh3"]
}

class Game():
    
    def __init__(self, playerlist, message_id):
        self.playerlist = playerlist
        self.gamestate = GameState.AWAIT_ACCEPT
        self.board = {}
        self.current_turn = 0
        self.current_card = 5
        self.message_id = message_id
        #TODO: figure this out
        for key, value in space_data.items():
            self.board[key] = {"location": value, "piece": None}

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

        for player in self.playerlist:
            if player.color == Color.GREEN:
                self.board["gh1"]["piece"] = {"color": Color.GREEN, "id": 1}
                self.board["gh2"]["piece"] = {"color": Color.GREEN, "id": 2}
                self.board["gh3"]["piece"] = {"color": Color.GREEN, "id": 3}
            elif player.color == Color.YELLOW:
                self.board["yh1"]["piece"] = {"color": Color.YELLOW, "id": 1}
                self.board["yh2"]["piece"] = {"color": Color.YELLOW, "id": 2}
                self.board["yh3"]["piece"] = {"color": Color.YELLOW, "id": 3}
            elif player.color == Color.BLUE:
                self.board["bh1"]["piece"] = {"color": Color.BLUE, "id": 1}
                self.board["bh2"]["piece"] = {"color": Color.BLUE, "id": 2}
                self.board["bh3"]["piece"] = {"color": Color.BLUE, "id": 3}
            elif player.color == Color.RED:
                self.board["rh1"]["piece"] = {"color": Color.RED, "id": 1}
                self.board["rh2"]["piece"] = {"color": Color.RED, "id": 2}
                self.board["rh3"]["piece"] = {"color": Color.RED, "id": 3}
            else:
                print("ERROR PLAYER HAS NO COLOR")

        self.gamestate = GameState.DRAW_CARD

        #TODO: add discord avatar saving here

        generate_board(self)


        for player in self.playerlist:
            print(player.user.name, player.color)

    def get_space_by_piece(self, piece):
        for key, value in self.board.items():
            if value["piece"] == piece:
                return key
        return None


    def move_piece(self, piece, distance):
        messages = []
        space = self.get_space_by_piece(piece)
        print(f"space: {space}")
        _new_space = space

        from_spawn = False

        #spawn check
        if space in ["gh1", "gh2", "gh3", "yh1", "yh2", "yh3", "bh1", "bh2", "bh3", "rh1", "rh2", "rh3"]:
            if piece["color"] == Color.GREEN:
                #3 is hardcoded for the exit space of green home
                #negative cards arent checked as thats for on reaction add
                print("green lel")
                _new_space = 3 + distance
                from_spawn = True
                messages.append(f"You moved {str(distance)} spaces out of spawn.")
            elif piece["color"] == Color.YELLOW:
                _new_space = 48 + distance
                from_spawn = True
                messages.append(f"You moved {str(distance)} spaces out of spawn.")
            elif piece["color"] == Color.BLUE:
                _new_space = 33 + distance
                from_spawn = True
                messages.append(f"You moved {str(distance)} spaces out of spawn.")
            elif piece["color"] == Color.RED:
                _new_space = 18 + distance
                from_spawn = True
                messages.append(f"You moved {str(distance)} spaces out of spawn.")

        if not from_spawn:
            _new_space = space + distance

        #60 check
        if _new_space >= 60:
            _new_space -= 60

        #slide check
        if _new_space in [1, 9, 16, 24, 31, 39, 46, 54]:
            if piece["color"] == Color.RED:
                if _new_space in [1, 31, 46]:
                    for i in range(_new_space, _new_space + 4):
                        if self.board[i]["piece"] != None:
                            for j in ["rh1", "rh2", "rh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 3
                elif _new_space in [9, 39, 54]:
                    for i in range(_new_space, _new_space + 5):
                        if self.board[i]["piece"] != None:
                            for j in ["rh1", "rh2", "rh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 4
            elif piece["color"] == Color.BLUE:
                if _new_space in [1, 16, 46]:
                    for i in range(_new_space, _new_space + 4):
                        if self.board[i]["piece"] != None:
                            for j in ["bh1", "bh2", "bh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 3
                elif _new_space in [9, 24, 54]:
                    for i in range(_new_space, _new_space + 5):
                        if self.board[i]["piece"] != None:
                            for j in ["bh1", "bh2", "bh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 4
            elif piece["color"] == Color.GREEN:
                if _new_space in [16, 31, 46]:
                    for i in range(_new_space, _new_space + 4):
                        if self.board[i]["piece"] != None:
                            for j in ["gh1", "gh2", "gh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 3
                elif _new_space in [24, 39, 54]:
                    for i in range(_new_space, _new_space + 5):
                        if self.board[i]["piece"] != None:
                            for j in ["gh1", "gh2", "gh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 4
            elif piece["color"] == Color.YELLOW:
                if _new_space in [1, 16, 31]:
                    for i in range(_new_space, _new_space + 4):
                        if self.board[i]["piece"] != None:
                            for j in ["yh1", "yh2", "yh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 3
                elif _new_space in [9, 24, 39]:
                    for i in range(_new_space, _new_space + 5):
                        if self.board[i]["piece"] != None:
                            for j in ["yh1", "yh2", "yh3"]:
                                if self.board[j]["piece"] == None:
                                    self.board[j]["piece"] = self.board[i]["piece"]
                                    self.board[i]["piece"] = None
                                    messages.append("A piece was destroyed! (FIX)")
                                    break
                    _new_space += 4

        #piece in location check
        try:
            if self.board[_new_space]["piece"]["color"] == piece["color"]:
                return ["Invalid move! You can't move a piece to a space with a piece of your color on it."]
            elif self.board[_new_space]["piece"]["color"] != None:
                for i in homes[self.board[_new_space]["piece"]["color"]]:
                    if self.board[i]["piece"] == None:
                        self.board[i]["piece"] = self.board[_new_space]["piece"]
                        self.board[_new_space]["piece"] = None
                        messages.append("You knocked an opponent back to their spawn!")
                        break
        except (AttributeError, TypeError):
            pass

        self.board[_new_space]["piece"] = piece
        self.board[space]["piece"] = None
        if len(messages) == 0:
            messages.append(f"You moved {str(distance)} spaces.")
        return messages

def generate_board(game, is_choosing=None):
    if not is_choosing:
        board = images["board"].copy()
        for key, space in game.board.items():
            try:
                board.paste(images[space["piece"]["color"]], space["location"], images[space["piece"]["color"]])
            except (KeyError, TypeError):
                pass
    else:
        board = images["board"].copy()
        for key, space in game.board.items():
            try:
                if space["piece"]["color"] == is_choosing:
                    board.paste(images[space["piece"]["id"]], space["location"], images[space["piece"]["id"]])
            except (KeyError, TypeError):
                pass
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
    @botcommands_command()
    @commands.group()
    async def sorry(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send("Please use valid sub-command!")
    
    #create a sorry board
    @sorry.command()
    async def create(self, ctx, playercount: int, player2: discord.User, player3: discord.User = None, player4: discord.User = None):
        global game
        playerlist = [Player(i) for i in [ctx.author, player2, player3, player4] if i != None]
        if len(playerlist) != playercount:
            await ctx.send("PLAYER COUNT DOESNT MATCH")
            return
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
            await ctx.send("It's too late to cancel now!")
            return
        game = 17
        await ctx.send("Successfully cancelled the current game.")


    @sorry.command()
    async def draw(self, ctx):
        global game, availible_cards, used_cards
        if game == 17:
            await ctx.send("No game is currently running.")
            return
        if game.get_player_by_user(ctx.author) == None:
            await ctx.send("You are not in this game!")
            return
        if game.get_player_by_user(ctx.author) != game.playerlist[game.current_turn]:
            await ctx.send("It's not your turn!")
            return
        if len(availible_cards) == 0:
            availible_cards = used_cards
            used_cards = []
        game.current_card = choice(availible_cards)
        await ctx.send(game.current_card)
        generate_board(game, game.get_player_by_user(ctx.author).color)
        with open("current_frame.png", "rb") as f:
                    picture = discord.File(f)
                    message = await ctx.send("Which piece would you like to move?", file=picture)
                    game.message_id = message.id
                    await message.add_reaction("1️⃣")
                    await message.add_reaction("2️⃣")
                    await message.add_reaction("3️⃣")



    # EVENTS GROUP
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if game == 17:
            return
        if reaction.message_id != game.message_id:
            return
        player = game.get_player_by_user(reaction.member)
        if player != None:
            if game.gamestate == GameState.AWAIT_ACCEPT:
                player.ready = True
                if game.players_all_ready():
                    game.initialize()
                    with open("current_frame.png", "rb") as f:
                        picture = discord.File(f)
                        _channel = self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id)
                        await _channel.send("**Here are the colors:**")
                        _msg = "**"
                        for i in game.playerlist:
                            _msg = _msg + i.user.mention + ": " + str(i.color)[6:] + "\n"
                        _msg = _msg + "**"
                        await _channel.send(_msg)
                        await _channel.send("| ~ ***CURRENT BOARD*** ~ |", file=picture)
                        await _channel.send(f"{game.playerlist[game.current_turn].user.mention}, it's your turn!")

            elif game.gamestate == GameState.DRAW_CARD:
                #if game.current_card != Card.SEVEN and game.current_card != Card.TEN and game.current_card != Card.ELEVEN and game.current_card != Card.SORRY:
                if str(reaction.emoji) == "1️⃣":
                    messages = game.move_piece({"color": game.playerlist[game.current_turn].color, "id": 1}, game.current_card.value[0])
                    generate_board(game)
                    with open("current_frame.png", "rb") as f:
                        picture = discord.File(f)
                        _channel = self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id)
                        await _channel.send(*messages)
                        await _channel.send("| ~ ***CURRENT BOARD*** ~ |", file=picture)
                        game.current_turn += 1
                        if game.current_turn >= len(game.playerlist):
                            game.current_turn = 0
                        await _channel.send(f"{game.playerlist[game.current_turn].user.mention}, it's your turn!")
                elif str(reaction.emoji) == "2️⃣":
                    messages = game.move_piece({"color": game.playerlist[game.current_turn].color, "id": 2}, game.current_card.value[0])
                    generate_board(game)
                    with open("current_frame.png", "rb") as f:
                        picture = discord.File(f)
                        _channel = self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id)
                        await _channel.send(*messages)
                        await _channel.send("| ~ ***CURRENT BOARD*** ~ |", file=picture)
                        game.current_turn += 1
                        if game.current_turn >= len(game.playerlist):
                            game.current_turn = 0
                        await _channel.send(f"{game.playerlist[game.current_turn].user.mention}, it's your turn!")
                elif str(reaction.emoji) == "3️⃣":
                    messages = game.move_piece({"color": game.playerlist[game.current_turn].color, "id": 3}, game.current_card.value[0])
                    generate_board(game)
                    with open("current_frame.png", "rb") as f:
                        picture = discord.File(f)
                        _channel = self.bot.get_guild(reaction.guild_id).get_channel(reaction.channel_id)
                        await _channel.send(*messages)
                        await _channel.send("| ~ ***CURRENT BOARD*** ~ |", file=picture)
                        game.current_turn += 1
                        if game.current_turn >= len(game.playerlist):
                            game.current_turn = 0
                        await _channel.send(f"{game.playerlist[game.current_turn].user.mention}, it's your turn!")
        

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Sorry(bot))