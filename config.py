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
    "cogs.UtilityCog","cogs.EventsCog","cogs.EconomyCog","cogs.RandomCog","cogs.WheelCog","cogs.ImportantFunctions","cogs.StarboardCog","cogs.OwnerCog","cogs.ReactionCog","jishaku","utils.ErrorHandler",#"cogs.RedditDownloader"
    ]

#Channels
main_chat_id=748786284599705688
suggestions_channel_id=799552024156045332
meme_channel_id=748786284599705689
dank_meme_channel_id=875615960843812874
giveaways_channel_id=761123670030286848
events_channel_id=748786284599705688
starboard_channel_id=788600643925180426
bot_commands_channel_id=748907059965067324

#Reactions
upvote_reaction="<:Logo_Reddit_Upvote:748810439885979718>"
downvote_reaction="<:Logo_Reddit_downvote:748810439688716328>"
loading_reaction="<a:loading:876422173269585932>"

#Awards
reddit_award_ternion="<:reddit_award_ternion:809384449413742633>"
reddit_award_argentinum="<:reddit_award_argentinum:818740567734878248>" 
reddit_award_ternion_animated="<a:reddit_award_ternion:873771542155243540>" 
reddit_award_argentinum_animated="<a:reddit_award_argentinum:873771537986109472>"
reddit_award_platinum="<:reddit_award_platinum:809383626085105694>"
reddit_award_gold="<:reddit_award_gold:808916667127300097>"
reddit_award_silver="<:reddit_award_silver:808916666788347926>"
reddit_award_wholesome="<:reddit_award_wholsome:807938111027413002>"
reddit_award_rocket_like="<:reddit_award_rocket_like:820293533642653717>"
reddit_award_rocket_dislike="<:reddit_award_rocket_dislike:820297716177043476>"



#Badges
badge_stonks="<:stonks:873763656712716298>"
badge_legendary="<a:legendary_badge:873826074201554945>"
badge_mythic="<a:mythic_badge:873997984340275251>"
badge_ultimate="<a:ultimate_badge:873893517607469087>"
badge_double_credits="<:doublecredits:875385394458419281>"
badge_double_karma="<:doubleupvote:875385393401430027>"
badge_gold_stonks="<:goldstonks:875432737861955625>"



#Emojis
credits_emoji="<:credit:873523287760699412>"


#Utility roles
muted_role_id=748786284385796123
admin_role_id=748786284385796122
moderator_role_id=748786284385796121

#Wheel Roles
wheel_mod_role_id=861833144897372160
wheel_server_perms_role_id=861138978609430558# arole with the Manage Server Permissions
wheel_muted_role_id=861148090143997953
wheel_celebrity_role_id=862547216636182529



#to run the events
#run_event=True
run_event=True
maintenance_mode=False #locks all commands to owner only


embed_colours=[ 0xFFFF00,#yellow
                0xFF0000,#red
                0xFF0000,#green
                0x00FFFF,#blue
                0xFF00FF,#pink
            ]

