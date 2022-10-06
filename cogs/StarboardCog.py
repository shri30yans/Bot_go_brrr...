from core.StarboardFunctions import StarboardFunctions
from logging import error
from utils.ErrorHandler import InvalidSubcommand
from discord.ext import commands
import config, discord
import core.checks as checks
import random, asyncio

colourlist = config.embed_colours

# All reaction listeners take place in Reactions.py


class Starboard(commands.Cog, name="Starboard", description="Starboard functions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.group(
        name="Starboard",
        invoke_without_command=True,
        case_insensitive=True,
        aliases=["star", "sb"],
        help=f"Change starboard settings.",
    )
    async def starboard(self, ctx):
        raise InvalidSubcommand()

    @commands.has_permissions(manage_channels=True)
    @checks.CheckIfSetupNotCommandUsedBefore()
    @starboard.command(name="Setup", help=f"Setup a starboard for that server.")
    async def starboard_setup(self, ctx):
        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        starboard_channel = self.bot.get_channel(starboard_info["starboard_channel_id"])

        async def exit_command(message, user, reason):
            embed = discord.Embed(
                title="Setup command exited",
                description=f"{reason}",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
                colour=random.choice(colourlist),
            )
            embed.set_footer(
                icon_url=user.avatar_url,
                text=f"Requested by {user.name} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)

        async def timeout_error(message, user):
            embed = discord.Embed(
                title="Time limit exceeded",
                description=f"{user.name} took too much time to reply to this message. This action is cancelled.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                icon_url=user.avatar_url,
                text=f"Requested by {user.name} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)

        async def channel_setup():
            embed = discord.Embed(
                title=f"Starboard setup",
                description="This command will take you through the steps to configure your starboard.",
                colour=random.choice(colourlist),
            )
            embed.add_field(
                name="How would you like to set a Starboard channel",
                value="`➕`  Create a new starboard channel\n`✏️`  Modify an existing channel\n You can select `❌` to cancel.",
            )
            message = await ctx.reply(embed=embed)
            await message.add_reaction("➕")
            await message.add_reaction("✏️")
            await message.add_reaction("❌")

            def check(reaction, user):
                return (str(reaction.emoji) in ["➕", "✏️", "❌"]) and (
                    user == ctx.author
                )

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=60
                )

            except asyncio.TimeoutError:
                await timeout_error(message=message, user=ctx.author)

            else:
                if str(reaction) in ["➕"]:
                    await message.clear_reactions()
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(
                            send_messages=False
                        ),
                        ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                    }
                    channel = await ctx.guild.create_text_channel(
                        name="starboard", overwrites=overwrites
                    )
                    embed = discord.Embed(
                        title="New Starboard channel created",
                        description=f"A new starboard channel {channel.mention} has been created.",
                        color=random.choice(colourlist),
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url,
                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                    )
                    await message.edit(embed=embed)
                    return channel

                elif str(reaction) in ["✏️"]:
                    await message.clear_reactions()
                    embed = discord.Embed(
                        title="Enter the text channel",
                        description=f"Mention the channel or type it's ID.\nCancel setup command by typing `cancel`.",
                        color=random.choice(colourlist),
                        timestamp=ctx.message.created_at,
                    )
                    embed.set_footer(
                        icon_url=ctx.author.avatar_url,
                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                    )
                    await message.edit(embed=embed)

                    # Retries are the number of chances to input a text channel correctly
                    async def ask_channel_name(ctx, message, retries):
                        try:
                            channelmessage = await self.bot.wait_for(
                                "message",
                                check=lambda m: (m.author == ctx.author),
                                timeout=120,
                            )

                        except asyncio.TimeoutError:
                            await timeout_error(message=message, user=ctx.author)

                        else:
                            if channelmessage.content.lower() in ["cancel", "exit"]:
                                await exit_command(
                                    message=message,
                                    user=ctx.author,
                                    reason=f"{ctx.author.name} exited the command.",
                                )
                                return
                            try:
                                channel = await commands.TextChannelConverter().convert(
                                    ctx, channelmessage.content
                                )
                                return channel
                            except:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid channel entered",
                                        description=f"You entered a Invalid Text channel.\nMention the channel or type it's ID.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_channel_name(ctx, message, retries)
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                    return await ask_channel_name(ctx, message=message, retries=3)

                elif str(reaction) in ["❌"]:
                    await message.clear_reactions()
                    await exit_command(
                        message=message,
                        user=ctx.author,
                        reason=f"{ctx.author.name} exited the command.",
                    )
                    return

        async def star_limit_setup():
            embed = discord.Embed(
                title="Enter Star limit",
                description=f"Enter the number of stars required for a post to be sent to starboard.\nCancel setup command by typing `cancel`.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            message = await ctx.send(embed=embed)

            # Retries are the number of chances to input a text channel correctly
            async def ask_star_limit(ctx, retries):
                try:
                    starlimitmessage = await self.bot.wait_for(
                        "message", check=lambda m: (m.author == ctx.author), timeout=120
                    )

                except asyncio.TimeoutError:
                    await timeout_error(message=message, user=ctx.author)

                else:
                    if starlimitmessage.content.lower() in ["cancel", "exit"]:
                        await exit_command(
                            message=message,
                            user=ctx.author,
                            reason=f"{ctx.author.name} exited the command.",
                        )
                        return
                    try:
                        star_limit = int(starlimitmessage.content)
                        if star_limit <= 0:
                            raise Exception
                        return star_limit
                    except:
                        if retries > 0:
                            embed = discord.Embed(
                                title="Invalid star limit entered",
                                description=f"You entered an invalid star limit\nThe star limit needs to be a positive integer.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                color=random.choice(colourlist),
                                timestamp=ctx.message.created_at,
                            )
                            embed.set_footer(
                                icon_url=ctx.author.avatar_url,
                                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                            )
                            await message.edit(embed=embed)
                            retries -= 1
                            return await ask_star_limit(ctx, retries)
                        else:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.mention} reached the maximum number of retries.",
                            )
                            return

            return await ask_star_limit(ctx, retries=3)

        if starboard_channel is None:
            channel = await channel_setup()
            if channel:
                pass
            else:
                return

            star_limit = await star_limit_setup()
            if star_limit:
                pass
            else:
                return

            # Reaches this point if channel and star_limit has been set
            embed = discord.Embed(
                title="Setup command executed.",
                description=f"Starboard Channel: {channel.mention}\nStars required: {star_limit}",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.set_thumbnail(url=str(ctx.guild.icon_url))
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await ctx.reply(embed=embed)
            guild_id = ctx.guild.id
            starboard_info = await StarboardFunctions.get_starboard_info(guild_id)
            starboard_info["starboard_channel_id"] = channel.id
            starboard_info["stars_required"] = star_limit
            await StarboardFunctions.update_starboard(starboard_info, guild_id)

    @commands.has_permissions(manage_channels=True)
    @checks.CheckIfStarboardExists()
    @starboard.command(
        name="Settings",
        aliases=["setting", "changesettings"],
        help=f"Change starboard settings",
    )
    async def settings(self, ctx):
        user = ctx.author
        guild_id = ctx.guild.id
        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        starboard_info = await StarboardFunctions.get_starboard_info(guild_id)

        async def timeout_error(message, user):
            await message.clear_reactions()
            embed = discord.Embed(
                title="Time limit exceeded",
                description=f"{user.name} took too much time to reply to this message. This action is cancelled.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.set_footer(
                icon_url=user.avatar_url,
                text=f"Requested by {user.name} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)

        async def exit_command(message, user, reason):
            await message.clear_reactions()
            embed = discord.Embed(
                title="Setup command exited",
                description=f"{reason}",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
                colour=random.choice(colourlist),
            )
            embed.set_footer(
                icon_url=user.avatar_url,
                text=f"Requested by {user.name} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)

        async def add_reactions_to_submenu(message, reactions):
            for reaction in reactions:
                await message.add_reaction(reaction)

        async def wait_for_reactions(message, valid_reactions_list):
            def check(reaction, user):
                return (str(reaction.emoji) in valid_reactions_list) and (
                    user == ctx.author
                )

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=120
                )

            except asyncio.TimeoutError:
                await timeout_error(message=message, user=ctx.author)

            else:
                return str(reaction.emoji)

        def boolean_check(value: str):
            value = value.lower()
            if value in ["true", "enable"]:

                return True
            elif value in ["false", "disable"]:

                return False
            else:
                return

        async def channel_settings(message):
            channel_id = starboard_info["starboard_channel_id"]
            starboard_channel = self.bot.get_channel(channel_id)

            await message.clear_reactions()
            embed = discord.Embed(
                title="Starboard Channel Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="Starboard Channel",
                value=f"Current channel: {starboard_channel.mention}\nIf you would like to edit this setting choose `✏️`\nSelect `❌` to return back to home.",
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)
            reactions_list = ["✏️", "❌"]
            await add_reactions_to_submenu(message, reactions_list)
            emoji = await wait_for_reactions(message, reactions_list)
            if emoji == "❌":
                await settings_menu(message)

            elif emoji == "✏️":
                await message.clear_reactions()
                embed = discord.Embed(
                    title="Enter the new starboard channel.",
                    description=f"Current starboard channel: {starboard_channel.mention} \nMention the channel or type it's ID.\nCancel setup command by typing `cancel`.",
                    color=random.choice(colourlist),
                    timestamp=ctx.message.created_at,
                )
                embed.add_field(
                    name="Important note:",
                    value="Proceeding with this action will **delete** all post information regarding old starboard posts. Any old starred posts will no longer get updated.",
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                    text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                )
                await message.edit(embed=embed)

                # Retries are the number of chances to input a text channel correctly
                async def ask_channel_name(ctx, message, retries):
                    try:
                        responsemessage = await self.bot.wait_for(
                            "message",
                            check=lambda m: (m.author == ctx.author),
                            timeout=120,
                        )

                    except asyncio.TimeoutError:
                        await timeout_error(message=message, user=ctx.author)

                    else:
                        if responsemessage.content.lower() in ["cancel", "exit"]:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.name} exited the command.",
                            )
                            return
                        else:
                            try:
                                channel = await commands.TextChannelConverter().convert(
                                    ctx, responsemessage.content
                                )
                                if channel == starboard_channel:
                                    if retries > 0:
                                        embed = discord.Embed(
                                            title="Invalid channel entered",
                                            description=f"{channel.mention} is already set as the starboard channel.\nMention another channel or type it's ID.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                            color=random.choice(colourlist),
                                            timestamp=ctx.message.created_at,
                                        )
                                        embed.set_footer(
                                            icon_url=ctx.author.avatar_url,
                                            text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                        )
                                        await message.edit(embed=embed)
                                        retries -= 1
                                        return await ask_channel_name(
                                            ctx, message, retries
                                        )
                                    else:
                                        await exit_command(
                                            message=message,
                                            user=ctx.author,
                                            reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                        )
                                        return
                                else:
                                    await responsemessage.add_reaction("✅")
                                    return channel
                            except:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid channel entered",
                                        description=f"You entered a Invalid Text channel.\nMention the channel or type it's ID.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_channel_name(ctx, message, retries)
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                channel = await ask_channel_name(ctx, message=message, retries=3)
                if channel is None:
                    return

                else:
                    channel_id = channel.id
                    starboard_info["starboard_channel_id"] = channel.id
                    await StarboardFunctions.update_starboard(starboard_info, guild_id)
                    await settings_menu(message)

        async def star_limit_settings(message):
            star_limit = starboard_info["stars_required"]
            await message.clear_reactions()
            embed = discord.Embed(
                title="Starboard Limit Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="Stars required",
                value=f"Current stars requirement: `{star_limit}`\nIf you would like to edit this setting choose `✏️`\nSelect `❌` to return back to home.",
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)
            reactions_list = ["✏️", "❌"]
            await add_reactions_to_submenu(message, reactions_list)
            emoji = await wait_for_reactions(message, reactions_list)
            if emoji == "❌":
                await settings_menu(message)

            elif emoji == "✏️":
                await message.clear_reactions()
                embed = discord.Embed(
                    title="Enter the new stars required ",
                    description=f"Current stars required: `{star_limit}` \nEnter the new stars required\nCancel setup command by typing `cancel`.",
                    color=random.choice(colourlist),
                    timestamp=ctx.message.created_at,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                    text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                )
                await message.edit(embed=embed)

                # Retries are the number of chances to input correctly
                async def ask_star_limit(ctx, message, retries):
                    try:
                        responsemessage = await self.bot.wait_for(
                            "message",
                            check=lambda m: (m.author == ctx.author),
                            timeout=120,
                        )

                    except asyncio.TimeoutError:
                        await timeout_error(message=message, user=ctx.author)

                    else:
                        if responsemessage.content.lower() in ["cancel", "exit"]:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.name} exited the command.",
                            )
                            return
                        else:
                            try:
                                new_star_limit = int(responsemessage.content)
                                if new_star_limit == star_limit:
                                    if retries > 0:
                                        embed = discord.Embed(
                                            title="Invalid limit entered",
                                            description=f"`{star_limit}` is already set as the limit.\nMention another limit.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                            color=random.choice(colourlist),
                                            timestamp=ctx.message.created_at,
                                        )
                                        embed.set_footer(
                                            icon_url=ctx.author.avatar_url,
                                            text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                        )
                                        await message.edit(embed=embed)
                                        retries -= 1
                                        return await ask_star_limit(
                                            ctx, message, retries
                                        )
                                    else:
                                        await exit_command(
                                            message=message,
                                            user=ctx.author,
                                            reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                        )
                                        return
                                elif new_star_limit < 1 or new_star_limit > 200:
                                    raise Exception
                                else:
                                    await responsemessage.add_reaction("✅")
                                    return new_star_limit
                            except:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid limit entered",
                                        description=f"The Star limit needs to be a positive integer between 1 to 200.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_star_limit(ctx, message, retries)
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                new_star_limit = await ask_star_limit(ctx, message=message, retries=3)

                if new_star_limit is None:
                    return

                else:
                    starboard_info["stars_required"] = new_star_limit
                    await StarboardFunctions.update_starboard(starboard_info, guild_id)
                    await settings_menu(message)

        async def self_star_settings(message):
            self_star = starboard_info["self_star"]
            await message.clear_reactions()
            embed = discord.Embed(
                title="Starboard self star Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="Self star",
                value=f"Current self star setting: `{self_star}`\nIf you would like to edit this setting choose `✏️`\nSelect `❌` to return back to home.",
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)
            reactions_list = ["✏️", "❌"]
            await add_reactions_to_submenu(message, reactions_list)
            emoji = await wait_for_reactions(message, reactions_list)
            if emoji == "❌":
                await settings_menu(message)

            elif emoji == "✏️":
                await message.clear_reactions()
                embed = discord.Embed(
                    title="Enter the self star settings",
                    description=f"Current self star setting: `{self_star}` \nType `{not(self_star)}` to change it.\nCancel setup command by typing `cancel`.",
                    color=random.choice(colourlist),
                    timestamp=ctx.message.created_at,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                    text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                )
                await message.edit(embed=embed)

                # Retries are the number of chances to input correctly
                async def ask_self_star(ctx, message, retries):
                    try:
                        responsemessage = await self.bot.wait_for(
                            "message",
                            check=lambda m: (m.author == ctx.author),
                            timeout=120,
                        )

                    except asyncio.TimeoutError:
                        await timeout_error(message=message, user=ctx.author)

                    else:
                        if responsemessage.content.lower() in ["cancel", "exit"]:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.name} exited the command.",
                            )
                            return
                        else:
                            check = boolean_check(responsemessage.content)
                            if check is self_star:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"Current self star limit is already {self_star}.\nType `{not(self_star)}` to change it.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_self_star(ctx, message, retries)

                            elif check is not (self_star):
                                await responsemessage.add_reaction("✅")
                                return not (self_star)

                            else:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"Self star can only be set to `True` or `False`\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_self_star(ctx, message, retries)
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                new_self_star = await ask_self_star(ctx, message=message, retries=3)

                if new_self_star is None:
                    return

                else:
                    starboard_info["self_star"] = new_self_star
                    await StarboardFunctions.update_starboard(starboard_info, guild_id)
                    await settings_menu(message)

        async def nsfw_channel_settings(message):
            nsfw = starboard_info["nsfw"]
            await message.clear_reactions()
            embed = discord.Embed(
                title="Starboard NSFW channel Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="NSFW channel",
                value=f"Current NSFW setting: `{nsfw}`\nIf you would like to edit this setting choose `✏️`\nSelect `❌` to return back to home.",
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)
            reactions_list = ["✏️", "❌"]
            await add_reactions_to_submenu(message, reactions_list)
            emoji = await wait_for_reactions(message, reactions_list)
            if emoji == "❌":
                await settings_menu(message)

            elif emoji == "✏️":
                await message.clear_reactions()
                embed = discord.Embed(
                    title="Enter the NSFW channel settings",
                    description=f"Current NSFW channel setting: `{nsfw}` \nType `{not(nsfw)}` to change it.\nCancel setup command by typing `cancel`.",
                    color=random.choice(colourlist),
                    timestamp=ctx.message.created_at,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                    text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                )
                await message.edit(embed=embed)

                # Retries are the number of chances to input correctly
                async def ask_nsfw_settings(ctx, message, retries):
                    try:
                        responsemessage = await self.bot.wait_for(
                            "message",
                            check=lambda m: (m.author == ctx.author),
                            timeout=120,
                        )

                    except asyncio.TimeoutError:
                        await timeout_error(message=message, user=ctx.author)

                    else:
                        if responsemessage.content.lower() in ["cancel", "exit"]:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.name} exited the command.",
                            )
                            return
                        else:
                            check = boolean_check(responsemessage.content)
                            if check is nsfw:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"Current NSFW channel setting is already {nsfw}.\nType `{not(nsfw)}` to change it.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_nsfw_settings(
                                        ctx, message, retries
                                    )
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                            elif check is not (nsfw):
                                await responsemessage.add_reaction("✅")
                                return not (nsfw)

                            else:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"NSFW channel settings can only be set to `True` or `False`\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_nsfw_settings(
                                        ctx, message, retries
                                    )
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                new_nsfw = await ask_nsfw_settings(ctx, message=message, retries=3)

                if new_nsfw is None:
                    return

                else:
                    starboard_info["nsfw"] = new_nsfw
                    await StarboardFunctions.update_starboard(starboard_info, guild_id)
                    await settings_menu(message)

        async def private_channel_settings(message):
            private = starboard_info["private_channel"]
            await message.clear_reactions()
            embed = discord.Embed(
                title="Starboard Private channel Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="Private channel",
                value=f"Current private channel setting: `{private}`\nIf you would like to edit this setting choose `✏️`\nSelect `❌` to return back to home.",
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )
            await message.edit(embed=embed)
            reactions_list = ["✏️", "❌"]
            await add_reactions_to_submenu(message, reactions_list)
            emoji = await wait_for_reactions(message, reactions_list)
            if emoji == "❌":
                await settings_menu(message)

            elif emoji == "✏️":
                await message.clear_reactions()
                embed = discord.Embed(
                    title="Enter the private channel settings",
                    description=f"Current Private channel setting: `{private}` \nType `{not(private)}` to change it.\nCancel setup command by typing `cancel`.",
                    color=random.choice(colourlist),
                    timestamp=ctx.message.created_at,
                )
                embed.set_footer(
                    icon_url=ctx.author.avatar_url,
                    text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                )
                await message.edit(embed=embed)

                # Retries are the number of chances to input correctly
                async def ask_private_settings(ctx, message, retries):
                    try:
                        responsemessage = await self.bot.wait_for(
                            "message",
                            check=lambda m: (m.author == ctx.author),
                            timeout=120,
                        )

                    except asyncio.TimeoutError:
                        await timeout_error(message=message, user=ctx.author)

                    else:
                        if responsemessage.content.lower() in ["cancel", "exit"]:
                            await exit_command(
                                message=message,
                                user=ctx.author,
                                reason=f"{ctx.author.name} exited the command.",
                            )
                            return
                        else:
                            check = boolean_check(responsemessage.content)
                            if check is private:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"Current Private channel setting is already {private}.\nType `{not(private)}` to change it.\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_private_settings(
                                        ctx, message, retries
                                    )
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return
                            elif check is not (private):
                                await responsemessage.add_reaction("✅")
                                return not (private)
                            else:
                                if retries > 0:
                                    embed = discord.Embed(
                                        title="Invalid value entered",
                                        description=f"Private channel settings can only be set to `True` or `False`\nCancel setup command by typing `cancel`.\nRetries left: `{retries}`",
                                        color=random.choice(colourlist),
                                        timestamp=ctx.message.created_at,
                                    )
                                    embed.set_footer(
                                        icon_url=ctx.author.avatar_url,
                                        text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
                                    )
                                    await message.edit(embed=embed)
                                    retries -= 1
                                    return await ask_private_settings(
                                        ctx, message, retries
                                    )
                                else:
                                    await exit_command(
                                        message=message,
                                        user=ctx.author,
                                        reason=f"{ctx.author.mention} reached the maximum number of retries.",
                                    )
                                    return

                new_private = await ask_private_settings(
                    ctx, message=message, retries=3
                )

                if new_private is None:
                    return

                else:
                    starboard_info["private_channel"] = new_private
                    await StarboardFunctions.update_starboard(starboard_info, guild_id)
                    await settings_menu(message)

        async def settings_menu(message=None):
            channel_id = starboard_info["starboard_channel_id"]
            starboard_channel = self.bot.get_channel(channel_id)
            star_limit = starboard_info["stars_required"]
            nsfw = starboard_info["nsfw"]
            private_channel = starboard_info["private_channel"]
            self_star = starboard_info["self_star"]

            embed = discord.Embed(
                title="Starboard Settings",
                description=f"Select an option.",
                color=random.choice(colourlist),
                timestamp=ctx.message.created_at,
            )
            embed.add_field(
                name="`1️⃣` Channel",
                value=f"Change channel settings\nCurrent channel: {starboard_channel.mention}",
                inline=False,
            )
            embed.add_field(
                name="`2️⃣` Stars required",
                value=f"Change stars required settings\nCurrent stars required: `{star_limit}`",
                inline=False,
            )
            embed.add_field(
                name="`3️⃣` Self star",
                value=f"Toggle users able to star their own posts\nCurrent setting: `{self_star}`",
                inline=False,
            )
            embed.add_field(
                name="`4️⃣` NSFW Channel settings",
                value=f"Change ability to post from NSFW channels.\nCurrent setting: `{nsfw}`",
                inline=False,
            )
            embed.add_field(
                name="`5️⃣` Private Channel settings",
                value=f"Change ability to post from private channels.\nCurrent setting: `{private_channel}`",
                inline=False,
            )
            embed.add_field(
                name="`❌` Exit",
                value=f"Slect the `❌` reaction to exit the menu.",
                inline=False,
            )
            embed.set_footer(
                icon_url=ctx.author.avatar_url,
                text=f"Requested by {ctx.message.author} • {self.bot.user.name}",
            )

            if message is None:
                message = await ctx.send(embed=embed)
            else:
                await message.clear_reactions()
                await message.edit(embed=embed)

            number_emojis = [
                "1\N{variation selector-16}\N{combining enclosing keycap}",
                "2\N{variation selector-16}\N{combining enclosing keycap}",
                "3\N{variation selector-16}\N{combining enclosing keycap}",
                "4\N{variation selector-16}\N{combining enclosing keycap}",
                "5\N{variation selector-16}\N{combining enclosing keycap}",
                "❌",
            ]

            for x in number_emojis:
                await message.add_reaction(x)

            def check(reaction, user):
                return (str(reaction.emoji) in number_emojis) and (user == ctx.author)

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", check=check, timeout=120
                )

            except asyncio.TimeoutError:
                await timeout_error(message=message, user=ctx.author)

            else:
                if str(reaction.emoji) == "1️⃣":
                    await channel_settings(message)
                elif str(reaction.emoji) == "2️⃣":
                    await star_limit_settings(message)
                elif str(reaction.emoji) == "3️⃣":
                    await self_star_settings(message)
                elif str(reaction.emoji) == "4️⃣":
                    await nsfw_channel_settings(message)
                elif str(reaction.emoji) == "5️⃣":
                    await private_channel_settings(message)
                elif str(reaction.emoji) == "❌":
                    await exit_command(
                        message=message,
                        user=ctx.author,
                        reason=f"{ctx.author.name} exited the command.",
                    )

        await settings_menu()

    @checks.CheckIfStarboardExists()
    @starboard.command(
        name="Random", help=f"Command to get a random message from the starboard."
    )
    async def star_random(self, ctx):
        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        starboard_posts_list = starboard_info["starboard_posts"]
        channel_id = starboard_info["starboard_channel_id"]
        starboard_channel = self.bot.get_channel(channel_id)

        # load the json content of the starboard column
        if len(starboard_posts_list) > 0:
            post = random.choice(starboard_posts_list)
            StarMessage = await starboard_channel.fetch_message(post["star_message_id"])
            await ctx.reply(content=StarMessage.content, embed=StarMessage.embeds[0])
        else:
            await ctx.reply(
                "The Starboard currently doesn't have enough posts for this command. Try again later."
            )

    # @starboard.command(name="Stats")
    # async def starboard_stats(self,ctx,user):
    #     user= user or ctx.author
    #     total_stars=0
    #     #ImportantFunctions = self.bot.get_cog('ImportantFunctions')
    #     UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
    #     # starboard_posts_list = (await ImportantFunctions.get_starboard_info(ctx.guild.id))["starboard_posts"]
    #     reactions_given, reactions_received =await UserDatabaseFunctions.get_user_reactions(user)
    #     embed=discord.Embed(title=f"Starboard",)
    #     embed.add_field(name="Total stars:",value=f"{total_stars}",inline=True)

    #     embed.add_field(name="Stars given:",value=f'{reactions_given["star"]}',inline=True)
    #     embed.add_field(name="Stars received:",value=f'{reactions_received["star"]}',inline=True)
    #     embed.set_footer(icon_url= ctx.author.avatar_url,text=f"Requested by {ctx.message.author} • {self.bot.user.name}")
    #     await ctx.reply(embed = embed)

    @commands.has_permissions(manage_channels=True)
    @checks.CheckIfStarboardExists()
    @starboard.command(
        name="Lock",
        aliases=["enable", "disable"],
        help=f"Command to toggle locking the Starboard. If Starboard channel is locked no other messages can be sent to it.",
    )
    async def starboard_change_lock(self, ctx, value: bool = None):
        user = ctx.author
        guild_id = ctx.guild.id

        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        starboard_info = await StarboardFunctions.get_starboard_info(ctx.guild.id)
        lock = starboard_info["lock"]
        if value is None:
            if lock:
                value = f"Starboard is currently locked. No messages can be sent to the starboard.\nUse `starboard Lock False` to change this."
            else:
                value = (
                    f"Starboard is unlocked.\nUse `starboard Lock True` to change this."
                )

            title = "Starboard Lock"
            name = f"Current Lock setting:{lock}"
            await self.send_embed_message_for_starboard_settings(
                ctx, user=user, title=title, name=name, value=value
            )

        elif lock is value:
            if lock:
                value = f"Starboard is currently locked. No messages can be sent to the starboard.\nUse `starboard Lock False` to change this."
            else:
                value = (
                    f"Starboard is unlocked.\nUse `starboard Lock True` to change this."
                )

            title = "Starboard Lock"
            name = f"Starboard Lock is already set to {lock}"
            await self.send_embed_message_for_starboard_settings(
                ctx, user=user, title=title, name=name, value=value
            )

        else:
            lock = value
            title = "Starboard Lock"
            name = f"Lock: {lock}"
            if lock == False:
                value = f"Starboard has been unlocked and is working again."

            elif lock == True:
                value = f"Starboard has been locked. No other messages can be sent to the starboard."

            await self.send_embed_message_for_starboard_settings(
                ctx, user=user, title=title, name=name, value=value
            )

            await StarboardFunctions.update_starboard_key(
                starboard_info=starboard_info,
                starboard_info_key="lock",
                value=lock,
                guild_id=guild_id,
            )

    async def send_embed_message_for_starboard_settings(
        self, ctx, user, title, name, value
    ):
        embed = discord.Embed(title=title, color=0xFFD700)
        embed.add_field(name=name, value=value)
        embed.set_thumbnail(url=str(ctx.guild.icon_url))
        embed.set_footer(
            icon_url=user.avatar_url,
            text=f"Requested by {user.name} • {self.bot.user.name} ",
        )
        await ctx.reply(embed=embed)

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def star_reaction_add(self, payload):
        await self.bot.wait_until_ready()
        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        emoji = payload.emoji
        user = self.bot.get_user(payload.user_id)
        guild_id = payload.guild_id
        sb_emoji = await StarboardFunctions.get_server_starboard_emoji(guild_id)

        if user.bot:
            # if a bot has sent the reaction
            return

        # =============================================
        # Starboard
        # =============================================
        elif str(emoji) in sb_emoji:

            # UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            channel = self.bot.get_channel(payload.channel_id)
            user = self.bot.get_user(payload.user_id)
            message = await channel.fetch_message(payload.message_id)
            await StarboardFunctions.post_to_starboard(
                message=message,
                channel=channel,
                user=user,
                emoji=emoji,
                reaction_name="star",
            )

    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def star_reaction_remove(self, payload):
        await self.bot.wait_until_ready()
        StarboardFunctions = self.bot.get_cog("StarboardFunctions")
        emoji = payload.emoji
        user = self.bot.get_user(payload.user_id)
        guild_id = payload.guild_id
        sb_emoji = await StarboardFunctions.get_server_starboard_emoji(guild_id)

        if user.bot:
            # if a bot has sent the reaction
            return

        # =============================================
        # Starboard
        # =============================================
        elif str(emoji) in sb_emoji:

            # UserDatabaseFunctions = self.bot.get_cog('UserDatabaseFunctions')
            channel = self.bot.get_channel(payload.channel_id)
            user = self.bot.get_user(payload.user_id)
            message = await channel.fetch_message(payload.message_id)
            await StarboardFunctions.post_to_starboard(
                message=message,
                channel=channel,
                user=user,
                emoji=emoji,
                reaction_name="star",
            )


def setup(bot):
    bot.add_cog(Starboard(bot))
