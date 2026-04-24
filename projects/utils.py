import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def generate_avatar(letters):
    size = (200, 200)
    colors = [
        "#A8DADC",
        "#BDE0FE",
        "#CDB4DB",
        "#CCD5AE",
        "#D9ED92",
        "#F4A261",
        "#B8C0FF",
        "#FFD1DC",
        "#FFB28B",
        "#E6E6FA"
    ]
    background = random.choice(colors)
    image = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(image)
    font_size = 100
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()
    text = letters.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    x = (size[0] - w) / 2 - bbox[0]
    y = (size[1] - h) / 2 - bbox[1]

    draw.text((x, y), text, fill="white", font=font)
    buffer = BytesIO()
    image.save(buffer, format="PNG")

    return ContentFile(buffer.getvalue(), name="avatar.png")
