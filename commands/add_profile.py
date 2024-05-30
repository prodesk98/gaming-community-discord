import discord
from discord import Interaction, Embed, Button
from services.tracker_gg import TrackerGGService

tracker_gg_service = TrackerGGService()


class ConfirmationView(discord.ui.View):
    def __init__(self, interaction: Interaction, nick: str):
        super().__init__()
        self.interaction = interaction

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm_button_callback(self, interaction: Interaction, button: Button):
        await self.interaction.edit_original_response(
            embed=Embed(
                title='Profile added',
                description='Profile added successfully',
                color=0x00ff00,
            ),
            view=None
        )

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
    async def cancel_button_callback(self, interaction: Interaction, button: Button):
        await self.interaction.edit_original_response(
            embed=Embed(
                title='Profile not added',
                description='Profile not added, please try again.',
                color=0xff0000,
            ),
            view=None
        )


async def AddProfileCommand(
        interaction: Interaction,
        nick: str,
):
    profile = tracker_gg_service.get_profile_stats(nick, 'ubi')
    if not profile:
        return await interaction.edit_original_response(
            embed=Embed(
                title='Connect your account to tracker.gg',
                description=f'Profile {nick} not found, please connect your account to tracker.gg',
                color=0xff0000,
                url='https://tracker.gg/'
            )
        )

    # sum all stats
    stats = {
        'matches': 0,
        'wins': 0,
        'losses': 0,
        'kills': 0,
        'score': 0.0,
    }

    for match in profile.data.matches:
        for segment in match.segments:
            if segment.type != 'overview':
                continue
            stats['matches'] += segment.stats.matchesCompleted.value
            stats['wins'] += segment.stats.matchesWon.value
            stats['losses'] += segment.stats.matchesLost.value
            stats['kills'] += segment.stats.kills.value
            stats['score'] += segment.stats.score.value

    level = next(iter(next(iter(profile.data.matches)).segments)).stats.playerLevel.value
    embed = Embed(
        title=f"{nick} (lvl {level})",
        description=f'Matches: **{stats["matches"]}**\n'
                    f'Wins: **{stats["wins"]}**\n'
                    f'Losses: **{stats["losses"]}**\n'
                    f'Kills: **{stats["kills"]}**\n'
                    f'Score: **{stats["score"]}**\n',
        color=0x2986CC,
        url=f'https://tracker.gg/xdefiant/profile/ubi/{nick}/overview'
    )

    embed.set_footer(text='This is your profile? Click the button to confirm.')
    await interaction.edit_original_response(embed=embed, view=ConfirmationView(interaction, nick))
