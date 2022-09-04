from discord.ext import commands
import discord
from main import botcommands_command
import aiohttp
import json
from time import time
from random import randint, choice

tracks = {
"Tim McGraw": [1, "Taylor Swift"],
"Picture to Burn": [2, "Taylor Swift"],
"Teardrops on My Guitar": [3, "Taylor Swift"],
"A Place in This World": [4, "Taylor Swift"],
"Cold as You": [5, "Taylor Swift"],
"The Outside": [6, "Taylor Swift"],
"Tied Together with a Smile": [7, "Taylor Swift"],
"Stay Beautiful": [8, "Taylor Swift"],
"Should’ve Said No": [9, "Taylor Swift"],
"Mary’s Song (Oh My My My)": [10, "Taylor Swift"],
"Our Song": [11, "Taylor Swift"],
"I’m Only Me When I’m with You": [12, "Taylor Swift"],
"Invisible": [13, "Taylor Swift"],
"A Perfectly Good Heart": [14, "Taylor Swift"],
"Fearless": [1, "Fearless"],
"Fifteen": [2, "Fearless"],
"Love Story": [3, "Fearless"],
"Hey Stephen": [4, "Fearless"],
"White Horse": [5, "Fearless"],
"You Belong with Me": [6, "Fearless"],
"Breathe": [7, "Fearless"],
"Tell Me Why": [8, "Fearless"],
"You’re Not Sorry": [9, "Fearless"],
"The Way I Loved You": [10, "Fearless"],
"Forever & Always": [11, "Fearless"],
"The Best Day": [12, "Fearless"],
"Change": [13, "Fearless"],
"Jump Then Fall": [14, "Fearless"],
"Untouchable": [15, "Fearless"],
"Forever & Always (Piano Version)": [16, "Fearless"],
"Come in with the Rain": [17, "Fearless"],
"Superstar": [18, "Fearless"],
"The Other Side of the Door": [19, "Fearless"],
"Today Was a Fairytale": [20, "Fearless"],
"You All Over M": [21, "Fearless"],
"Mr. Perfectly Fine": [22, "Fearless"],
"We Were Happy": [23, "Fearless"],
"That’s Whe": [24, "Fearless"],
"Don’t You": [25, "Fearless"],
"Bye Bye Baby": [26, "Fearless"],
"Mine": [1, "Speak Now"],
"Sparks Fly": [2, "Speak Now"],
"Back to December": [3, "Speak Now"],
"Speak Now": [4, "Speak Now"],
"Dear John": [5, "Speak Now"],
"Mean": [6, "Speak Now"],
"The Story of Us": [7, "Speak Now"],
"Never Grow Up": [8, "Speak Now"],
"Enchanted": [9, "Speak Now"],
"Better than Revenge": [10, "Speak Now"],
"Innocent": [12, "Speak Now"],
"Haunted": [13, "Speak Now"],
"Last Kiss": [14, "Speak Now"],
"Long Live": [15, "Speak Now"],
"Ours": [16, "Speak Now"],
"If This Was a Movie": [17, "Speak Now"],
"Superman": [18, "Speak Now"],
"State of Grace": [1, "Red"],
"Red": [2, "Red"],
"Treacherous": [3, "Red"],
"I Knew You Were Trouble": [4, "Red"],
"All Too Well": [5, "Red"],
"22": [6, "Red"],
"I Almost Do": [7, "Red"],
"We Are Never Ever Getting Back Together": [8, "Red"],
"Stay Stay Stay": [9, "Red"],
"The Last Time": [10, "Red"],
"Holy Ground": [11, "Red"],
"Sad Beautiful Tragic": [12, "Red"],
"The Lucky One": [13, "Red"],
"Everything Has Changed": [14, "Red"],
"Starlight": [15, "Red"],
"Begin Again": [16, "Red"],
"The Moment I Knew": [17, "Red"],
"Come Back…Be Here": [18, "Red"],
"Girl at Home": [19, "Red"],
"Ronan": [20, "Red"],
"Better Man": [21, "Red"],
"Nothing New": [22, "Red"],
"Babe": [23, "Red"],
"Message in a Bottle": [24, "Red"],
"I Bet You Think About Me": [25, "Red"],
"Forever Winter": [26, "Red"],
"Run": [27, "Red"],
"The Very First Night": [28, "Red"],
"All Too Well (10 minute version)": [29, "Red"],
"Welcome to New York": [1, "1989"],
"Blank Space": [2, "1989"],
"Style": [3, "1989"],
"Out of the Woods": [4, "1989"],
"All You Had to Do Was Stay": [5, "1989"],
"Shake It Off": [6, "1989"],
"I Wish You Would": [7, "1989"],
"Bad Blood": [8, "1989"],
"Wildest Dreams": [9, "1989"],
"How You Get the Girl": [10, "1989"],
"This Love": [11, "1989"],
"I Know Places": [12, "1989"],
"Clean": [13, "1989"],
"Wonderland": [14, "1989"],
"You Are in Love": [15, "1989"],
"New Romantics": [16, "1989"],
"…Ready for It?": [1, "Reputation"],
"End Game": [2, "Reputation"],
"I Did Something Bad": [3, "Reputation"],
"Don’t Blame Me": [4, "Reputation"],
"Delicate": [5, "Reputation"],
"Look What You Made Me Do": [6, "Reputation"],
"So It Goes…": [7, "Reputation"],
"Gorgeous": [8, "Reputation"],
"Getaway Car": [9, "Reputation"],
"King of My Heart": [10, "Reputation"],
"Dancing with Our Hands Tied": [11, "Reputation"],
"Dress": [12, "Reputation"],
"This Is Why We Can’t Have Nice Things": [13, "Reputation"],
"Call It What You Want": [14, "Reputation"],
"New Year’s Day": [15, "Reputation"],
"I Forgot That You Existed": [1, "Lover"],
"Cruel Summer": [2, "Lover"],
"Lover": [3, "Lover"],
"The Man": [4, "Lover"],
"The Archer": [5, "Lover"],
"I Think He Knows": [6, "Lover"],
"Miss Americana & The Heartbreak Prince": [7, "Lover"],
"Paper Rings": [8, "Lover"],
"Cornelia Street": [9, "Lover"],
"Death By A Thousand Cuts": [10, "Lover"],
"London Boy": [11, "Lover"],
"Soon You’ll Get Better": [12, "Lover"],
"False God": [13, "Lover"],
"You Need to Calm Down": [14, "Lover"],
"Afterglow": [15, "Lover"],
"ME!": [16, "Lover"],
"It’s Nice to Have a Friend": [17, "Lover"],
"Daylight": [18, "Lover"],
"The 1": [1, "Folklore"],
"Cardigan": [2, "Folklore"],
"The Last Great American Dynasty": [3, "Folklore"],
"Exile Ft. Bon Iver": [4, "Folklore"],
"My Tears Ricochet": [5, "Folklore"],
"Mirrorball": [6, "Folklore"],
"Seven": [7, "Folklore"],
"August": [8, "Folklore"],
"This is Me Trying": [9, "Folklore"],
"Illicit Affairs": [10, "Folklore"],
"Invisible String": [11, "Folklore"],
"Mad Woman": [12, "Folklore"],
"Epiphany": [13, "Folklore"],
"Betty": [14, "Folklore"],
"Peace": [15, "Folklore"],
"Hoax": [16, "Folklore"],
"The Lakes": [17, "Folklore"],
"willow": [1, "Evermore"],
"champagne problems": [2, "Evermore"],
"gold rush": [3, "Evermore"],
"’tis the damn season": [4, "Evermore"],
"tolerate it": [5, "Evermore"],
"no body, no crime": [6, "Evermore"],
"happiness": [7, "Evermore"],
"​dorothea": [8, "Evermore"],
"coney island": [9, "Evermore"],
"​ivy": [10, "Evermore"],
"cowboy like me": [11, "Evermore"],
"​l​ong story short": [12, "Evermore"],
"marjorie": [13, "Evermore"],
"closure": [14, "Evermore"],
"evermore": [15, "Evermore"],
"right where you left me": [16, "Evermore"],
"it’s time to go": [17, "Evermore"]

}

