import os

import discord
import time
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import random

# declare discord bot intents
client_intents = discord.Intents(guilds=True, members=True, bans=False, emojis=True, integrations=False,
                                 webhooks=False,
                                 invites=False, voice_states=False, presences=False, messages=True,
                                 guild_messages=True,
                                 dm_messages=False, reactions=True, guild_reactions=True, dm_reactions=False,
                                 typing=False, guild_typing=False, dm_typing=False)

# intitialize discord client
client = commands.Bot(command_prefix=["Dear majestic Cyber Cow, ", "DMCC, "], case_insensitive=True, intents=client_intents)


# client.remove_command('help')


# generate a discord embed with an optional attached image
async def generate_embed(color, title, description, attachment=None, thumbnail=None, footer=None, timestamp=None):
    # given color string, create color hex
    if color == 'green':
        color = 0x00cc00
    elif color == 'red':
        color = 0xe60000
    elif color == 'yellow':
        color = 0xffff33
    elif color == 'pink':
        color = 0xcc0099
    elif color == 'blue':
        color = 0x2691d9
    elif color == 'orange':
        color = 0xff9900

    # given timestamp string, create datetime object
    if timestamp is not None:
        datetime_obj = datetime.fromtimestamp(timestamp)
    else:
        datetime_obj = datetime.now()

    # create discord embed
    embed = discord.Embed(
        color=color,
        title=title,
        description=description,
        timestamp=datetime_obj)
    if footer is not None:
        embed.set_footer(text=footer)
    else:
        embed.set_footer(text='Developed by LaZoR_Bear')
    if attachment is not None:
        try:
            embed.set_image(url=attachment)
        except Exception as error:
            print(f'error setting url as image in discord embed: {type(error)}: {error}')
    if thumbnail is not None:
        try:
            embed.set_thumbnail(url=thumbnail)
        except Exception as error:
            print(f'error setting url as thumbnail in discord embed: {type(error)}: {error}')
    return embed


# client event triggers when a command hits an error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        # build error embed
        embed_title = 'Command Cooldown'
        embed_description = f'You cannot use this command for another {time_string(error.retry_after)}.'
        embed = await generate_embed('red', embed_title, embed_description)
        await ctx.send(embed=embed)
        return
    if isinstance(error, commands.CommandNotFound):
        return
    raise error


# client event triggers when discord bot client is fully loaded and ready
@client.event
async def on_ready():
    # change discord bot client presence
    status_options = [
        "with his Cyber Cycle",
        "with his CAN-D",
        "with his Chrome Cannon"
    ]
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.playing, name=random.choice(status_options)))

    # send ready confirmation to command line
    print(f'Discord logged in as {client.user.name} - {client.user.id}')

    for channel in [997477600505106614, 999490394834358335]:
        ch = client.get_channel(channel)
        await ch.send("Clone is ready!")
    print("Initialization completed!")


# check_roles command
@client.command(name="check my roles", aliases=["cr", "roles", "check"])
@commands.cooldown(2, 60, commands.BucketType.member)
async def check_roles(ctx):
    await ctx.trigger_typing()
    role_list = ctx.message.author.roles
    if len(role_list) <= 1:
        await ctx.channel.send("You don't have any roles!")
        return
    msg = "Here are your roles:\n"
    for i, role in enumerate(role_list[1:]):
        msg += f"{i + 1}" + ": " + role.name + "\n"
    msg.strip()
    embed_title = 'Roles List'
    embed_description = msg
    embed = await generate_embed('green', embed_title, embed_description)
    await ctx.send(embed=embed)


