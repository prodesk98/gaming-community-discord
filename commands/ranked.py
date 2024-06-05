from discord import Interaction, Embed
from loguru import logger

from controllers.ranked import RankedController
from services.ranked import get_discord_icon_by_level, calc_level


async def Top10RankCommand(
    interaction: Interaction,
):
    ranking = await RankedController().get_ranked(
        interaction.guild_id, 10
    )

    lines = []

    top1 = None
    for n, rank in enumerate(ranking):
        profile_id, user_id, nick, total_score = rank
        if n == 0:
            top1 = user_id
        ranked_level = calc_level(total_score)
        content = f"{n + 1}. <@{user_id}> **{nick}** {get_discord_icon_by_level(ranked_level)} ({total_score} xp)"
        lines.append(content)

    embed_ranked = Embed(
        title=":trophy: Top 10 Rank",
        description="\n".join(lines) if len(lines) > 0 else "No ranked players found.",
        color=0x2F3136
    )

    if top1 is not None:
        top1_member = await interaction.guild.fetch_member(top1)
        if top1_member is not None:
            embed_ranked.set_thumbnail(
                url=top1_member.avatar
            )

    await interaction.edit_original_response(
        embed=embed_ranked
    )
