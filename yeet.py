# import discord
# import datetime
# import contextlib
# from discord.ext import commands


# bot = commands.Bot("hey pika ")

# class HelpEmbed(discord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.timestamp = datetime.datetime.utcnow()
#         text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
#         self.set_footer(text=text)
#         self.color = discord.Color.blurple()


# class MyHelp(commands.HelpCommand):
#     def __init__(self):
#         super().__init__( # create our class with some aliases and cooldown
#             command_attrs={
#                 "help": "The help command for the bot",
#                 "cooldown": commands.Cooldown(1, 3.0, commands.BucketType.user),
#                 "aliases": ['commands']
#             }
#         )
    
#     async def send(self, **kwargs):
#         """a short cut to sending to get_destination"""
#         await self.get_destination().send(**kwargs)

#     async def send_bot_help(self, mapping):
#         """triggers when a `<prefix>help` is called"""
#         ctx = self.context
#         embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
#         embed.set_thumbnail(url=ctx.me.avatar_url)
#         usable = 0 

#         for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
#             if filtered_commands := await self.filter_commands(commands): 
#                 # if no commands are usable in this category, we don't want to display it
#                 amount_commands = len(filtered_commands)
#                 usable += amount_commands
#                 if cog: # getting attributes dependent on if a cog exists or not
#                     name = cog.qualified_name
#                     description = cog.description or "No description"
#                 else:
#                     name = "No Category"
#                     description = "Commands with no category"

#                 embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

#         embed.description = f"{len(bot.commands)} commands | {usable} usable" 

#         await self.send(embed=embed)

#     async def send_command_help(self, command):
#         """triggers when a `<prefix>help <command>` is called"""
#         signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
#         embed = HelpEmbed(title=signature, description=command.help or "No help found...")

#         if cog := command.cog:
#             embed.add_field(name="Category", value=cog.qualified_name)

#         can_run = "No"
#         # command.can_run to test if the cog is usable
#         with contextlib.suppress(commands.CommandError):
#             if await command.can_run(self.context):
#                 can_run = "Yes"
            
#         embed.add_field(name="Usable", value=can_run)

#         if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
#             embed.add_field(
#                 name="Cooldown",
#                 value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
#             )

#         await self.send(embed=embed)

#     async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
#         embed = HelpEmbed(title=title, description=description or "No help found...")

#         if filtered_commands := await self.filter_commands(commands):
#             for command in filtered_commands:
#                 embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")
           
#         await self.send(embed=embed)

#     async def send_group_help(self, group):
#         """triggers when a `<prefix>help <group>` is called"""
#         title = self.get_command_signature(group)
#         await self.send_help_embed(title, group.help, group.commands)

#     async def send_cog_help(self, cog):
#         """triggers when a `<prefix>help <cog>` is called"""
#         title = cog.qualified_name or "No"
#         await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        

# bot.help_command = MyHelp()

  
import json
from types import MappingProxyType

import discord
from discord.ext import commands


# Here's a link to the original source https://gist.github.com/StudioMFTechnologies/ad41bfd32b2379ccffe90b0e34128b8b. This has been eddited


class Help(commands.Cog, name="Help"):
    """The help command!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx, *, command=None):
        """Gets all category and commands of mine."""
        prefix = self.bot.command_prefix  # If you are using a bot with customizable prefixes, change the prefix here.
        try:
            if command is None:
                """Command listing.  What more?"""
                halp = discord.Embed(color=discord.Color.dark_blue())
                halp.set_author(name="All commands", icon_url=self.bot.user.avatar_url)
                mp = MappingProxyType(self.bot.cogs)
                for x in self.bot.cogs:
                    if x.lower() == "help":
                        continue
                    cog_info = mp[x]
                    all_commands = []
                    for y in cog_info.walk_commands():
                        all_commands.append(f"`{y.name}`")
                    halp.add_field(name=x, value=", ".join(all_commands), inline=False)
                halp.set_footer(text=f"To find out more about a command please do: {prefix}help <command name>")
                await ctx.send(embed=halp)
            else:
                """Command listing within a category."""
                found = False
                for x in self.bot.walk_commands():
                    if x.name.lower() == command.lower():
                        params = []
                        paramsDict = list(x.clean_params.items())
                        for i in range(len(x.clean_params)):
                            if str(paramsDict[i][1])[-5:] == "=None":
                                params.append(f"[{str(paramsDict[i][0])}]")
                            else:
                                params.append(f"<{str(paramsDict[i][0])}>")
                        aliases = []
                        for alias in x.aliases:
                            aliases.append(f"`{alias}`")
                        halp = discord.Embed(color=discord.Color.dark_blue())
                        halp.set_author(name=f"{prefix}{x.name} info", icon_url=self.bot.user.avatar_url)
                        halp.add_field(name="Description:", value=x.help, inline=False)
                        halp.add_field(name="Usage:", value=f"`{prefix}{x.name} {' '.join(params)}`", inline=False)
                        if aliases:
                            halp.add_field(name="Aliases", value=', '.join(aliases), inline=False)
                        await ctx.send(embed=halp)
                        return
                if not found:
                    """Reminds you if that category doesn't exist."""
                    halp = discord.Embed(title='Error!', description=f'Command `{command}` was not found.',
                                         color=discord.Color.red())
                    await ctx.send(embed=halp)
                else:
                    # await ctx.message.add_reaction(emoji='✔️')
                    pass
        except ValueError:
            await ctx.send("Excuse me, I can't send embeds.")


def setup(bot):
    bot.add_cog(Help(bot))
