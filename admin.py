# +++++++++++ Imports and definitions +++++++++++ #
import asyncio
import discord
import os
from discord import app_commands
import datetime
from datetime import date
import sqlite3
from discord.ui import Select, View
from libs import rnd
import tomllib
import time
from rembg import remove
from PIL import Image
from io import BytesIO
import re
import string
import ast
import pip
import subprocess
import sys
from packaging.version import parse
import pkg_resources
import requests





#Load our config
with open('config.toml', 'rb') as fileObj:
  config = tomllib.load(fileObj) #dictionary/json



#channels
log_channel = config["log_channel"]
mod_log_channel = config["mod_log_channel"]
user_reports_channel_id = config["user_reports_channel"]
welcome_channel_id = config["welcome_channel"]
verification_channel_id = config["verification_channel"]


#roles
verified_role = config["verified_role"]
staff_role_id = config["staff_role"]


#other
guild_id = config["guild_id"]
db_name = config["db_name"]
__authors__ = '@therealOri'
token = config["TOKEN"]
MY_GUILD = discord.Object(id=guild_id)
today = date.today()
bot_logo = 'https://cdn.discordapp.com/attachments/1008056064593379379/1155968367065321523/the_admin.png?size=4098' #BOT_LOGO/ICON_HERE
author_logo = None


#for showing up in embeds
emoji1='🎄' #christmas tree
emoji2='🎁' #wrapped gift


# Colors
hex_red=0xFF0000
hex_green=0x0AC700
hex_yellow=0xFFF000 # I also like -> 0xf4c50b
# +++++++++++ Imports and definitions +++++++++++ #









# +++++++++++ Normal Functions +++++++++++ #
def clear():
    os.system('clear||cls')


#for when I want to check and see if a variable has been defined and what its type is.
def check(a):
    return print(f"{a}\n{type(a)}")


def random_hex_color():
  hex_digits = '0123456789abcdef'
  hex_digits = rnd.shuffle(hex_digits)
  color_code = ''
  nums = rnd.randint(0, len(hex_digits)-1, 6)
  for _ in nums:
    color_code += hex_digits[_]
  value =  int(f'0x{color_code}', 16)
  return value


def rand_name(length=12):
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890123456789"
    shuffled_chars = rnd.shuffle(chars)
    name = ''.join(rnd.choice(shuffled_chars) for _ in range(length))
    return name


def capitalize_sentences(text):
    text = text[0].upper() + text[1:] # Capitalize very first letter

    def replace(match):
        return ". " + match.group(1).capitalize()

    text = re.sub(r'\. ([a-z])', replace, text)
    return text
# +++++++++++ Normal Functions +++++++++++ #






# +++++++++++ Client Setup +++++++++++ #
class Admin(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        #self.tree.clear_commands(guild=None)
        #self.tree.clear_commands(guild=MY_GUILD) # clears guild commands
        await self.tree.sync(guild=MY_GUILD)



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
admin = Admin(intents=intents)
# +++++++++++ Client Setup +++++++++++ #







# +++++++++++ Async Functions, buttons, modals, etc. +++++++++++ #
async def check_and_upgrade_package(package_names, package_update_timer):
    while True:
        print("Monthly package update check has started...")
        activate_this = '~/admnENV/bin/activate_this.py' #this path is just for show, you will (if you use virtualenv like I do, use your own file path to the activate_this.py file.) So that way it will install updates to there instead of to your system path.
        exec(open(activate_this).read(), dict(__file__=activate_this))

        if isinstance(package_names, list):
            for package_name in package_names:
                try:
                    pypi_url = f"https://pypi.org/pypi/{package_name}/json"
                    releases = requests.get(pypi_url).json()["releases"]
                except KeyError:
                    print(f"Package {package_name} not found on PyPI")
                    continue

                latest_version = max(parse(v) for v in releases)
                try:
                    installed_dist = pkg_resources.get_distribution(package_name)
                    installed_version = parse(installed_dist.version)
                except pkg_resources.DistributionNotFound:
                    print(f"{package_name} not installed")
                    continue

                if latest_version > installed_version:
                    print(f"Upgrading {package_name}: v{installed_version} --> v{latest_version}\nInstalling dependencies..")
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name, '--upgrade'])
                    print(f'{package_name} upgraded to latest version {latest_version}')
                else:
                    print(f'{package_name} is at the latest version {installed_version}')


        else:
            package_name = package_names
            try:
                pypi_url = f"https://pypi.org/pypi/{package_name}/json"
                releases = requests.get(pypi_url).json()["releases"]
            except KeyError:
                print(f"Package {package_name} not found on PyPI")

            latest_version = max(parse(v) for v in releases)
            try:
                installed_dist = pkg_resources.get_distribution(package_name)
                installed_version = parse(installed_dist.version)
            except pkg_resources.DistributionNotFound:
                print(f"{package_name} not installed")
                continue

            if latest_version > installed_version:
                print(f"Upgrading {package_name}: v{installed_version} --> v{latest_version}\nInstalling dependencies..")
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name, '--upgrade'])
                print(f'{package_name} upgraded to latest version {latest_version}!')
            else:
                print(f'{package_name} is at the latest version {installed_version}')

        await asyncio.sleep(package_update_timer) # 1 month 60*60*24*30 in seconds.





async def status():
    while True:
        status_messages = ['my internals', '/help for help', 'your navigation history', 'Global Global Global', 'base all your 64', 'your security camera footage', 'myself walking on the moon', 'your browser search history']
        smsg = rnd.choice(status_messages)
        activity = discord.Streaming(type=1, url='https://twitch.tv/Monstercat', name=smsg)
        await admin.change_presence(status=discord.Status.online, activity=activity)
        await asyncio.sleep(60) #Seconds



async def purge_rmbg_imgs_channel():
    while True:
        purge_timer = config["other"]["purge_timer"]
        guild = admin.get_guild(guild_id)
        channel = discord.utils.get(guild.channels, name="rmbg-imgs")
        if channel is not None:
            await channel.clone(reason="Content Purge. Has been 24hrs.")
            await channel.delete(reason="Content Purge. Has been 24hrs.")
        await asyncio.sleep(purge_timer)



