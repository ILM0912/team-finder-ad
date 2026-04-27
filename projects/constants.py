from enum import Enum

# Avatars generation constants
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


# models constants
NAME_MAX_LENGTH = 124
SURNAME_MAX_LENGTH = 124
PHONE_MAX_LENGTH = 12
ABOUT_MAX_LENGTH = 256
PROJECT_NAME_MAX_LENGTH = 200

USER_AVATAR_UPLOAD_TO = 'avatars/'

STATUS_OPEN = 'open'
STATUS_CLOSED = 'closed'

PROJECT_STATUS_CHOICES = [
    (STATUS_OPEN, 'Открыт'),
    (STATUS_CLOSED, 'Закрыт'),
]

PROJECT_STATUS_MAX_LENGTH = max(
    len(status[0]) for status in PROJECT_STATUS_CHOICES
)
