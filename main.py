from typing import Any

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from commands import (
    AddProfileCommand, MeCommand, FetchProfileCommand,
    Top10RankCommand, RemoveNickCommand, RemoveProfileCommand,
)
from config import DISCORD_TOKEN, MANAGER_ROLE


class ClientBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.tree.sync()


intents = discord.Intents.default()
intents.message_content = False
client = ClientBot(command_prefix='$', intents=intents)


async def error_message(interaction: Interaction, title: str = "Error", exception: str = ""):
    embed = discord.Embed(
        title=title,
        description=exception,
        color=0xff0000,
    )
    await interaction.edit_original_response(embed=embed, view=None)


@client.tree.command(
    name='ping',
    description='Check if the bot is online',
)
@app_commands.checks.has_role(MANAGER_ROLE)
async def ping(interaction: Interaction):
    embed = discord.Embed(
        title='Pong!',
        description=f'Latency: {round(client.latency * 1000)}ms',
        color=0x00ff00,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)  # noqa


@client.tree.command(
    name='add_profile',
    description='Add a profile to the bot',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def add_profile(interaction: Interaction, nick: str):
    await interaction.response.defer(ephemeral=True)  # noqa
    try:
        await AddProfileCommand(interaction, nick)
    except Exception as e:
        await error_message(interaction, 'Profile not added', f'Profile not added, error: {e}')


@client.tree.command(
    name='remove_nick',
    description='Remove a nickname',
)
@app_commands.checks.has_role(MANAGER_ROLE)
async def remove_nick(interaction: Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)  # noqa
    try:
        await RemoveNickCommand(interaction, user)
    except Exception as e:
        await error_message(interaction, 'Nickname not removed', f'Nickname not removed, error: {e}')


@client.tree.command(
    name='me',
    description='Get your profile',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def me(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)  # noqa
    try:
        await MeCommand(interaction)
    except Exception as e:
        await error_message(interaction, exception=str(e))


@client.tree.command(
    name='ranked',
    description='Get top 10 ranked players',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def get_ranked(interaction: Interaction):
    await interaction.response.defer(ephemeral=False)  # noqa
    try:
        await Top10RankCommand(interaction)
    except Exception as e:
        await error_message(interaction, exception=str(e))


@client.tree.command(
    name='remove_profile',
    description='Remove a profile',
)
@app_commands.checks.has_role(MANAGER_ROLE)
async def remove_profile(interaction: Interaction, nick: str):
    await interaction.response.defer(ephemeral=True)  # noqa
    try:
        await RemoveProfileCommand(interaction, nick)
    except Exception as e:
        await error_message(interaction, exception=str(e))


@client.tree.command(
    name='profile',
    description='Get a profile',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def get_profile(interaction: Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)  # noqa
    try:
        await FetchProfileCommand(interaction, user)
    except Exception as e:
        await error_message(interaction, exception=str(e))


@client.tree.command(
    name='help',
    description='Get help',
)
async def help(interaction: Interaction):
    embed = discord.Embed(
        title='Help',
        description='**/me**: Get your profile\n'
                    '**/ranked**: Get top 10 ranked players\n'
                    '**/profile**: Get a profile\n'
                    '**/add_profile**: Add a profile\n',
        color=0x00ff00,
    )
    await interaction.response.send_message(embed=embed)  # noqa


@client.tree.error
async def error(interaction: Interaction, error: Any):
    embed = discord.Embed(
        title='Error',
        description=error,
        color=0xff0000,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)  # noqa


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
