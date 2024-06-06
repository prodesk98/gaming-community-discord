import os
from os import PathLike

from discord import Interaction, Embed, File

from controllers.ranked import RankedController
from services.banner import create_player_profile_banner
from services.ranked import get_discord_icon_by_level, calc_level


async def Top10RankCommand(
    interaction: Interaction,
):
    ranking = await RankedController().get_ranked(
        interaction.guild_id, 10
    )

    lines = []

    top1 = None
    top1_nickname = None
    top1_level = None
    top1_score = None
    medal_emojis = [
        ":first_place:",
        ":second_place:",
        ":third_place:",
    ]
    spacer = "<:spacer:1248155241439039560>"
    for n, rank in enumerate(ranking):
        profile_id, user_id, nick, level, total_score = rank
        if n == 0:
            top1 = user_id
            top1_nickname = nick
            top1_level = level
            top1_score = total_score
        ranked_level = calc_level(total_score)
        medal = medal_emojis[n] if n < 3 else f"**#{n + 1}**"
        content = (f"{medal} <@{user_id}> **{nick}** {get_discord_icon_by_level(ranked_level)}\n"
                   f"{spacer} Level: ``{level}``\n"
                   f"{spacer} Exp: ``{total_score}xp``")
        lines.append(content)

    embed_ranked = Embed(
        title="Top 10 Rank",
        description="\n\n".join(lines) if len(lines) > 0 else "No ranked players found.",
        color=0x2F3136
    )

    banner_ranked: File | None = None
    banner_image: str | PathLike | None = None
    if top1 is not None:
        top1_member = await interaction.guild.fetch_member(top1)
        if top1_member is not None:
            banner_image = await create_player_profile_banner(
                top1_nickname,
                "#1",
                top1_level,
                top1_score,
                avatar_url=top1_member.avatar.url
            )
            banner_ranked = File(banner_image, filename="banner.jpg")
            embed_ranked.set_image(url=f"attachment://banner.jpg")

    embed_ranked.set_footer(text="Ranking updated every 8 days, To more info use /profile @user")

    await interaction.edit_original_response(
        embed=embed_ranked,
        attachments=[banner_ranked] if banner_ranked is not None else None
    )

    os.remove(banner_image)
