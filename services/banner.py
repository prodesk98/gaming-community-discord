import asyncio
import os
from os import PathLike

import requests
from tempfile import NamedTemporaryFile
from PIL import Image, ImageDraw, ImageFont, ImageOps

# Configurações iniciais
width, height = 800, 200  # Tamanho da imagem
background_color = (45, 45, 45)  # Cor de fundo
text_color = (255, 230, 150)  # Cor do texto (amarelo claro)
link_color = (0, 102, 204)  # Cor do link (azul)
secondary_text_color = (185, 185, 185)  # Cor do texto secundário (cinza)
border_color = (35, 35, 35)  # Cor da borda
font_size = 20
font_size_small = 11
font_size_large = 30

# Carregar fontes
font = ImageFont.truetype("assets/fonts/lato/Lato-Black.ttf", font_size)
font_large = ImageFont.truetype("assets/fonts/lato/Lato-Bold.ttf", font_size_large)
font_link = ImageFont.truetype("assets/fonts/lato/Lato-Regular.ttf", font_size_small)


def create_circular_image(image_path, size=(100, 100)):
    """
    Cria uma imagem circular a partir de uma imagem quadrada.
    """
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.Resampling.LANCZOS)  # Usar redimensionamento de alta qualidade

    # Criar uma máscara circular
    mask = Image.new('L', size, 0)
    draw = ImageDraw.Draw(mask)
    # draw.ellipse((0, 0) + size, fill=255)
    draw.rounded_rectangle((0, 0) + size, 100, 255)

    # Aplicar a máscara à imagem
    output = ImageOps.fit(img, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    return output


def _download_image(url: str) -> str | PathLike:
    stream = requests.get(url, stream=True)
    file = NamedTemporaryFile(delete=False)

    for chunk in stream.iter_content(chunk_size=128):
        file.write(chunk)

    file.seek(0)
    return file.name


def _create_banner(
        player_name: str,
        weekly_rank: str,
        level: int,
        exp_total: int,
        avatar_url: str
) -> str | PathLike:
    # Criar a imagem vazia com fundo
    image = Image.new("RGB", (width, height), background_color)
    draw = ImageDraw.Draw(image)

    # Carregar e processar a imagem do jogador
    player_image_path = _download_image(avatar_url)
    player_image = create_circular_image(player_image_path, size=(100, 100))

    from services.ranked import calc_level
    ranked_level = calc_level(exp_total)

    medal_image = Image.open(f"assets/scores/lvl_{ranked_level}.png").convert("RGBA")
    medal_image = medal_image.resize((30, 30), Image.Resampling.LANCZOS)

    # xdefiant logo
    xdefiant_logo = Image.open("assets/logos/discord.png").convert("RGBA")
    xdefiant_logo = xdefiant_logo.resize((20, 20), Image.Resampling.LANCZOS)
    image.paste(xdefiant_logo, (10, 10), xdefiant_logo)

    # add link discord text
    draw.text((40, 11), "(COMUNIDADE GAMER) https://discord.gg/xdefiant-brasil", font=font_link, fill=link_color)

    # calc position to add medal
    medal_padding = 200 if player_name.__len__() < 11 else 160
    medal_pos_x = player_name.__len__() * 10 + medal_padding
    medal_pos_y = 70 if player_name.__len__() < 11 else 63
    # add medal to image name player
    image.paste(medal_image, (medal_pos_x, medal_pos_y), medal_image)

    # Posicionar a imagem do jogador
    image.paste(player_image, (20, 50), player_image)

    # Desenhar informações do jogador
    draw.text((140, 66), player_name, font=font_large if player_name.__len__() < 11 else font, fill=text_color)
    draw.text((140, 105), f"WEEKLY RANK  {weekly_rank}", font=font, fill=secondary_text_color)

    # Desenhar retângulos para nível e exp
    draw.rectangle([(450, 50), (770, 100)], fill=border_color)
    draw.rectangle([(450, 120), (770, 170)], fill=border_color)

    # Desenhar texto de nível e exp
    draw.text((500, 63), "LEVEL", font=font, fill=secondary_text_color)
    draw.text((580, 56), str(level), font=font_large, fill=text_color)
    draw.text((500, 133), "EXP", font=font, fill=secondary_text_color)
    draw.text((580, 133), f"{exp_total}", font=font, fill=text_color)

    # Salvar a imagem em um arquivo
    temp = NamedTemporaryFile(delete=False, suffix=".jpg", prefix="banner_")
    image.save(temp.name, "JPEG", quality=100)

    os.remove(player_image_path)
    return temp.name


async def create_player_profile_banner(
        player_name: str,
        weekly_rank: str,
        level: int,
        exp_total: int,
        avatar_url: str
) -> str | PathLike:
    return await asyncio.to_thread(_create_banner, player_name, weekly_rank, level, exp_total, avatar_url)
