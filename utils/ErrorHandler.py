import discord,random,traceback
from discord.ext import commands
import config #our config.py
colourlist=config.embed_colours
class CommandErrorHandler(commands.Cog):
    #https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        def __init__(self, bot):
            self.bot = bot
        
        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="⚠️ | Missing Argument",description="Oops...You missed an argument.",color = random.choice(colourlist))
            embed.add_field(name="You are missing a required argument.",value=f"Use this format: {ctx.command.help}", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MemberNotFound):
            embed=discord.Embed(title="⚠️ | Invalid User",description="Mention a valid user", color = random.choice(colourlist))
            embed.add_field(name="An incorrect user was mentioned",value="Mention a user or a users user id", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error,commands.CommandNotFound):pass

        elif isinstance(error,commands.errors.BadArgument):
            embed=discord.Embed(title="⚠️ | Invalid Argument",color = random.choice(colourlist))
            embed.add_field(name="You passed a incorrect or invalid argument", value=f" Please make sure that you are using the correct format.\n Type \"{config.prefix}help command_name\" to learn how to use a command.", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error,TypeError):pass

        elif isinstance(error, commands.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            embed=discord.Embed(title="⚠️ | Bot doesn't have required permissions",color = random.choice(colourlist))
            embed.add_field(name="Please give me the required permissions and try again.", value=f"{missing_permissions}", inline=False)
            await ctx.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            embed=discord.Embed(title="⚠️ | Missing Permissions",color = random.choice(colourlist))
            embed.add_field(name="You don't have the required permissions", value=f"{missing_permissions}", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.MaxConcurrencyReached):
            embed=discord.Embed(title="⚠️ | Maximimum Concurrency",color = random.choice(colourlist))
            embed.add_field(name="The same command is currently ongoing in this channel.", value=f"Use a different Channel or wait until the current command is completed.", inline=False)
            await ctx.send(embed=embed)
        
        elif isinstance(error, commands.NotOwner):
            user = self.bot.get_user(self.bot.owner_id)
            embed=discord.Embed(title="⚠️ | You are not the owner of this bot.",color = random.choice(colourlist))
            embed.add_field(name="You need to own this bot to use this command.", value=f"Please ask {user.name} to help you out.", inline=False)
            await ctx.send(embed=embed)
        
        # elif isinstance(error, commands.UserInputError):
        #     await ctx.send("Invalid input.")
        #     await self.send_command_help(ctx)
        #     return

        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id in [571957935270395925]:
                await ctx.reinvoke()
            #elif ctx.guild.id in [748786284373475358,748754737695948860,774113408378863666]:
                #await ctx.reinvoke()
            else:
                embed=discord.Embed(title="⚠️ | Command on Cooldown",color = random.choice(colourlist))
                embed.add_field(name="Slow down there, Romeo :rose: :race_car:", value=" Please wait before using this command again. You can use this command in {:.2f} s'seconds again.".format(error.retry_after), inline=False)
                await ctx.send(embed=embed)
        else:
            #traceback=traceback.format_exception(type(error), error, error.__traceback__)
            embed=discord.Embed(title="⚠️ | Goddamn Karen!",description="I knew I could count on you for screwing this up...",color = random.choice(colourlist))
            #embed.add_field(name='Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #etype, value, tb = sys.exc_info()
            embed.add_field(name="Something went wrong. Try again later",value=f"{error} \n {traceback.format_exc()}", inline=False)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))