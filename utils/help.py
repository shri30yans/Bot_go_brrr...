import os, sys, discord, platform, random, aiohttp, json, time, asyncio
from discord.ext import commands,tasks
from discord.ext.commands.cooldowns import BucketType
import config

colourlist=config.embed_colours

class EmbedHelpCommand(commands.HelpCommand):
    """This is an example of a HelpCommand that utilizes embeds.
    It's pretty basic but it lacks some nuances that people might expect.
    1. It breaks if you have more than 25 cogs or more than 25 subcommands. (Most people don't reach this)
    2. It doesn't DM users. To do this, you have to override `get_destination`. It's simple.
    Other than those two things this is a basic skeleton to get you started. It should
    be simple to modify if you desire some other behaviour.
    
    To use this, pass it to the bot constructor e.g.:
       
    bot = commands.Bot(help_command=EmbedHelpCommand())
    """
    # Set the embed colour here

    def get_ending_note(self):
        return f'Usage format: <required> [optional]\nUse {self.clean_prefix}{self.invoked_with} [command] for more info on a command.'
    
    def get_bot_help_ending_note(self):
        return f'Use {self.clean_prefix}{self.invoked_with} [category] for more info on a category.'

    def get_command_signature(self, command):
        return f'{command.qualified_name} {command.signature}'

    # def get_format_info(self):
    #     return f'```diff\n- Usage format: <required> [optional]\n- Don\'t type these brackets to use the command.\n+ {self.clean_prefix}help [command] - get information on a command\n+ {self.clean_prefix}help [category] - get information on a category```'

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='**Bot Commands**',description="[Invite Link](https://ptb.discord.com/api/oauth2/authorize?client_id=800371434785865789&permissions=1543896182&scope=bot) | [Support Server](https://discord.gg/cDk6pZYQWC) | [Source](https://github.com/shri30yans/Bot_go_brrr...) ",colour=random.choice(colourlist))
        #embed.add_field(name=f"How to get help", value=f"{self.get_format_info()}",inline=True)
        for cog,commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                if cog is None:
                    pass 
                else:
                    name = f"{config.cog_emojis[cog.qualified_name.lower()]} {cog.qualified_name}\n" if cog.qualified_name.lower() in config.cog_emojis else f"{cog.qualified_name}\n"
                    value = f"`{self.clean_prefix}{self.invoked_with} {cog.qualified_name}`"
                    
                    if cog and cog.description:
                        value = f'{cog.description}\n{value}'
                    
                    embed.add_field(name=f"{name}", value=f"{value}\u200b",inline=True)
            
                    
        embed.set_image(url=config.help_animation_link)
        embed.set_footer(text=self.get_bot_help_ending_note())
        await self.get_destination().send(embed=embed)
        


        # for cog, commands in mapping.items():
        #     name = 'No Category' if cog is None else cog.qualified_name
        #     filtered = await self.filter_commands(commands, sort=True)
        #     if filtered:
        #         value = '\u2002'.join(c.name for c in commands)
        #         if cog and cog.description:
        #             value = f'{cog.description}\n{value}'
        #         if name.lower() in config.cog_emojis:
        #             embed.add_field(name=f"{config.cog_emojis[name.lower()]} {name} [{len(filtered)}]", value=value)
        #         else:
        #             embed.add_field(name=f"{name} [{len(filtered)}]", value=value)


    async def send_command_help(self,command):
        embed = discord.Embed(title=f"**{command} help**",description=command.help,colour=random.choice(colourlist))
        #embed.add_field(name=", value=f"{command.help}", inline=False)
        
        
        embed.add_field(name="Format", value=f"`{self.clean_prefix}{self.get_command_signature(command)}`", inline=False)
        aliases = command.aliases
        
        if aliases:
            embed.add_field(name="Aliases", value=', '.join([f'`{alias.capitalize()}`' for alias in aliases]), inline=False)
        
        embed.set_thumbnail(url=str(self.context.bot.user.avatar_url)) 
        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

   

    async def send_cog_help(self, cog):
        name = f"{config.cog_emojis[cog.qualified_name.lower()]} {cog.qualified_name}\n" if cog.qualified_name.lower() in config.cog_emojis else f"{cog.qualified_name}\n"
        embed = discord.Embed(title=f'**{name} Commands**', colour=random.choice(colourlist))
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=command, value=f"{command.short_doc or '...'}\n`{self.clean_prefix}{self.get_command_signature(command)}`", inline=True)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"**{group.qualified_name}**", colour=random.choice(colourlist))
        
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=command, value=f"{command.short_doc or '...'}\n`{self.clean_prefix}{self.get_command_signature(command)}`", inline=False)


        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)



  

