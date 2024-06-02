from discord import Interaction, Embed
from controllers.ranked import RankedController
from services.ranked import get_discord_icon_by_level, calc_level


async def Top10RankCommand(
    interaction: Interaction,
):
    ranking = await RankedController().get_ranked(
        interaction.guild_id, 10
    )

    body = ""

    top1 = None
    for n, rank in enumerate(ranking):
        profile_id, user_id, nick, total_score = rank
        if n == 0:
            top1 = user_id
        ranked_level = calc_level(total_score)
        body += f"{n + 1}. <@{user_id}> **{nick}** ({get_discord_icon_by_level(ranked_level)} {ranked_level} lvl / {total_score} xp)\n"

    if not body:
        body = "No ranked players found."

    embed_ranked = Embed(
        title="Top 10 Rank",
        description=body,
        color=0x2F3136
    )

    if top1 is not None:
        top1_member = interaction.guild.get_member(top1)
        if top1_member is not None:
            embed_ranked.set_thumbnail(
                url=top1_member.avatar
            )

    await interaction.edit_original_response(
        embed=embed_ranked
    )
