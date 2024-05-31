from discord import Interaction, Member

from controllers.profiles import ProfileController


async def RemoveNickCommand(
    interaction: Interaction,
    user: Member,
):
    await ProfileController().remove_nickname(user_id=user.id, guild_id=interaction.guild_id)
    await interaction.edit_original_response(
        content=f"Nickname removed for <@{user.id}>",
    )
