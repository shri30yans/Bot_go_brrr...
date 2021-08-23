from dotenv import load_dotenv
import os

#Fetch details from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
#Fetching database details is shifted to main.py
#DATABASE_DICT = dict(eval(os.getenv("DISCORD_DATABASE_DETAILS")))


default_prefixes=["lol"]

APPROVED_SERVERS=[748786284373475358,]
#BLACKLIST = []
#List of Cogs to run on startup;
help_animation_link="https://media.giphy.com/media/jGPb050sylyTulVFOi/giphy.gif"
STARTUP_COGS = [
    "cogs.UtilityCog","cogs.EventsCog","cogs.EconomyCog","cogs.RandomCog","cogs.ModerationCog","cogs.ReactionCog","cogs.SettingsCog","cogs.StarboardCog","cogs.OwnerCog","core.ImportantFunctions","core.StarboardFunctions","core.UserDatabaseFunctions","jishaku","utils.ErrorHandler"
    ]

#Channels
main_chat_id=748786284599705688
suggestions_channel_id=799552024156045332
meme_channel_id=748786284599705689
dank_meme_channel_id=875615960843812874
#giveaways_channel_id=761123670030286848
events_channel_id=748786284599705688
bot_commands_channel_id=748907059965067324

award_reaction_menu_emoji=["🏆"]

#Reactions
upvote_reaction="<:Logo_Reddit_Upvote:748810439885979718>"
downvote_reaction="<:Logo_Reddit_downvote:748810439688716328>"
loading_reaction="<a:loading:876422173269585932>"

#Awards
reddit_award_ternion="<a:ternion:873771542155243540>"
reddit_award_argentinum="<a:argentinum:873771537986109472>" 
reddit_award_platinum="<:platinum:878908590214242325>"
reddit_award_gold="<:gold:877550049201119322>"
reddit_award_silver="<:silver:877550048907513877>"
reddit_award_wholesome="<:wholesome:877550049037516840>"
reddit_award_rocket_like="<:rocket_like:877550049654087781>"
reddit_award_rocket_dislike="<:rocket_disklike:877550049679257681>"


#Badges
badge_stonks="<:stonks:873763656712716298>"
badge_legendary="<a:legendary_badge:873826074201554945>"
badge_mythic="<a:mythic_badge:873997984340275251>"
badge_ultimate="<a:ultimate_badge:873893517607469087>"
badge_double_credits="<:doublecredits:875385394458419281>"
badge_double_karma="<:doubleupvote:875385393401430027>"
badge_gold_stonks="<:goldstonks:875432737861955625>"


cog_emojis={"utility":"<:utility:878323140793630770>",
"economy":"<:economy:878340364010942524>",
"settings":"<:settings:878323779443507210>",
"owner":"<:owner:878380736766431263>",
"starboard":"<:starboard:878331707055570955>",
"random":"<:random:878348942016913418>",
"moderation":"<:moderation:878337158820270140>"}

meme_score_needed_to_pin=7


#Emojis
credits_emoji="<:credit:873523287760699412>"


#Utility roles
muted_role_id=748786284385796123
admin_role_id=748786284385796122
moderator_role_id=748786284385796121

guild_join_update_channel_id=878520341109039105
guild_leave_update_channel_id=878520393118408704



#to run the events
#run_event=True
run_event=True
maintenance_mode=False  #locks all commands to owner only


# embed_colours=[ 0xFFFF00,#yellow
#                 0xFF0000,#red
#                 0xFF0000,#green
#                 0x00FFFF,#blue
#                 0xFF00FF,#pink
#             ]

embed_colours=[ 0x00FFFF]#blue

            
