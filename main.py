from typing import Any

import discord
from discord import Interaction, app_commands
from discord.ext import commands

from commands import AddProfileCommand, MeCommand, FetchProfileCommand, Top10RankCommand
from config import DISCORD_TOKEN, MANAGER_ROLE


class ClientBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        await self.tree.sync()


intents = discord.Intents.default()
intents.message_content = False
client = ClientBot(command_prefix='$', intents=intents)


@client.tree.command(
    name='ping',
    description='Check if the bot is online',
)
@app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
async def ping(interaction: Interaction):
    embed = discord.Embed(
        title='Pong!',
        description=f'Latency: {round(client.latency * 1000)}ms',
        color=0x00ff00,
    )
    await interaction.response.send_message(embed=embed)  # noqa


@client.tree.command(
    name='add_profile',
    description='Add a profile to the bot',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
@app_commands.checks.has_role(MANAGER_ROLE)
async def add_profile(interaction: Interaction, nick: str):
    await interaction.response.defer(ephemeral=True) # noqa
    await AddProfileCommand(interaction, nick)


@client.tree.command(
    name='me',
    description='Get your profile',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def me(interaction: Interaction):
    await interaction.response.defer(ephemeral=True)  # noqa
    await MeCommand(interaction)


@client.tree.command(
    name='ranked',
    description='Get top 10 ranked players',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def get_ranked(interaction: Interaction):
    await interaction.response.defer(ephemeral=False)  # noqa
    await Top10RankCommand(interaction)


@client.tree.command(
    name='profile',
    description='Get a profile',
)
@app_commands.checks.cooldown(1, 30, key=lambda i: (i.guild_id, i.user.id))
async def get_profile(interaction: Interaction, user: discord.Member):
    await interaction.response.defer(ephemeral=True)  # noqa
    await FetchProfileCommand(interaction, user)


@client.tree.command(
    name='help',
    description='Get help',
)
async def help(interaction: Interaction):
    embed = discord.Embed(
        title='Help',
        description='**/ping**: Latency\n'
                    '**/me**: Get your profile\n'
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
    await interaction.response.send_message(embed=embed)  # noqa


if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
