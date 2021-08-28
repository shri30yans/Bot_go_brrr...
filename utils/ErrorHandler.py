import discord,random,traceback,sys,asyncio
import datetime
from discord.ext import commands
import config 
colourlist=config.embed_colours
import utils as utils

class CommandErrorHandler(commands.Cog):
    #https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        
        def __init__(self, bot):
            self.bot = bot    
        
        # if hasattr(ctx.command, 'on_error'):
        #     return
        try:
            if ctx.command.has_error_handler():
                return
            elif ctx.cog.has_error_handler():
                return
        except:
            pass

        # async def owner_check(ctx):
        #     user = ctx.author
        #     owner_check = await self.bot.is_owner(user)
        #     if owner_check:    
        #         await ctx.reinvoke()
        #         return True
        #     else:
        #         return False
        
        async def CooldownFunction(ctx):
            def convert(seconds):
                td = datetime.timedelta(seconds=seconds)
                years,remainder = divmod(td.days,365)   
                months,days = divmod(remainder,30)
                hours, remainder = divmod(td.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)        
                d={"years":years,"months":months,"days":days,"hours":hours,"minutes":minutes,"seconds":seconds}
                #print(d)
                
                revised_d={}
                string=""
                for unit in list(d):
                    if d[unit] != 0:
                        revised_d[unit] = d[unit]
                
                #Units and conjuctions
                for unit in list(revised_d):
                    string += f"{revised_d[unit]} {unit}"
                    if len(revised_d) > 1:
                        if list(revised_d)[-2] == unit:
                            string += " and "
                        elif list(revised_d)[-1] == unit:
                            pass
                        else:
                            string += ", "
                if string == "":
                    string = "1 second"
                return string

            retry_after= convert(int(error.retry_after))
            embed=discord.Embed(title="⚠️ | Command on Cooldown",color = random.choice(colourlist))
            embed.add_field(name="Slow down there, Romeo :rose: :race_car:", value=f"Please wait before using {ctx.command} command again.\nYou can use this command in **{retry_after}** again.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)

        if isinstance(error, commands.errors.MissingRequiredArgument):
            embed=discord.Embed(title="⚠️ | Missing Argument",description="Oops...You missed an argument.",color = random.choice(colourlist))
            embed.add_field(name="You are missing a required argument.",value=f"**Command help:** \n{ctx.command.help}\nFormat: `{ctx.command.qualified_name} {ctx.command.signature}`", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.MemberNotFound):
            embed=discord.Embed(title="⚠️ | Invalid User",description="Mention a valid user", color = random.choice(colourlist))
            embed.add_field(name="An incorrect user was mentioned",value="Mention a user or a users user id.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error,commands.errors.CommandNotFound):pass

        elif isinstance(error,commands.errors.BadArgument):
            embed=discord.Embed(title="⚠️ | Invalid Argument",color = random.choice(colourlist))
            embed.add_field(name="You passed a incorrect or invalid argument.", value=f"Command help: {ctx.command.help}\nFormat: `{ctx.command.qualified_name} {ctx.command.signature}`", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error,TypeError):
            pass

        elif isinstance(error, commands.errors.BotMissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'I need the **{}** permission(s) to run this command.'.format(fmt)
            embed=discord.Embed(title="⚠️ | Bot doesn't have required permissions",color = random.choice(colourlist))
            embed.add_field(name="Please give me the required permissions and try again.", value=f"{missing_permissions}", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")

            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            missing_permissions = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            embed=discord.Embed(title="⚠️ | Missing Permissions",color = random.choice(colourlist))
            embed.add_field(name="You don't have the required permissions", value=f"{missing_permissions}", inline=False)
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error, commands.errors.MaxConcurrencyReached):
            embed=discord.Embed(title="⚠️ | Maximimum Concurrency",color = random.choice(colourlist))
            embed.add_field(name="The same command is currently ongoing in this channel.", value=f"Use a different Channel or wait until the current command is completed.", inline=False)
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error, commands.errors.NotOwner):
            user = self.bot.get_user(self.bot.owner_id)
            embed=discord.Embed(title="⚠️ | You are not the owner of this bot.",color = random.choice(colourlist))
            embed.add_field(name="You need to own this bot to use this command.", value=f"Please ask {user.name} to help you out.", inline=False)
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.CommandOnCooldown):
            await CooldownFunction(ctx)
        
        elif isinstance(error, utils.ErrorHandler.CustomCommandOnCooldown):
            await CooldownFunction(ctx)
            
        
        elif isinstance(error,commands.errors.CheckFailure):
            embed=discord.Embed(title="⚠️ | The checks failed", color = random.choice(colourlist))
            embed.add_field(name="This action has been temporarily paused.",value=f"Error: {error}", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error,utils.ErrorHandler.MaintenanceMode):
            embed=discord.Embed(title="⚠️ | Maintenance mode", color = random.choice(colourlist))
            embed.add_field(name="This action has been temporarily paused.",value=f"Please try again later.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error,utils.ErrorHandler.StarboardChannelNotSet):
            embed=discord.Embed(title="⚠️ | Starboard Error", color = random.choice(colourlist))
            embed.add_field(name="Starboard is not enabled in this server.",value=f"To enable the starboard set it up using the setup subcommand.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error,utils.ErrorHandler.StarboardSetupCommandAlreadyRun):
            embed=discord.Embed(title="⚠️ | Setup Command Error", color = random.choice(colourlist))
            embed.add_field(name="Starboard has already been set in this server.",value=f"The Setup command cannot be run multiple times.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
        
        elif isinstance(error,utils.ErrorHandler.NotApprovedServer):
            embed=discord.Embed(title="⚠️ | Not Approved Server", color = random.choice(colourlist))
            embed.add_field(name="This action has been disabled for this server.",value=f"Please try contacting the admins.", inline=False)
            embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name} ")
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error,utils.ErrorHandler.InvalidSubcommand):
            await ctx.send_help(ctx.command)
       
        else:
            #traceback=traceback.format_exception(type(error), error, error.__traceback__)
            embed=discord.Embed(title="⚠️ | Oops. Something unexpected happended",color = random.choice(colourlist))
            #embed.add_field(name='Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            #etype, value, tb = sys.exc_info()
            embed.add_field(name="Something went wrong. Try again later",value=f"```{error}```\n ```{traceback.format_exc()}```", inline=False)
            await ctx.reply(embed=embed)
            ctx.command.reset_cooldown(ctx)
            print(f'Ignoring exception in command {ctx.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            

class NotApprovedServer(commands.CommandError):
    pass

class MaintenanceMode(commands.CommandError):
    pass


class InvalidSubcommand(commands.CommandError):
    pass

class StarboardChannelNotSet(commands.CommandError):
    pass

class StarboardSetupCommandAlreadyRun(commands.CommandError):
    pass

class CustomCommandOnCooldown(commands.CommandError):
    def __init__(self,ctx,retry_after, user, *args, **kwargs):
        self.user = user
        self.ctx=ctx
        self.retry_after=retry_after
        super().__init__(*args, **kwargs)
    

    

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))