from discord import Member, Interaction, Embed

from controllers.profiles import ProfileController
from services.ranked import fetch_ranked_by_profile


async def FetchProfile(
    interaction: Interaction,
    member: Member
):
    profile = await ProfileController().query(user_id=member.id, guild_id=interaction.guild_id)
    if not profile:
        return await interaction.edit_original_response(
            embed=Embed(
                title='Profile not found',
                description=f'Profile of {member.display_name} not found',
                color=0xff0000,
            )
        )

    await fetch_ranked_by_profile(interaction, profile)
