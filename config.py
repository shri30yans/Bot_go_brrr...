from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_DICT = dict(eval(os.getenv("DISCORD_DATABASE_DETAILS")))
prefix="?"
class DATABASE_FORMAT:
    def __init__(self):
        self.database=DATABASE_DICT["database"]
        self.user=DATABASE_DICT["user"]
        self.password=DATABASE_DICT["password"]
        self.host=DATABASE_DICT["host"]
        self.port=DATABASE_DICT["port"]

DATABASE_DETAILS= DATABASE_FORMAT()
#BLACKLIST = []
STARTUP_COGS = [
    "cogs.UtilityCog","jishaku","cogs.EventsClass","cogs.EconomyCog","cogs.FunCog",
    
]

muted_role_id=748786284385796123
suggestions_channel_id=799552024156045332
meme_channel_id=748786284599705689
giveaways_channel_id=761123670030286848


upvote_reaction="<:Logo_Reddit_Upvote:748810439885979718>"
downvote_reaction="<:Logo_Reddit_downvote:748810439688716328>"
reddit_award_trinity="<:reddit_award_trinity:809384449413742633>"
reddit_award_platinum="<:reddit_award_platinum:809383626085105694>"
reddit_award_gold="<:reddit_award_gold:808916667127300097>"
reddit_award_silver="<:reddit_award_silver:808916666788347926>"