# add_role command
@client.command(name="manage my roles", aliases=["mr", "manage"])
@commands.cooldown(5, 60, commands.BucketType.member)
async def add_role(ctx, *args):
    def check(r, u):
        print("CHECKING")
        print(r, u)
        return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in ["✅",
                                                                                                     "❌"]

    def check2(r, u):
        print("CHECKING")
        print(r, u)
        return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and str(r.emoji) in ["1️⃣",
                                                                                                     "2️⃣",
                                                                                                     "3️⃣",
                                                                                                     "4️⃣",
                                                                                                     "5️⃣",
                                                                                                     "❌"]

    og_message = await ctx.send("Do you want to manage your role?")
    await og_message.add_reaction("✅")
    await og_message.add_reaction("❌")
    try:
        print("WAITING")
        reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)
        print(reaction)
        if reaction.emoji == "❌":
            await ctx.send("You dared disturb the Cyber Cow for THIS!!!")
            await reaction.message.clear_reactions()
        if ctx.message.author in await reaction.users().flatten():
            role_list = ["Chrome Cannon ID:G08 (CANNON Enthusiast)",
                         "Cyber Clone ID:G09 (Gear and Mayhem Subscriber)",
                         "Clone Card ID:G10 (Gear and Mayhem Subscriber)",
                         "Cyber Cycle ID:G11 (Cyber Cycle Gang)",
                         "CAN-D ID:G13 (CAN-D Fiend)"
                         ]
            embed_title = "Role Manager"
            embed_description = "Which role do you want?\n"
            for i, role in enumerate(role_list):
                embed_description += f"    {i + 1}: {role}\n"
            embed_description.strip()
            embed = await generate_embed('green', embed_title, embed_description)
            message = await ctx.send(embed=embed)
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("❌")

            try:
                r, u = await client.wait_for("reaction_add", check=check2, timeout=30)
                if r.emoji == "❌":
                    await reaction.message.clear_reactions()
            except asyncio.TimeoutError:
                await ctx.send("I am going back to sleep now.")
                await reaction.message.clear_reactions()
                return

            @client.event
            async def on_reaction_add(reaction, user):
                await ctx.trigger_typing()
                if user.bot:
                    return
                if reaction.emoji == "❌":
                    await reaction.message.clear_reactions()
                if reaction.emoji == "1️⃣":
                    role = client.get_guild(874623755165503549).get_role(996858795831603250)
                    roles = user.roles
                    await asyncio.sleep(500)
                    if role.name in [x.name for x in roles]:
                        await ctx.send(f"{user.display_name} already posses this role.")
                    else:
                        await user.add_roles(role)
                        await ctx.send(f"I have blessed {user.display_name} with the {role.name}'s role.")
                        return
                if reaction.emoji in ["2️⃣", "3️⃣"]:
                    role = client.get_guild(874623755165503549).get_role(996855832811667496)
                    if role in user.roles:
                        await ctx.send(f"{user.display_name} already posses this role.")
                    else:
                        await user.add_roles(role)
                        await ctx.send(f"I have blessed {user.display_name} with the {role.name}'s role.")
                        return
                if reaction.emoji == "4️⃣":
                    role = client.get_guild(874623755165503549).get_role(996857390177734746)
                    if role in user.roles:
                        await ctx.send(f"{user.display_name} already posses this role.")
                    else:
                        await user.add_roles(role)
                        await ctx.send(f"I have blessed {user.display_name} with the {role.name}'s role.")
                        return
                if reaction.emoji == "5️⃣":
                    role = client.get_guild(874623755165503549).get_role(996857994417549423)
                    if role in user.roles:
                        await ctx.send(f"{user.display_name} already posses this role.")
                    else:
                        await user.add_roles(role)
                        await ctx.send(f"I have blessed {user.display_name} with the {role.name}'s role.")
                        return

            @client.event
            async def on_reaction_remove(reaction, user):
                if user.bot:
                    return
                if reaction.emoji == "1️⃣":
                    role = client.get_guild(874623755165503549).get_role(997550983011913838)
                    await user.remove_roles(role)
                    await ctx.send(f"I have deposed {user.display_name} from the {role.name}s.")
                    return
                if reaction.emoji in ["2️⃣", "3️⃣"]:
                    role = client.get_guild(874623755165503549).get_role(996855832811667496)
                    await user.remove_roles(role)
                    await ctx.send(f"I have deposed {user.display_name} from the {role.name}s.")
                    return
                if reaction.emoji == "4️⃣":
                    role = client.get_guild(874623755165503549).get_role(996857390177734746)
                    await user.remove_roles(role)
                    await ctx.send(f"I have deposed {user.display_name} from the {role.name}.")
                    return
                if reaction.emoji == "5️⃣":
                    role = client.get_guild(874623755165503549).get_role(996857994417549423)
                    await user.remove_roles(role)
                    await ctx.send(f"I have deposed {user.display_name} from the {role.name}s.")
                    return

    except asyncio.TimeoutError:
        await ctx.send("I am going back to sleep now.")

    # if args[0].lower() == "g08":
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).get_role(997550983011913838))
    # if args[0].lower() == "g09":
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).get_role(997550983011913838))
    # if args[0].lower() == "g10":
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).get_role(997551233399263252))
    # if args[0].lower() == "g11":
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).get_role(997550627322339328))
    # if args[0].lower() == "g13":
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).get_role(997550906646200330))
    # if args[0] in ["can-d", "cyber-cycle", "clone", "card"]:
    #     role_list = client.get_guild(997477373580693515).roles
    #     print(role_list)
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).roles.get_role(""))


