from discord import Interaction, Member

from controllers.profiles import ProfileController


async def RemoveProfileCommand(
    interaction: Interaction,
    user: Member,
):
    await ProfileController().remove(user_id=user.id, guild_id=interaction.guild_id)
    await interaction.edit_original_response(
        content=f"Profile removed for <@{user.id}>",
    )
