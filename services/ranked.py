import discord.ui
from discord import Embed, Interaction, File, Button

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
    if exp < 100:
        return 1
    elif exp < 200:
        return 2
    elif exp < 300:
        return 3
    elif exp < 400:
        return 4
    return 5


def get_color(level: int) -> int:
    if level == 1:
        return 0xCE7E00
    elif level == 2:
        return 0x999999
    elif level == 3:
        return 0xF1C232
    elif level == 4:
        return 0xFFC000
    return 0x5D3AB6


def get_ranked_name(level: int) -> str:
    if level == 1:
        return "Bronze"
    elif level == 2:
        return "Silver"
    elif level == 3:
        return "Gold"
    elif level == 4:
        return "Platinum"
    return "Diamond"


def get_discord_icon(level: int) -> str:
    if level == 1:
        return "<:lvl_1:1245862237927772160>"
    elif level == 2:
        return "<:lvl_2:1245862239701958706>"
    elif level == 3:
        return "<:lvl_3:1245862242004500571>"
    elif level == 4:
        return "<:lvl_4:1245862244542320701>"
    return "<:lvl_5:1245862686248669305>"


async def calc_exp(profile_id: int) -> int:
    return await ScoresController().get_scores_by_user_id(profile_id)


async def calc_likes(target_id: int) -> int:
    return await LikesController().get_likes_by_target_id(target_id)


async def fetch_ranked_by_profile(interaction: Interaction, profile: Profile) -> None:
    exp = await calc_exp(profile.id)
    likes = await calc_likes(target_id=profile.id)
    ranked_level = calc_level(exp)

    embed = Embed(
        title=f"{profile.nick_name.upper()} (lvl {profile.level})",
        description=f'{get_discord_icon(ranked_level)} **{ranked_level} ({get_ranked_name(ranked_level)})**\n'
                    f'{exp} xp\n'
                    f'{likes} likes',
        color=get_color(ranked_level),
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

    ranked_icon = File(f"assets/scores/lvl_{ranked_level}.png", filename=f"ranked.png")
    embed.set_thumbnail(url=f"attachment://ranked.png")

    me = await ProfileController().query(user_id=interaction.user.id)

    has_liked = await LikesController().has_like(profile_id=me.id, target_id=profile.id)
    await interaction.edit_original_response(
        embed=embed,
        attachments=[ranked_icon],
        view=LikesButton(interaction=interaction, profile_id=me.id, target_id=profile.id)
        if profile.user_id != me.user_id and not has_liked else None,
    )