async def messages_check(channel):
    check = []
    async for msg in channel.history(limit=1):
        check.append(msg)

    if not check:
        return False
    else:
        return True





why_does_this_code_run_when_not_called=True
if why_does_this_code_run_when_not_called == True:
    class Captcha(discord.ui.Modal, title='Captcha'):
        # Our modal classes MUST subclass `discord.ui.Modal`,
        # but the title can be whatever you want.
        # you can have whatever here, as long as you save the answer/math to the database to be checked later. I just decided to do a math question.


        #set defaults
        nums = rnd.randint(0, 999, 3)
        math = nums[0] * nums[1] + nums[2]
        default_label = f'What does {nums[0]} x {nums[1]} + {nums[2]} equal?'

        #redefine defaults when called
        def regenerate_captcha():
            new_nums = rnd.randint(0, 999, 3)
            label = f'What does {new_nums[0]} x {new_nums[1]} + {new_nums[2]} equal?'
            Captcha.name.label = label
            Captcha.math = new_nums[0] * new_nums[1] + new_nums[2]

        name = discord.ui.TextInput(
            label=default_label,
            placeholder='Answer here...',
            required=True
        )

        async def on_submit(self, interaction: discord.Interaction):
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute("SELECT math FROM queue WHERE userId = ?", (interaction.user.id,))
            math_int = cur.fetchone()[0]
            if int(self.name.value) == math_int:
                cur.execute("DELETE FROM queue WHERE userId=?", (interaction.user.id,))
                con.commit()

                rnd_hex = random_hex_color()
                role = interaction.guild.get_role(verified_role)
                await interaction.user.add_roles(role, reason="Passed Verification Captcha.")

                dm_embed = discord.Embed(title=f'Captcha Complete!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nValue: `{self.name.value}` was the correct answer.\nYour packets are free to access the server now!\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
                dm_embed.set_thumbnail(url=interaction.user.avatar)
                dm_embed.set_footer(text=__authors__, icon_url=author_logo)
                await interaction.user.send(embed=dm_embed)
                await interaction.response.send_message("Captcha Complete!", ephemeral=True, delete_after=3)

                log_embed = discord.Embed(title=f'{emoji1} User passed verification! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nUser: `@{interaction.user.name}`\nUser ID: `{interaction.user.id}`\nRole given: `{role}`\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
                log_embed.set_thumbnail(url=bot_logo)
                log_embed.set_footer(text=__authors__, icon_url=author_logo)
                channel = admin.get_channel(log_channel)
                await channel.send(embed=log_embed)
                Captcha.regenerate_captcha()
            else:
                cur.execute("DELETE FROM queue WHERE userId=?", (interaction.user.id,))
                con.commit()
                Captcha.regenerate_captcha()
                error_embed = discord.Embed(title='Error  |  Invalid answer to math captcha.\n\nPlease Try Again...\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
                error_embed.set_thumbnail(url=bot_logo)
                error_embed.set_footer(text=__authors__, icon_url=author_logo)
                await interaction.response.send_message(embed=error_embed, ephemeral=True, delete_after=10)


        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            con = sqlite3.connect(db_name)
            cur = con.cursor()
            cur.execute("DELETE FROM queue WHERE userId=?", (interaction.user.id,))
            con.commit()
            Captcha.regenerate_captcha()
            await interaction.response.send_message(f'Oops! Something went wrong...\n\nError;\n```{error}```\n', ephemeral=True)
else:
    pass




class Verification(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    #This is for how many buttons you want, what they say, etc. and what happens when the button is pressed.
    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green)
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute("SELECT userId FROM queue WHERE userId = ?", (interaction.user.id,))
        uuid = cur.fetchone()

        if uuid:
            role = interaction.guild.get_role(verified_role)
            if role in interaction.user.roles:
                await interaction.response.send_message("You already have the 'packets' role and don't need to verify.", ephemeral=True, delete_after=10)
            else:
                captcha = Captcha()
                await interaction.response.send_modal(captcha)
                self.value = True
        else:
            role = interaction.guild.get_role(verified_role)
            if role in interaction.user.roles:
                #just in case somehow someone with the role already tried to verify again.
                await interaction.response.send_message("You already have the 'packets' role and don't need to verify.", ephemeral=True, delete_after=10)
            else:
                captcha = Captcha()
                math_int = captcha.math
                cur.execute("INSERT INTO queue VALUES(?, ?)", (interaction.user.id, math_int))
                con.commit()

                await interaction.response.send_modal(captcha)
                self.value = True #idk what this is for...probably just to show somwthing that the button was pressed and finished.
                #self.stop() # This is for if you just want the button pressed once and for admin to stop listening.




class Tickets(discord.ui.View):
    def __init__(self, user, message, title):
        super().__init__()
        self.value = None
        self.user = user
        self.message = message
        self.title = title

    @discord.ui.button(label='Close Ticket', style=discord.ButtonStyle.red, emoji="🔒")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(staff_role_id) # --> @staff
        if not role in interaction.user.roles:
            await interaction.response.send_message("You don't have permission to close tickets.", ephemeral=True, delete_after=10)
        else:
            channel = interaction.channel
            new_category = discord.utils.get(interaction.guild.categories, name="Archived-Tickets")
            await channel.edit(category=new_category)
            overwrites = channel.overwrites
            overwrites[self.user].read_messages = False
            overwrites[self.user].send_messages = False
            overwrites[self.user].read_message_history=False
            await channel.edit(overwrites=overwrites)

            archive_embed = discord.Embed(title=f"__ARCHIVED__  |  {self.title}!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\n", colour=0xf4c50b, timestamp=datetime.datetime.now(datetime.timezone.utc))
            archive_embed.add_field(name='**Message**', value=f"```{self.message}```", inline=False)
            archive_embed.set_thumbnail(url=bot_logo) # envelope or mailbox?
            archive_embed.set_footer(text=__authors__, icon_url=author_logo)
            await interaction.response.edit_message(content="Channel has been archived.", embed=archive_embed, view=None)
            self.value = True








#drop-down menus
class Select(Select):
    def __init__(self, user, message_id, chan_Id, evidence):
        self.user = user
        self.message_id = message_id
        self.chan_Id = chan_Id
        self.evidence = evidence
        options=[
            discord.SelectOption(label="Rule 1", emoji="👌", description="<instert rule 1 here>"),
            discord.SelectOption(label="Rule 2", emoji="✨", description="<instert rule 2 here>"),
            discord.SelectOption(label="Rule 3", emoji="🎭", description="<instert rule 3 here>") # add more rules and stuff/options if you need.
            ]
        super().__init__(placeholder="Wich Rule did the user break?", max_values=1, min_values=1, options=options)

    #https://discord.com/channels/{guild_id}/{channel_id}/{message_id}
    # Use online forum next time?
    # If option chosen is Rule 1, do something, etc.
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Rule 1":
            rule="Rule 1"

        if self.values[0] == "Rule 2":
            rule="Rule 2"

        if self.values[0] == "Rule 3":
            rule="Rule 3"


        channel = admin.get_channel(int(self.chan_Id))
        guild = interaction.guild
        staff_role = interaction.guild.get_role(staff_role_id)

        r_log_embed = discord.Embed(title=f'User Report!  |  Rule: "__`{rule}`__"\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        r_log_embed.add_field(name='UserId', value=f"`{self.user.id}`", inline=True)
        r_log_embed.add_field(name='UserName', value=f"`@{self.user.name}`", inline=True)
        r_log_embed.add_field(name='Reported Message', value=f'https://discord.com/channels/{guild.id}/{channel.id}/{self.message_id}', inline=False)
        r_log_embed.add_field(name='Channel', value=f"<#{channel.id}>", inline=False)
        r_log_embed.add_field(name='Evidence', value=f"[Screenshot]({self.evidence})", inline=False)
        r_log_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1008056064593379379/1174091691851010088/alert.png") #warning/Alert sign
        r_log_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(user_reports_channel_id) #log channel for user-reports.
        await channel.send(staff_role.mention, embed=r_log_embed)
        await interaction.response.edit_message(content="Thank you!, User has been reported!", view=None, delete_after=10)

class SelectView(View):
    def __init__(self, user, message_id, chan_Id, evidence, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(Select(user, message_id, chan_Id, evidence))

# +++++++++++ Async Functions, buttons, modals, etc. +++++++++++ #












####################################################################################
#                                                                                  #
#                                   Events                                         #
#                                                                                  #
####################################################################################
@admin.event
async def on_ready():
    flag = False
    global author_logo
    me = await admin.fetch_user(254148960510279683) #das me
    author_logo = me.avatar
    admin.loop.create_task(status())



    pkg_updating = config["other"]["package_updating"]
    if pkg_updating == True:
        package_name = config["other"]["packages"]
        package_update_timer = config["other"]["package_update_timer"]
        if isinstance(package_update_timer, int):
            pass # do nothing
        else:
            try:
                package_update_timer = int(package_update_timer)
            except Exception as e:
                print(f"Package_timer value is something that can not be turned into an 'int'. Setting default to 1 month or '2_592_000' seconds.\n\nError: {e}")
                package_update_timer = 2_592_000
        admin.loop.create_task(check_and_upgrade_package(package_name, package_update_timer))


    rmbg_imgs_channel_purge = config["other"]["rmbg_imgs_channel_purge"]
    if rmbg_imgs_channel_purge == True:
        admin.loop.create_task(purge_rmbg_imgs_channel())

    clear()
    print(f'Logged in as {admin.user} (ID: {admin.user.id})')
    print('------')

    if flag == True:
        rnd_hex = random_hex_color()
        channel = admin.get_channel(verification_channel_id)
        verify_embed = discord.Embed(title='Start verification.\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
        verify_embed.set_thumbnail(url=bot_logo)
        verify_embed.set_footer(text=__authors__, icon_url=author_logo)


        messages = await messages_check(channel)
        if messages == True:
            await channel.purge(limit=1)
            view = Verification()
            await channel.send(embed=verify_embed, view=view)
        else:
            view = Verification()
            await channel.send(embed=verify_embed, view=view)
    else:
        pass



@admin.event
async def on_member_join(member):
    # Can be replaced with your own images/URLs
    images=['https://cdn.discordapp.com/attachments/1008056064593379379/1156405110000332850/welcome_message_image.png',
            'https://cdn.discordapp.com/attachments/1008056064593379379/1168936555486904370/welcome_message_image_2.png',
            'https://cdn.discordapp.com/attachments/1008056064593379379/1169103701407969330/welcome_message_image_3.png']

    image = rnd.choice(images)
    rnd_hex = random_hex_color()
    welcome_embed = discord.Embed(title=f'{emoji1} Incomming connection! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nWelcome @{member.name} to {member.guild.name}!', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    welcome_embed.set_thumbnail(url=member.avatar)
    welcome_embed.set_image(url=image)
    welcome_embed.set_footer(text=__authors__, icon_url=author_logo)
    channel = admin.get_channel(welcome_channel_id)
    await channel.send(embed=welcome_embed)




invite_event = config["user_events"]["invites_created"]
if invite_event == True:
    @admin.event
    async def on_invite_create(invite):
        guild_invites = await invite.guild.invites()
        for guild_invite in guild_invites:
            if guild_invite.code == invite.code:
                inviter = guild_invite.inviter

        invite_log_embed = discord.Embed(title=f'{emoji1} An invite has been made! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nInvite: `https://discord.gg/{invite.code}`\nCreated By: `{inviter}`\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_green, timestamp=datetime.datetime.now(datetime.timezone.utc))
        invite_log_embed.set_thumbnail(url=bot_logo)
        invite_log_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(log_channel)
        await channel.send(embed=invite_log_embed)





# +++++++++++ Message deleteion & edits. +++++++++++ #
edit_msg = config["message_events"]["edit_msg"]
if edit_msg == True:
    @admin.event
    async def on_message_edit(before, after):
        if before.content == after.content:
            return
        else:
            author = before.author
            msg_edit_embed = discord.Embed(title=f'{emoji1} Message Edit! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n`@{author}` edited their message.\n\nIn channel: {before.channel.mention}\nBefore: `{before.content}`\nAfter: `{after.content}`\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_yellow, timestamp=datetime.datetime.now(datetime.timezone.utc))
            msg_edit_embed.set_thumbnail(url=before.author.avatar.url)
            msg_edit_embed.set_footer(text=__authors__, icon_url=author_logo)
            channel = admin.get_channel(log_channel)
            await channel.send(embed=msg_edit_embed)


delete_msg = config["message_events"]["delete_msg"]
if delete_msg == True:
    @admin.event
    async def on_message_delete(message):
        ignore_users=[254148960510279683] #you/whoever you don't want the bot to log messages for.
        if message.author.id in ignore_users:
            return
        else:
            if message.content:
                content = message.content
            else:
                content = "Message is to old, is an image, or is an embed. Can't retrieve content."

            msg_delete_embed = discord.Embed(title=f'{emoji1} Message Deleted! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n`@{message.author}` deleted a message.\n\nIn channel: {message.channel.mention}\nContent deleted: `{content}`\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_red, timestamp=datetime.datetime.now(datetime.timezone.utc))
            msg_delete_embed.set_thumbnail(url=message.author.avatar.url)
            msg_delete_embed.set_footer(text=__authors__, icon_url=author_logo)
            channel = admin.get_channel(log_channel)
            await channel.send(embed=msg_delete_embed)
# +++++++++++ Message deleteion & edits. +++++++++++ #






# +++++++++++ Role creation, deleteion, edits. +++++++++++ #
role_make = config["role_events"]["role_make"]
if role_make == True:
    #role_create
    @admin.event
    async def on_guild_role_create(role):
        async for audit_log in role.guild.audit_logs(limit=5, action=discord.AuditLogAction.role_create):
            if audit_log.target.id == role.id:
                role_creator = audit_log.user
            break

        role_add_embed = discord.Embed(title=f'{emoji1} Role created! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nRole Id: {role.id}\nCreated By: @{role_creator}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_green, timestamp=datetime.datetime.now(datetime.timezone.utc))
        role_add_embed.add_field(name="\u200B\n", value="\u200B\n", inline=False)
        role_add_embed.set_thumbnail(url=role_creator.avatar.url)
        role_add_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=role_add_embed)



role_edit = config["role_events"]["role_edit"]
if role_edit == True:
    #role_update
    @admin.event
    async def on_guild_role_update(before, after):
        async for audit_log in before.guild.audit_logs(limit=5, action=discord.AuditLogAction.role_update):
            if audit_log.target.id == before.id:
                role_updater = audit_log.user
            break


        role_edit_embed = discord.Embed(title=f'{emoji1} Role updated!  |  `@{before.name}` {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nRole Id: {before.id}\nUpdated By: @{role_updater}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n\u200B\n', colour=hex_yellow, timestamp=datetime.datetime.now(datetime.timezone.utc))

        if before.name != after.name:
            role_edit_embed.add_field(name="Name Changed", value=f"`@{before.name}` -> `@{after.name}`\u200B\n\u200B\n", inline=False)

        if before.color != after.color:
            role_edit_embed.add_field(name="Color Changed", value=f"`{before.color}` -> `{after.color}`\u200B\n\u200B\n", inline=False)

        if before.permissions != after.permissions:
            before_perms = set()
            after_perms = set()

            for perm, value in before.permissions:
                if value:
                    before_perms.add(perm)
            for perm, value in after.permissions:
                if value:
                    after_perms.add(perm)

            added = after_perms - before_perms
            removed = before_perms - after_perms

            if len(added) == 0:
                added_msg = "No perms added."
            else:
                added_msg = added

            if len(removed) == 0:
                removed_msg = "No perms removed."
            else:
                removed_msg = removed

            role_edit_embed.add_field(name="Permissions Changed", value=f"Added: `{added_msg}`\n\nRemoved: `{removed_msg}`\u200B\n\u200B\n", inline=False)


        role_edit_embed.add_field(name="-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", value="\u200B\n", inline=False)
        role_edit_embed.set_thumbnail(url=role_updater.avatar.url)
        role_edit_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=role_edit_embed)

role_delete = config["role_events"]["role_delete"]
if role_delete == True:
    #role_delete
    @admin.event
    async def on_guild_role_delete(role):
        async for audit_log in role.guild.audit_logs(limit=5, action=discord.AuditLogAction.role_delete):
            if audit_log.target.id == role.id:
                role_deletor = audit_log.user
            break

        role_delete_embed = discord.Embed(title=f'{emoji1} Role deleted!  |  `{role.name}` {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nRole Id: {role.id}\nDeleted By: @{role_deletor}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_red, timestamp=datetime.datetime.now(datetime.timezone.utc))
        role_delete_embed.add_field(name="\u200B\n", value="\u200B\n", inline=False)
        role_delete_embed.set_thumbnail(url=role_deletor.avatar.url)
        role_delete_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=role_delete_embed)
# +++++++++++ Role creation, deleteion, edits. +++++++++++ #










# +++++++++++ Channel creation, deleteion, edits. +++++++++++ #

channel_make = config["channel_events"]["channel_make"]
if channel_make == True:
    @admin.event
    async def on_guild_channel_create(channel):
        async for audit_log in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_create):
            if audit_log.target.id == channel.id:
                channel_creator = audit_log.user
            break

        channel_make_embed = discord.Embed(title=f'{emoji1} Channel created!  |  {channel.mention} {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nChannel Id: {channel.id}\nCreated By: @{channel_creator}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_green, timestamp=datetime.datetime.now(datetime.timezone.utc))
        channel_make_embed.add_field(name="\u200B\n", value="\u200B\n", inline=False)
        channel_make_embed.set_thumbnail(url=channel_creator.avatar.url)
        channel_make_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=channel_make_embed)



channel_delete = config["channel_events"]["channel_delete"]
if channel_delete == True:
    @admin.event
    async def on_guild_channel_delete(channel):
        async for audit_log in channel.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_delete):
            if audit_log.target.id == channel.id:
                channel_deletor = audit_log.user
            break

        channel_make_embed = discord.Embed(title=f'{emoji1} Channel deleted!  |  {channel.name} {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nChannel Id: {channel.id}\nDeleted By: @{channel_deletor}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=hex_red, timestamp=datetime.datetime.now(datetime.timezone.utc))
        channel_make_embed.add_field(name="\u200B\n", value="\u200B\n", inline=False)
        channel_make_embed.set_thumbnail(url=channel_deletor.avatar.url)
        channel_make_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=channel_make_embed)





channel_edit = config["channel_events"]["channel_edit"]
if channel_edit == True:
    @admin.event
    async def on_guild_channel_update(before, after):
        async for audit_log in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.channel_update):
            if audit_log.target.id == after.id:
                channel_editor = audit_log.user
            break

        if before.overwrites != after.overwrites:
            async for audit_log in after.guild.audit_logs(limit=5, action=discord.AuditLogAction.overwrite_update):
                if audit_log.target.id == after.id:
                    channel_editor = audit_log.user
                break

        channel_edit_embed = discord.Embed(title=f'{emoji1} Channel updated!  |  `@{before.name}` {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nChannel Id: {before.id}\nUpdated By: @{channel_editor}\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\u200B\n\u200B\n', colour=hex_yellow, timestamp=datetime.datetime.now(datetime.timezone.utc))
        if before.name != after.name:
            channel_edit_embed.add_field(name="Name Changed", value=f"`@{before.name}` -> `@{after.name}`\u200B\n\u200B\n", inline=False)

        if before.topic != after.topic:
            channel_edit_embed.add_field(name="Topic Changed", value=f"`{before.topic}` -> `{after.topic}`\u200B\n\u200B\n", inline=False)

        if before.category != after.category:
            channel_edit_embed.add_field(name="Category Changed", value=f"`{before.category}` -> `{after.category}`\u200B\n\u200B\n", inline=False)

        #More can be checked for but for rn this seems good enough.
        # I would like to check for overwrites updated but I am having to much of a headache with it rn.


        if before.overwrites != after.overwrites:
            for overwrite in after.overwrites:
                if overwrite not in before.overwrites:

                    role = overwrite if isinstance(overwrite, discord.Role) else None
                    member = overwrite if isinstance(overwrite, discord.Member) else None

                    field_name = f"Overwrite Added: @{role.name}" if role else f"Overwrite Added: {member.mention}"
                    field_value = f"__With default permissions__\u200B\n"

                    channel_edit_embed.add_field(name=field_name, value=field_value)



            for overwrite in before.overwrites:
                if overwrite not in after.overwrites:

                    role = overwrite if isinstance(overwrite, discord.Role) else None
                    member = overwrite if isinstance(overwrite, discord.Member) else None

                    field_name = f"Overwrite Removed: @{role.name}" if role else f"Overwrite Removed: {member.mention}"
                    field_value = "__All permissions revoked__"

                    channel_edit_embed.add_field(name=field_name, value=field_value)



            # Modified overwrites here...idk how to do that yet...




        channel_edit_embed.add_field(name="\u200B\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", value="\u200B\n", inline=False)
        channel_edit_embed.set_thumbnail(url=channel_editor.avatar.url)
        channel_edit_embed.set_footer(text=__authors__, icon_url=author_logo)
        channel = admin.get_channel(mod_log_channel)
        await channel.send(embed=channel_edit_embed)



# +++++++++++ Channel creation, deleteion, edits. +++++++++++ #














####################################################################################
#                                                                                  #
#                             Regular Commands                                     #
#                                                                                  #
####################################################################################
@admin.tree.command(description='Shows you what commands you can use.')
async def help(interaction: discord.Interaction):
    rnd_hex = random_hex_color()
    embed = discord.Embed(title='Commands  |  Help\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url=bot_logo)
    embed.add_field(name='\u200B\n/judgement help', value="Shows you a help message for judgement commands.", inline=False)
    embed.add_field(name='\u200B\n/ticket <title> <message>', value="Creates a support ticket", inline=False)
    embed.add_field(name='\u200B\n/report <userId> <message_Id> <channel_Id> (screenshot link)', value="Reports a user to staff.", inline=False)
    embed.add_field(name='\u200B\n/orb', value="Ask a question, get an answer.", inline=True)
    embed.add_field(name='\u200B\n/flip', value="Flips a coin for 'Heads' or 'Tails'.", inline=True)
    embed.add_field(name='\u200B\n/rmbg <image>', value="Remove the background from images.", inline=True)
    embed.add_field(name='\u200B\n/glcvrt <message> (option)', value="Will convert your message to and from the galactic alphabet.", inline=False)
    embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=embed, ephemeral=True)



@admin.tree.command(description='Test to see if the bot is responsive.')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"⏱️ Pong! ⏱️\nConnection speed is {round(admin.latency * 1000)}ms", ephemeral=True)




@admin.tree.command(description='Ask a question to the orb and ponder..')
async def orb(interaction: discord.Interaction, question: str):
    rnd_hex = random_hex_color()
    responses = ['Yes',
                'No',
                'Maybe',
                'Lol',
                'SuS'
                'Not SuS'
                "You're funny",
                'I can see it in your future',
                "I don't think that'll ever happen",
                "That'll be a hell no",
                'Perhaps'
    ]
    shuffled_responses = rnd.shuffle(responses)
    answer = rnd.choice(shuffled_responses)
    embed = discord.Embed(title=f"Magic Orb  |  Response\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nQuestion: `{question}`\n\nResponse: `{answer}`\u200B\n\u200B\n-=-=-=-=-=-=-=-=-=-=-=-=-=-", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url=bot_logo)
    embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=embed)


@admin.tree.command(description='Flip a coin.')
async def flip(interaction: discord.Interaction):
    rnd_hex = random_hex_color()
    responses = ['Heads', 'Tails']
    coin = rnd.choice(responses)
    embed = discord.Embed(title=f"Coin Flip\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nResult: `{coin}`\u200B\n\u200B\n-=-=-=-=-=-=-=-=-=-=-=-=-=-", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1008056064593379379/1173709779810656306/coin.png")
    embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=embed)



# https://discord.com/channels/{guild_id}/{channel_id}/{message_id}
@admin.tree.command(description='Report a user.')
async def report(interaction: discord.Interaction, user_id: str, message_id: str, channel_id: str, evidence: str=None):
    flag = True
    try:
        user = await interaction.guild.fetch_member(user_id)
    except Exception as e:
        flag = False
        u_error_embed = discord.Embed(title=f"Oops..  |  Failed to run command...\n\n\nError: 'Invalid user_id or User isn't in the server'\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-", colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        u_error_embed.add_field(name='Extra', value=f"```{e}```", inline=False)
        u_error_embed.set_thumbnail(url=bot_logo)
        u_error_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=u_error_embed, ephemeral=True, delete_after=10)

    if flag == True:
        try:
            channel_test = admin.get_channel(int(channel_id))
            message_test = await channel_test.fetch_message(message_id)
        except Exception as e:
            flag = False
            c_error_embed = discord.Embed(title=f"Oops..  |  Failed to run command...\n\n\nError: 'Can't find channel message is in, message doesn't exist, or Invalid message_id.'\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-", colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
            c_error_embed.add_field(name='Extra', value=f"```{e}```", inline=False)
            c_error_embed.set_thumbnail(url=bot_logo)
            c_error_embed.set_footer(text=__authors__, icon_url=author_logo)
            await interaction.response.send_message(embed=c_error_embed, ephemeral=True, delete_after=10)


    if flag == True:
        if not evidence:
            # Update to something better?
            evidence="https://cdn.discordapp.com/attachments/1008056064593379379/1174078071607926854/no_evidence.png"

        view=SelectView(user, message_id, channel_id, evidence)
        await interaction.response.send_message("Please select a report option.", view=view, ephemeral=True)




@admin.tree.command(description='Make a ticket for questions/support/help.')
async def ticket(interaction: discord.Interaction, title: str, message: str):
    if len(title) > 35:
        len_error_embed = discord.Embed(title=f"Oops..  |  Failed to run command...\n\n\nError: 'Title' is to long. Max length is '35' characters.\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-", colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        len_error_embed.set_thumbnail(url=bot_logo)
        len_error_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=len_error_embed, ephemeral=True, delete_after=10)
    else:
        channel_name = rand_name()
        rnd_hex = random_hex_color()
        guild = interaction.guild
        user = interaction.user
        staff_role = guild.get_role(staff_role_id)
        category = discord.utils.get(guild.categories, name="Tickets")
        await interaction.response.send_message("Making Ticket...", ephemeral=True, delete_after=15)


        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True),
            staff_role: discord.PermissionOverwrite(read_messages=True, send_messages=True, read_message_history=True)
        }
        ticket_channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        interaction_channel = admin.get_channel(ticket_channel.id)


        view=Tickets(user, message, title)
        ticket_embed = discord.Embed(title=f"Support Ticket  |  {title}!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\n", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
        ticket_embed.add_field(name='**Message**', value=f"```{message}```", inline=False)
        ticket_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1008056064593379379/1179541575668355092/ticket.png")
        ticket_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction_channel.send(f"{staff_role.mention}\n{user.mention}", embed=ticket_embed, view=view)






@admin.tree.command(description='Remove the background of images.')
async def rmbg(interaction: discord.Interaction, image: discord.Attachment):
    if not image.content_type.startswith("image/"):
        await interaction.response.send_message("Please only provide images!", ephemeral=True, delete_after=10)
        return

    await interaction.response.defer(ephemeral=True)
    image_bytes = await image.read()
    input_image = Image.open(BytesIO(image_bytes))

    output_name = rand_name(length=6)
    output = remove(input_image)
    output.save(f'./rmbg_imgs/{output_name}.png', format="PNG")

    d_out_name = rand_name(length=6)
    d_file = discord.File(f"./rmbg_imgs/{output_name}.png", filename=f"{d_out_name}.png")

    guild = admin.get_guild(guild_id)
    channel = discord.utils.get(guild.channels, name="rmbg-imgs")
    msg = await channel.send(file=d_file)

    attachment = msg.attachments[0]
    cdn_link = attachment.url

    cdn_url_regex = r"https?://cdn\.discordapp\.com/attachments/([0-9]+)/([0-9]+)/([A-Za-z0-9_.]+)"
    match = re.search(cdn_url_regex, cdn_link)
    if match:
        cdn_link = match.group(0)

    os.remove(f'./rmbg_imgs/{output_name}.png')


    rnd_hex = random_hex_color()
    rmbg_embed = discord.Embed(title=f"Background Removed!\nExpires in: 24hr\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\n", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    rmbg_embed.set_image(url=cdn_link)
    rmbg_embed.set_thumbnail(url=bot_logo)
    rmbg_embed.add_field(name="Full Image", value=f"[Link]({cdn_link})")
    rmbg_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.followup.send(embed=rmbg_embed, ephemeral=True)







@admin.tree.command(description='Convert text to galactic text.')
#have some choices set as an argument for a command.
@app_commands.choices(choice=[
    app_commands.Choice(name="ASCII -> Galactic", value="True"),
    app_commands.Choice(name="ASCII <- Galactic", value="False")
])
async def glcvrt(interaction: discord.Interaction, message: str, choice: str):
    #galactic_alphapet = "ᔑ ʖ ᓵ ↸ ᒷ ⎓ ⊣ ⍑ ╎ ⋮ ꖌ ꖎ ᒲ リ 𝙹 !¡ ᑑ ∷ ᓭ ℸ ̣ ⚍ ⍊ ∴  ̇/ || ⨅"
    ascii_to_galactic_alphabet = {
        'a':'ᔑ', 'b':'ʖ', 'c':'ᓵ', 'd':'↸', 'e':'ᒷ', 'f':'⎓', 'g':'⊣', 'h':'⍑',
        'i':'╎', 'j':'⋮', 'k':'ꖌ', 'l':'ꖎ', 'm':'ᒲ', 'n':'リ', 'o':'𝙹', 'p':'!¡',
        'q':'ᑑ', 'r':'∷', 's':'ᓭ', 't':'ℸ ̣', 'u':'⚍', 'v':'⍊', 'w':'∴', 'x':'̇/',
        'y':'||', 'z':'⨅', '.':'._.', ',': '_._', ' ':'<.>', '!':'%',
        '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9'}

    literal = ast.literal_eval(choice)
    if literal == True:
        if re.search(r'[A-Za-z0-9@#$^&*()]', message):
            galactic_message = ""
            for char in message.lower():
                if char in ascii_to_galactic_alphabet:
                    galactic_message += ascii_to_galactic_alphabet[char]
                else:
                    galactic_message += char


            rnd_hex = random_hex_color()
            rmbg_embed = discord.Embed(title=f"Message Converted!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nMessage: **`{galactic_message}`**\u200B\n\u200B\n", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
            rmbg_embed.set_thumbnail(url=bot_logo)
            rmbg_embed.set_footer(text=__authors__, icon_url=author_logo)
            await interaction.response.send_message(embed=rmbg_embed, ephemeral=True)
            return
        else:
            gla_error_embed = discord.Embed(title=f'Error!  |  Unable to convert to galactic.\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nPlease Make sure to only provide ascii characters in the english language.\u200B\n\u200B\n', colour=hex_red, timestamp=datetime.datetime.now(datetime.timezone.utc))
            gla_error_embed.set_thumbnail(url=bot_logo)
            gla_error_embed.set_footer(text=__authors__, icon_url=author_logo)
            await interaction.response.send_message(embed=gla_error_embed, ephemeral=True, delete_after=10)
            return


    if literal == False:
            # I suppose this could be reversed or made smaller or better or something..but ehhh.
            galactic_alphabet_to_ascii = {
                'ᔑ':'a', 'ʖ':'b', 'ᓵ':'c', '↸':'d', 'ᒷ':'e', '⎓':'f', '⊣':'g', '⍑':'h',
                '╎':'i', '⋮':'j', 'ꖌ':'k', 'ꖎ':'l', 'ᒲ':'m', 'リ':'n', '𝙹':'o', '!¡':'p',
                'ᑑ':'q', '∷':'r', 'ᓭ':'s', 'ℸ ̣':'t', '⚍':'u', '⍊':'v', '∴':'w', ' ̇/':'x',
                '||':'y', '⨅':'z', '._.':'.', '_._': ',', '<.>':' ', '%':'!',
                '0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9'
            }

            symbol_map = {
                "<.>": " ",
                "_._":",",
                "._.":".",
                "||":"y",
                "!¡":"p",
                "ℸ ̣":"t",
                "̇/":"x",
            }
            reversed_message = ""
            i = 0
            while i < len(message):
                symbol = message[i:i+3]

                if symbol in symbol_map:
                    reversed_message += symbol_map[symbol]
                    i += 3
                else:
                    symbol = message[i:i+2]

                    if symbol in symbol_map:
                        reversed_message += symbol_map[symbol]
                        i += 2
                    else:
                        reversed_message += galactic_alphabet_to_ascii.get(message[i], message[i])
                        i += 1

            reversed_message = capitalize_sentences(reversed_message)
            if re.search(r'[A-Za-z0-9@#$^&*()]', message):
                glg_error_embed = discord.Embed(title=f'Error!  |  Unable to convert to ascii.\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nPlease Make sure to only provide galactic characters.\u200B\n\u200B\n', colour=hex_red, timestamp=datetime.datetime.now(datetime.timezone.utc))
                glg_error_embed.set_thumbnail(url=bot_logo)
                glg_error_embed.set_footer(text=__authors__, icon_url=author_logo)
                await interaction.response.send_message(embed=glg_error_embed, ephemeral=True, delete_after=10)
                return
            else:
                rnd_hex = random_hex_color()
                rmbg_embed = discord.Embed(title=f"Message Converted!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\nMessage: **`{reversed_message}`**\u200B\n\u200B\n", colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
                rmbg_embed.set_thumbnail(url=bot_logo)
                rmbg_embed.set_footer(text=__authors__, icon_url=author_logo)
                await interaction.response.send_message(embed=rmbg_embed, ephemeral=True)
                return








####################################################################################
#                                                                                  #
#                           Moderation Commands                                    #
#                                                                                  #
####################################################################################
moderation_group = app_commands.Group(name="judgement", description="Moderation Commands.")
@moderation_group.command(name="help", description="Shows you all of the available judgement commands.")
async def help(interaction: discord.Interaction):
    rnd_hex = random_hex_color()
    embed = discord.Embed(title='Judgement Commands  |  Help\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url=bot_logo)
    embed.add_field(name='/purge', value="Purges messages in channels.", inline=False)
    embed.add_field(name='/kick <user_id> <reason>', value="Kicks uers from the server.", inline=True)
    embed.add_field(name='/ban <user_id> <reason> (delete_messages)', value="Bans users from the server and optionally deletes their messages.", inline=True)
    embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=embed, ephemeral=True)





@app_commands.checks.has_permissions(manage_messages=True)
@moderation_group.command(name="purge", description="Purges messages in channels.")
async def purge(interaction: discord.Interaction, channel: str, amount: int):
    rnd_hex = random_hex_color()
    interaction_channel = admin.get_channel(interaction.channel_id)
    if channel == '.':
        purge_channel = interaction_channel
    else:
        channel = int(channel)
        purge_channel = admin.get_channel(channel)

    m_check = await messages_check(purge_channel)
    if m_check == False:
        error_embed = discord.Embed(title='Error  |  No messages can be found to be purged. Channel seems to be empty...\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        error_embed.set_thumbnail(url=bot_logo)
        error_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=error_embed, ephemeral=True, delete_after=10)
    else:
        purge_embed = discord.Embed(title='Messages have been purged!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
        purge_embed.set_thumbnail(url=bot_logo)
        purge_embed.set_footer(text=__authors__, icon_url=author_logo)
        if purge_channel == interaction_channel:
            await interaction.response.send_message("Purging messages...", ephemeral=True, delete_after=2.5)
            await purge_channel.purge(limit=amount) #+1 if issues happen
            await interaction_channel.send(embed=purge_embed, delete_after=10)
        else:
            await interaction.response.send_message(embed=purge_embed, ephemeral=True, delete_after=10)
            await purge_channel.purge(limit=amount)
@purge.error
async def purge_error(interaction: discord.Interaction, error: Exception):
    check_error_embed = discord.Embed(title=f'Oops..  |  Failed to run command...\n\n\nError;\n```{error}```\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
    check_error_embed.set_thumbnail(url=bot_logo)
    check_error_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=check_error_embed, ephemeral=True, delete_after=10)





@app_commands.checks.has_permissions(kick_members=True)
@moderation_group.command(name='kick', description='Kicks a user from the server.')
async def kick(interaction: discord.Interaction, user_id: str, reason: str):
    try:
        user_id = int(user_id)
    except:
        error_embed = discord.Embed(title='Error  |  A valid user ID must be given.\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        error_embed.set_thumbnail(url=bot_logo)
        error_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=error_embed, ephemeral=True, delete_after=10)

    rnd_hex = random_hex_color()
    member = await interaction.guild.fetch_member(user_id)
    kick_embed = discord.Embed(title=f'`@{member}` has been kicked!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    kick_embed.set_thumbnail(url=bot_logo)
    kick_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=kick_embed, ephemeral=True, delete_after=10)
    await interaction.guild.kick(member, reason=reason)

    log_embed = discord.Embed(title=f'{emoji1} User has been kicked! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nUser: `@{member}`\nUser ID: `{member.id}`\n\nKicked By: `@{interaction.user.name}`\nUser ID: `{interaction.user.id}`\nFor Reason: `{reason}`\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    log_embed.set_thumbnail(url=bot_logo)
    log_embed.set_footer(text=__authors__, icon_url=author_logo)
    channel = await interaction.guild.fetch_channel(log_channel)
    await channel.send(embed=log_embed)
@kick.error
async def kick_error(interaction: discord.Interaction, error: Exception):
    check_error_embed = discord.Embed(title=f'Oops..  |  Failed to run command...\n\n\nError;\n```{error}```\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
    check_error_embed.set_thumbnail(url=bot_logo)
    check_error_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=check_error_embed, ephemeral=True, delete_after=10)





def days_to_seconds(days):
    return days * 24 * 60 * 60

@app_commands.checks.has_permissions(ban_members=True)
@moderation_group.command(name='ban', description='Bans a user from the server.')
async def ban(interaction: discord.Interaction, user_id: str, reason: str, delete_messages_after: int=None):
    try:
        user_id = int(user_id)
    except:
        error_embed = discord.Embed(title='Error  |  A valid user ID must be given.\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
        error_embed.set_thumbnail(url=bot_logo)
        error_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=error_embed, ephemeral=True, delete_after=10)

    if not delete_messages_after:
        delete_messages_after=0
    elif delete_messages_after > 7:
        delete_messages_after = 7
        notice_embed = discord.Embed(title='Notice  |  7 days is the max permitted by discord. Deleting users messages for the past 7 days.\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xe6d50e, timestamp=datetime.datetime.now(datetime.timezone.utc))
        notice_embed.set_thumbnail(url=bot_logo)
        notice_embed.set_footer(text=__authors__, icon_url=author_logo)
        await interaction.response.send_message(embed=notice_embed, ephemeral=True, delete_after=10)


    seconds = days_to_seconds(delete_messages_after)
    rnd_hex = random_hex_color()
    try:
        member = await interaction.guild.fetch_member(user_id)
    except:
        member = await admin.fetch_user(user_id)
    ban_embed = discord.Embed(title=f'`@{member}` has been Banned!\n-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    ban_embed.set_thumbnail(url=bot_logo)
    ban_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=ban_embed, ephemeral=True, delete_after=10)
    await interaction.guild.ban(member, reason=reason, delete_message_seconds=seconds)

    log_embed = discord.Embed(title=f'{emoji1} User has been Banned! {emoji2}\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-\n\n\nUser: `@{member}`\nUser ID: `{member.id}`\n\nBanned By: `@{interaction.user.name}`\nUser ID: `{interaction.user.id}`\nFor Reason: `{reason}`\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=rnd_hex, timestamp=datetime.datetime.now(datetime.timezone.utc))
    log_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1008056064593379379/1168769126739742753/BEANED_HAMMER.png')
    log_embed.set_footer(text=__authors__, icon_url=author_logo)
    channel = await interaction.guild.fetch_channel(log_channel)
    await channel.send(embed=log_embed)
@ban.error
async def ban_error(interaction: discord.Interaction, error: Exception):
    check_error_embed = discord.Embed(title=f'Oops..  |  Failed to run command...\n\n\nError;\n```{error}```\n\n\n-=-=-=-=-=-=-=-=-=-=-=-=-=-', colour=0xff0000, timestamp=datetime.datetime.now(datetime.timezone.utc))
    check_error_embed.set_thumbnail(url=bot_logo)
    check_error_embed.set_footer(text=__authors__, icon_url=author_logo)
    await interaction.response.send_message(embed=check_error_embed, ephemeral=True, delete_after=10)



# Can add more commands later











# make bot go brrrrrrrrrrrrrrr
if __name__ == '__main__':
    clear()
    admin.tree.add_command(moderation_group)
    admin.run(token, reconnect=True)
