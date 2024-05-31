from discord import Interaction, Embed
from controllers.ranked import RankedController
from services.ranked import get_discord_icon, calc_level


async def Top10RankCommand(
    interaction: Interaction,
):
    ranking = await RankedController().get_ranked(
        interaction.guild_id, 10
    )

    body = ""

    for n, rank in enumerate(ranking):
        profile_id, user_id, nick, level, total_score = rank
        if nick is None:
            continue
        ranked_level = calc_level(total_score)
        body += f"{n + 1}. {get_discord_icon(ranked_level)} <@{user_id}> (**{nick.upper()}** lvl {level} - {total_score} xp)\n"

    if not body:
        body = "No ranked players found."

    await interaction.edit_original_response(
        embed=Embed(
            title="Top 10 Rank",
            description=body,
            color=0x2F3136
        )
    )
