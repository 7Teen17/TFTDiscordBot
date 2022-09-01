from discord.ext import commands
import discord
from main import botcommands_command
import aiohttp
import json
from time import time
from random import randint

tracks = {
"Tim McGraw": 1,
"Picture to Burn": 2,
"Teardrops on My Guitar": 3,
"A Place in This World": 4,
"Cold as You": 5,
"The Outside": 6,
"Tied Together with a Smile": 7,
"Stay Beautiful": 8,
"Should’ve Said No": 9,
"Mary’s Song (Oh My My My)": 10,
"Our Song": 11,
"I’m Only Me When I’m with You": 12,
"Invisible": 13,
"A Perfectly Good Heart": 14,
"Fearless": 1,
"Fifteen": 2,
"Love Story": 3,
"Hey Stephen": 4,
"White Horse": 5,
"You Belong with Me": 6,
"Breath": 7,
"Tell Me Why": 8,
"You’re Not Sorry": 9,
"The Way I Loved You": 10,
"Forever & Always": 11,
"The Best Day": 12,
"Change": 13,
"Jump Then Fall": 14,
"Untouchable": 15,
"Forever & Always (Piano Version)": 16,
"Come in with the Rain": 17,
"Superstar": 18,
"The Other Side of the Door": 19,
"Today Was a Fairytale": 20,
"You All Over M": 21,
"Mr. Perfectly Fine": 22,
"We Were Happy": 23,
"That’s Whe": 24,
"Don’t You": 25,
"Bye Bye Baby": 26,
"Mine": 1,
"Sparks Fly": 2,
"Back to December": 3,
"Speak Now": 4,
"Dear John": 5,
"Mean": 6,
"The Story of Us": 7,
"Never Grow Up": 8,
"Enchanted": 9,
"Better than Revenge": 10,
"Innocent": 12,
"Haunted": 13,
"Last Kiss": 14,
"Long Live": 15,
"Ours": 16,
"If This Was a Movie": 17,
"Superman": 18,
"State of Grace": 1,
"Red": 2,
"Treacherous": 3,
"I Knew You Were Trouble": 4,
"All Too Well": 5,
"22": 6,
"I Almost Do": 7,
"We Are Never Ever Getting Back Together": 8,
"Stay Stay Stay": 9,
"The Last Time": 10,
"Holy Ground": 11,
"Sad Beautiful Tragic": 12,
"The Lucky One": 13,
"Everything Has Changed": 14,
"Starlight": 15,
"Begin Again": 16,
"The Moment I Knew": 17,
"Come Back…Be Here": 18,
"Girl at Home": 19,
"Ronan": 20,
"Better Man": 21,
"Nothing New": 22,
"Babe": 23,
"Message in a Bottle": 24,
"I Bet You Think About Me": 25,
"Forever Winter": 26,
"Run": 27,
"The Very First Night": 28,
"All Too Well (10 minute version)": 29,
"Welcome to New York": 1,
"Blank Space": 2,
"Style": 3,
"Out of the Woods": 4,
"All You Had to Do Was Stay": 5,
"Shake It Off": 6,
"I Wish You Would": 7,
"Bad Blood": 8,
"Wildest Dreams": 9,
"How You Get the Girl": 10,
"This Love": 11,
"I Know Places": 12,
"Clean": 13,
"Wonderland": 14,
"You Are in Love": 15,
"New Romantics": 16,
"…Ready for It?": 1,
"End Game": 2,
"I Did Something Bad": 3,
"Don’t Blame Me": 4,
"Delicate": 5,
"Look What You Made Me Do": 6,
"So It Goes…": 7,
"Gorgeous": 8,
"Getaway Car": 9,
"King of My Heart": 10,
"Dancing with Our Hands Tied": 11,
"Dress": 12,
"This Is Why We Can’t Have Nice Things": 13,
"Call It What You Want": 14,
"New Year’s Day": 15,
"I Forgot That You Existed": 1,
"Cruel Summer": 2,
"Lover": 3,
"The Man": 4,
"The Archer": 5,
"I Think He Knows": 6,
"Miss Americana & The Heartbreak Prince": 7,
"Paper Rings": 8,
"Cornelia Street": 9,
"Death By A Thousand Cuts": 10,
"London Boy": 11,
"Soon You’ll Get Better": 12,
"False God": 13,
"You Need to Calm Down": 14,
"Afterglow": 15,
"ME!": 16,
"It’s Nice to Have a Friend": 17,
"Daylight": 18,
"The 1": 1,
"Cardigan": 2,
"The Last Great American Dynasty": 3,
"Exile Ft. Bon Iver": 4,
"My Tears Ricochet": 5,
"Mirrorball": 6,
"Seven": 7,
"August": 8,
"This is Me Trying": 9,
"Illicit Affairs": 10,
"Invisible String": 11,
"Mad Woman": 12,
"Epiphany": 13,
"Betty": 14,
"Peace": 15,
"Hoax": 16,
"The Lakes": 17,
"willow": 1,
"champagne problems": 2,
"gold rush": 3,
"’tis the damn season": 4,
"tolerate it": 5,
"no body, no crime": 6,
"happiness": 7,
"​dorothea": 8,
"coney island": 9,
"​ivy": 10,
"cowboy like me": 11,
"​l​ong story short": 12,
"marjorie": 13,
"closure": 14,
"evermore": 15,
"right where you left me": 16,
"it’s time to go": 17

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
        self.is_album = False
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
                self.current_quote = response
                self.current_user = ctx.author.name
                self.availible = False
                self.is_album = False
                embed = discord.Embed(title="What Taylor Swift song is this from?", description=response["quote"])
                await ctx.send(embed=embed)

    @commands.command(aliases=["tt"])
    @botcommands_command()
    async def taylortrack(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        response = tracks[randint(0, len(tracks)-1)]


    @commands.command(aliases=["tal"])
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

    @commands.command(aliases=["ta"])
    @botcommands_command()
    async def tayloracronym(self, ctx):
        if not self.availible:
            await ctx.send("Awaiting a response, please wait before generating a new one!")
            return
        async with aiohttp.ClientSession() as session:
            async with session.get("https://taylorswiftapi.herokuapp.com/get") as response:
                response = await response.json()
                self.current_quote = response
                if self.current_quote["song"] == "All Too Well":
                    self.current_quote["song"] = "All Too Well Ten Minute Version Taylor's Version From The Vault"
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
