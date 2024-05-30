from discord import Interaction, Embed
from controllers.profiles import ProfileController
from services.ranked import fetch_ranked_by_profile


async def MeCommand(
    interaction: Interaction,
):
    profile = await ProfileController().query(user_id=interaction.user.id)
    if not profile:
        return await interaction.edit_original_response(
            embed=Embed(
                title='Profile not found',
                description='Profile not found, please add a profile.\n'
                            'Please use `/add_profile` to add a profile.',
                color=0xff0000,
            )
        )

    await fetch_ranked_by_profile(interaction, profile)

