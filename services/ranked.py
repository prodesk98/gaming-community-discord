from typing import Dict, List

import discord.ui
from discord import Embed, Interaction, File, Button, Member

from config.environments import DATA_CONFIG
from controllers.likes import LikesController
from controllers.profiles import ProfileController
from controllers.scores import ScoresController
from models.likes import Likes
from models.profile import Profile


class LikesButton(discord.ui.View):
    def __init__(self, interaction: Interaction, profile_id: int, target_id: int):
        super().__init__()
        self.interaction = interaction
        self.profile_id = profile_id
        self.target_id = target_id

    @discord.ui.button(label="Like", style=discord.ButtonStyle.grey, emoji="👍")
    async def like(self, interaction: Interaction, button: Button):
        has_liked = await LikesController().has_like(self.profile_id, self.target_id)
        if has_liked:
            return await self.interaction.edit_original_response(
                content="You already liked this profile",
                view=None,
            )
        await LikesController().add_like(
            Likes(
                profile_id=self.profile_id,
                target_id=self.target_id,
            )
        )
        await self.interaction.edit_original_response(
            content="Liked!",
            view=None,
        )


def calc_level(exp: int) -> int:
    levels_peer_exp: List[int] = DATA_CONFIG['levels_peer_exp']
    for level, exp_level in enumerate(levels_peer_exp, start=1):
        if exp < exp_level:
            return level
    return len(levels_peer_exp) + 1


def get_color_by_level(level: int) -> int:
    colours_level = [
        0xCE7E00,
        0x999999,
        0xF1C232,
        0xFFC000,
        0x5D3AB6,
    ]
    return colours_level[level - 1]


def get_ranked_name_by_level(level: int) -> str:
    names_level: List[str] = DATA_CONFIG['names_level']
    return names_level[level - 1]


def get_discord_icon_by_level(level: int) -> str:
    discord_icons_level: List[str] = DATA_CONFIG['discord_icons_level']
    return discord_icons_level[level - 1]


def get_role_level(level: int) -> str | None:
    roles_level: Dict[str, str] = DATA_CONFIG['roles_level']
    return next((v for k, v in roles_level.items() if k == f"lvl_{level}"), None)


def get_roles_level() -> List[str]:
    roles_level: Dict[str, str] = DATA_CONFIG['roles_level']
    return [name for name in roles_level.values()]


async def remove_role_level(interaction: Interaction, roles: List[str], author: Member) -> None:
    for role in get_roles_level():
        if role in roles:
            role = discord.utils.get(interaction.guild.roles, name=role)
            await author.remove_roles(role)


async def calc_exp(profile_id: int) -> int:
    return await ScoresController().get_scores_by_user_id(profile_id)


async def calc_likes(target_id: int) -> int:
    return await LikesController().get_likes_by_target_id(target_id)


async def fetch_ranked_by_profile(interaction: Interaction, profile: Profile) -> None:
    if profile.nick_name is None:
        await interaction.edit_original_response(
            embed=Embed(
                title='Profile not found',
                description='This profile does not have a nickname.\n',
                color=0xff0000,
            )
        )
        return

    exp = await calc_exp(profile.id)
    likes = await calc_likes(target_id=profile.id)
    ranked_level = calc_level(exp)

    embed = Embed(
        title=f"{profile.nick_name} ({profile.level} lvl)",
        description=f'{exp} xp ({get_discord_icon_by_level(ranked_level)} {ranked_level} lvl - {get_ranked_name_by_level(ranked_level)})\n'
                    f'{likes} likes\n\n',
        color=get_color_by_level(ranked_level),
    )
    embed.add_field(
        name='Kills',
        value=profile.kills,
        inline=True,
    )
    embed.add_field(
        name='Assists',
        value=profile.assists,
        inline=True,
    )
    embed.add_field(
        name='Wins',
        value=profile.wins,
        inline=True,
    )
    embed.add_field(
        name='K/M',
        value=round(profile.kills / profile.matches, 2),
        inline=True,
    )
    embed.add_field(
        name='W/L',
        value="%.1f%%" % (round(profile.wins / profile.matches, 2) * 100),
        inline=True,
    )
    embed.add_field(
        name='Score',
        value=profile.score,
        inline=True,
    )

    # Weekly stats
    weekly_stats = await ScoresController().aget_weekly(profile.id)
    if weekly_stats:
        kills_diff = profile.kills - weekly_stats.kills
        assist_diff = profile.assists - weekly_stats.assist
        wins_diff = profile.wins - weekly_stats.wons
        losses_diff = profile.losses - weekly_stats.losses

        weekly_kills_percent = round(
            (1 - (weekly_stats.kills / profile.kills)) * 100,
            2
        )
        weekly_assist_percent = round(
            (1 - (weekly_stats.assist / profile.assists)) * 100,
            2
        )
        weekly_wons_percent = round(
            (1 - (weekly_stats.wons / profile.wins)) * 100,
            2
        )
        weekly_matches = wins_diff + losses_diff

        EMOJI_INCREASE = '<:increase:1246942607775371388>'
        embed.add_field(
            name='Weekly Stats',
            value=f'Kills: +%i / %.2f%% %s\n' % (kills_diff, weekly_kills_percent, EMOJI_INCREASE if kills_diff > 0 else '') +
                  f'Assists: +%i / %.2f%% %s\n' % (assist_diff, weekly_assist_percent, EMOJI_INCREASE if assist_diff > 0 else '') +
                  f'Wins: +%i / %.2f%% %s\n' % (wins_diff, weekly_wons_percent, EMOJI_INCREASE if wins_diff > 0 else '') +
                  f'K/M: %.2f\n' % (round(kills_diff / weekly_matches, 2) if weekly_matches > 0 else 0),
        )

    author = await interaction.guild.fetch_member(profile.user_id)

    if interaction.user.id == profile.user_id:
        author_roles = author.roles
        roles = [role.name for role in author_roles]
        role_level = get_role_level(ranked_level)
        if role_level not in roles:
            await remove_role_level(interaction, roles, author)

            role = discord.utils.get(interaction.guild.roles, name=role_level)
            await author.add_roles(role)

    ranked_icon = File(f"assets/scores/lvl_{ranked_level}.png", filename=f"ranked.png")
    embed.set_thumbnail(url=f"attachment://ranked.png")
    embed.set_author(
        name=author.display_name,
        icon_url=author.avatar
    )

    me = await ProfileController().query(user_id=interaction.user.id)

    has_liked = await LikesController().has_like(profile_id=me.id, target_id=profile.id)
    await interaction.edit_original_response(
        embed=embed,
        attachments=[ranked_icon],
        view=LikesButton(interaction=interaction, profile_id=me.id, target_id=profile.id)
        if profile.user_id != me.user_id and not has_liked else None,
    )
