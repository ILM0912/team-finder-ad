from enum import Enum


AVATAR_SIZE = (200, 200)
AVATAR_FONT_SIZE = 100
AVATAR_FONT_NAME = "DejaVuSans-Bold.ttf"
AVATAR_TEXT_ANCHOR = (0, 0)
AVATAR_TEXT_COLOR = "white"
AVATAR_FILE_NAME = "avatar.png"


class AvatarColor(Enum):
    BLUE = "#A8DADC"
    LIGHT_BLUE = "#BDE0FE"
    PURPLE = "#CDB4DB"
    GREEN = "#CCD5AE"
    LIME = "#D9ED92"
    ORANGE = "#F4A261"
    LAVENDER_BLUE = "#B8C0FF"
    PINK = "#FFD1DC"
    PEACH = "#FFB28B"
    LAVENDER = "#E6E6FA"


AVATAR_COLORS = [color.value for color in AvatarColor]