# remove_role command
# @client.command(name="remove-role", aliases=["rr", "remove"])
# @commands.cooldown(5, 60, commands.BucketType.member)
# async def remove_role(ctx, *args):
#     if args[0].lower() == "g08":
#         await ctx.message.author.remove_roles(client.get_guild(874623755165503549).get_role(997550983011913838))
#     if args[0].lower() == "g09":
#         await ctx.message.author.remove_roles(client.get_guild(874623755165503549).get_role(997550983011913838))
#     if args[0].lower() == "g10":
#         await ctx.message.author.remove_roles(client.get_guild(874623755165503549).get_role(997551233399263252))
#     if args[0].lower() == "g11":
#         await ctx.message.author.remove_roles(client.get_guild(874623755165503549).get_role(997550627322339328))
#     if args[0].lower() == "g13":
#         await ctx.message.author.remove_roles(client.get_guild(874623755165503549).get_role(997550906646200330))
    # if args[0] in ["can-d", "cyber-cycle", "clone", "card"]:
    #     role_list = client.get_guild(997477373580693515).roles
    #     print(role_list)
    #     await ctx.message.author.add_roles(client.get_guild(997477373580693515).roles.get_role(""))


# ping command
@client.command(name='ping')
async def ping(ctx):
    await ctx.trigger_typing()
    # build response embed
    embed_title = 'Pong!'
    embed_description = ms_string(client.latency * 1000)
    embed = await generate_embed('yellow', embed_title, embed_description)
    await ctx.send(embed=embed)
    return


# function to translate milliseconds into seconds/milliseconds
def ms_string(milliseconds):
    if milliseconds < 500:
        return f'{round(milliseconds, 2)}ms'
    elif milliseconds >= 500:
        return f'{round(milliseconds / 1000, 3)}s'
    return 'invalid'


# function to translate seconds into hours/minutes/seconds
def time_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if d > 0:
        if h > 0:
            return f'{int(d)}d {int(h)}h'
        else:
            return f'{int(d)}d'
    elif h > 0:
        if m > 0:
            return f'{int(h)}h {int(m)}m'
        else:
            return f'{int(h)}h'
    elif m > 0:
        if s > 0:
            return f'{int(m)}m {int(s)}s'
        else:
            return f'{int(m)}m'
    elif s > 0:
        return f'{int(s)}s'
    else:
        return 'invalid'


# @client.event
# async def on_message(message):
#    print("ok... " + message.author.name)


def connect_bot():
    pass


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    print("Discord Bot Started")
    client.run(os.environ["BOT_TOKEN"])