collabs = {
    "Breathe": ["Breathe", "Breathe Featuring Colbie Caillat"],
    "You All Over Me": ["You All Over Me", "You All Over Me Featuring Maren Morris"],
    "That's When": ["That's When", "That's When Featuring Keith Urban"],
    "The Last Time": ["The Last Time", "The Last Time Featuring Gary Lightbody"],
    "Everything Has Changed": ["Everything Has Changed", "Everything Has Changed Featuring Ed Sheeran"],
    "Nothing New": ["Nothing New", "Phoebe Bridgers"],
    "I Bet You Think About Me": ["I Bet You Think About Me", "I Bet You Think About Me Featuring Chris Stapleton"],
    "Run": ["Run", "Run Featuring Ed Sheeran"],
    "End Game": ["End Game", "End Game Featuring Ed Sheeran"],
    "Soon You'll Get Better": ["Soon You'll Get Better", "Soon You'll Get Better Featuring The Chicks"],
    "ME!": ["ME!", "ME! Featuring Brendon Urie"],
    "exile": ["exile", "exile Featuring Bon Iver"],
    "no body, no crime": ["no body, no crime", "no body, no crime Featuring HAIM"],
    "coney island": ["coney island", "coney island Featuring The National"],
    "evermore": ["evermore", "evermore Featuring Bon Iver"],
    "Lover": ["Lover", "Lover Featuring Shawn Mendes"]
}

