from discord import Interaction

from controllers.profiles import ProfileController


async def RemoveProfileCommand(
    interaction: Interaction,
    nick: str,
):
    profile = await ProfileController().query(nick_name=nick, guild_id=interaction.guild_id)
    if not profile:
        await interaction.edit_original_response(
            content=f"Profile not found for {nick}",
        )
        return
    await ProfileController().remove(user_id=profile.user_id, guild_id=interaction.guild_id)
    await interaction.edit_original_response(
        content=f"Profile removed for <@{profile.user_id}>",
    )
