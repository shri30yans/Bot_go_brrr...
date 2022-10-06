import os, discord, platform, random, json, asyncio, re
from discord.ext import commands
import config
import core.checks as checks
from datetime import datetime

colourlist = config.embed_colours


class Moderation(
    commands.Cog, name="Moderation", description="Perform moderation commands."
):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.command(name="Delete", aliases=["del", "clear"], help=f"Deletes messages")
    async def delete(self, ctx, num: int):
        '''
        Purges messages
        '''

        if num >= 100:
            embed = discord.Embed(
                color=random.choice(colourlist), timestamp=ctx.message.created_at
            )
            embed.add_field(
                name="Too many messages deleted.",
                value=f"You can delete a maximum of 100 messages at one go to prevent excessive deleting. ",
            )
            author_avatar = ctx.author.avatar_url
            embed.set_footer(
                icon_url=author_avatar,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name} ",
            )
            await ctx.reply(embed=embed, delete_after=4)
            ctx.command.reset_cooldown(ctx)

        else:
            await ctx.channel.purge(limit=num + 1, bulk=True)
            embed = discord.Embed(
                color=random.choice(colourlist), timestamp=ctx.message.created_at
            )
            embed.add_field(name="Deleted", value=f"Deleted {num} message(s)")
            author_avatar = ctx.author.avatar_url
            embed.set_footer(
                icon_url=author_avatar,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name} ",
            )
            await ctx.send(embed=embed, delete_after=4)



def setup(bot):
    bot.add_cog(Moderation(bot))