class TaylorSwift(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.current_quote = ""
        self.availible = True
        self.current_user = ""
        self.total_correct = 0
        self.counter_eligible = True
        self.cooldowns = {}
        self.current_mode = "quote"
        self.atwcooldown = time() - 780
        with open("data/ts.json", "r") as f:
            self.total_correct = json.load(f)["correct"]

    @commands.command(aliases=["tq"])
    @botcommands_command()
    async def taylorquote(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                if response["song"] != "Gateway Car":
                    self.current_quote = response
                else:
                    response["song"] = "Getaway Car"
                    self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.current_mode = "quote"
                embed = discord.Embed(title="What Taylor Swift song is this from?", description=response["quote"])
                await ctx.send(embed=embed)

    @commands.command(aliases=["tt"])
    @botcommands_command()
    async def taylortrack(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        album = 17
        keys = [key for key in tracks.keys()]
        for i in range(2):
            song = keys[randint(0, len(tracks)-1)]
            track = tracks[song][0]
            album = tracks[song][1]
            if album in ["1989", "Folklore", "Evermore", "Reputation", "Lover"]:
                break
            

        self.current_quote = {"quote": "", "song": song, "album": album, "track": track}
        self.current_user = ctx.author.name
        self.availible = False
        self.current_mode = "track"
        embed = discord.Embed(title="What track number is this Taylor Swift song?", description=song)
        await ctx.send(embed=embed)


    @commands.command(aliases=["tal"])
    @botcommands_command()
    async def tayloralbum(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                if response["song"] != "Gateway Car":
                    self.current_quote = response
                else:
                    response["song"] = "Getaway Car"
                    self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.current_mode = "album"
                embed = discord.Embed(title="What Taylor Swift album is this from?", description=response["quote"])
                await ctx.send(embed=embed)

    @commands.command(aliases=["ta"])
    @botcommands_command()
    async def tayloracronym(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                if response["song"] != "Gateway Car":
                    self.current_quote = response
                else:
                    response["song"] = "Getaway Car"
                    self.current_quote = response
                if self.current_quote["song"] == "All Too Well":
                    self.current_quote["song"] = "All Too Well Ten Minute Version Taylor's Version From The Vault"
                if self.current_quote["song"] in [i for i in collabs.keys()]:
                    self.current_quote ["song"] = choice(collabs[self.current_quote["song"]])
                self.current_user = ctx.author.name
                self.availible = False
                self.current_mode = "quote"
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
        if self.current_mode == "quote":
            if "".join(filter(lambda x: x.isalnum(), message.content.lower())) != "".join(filter(lambda x: x.isalnum(), self.current_quote["song"].lower())):
                await message.reply("Incorrect!")
                self.counter_eligible = False
                return
        elif self.current_mode == "album":
            if "".join(filter(lambda x: x.isalnum(), message.content.lower())) != "".join(filter(lambda x: x.isalnum(), self.current_quote["album"].lower())):
                await message.reply("Incorrect!")
                self.counter_eligible = False
                return
        elif self.current_mode == "track":
            if message.content.lower() != str(self.current_quote["track"]):
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
        if self.current_mode == "track":
            await ctx.send(f"**Correct Track:** {self.current_quote['track']}\n**Song:** {self.current_quote['song']}\n**Album:** {self.current_quote['album']}")
        else:
            await ctx.send(f"**Correct Answer:** {self.current_quote['song']}\n**Album:** {self.current_quote['album']}")

    @commands.command()
    @botcommands_command()
    async def tscorrect(self, ctx):
        with open("data/ts.json", "r") as f:
                self.total_correct = json.load(f)["correct"]
        await ctx.send(f"Taylor Swift quotes identified correctly: {self.total_correct}")
        
    @commands.command()
    @botcommands_command()
    async def atwtmvtvftv(self, ctx):
        if time() - self.atwcooldown < 780:
            await ctx.send("On cooldown!")
            return
        self.atwcooldown = time()
        await ctx.send("""
        I walked through the door with you, the air was cold
But somethin' 'bout it felt like home somehow
And I left my scarf there at your sister's house
And you've still got it in your drawer, even now

Oh, your sweet disposition and my wide-eyed gaze
We're singin' in the car, getting lost upstate
Autumn leaves fallin' down like pieces into place
And I can picture it after all these days

And I know it's long gone and
That magic's not here no more
And I might be okay, but I'm not fine at all
Oh, oh, oh

'Causе there we arе again on that little town street
You almost ran the red 'cause you were lookin' over at me
Wind in my hair, I was there
I remember it all too well

Photo album on the counter, your cheeks were turnin' red
You used to be a little kid with glasses in a twin-sized bed
And your mother's tellin' stories 'bout you on the tee-ball team
You taught me 'bout your past, thinkin' your future was me
And you were tossing me the car keys, "FUCK THE PATRIARCHY"
Keychain on the ground, we were always skippin' town
And I was thinkin' on the drive down, "Any time now
He's gonna say it's love," you never called it what it was
'Til we were DEAD and gone and buried
Check the pulse and come back swearin' it's the same
After three months in the grave
And then you wondered where it went to as I reached for you
But all I felt was shame and you held my lifeless frame

And I know it's long gone and
There was nothing else I could do
And I forget about you long enough
To forget why I needed to

'Cause there we are again in the middle of the night
We're dancin' 'round the kitchen in the REFRIGERATOR LIGHT
Down the stairs, I was there
I remember it all too well
And there we are again when nobody had to know
You kept me like a secret, but I kept you like an oath
Sacred prayer and we'd swear
To remember it all too well, yeah

Well, MAYBE WE GOT LOST IN TRANSLATION, maybe I asked for too much
But maybe this THING WAS A MASTERPIECE TIL YOU TORE IT ALL UP
""")
        await ctx.send("""
        Runnin' scared, I was there
I remember it ALL TOO WELL
And you call me up again just to BREAK ME LIKE A PROMISE
So CASUALLY CRUEL IN THE NAME OF BEIN’ HONEST
I'm a crumpled-up PIECE OF PAPER lyin' here
'Cause I remember it all, all, all

They say ALL’S WELL THAT ENDS WELL, but I’M IN A NEW HELL
Every time you DOUBLE CROSS MY MIND
You said if we had been closer in age, maybe it would've been fine
And that made me want to DIE
The idea you had of me, who was she?
A never-needy, ever-lovely jewel whose shine reflects on you
Not weepin' in a party bathroom
Some actress askin' me what happened, you
THAT’S WHAT HAPPENED, YOU
You who charmed my dad with self-effacing jokes
Sippin' coffee like you're on a late-night show
But then he watched me watch the front door all night, willin' you to come
And he said, "It's supposed to be fun turning twenty-one"

Time won't fly, it's like I'm paralyzed by it
I'd like to be my old self again, but I'm still tryin' to find it
After plaid shirt days and nights when you made me your own
Now you mail back my things and I walk home alone
But you keep my old scarf from that very first week
'Cause it reminds you of innocence and it smells like me
You can't get rid of it
'Cause you remember it ALL TOO WELL, yeah
        """)
        await ctx.send("""
        'Cause there we are again when I loved you so
Back before you lost the ONE REAL THING YOU’VE EVER KNOWN
It was rare, I was there
I remember it ALL TOO WELL
Wind in my hair, you were there
You remember it ALL
Down the stairs, you were there
You remember it ALL
It was rare, I was there
I remember it all too well

And I was never good at tellin' jokes, but the punch line goes
"I'll get older, but your lovers stay my age"
From when your Brooklyn broke my skin and bones
I'm a soldier who's returning half her weight
And did the twin flame bruise paint you blue?
Just between us, did the love affair maim you too?
'Cause in this city's barren cold
I still remember the first fall of snow
And how it glistened as it fell
I remember it all too well

Just between us, did the love affair maim you all too well?
Just between us, do you remember it all too well?
Just between us, I remember it (Just between us) all too well
Wind in my hair, I was there, I was there (I was there)
Down the stairs, I was there, I was there
Sacred prayer, I was there, I was there
It was rare, you remember it all too well
Wind in my hair, I was there, I was there (Oh)
Down the stairs, I was there, I was there (I was there)
Sacred prayer, I was there, I was there
It was rare, you remember it (All too well)
Wind in my hair, I was there, I was there
Down the stairs, I was there, I was there
Sacred prayer, I was there, I was there
It was rare, you remember it
Wind in my hair, I was there, I was there
Down the stairs, I was there, I was there
Sacred prayer, I was there, I was there
It was rare, you remember it
        """)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TaylorSwift(bot))
