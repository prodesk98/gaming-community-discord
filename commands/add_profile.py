import discord
from discord import Interaction, Embed, Button

from models.profile import Profile
from schemas.stats import StatsORM
from services.tracker_gg import TrackerGGService
from controllers.profiles import ProfileController

tracker_gg_service = TrackerGGService()


class ConfirmationView(discord.ui.View):
    def __init__(self, interaction: Interaction, nick: str, stats: StatsORM):
        super().__init__()
        self.interaction = interaction
        self.nick = nick
        self.stats = stats

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.success)
    async def confirm_button_callback(self, interaction: Interaction, button: Button):
        try:
            # create profile
            profile = Profile(
                nick_name=self.nick,
                guild_id=interaction.guild_id,
                user_id=interaction.user.id,
                level=self.stats.level,
                matches=self.stats.matches,
                wins=self.stats.wins,
                losses=self.stats.losses,
                kills=self.stats.kills,
                assists=self.stats.assists,
                score=self.stats.score,
            )
            has_profile = await ProfileController().query(user_id=interaction.user.id)
            if has_profile:
                has_profile.nick_name = self.nick
                await ProfileController().update_profile(has_profile)
            else:
                await ProfileController().add_profile(profile)
        except Exception as e:
            return await self.interaction.edit_original_response(
                embed=Embed(
                    title='Profile not added',
                    description=f'Profile not added, error: {e}',
                    color=0xff0000,
                ),
                view=None
            )

        await self.interaction.edit_original_response(
            embed=Embed(
                title='Profile added',
                description='Profile added successfully\n'
                            'You can now use the `/me` command to see your profile.',
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
    has_nick = await ProfileController().query(guild_id=interaction.guild_id, nick_name=nick)
    if has_nick:
        return await interaction.edit_original_response(
            embed=Embed(
                title='Profile already exists',
                description=f'Profile {nick} already exists\n',
                color=0xff0000,
            )
        )

    has_profile = await ProfileController().query(user_id=interaction.user.id)
    if has_profile and has_profile.nick_name is not None:
        return await interaction.edit_original_response(
            embed=Embed(
                title='Profile already exists',
                description=f'You already have a profile\n',
                color=0xff0000,
            )
        )

    profile = await tracker_gg_service.get_profile_stats(nick, 'ubi')
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
    stats = StatsORM()
    stats.level = next(iter(next(iter(profile.data.matches)).segments)).stats.playerLevel.value
    for match in profile.data.matches:
        for segment in match.segments:
            if segment.type != 'overview':
                continue
            stats.matches += segment.stats.matchesCompleted.value
            stats.wins += segment.stats.matchesWon.value
            stats.losses += segment.stats.matchesLost.value
            stats.kills += segment.stats.kills.value
            stats.score += segment.stats.score.value
            stats.assists += segment.stats.assists.value

    embed = Embed(
        title=f"{nick} (lvl {stats.level})",
        description=f'Matches: **{stats.matches}**\n'
                    f'Wins: **{stats.wins}**\n'
                    f'Losses: **{stats.losses}**\n'
                    f'Kills: **{stats.kills}**\n'
                    f'Assists: **{stats.assists}**\n',
        color=0x2986CC,
        url=f'https://tracker.gg/xdefiant/profile/ubi/{nick}/overview'
    )

    embed.set_footer(text='This is your profile? Click the button to confirm.')
    await interaction.edit_original_response(embed=embed, view=ConfirmationView(interaction, nick, stats))
