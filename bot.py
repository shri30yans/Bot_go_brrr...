import os, sys, discord, platform, random, asyncio,asyncpg
from utils.ErrorHandler import MaintenanceMode, NotApprovedServer
from discord.ext import commands,tasks
from utils.help import EmbedHelpCommand
import config #our config.py
import json
if not os.path.isfile("config.py"):
	sys.exit("'config.py' not found! Please add it and try again.")
else:
	import config
colourlist=config.embed_colours

async def get_prefix(bot, message):
    ImportantFunctions = bot.get_cog('ImportantFunctions')
    prefix = await ImportantFunctions.get_server_prefixes_string(message.guild.id)
    if prefix:
        return commands.when_mentioned_or(prefix)(bot,message) 
    else:
        return commands.when_mentioned_or(config.default_prefixes[0])(bot,message)




#bot
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=get_prefix,strip_after_prefix=True,case_insensitive = True,intents = intents,help_command=EmbedHelpCommand())
bot.Info_Table={}
bot.server_prefixes={}


TOKEN = config.TOKEN

@tasks.loop(minutes=15)
async def status_update():
    await bot.wait_until_ready()
    list_of_statuses=[
                        discord.Activity(type = discord.ActivityType.watching, name = f'Shri30yans Gaming'),
                        discord.Activity(type = discord.ActivityType.watching, name = f"How to get a PS5?"),
                        discord.Activity(type = discord.ActivityType.playing, name = f"Send help"),
                        discord.Activity(type = discord.ActivityType.watching, name = f"Bots go Brrrr..."),
                        discord.Activity(type = discord.ActivityType.playing, name = f"Cyberpunk on my toaster"),

                        ]

    activity=random.choice(list_of_statuses)
    #activity=list_of_statuses[3]

    await bot.change_presence(status = discord.Status.online, activity =activity)

status_update.start()


for extension in config.STARTUP_COGS:
		try:
			bot.load_extension(extension)
			extension = extension.replace("cogs.", "")
			print(f"Loaded extension '{extension}'")
		except Exception as e:
			exception = f"{type(e).__name__}: {e}"
			extension = extension.replace("cogs.", "")
			print(f"Failed to load extension {extension}\n{exception}")


@bot.check
async def owner_only_mode(ctx):
    if config.maintenance_mode:
        owner_check=await bot.is_owner(ctx.author)
        if owner_check:
            return True
        else:
            raise MaintenanceMode()
            
    else:
        return True

 

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")


DATABASE_DICT = dict(eval(os.getenv("DISCORD_DATABASE_DETAILS")))
class DATABASE_FORMAT:
    def __init__(self):
        self.database=DATABASE_DICT["database"]
        self.user=DATABASE_DICT["user"]
        self.password=DATABASE_DICT["password"]
        self.host=DATABASE_DICT["host"]
        self.port=DATABASE_DICT["port"]

DATABASE_DETAILS= DATABASE_FORMAT()

async def connection_pool():
    bot.pool = await asyncpg.create_pool(database=DATABASE_DETAILS.database,user=DATABASE_DETAILS.user,password=DATABASE_DETAILS.password,host=DATABASE_DETAILS.host,port=DATABASE_DETAILS.port,max_inactive_connection_lifetime=5)
    #bot.pool = await asyncpg.create_pool(database=DATABASE_DETAILS.database,user=DATABASE_DETAILS.user,password=DATABASE_DETAILS.password,host=DATABASE_DETAILS.host,port=DATABASE_DETAILS.port)
    
bot.loop.run_until_complete(connection_pool())   

bot.run(TOKEN)
