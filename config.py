from dotenv import load_dotenv
import os

#Fetch details from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#Fetching database details is shifted to main.py
#DATABASE_DICT = dict(eval(os.getenv("DISCORD_DATABASE_DETAILS")))


prefix="?"

APPROVED_SERVERS=[748786284373475358,]
#BLACKLIST = []
#List of Cogs to run on startup;
STARTUP_COGS = [
    "cogs.UtilityCog","cogs.EventsCog","cogs.EconomyCog","cogs.FunCog","cogs.ImportantFunctions","cogs.StarboardCog","cogs.OwnerCog","cogs.ReactionCog","jishaku","utils.ErrorHandler"#,"cogs.WebHookCog"#For notro emojis
    ]

#Channels and Roles
muted_role_id=748786284385796123
suggestions_channel_id=799552024156045332
meme_channel_id=748786284599705689
giveaways_channel_id=761123670030286848
events_channel_id=748786284599705688
starboard_channel_id=788600643925180426

#Reactions
upvote_reaction="<:Logo_Reddit_Upvote:748810439885979718>"
downvote_reaction="<:Logo_Reddit_downvote:748810439688716328>"
# upvote_reaction="<:dingding:830695446821339137>"
# downvote_reaction="<:dongdong:830697221959450656>"

reddit_award_ternion="<:reddit_award_ternion:809384449413742633>"
reddit_award_argentinum="<:reddit_award_argentinum:818740567734878248>" 
reddit_award_platinum="<:reddit_award_platinum:809383626085105694>"
reddit_award_gold="<:reddit_award_gold:808916667127300097>"
reddit_award_silver="<:reddit_award_silver:808916666788347926>"
reddit_award_wholesome="<:reddit_award_wholsome:807938111027413002>"
#reddit_award_helpful="<:reddit_award_helpful:808916667160592385>"
reddit_award_rocket_like="<:reddit_award_rocket_like:820293533642653717>"
reddit_award_rocket_dislike="<:reddit_award_rocket_dislike:820297716177043476>"

#stars_required_for_starboard=6
#score_needed_to_pin = 8# for meme channel

#to run the events
run_event=True


embed_colours=[0xFFFF00,#yellow
            0xFF0000,#red
            0xFF0000,#green
            0x00FFFF,#blue
            0xFF00FF,#pink
]

