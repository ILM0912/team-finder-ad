import random
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

from .constants import (
    AVATAR_COLORS,
    AVATAR_FILE_NAME,
    AVATAR_FONT_NAME,
    AVATAR_FONT_SIZE,
    AVATAR_SIZE,
    AVATAR_TEXT_ANCHOR,
    AVATAR_TEXT_COLOR,
)


def generate_avatar(letters):
    background = random.choice(AVATAR_COLORS)
    image = Image.new("RGB", AVATAR_SIZE, background)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    text = letters.upper()
    bbox = draw.textbbox(AVATAR_TEXT_ANCHOR, text, font=font)

    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (AVATAR_SIZE[0] - w) / 2 - bbox[0]
    y = (AVATAR_SIZE[1] - h) / 2 - bbox[1]

    draw.text((x, y), text, fill=AVATAR_TEXT_COLOR, font=font)
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return ContentFile(buffer.getvalue(), name=AVATAR_FILE_NAME)
