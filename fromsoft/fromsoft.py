from PIL import Image, ImageDraw, ImageFont
from ._gradient import Gradient

IMG_SIZE = (1920, 300)
COLOR = (255, 208, 66)
try:
    FONT_S = ImageFont.truetype("agmena.ttf", 96)
    FONT_L = ImageFont.truetype("agmena.ttf", 104)
except OSError:
    raise FileNotFoundError("Font `agmena.tff` could not be found!") from None

TRANSPARENT = (0, 0, 0, 0)
SHADOW_BAR = Gradient.from_hex(["0000", "000a", "000a", "000a", "0000"])

GRADIENTS = {
    # fmt: off
    "gay":      "f00 f80 fe0 0a0 26c a0a",
    "trans":    "7bf 7bf f9a f9a fff fff f9a f9a 7bf 7bf",
    "bi":       "f08 f08 a6a 80f 80f",
    "lesbian":  "f20 f64 fa8 fff f8f f4c f08",
    "nb":       "ff2 fff 84d 333",
    "pan":      "f2c f2c ff2 ff2 2cf 2cf",
    "mlm":      "2a6 6ea 8fc fff 88f 44c 22a",
    "ace":      "000 aaa fff 808",
    "aro":      "000 aaa fff ad7 3a4",
    "aroace":   "235 6ad fff ec0 e80",
    "intersex": "70a 70a fd0 70a 70a",
    # fmt: on
}


def centre_text(
    img: Image.Image,
    text: str,
    font,
    color: str | tuple[int, ...],
):
    cvs = Image.new("RGBA", img.size, TRANSPARENT)
    draw = ImageDraw.Draw(cvs)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = int((cvs.width - w) * 0.5)
    y = int((cvs.height - h) * 0.485)
    draw.text((x, y), text, color, font=font)
    return cvs


def generate(text: str, col: str | Gradient) -> Image.Image:
    img = Image.new("RGBA", IMG_SIZE, TRANSPARENT)

    if isinstance(col, str) and " " in col:
        col = Gradient.from_hex(col.split())

    x_mid = img.width // 2
    y_mid = img.height // 2
    _, _, w, _ = ImageDraw.Draw(img).textbbox((0, 0), text, font=FONT_L)

    BAR_HEIGHT = 100
    SHADOW_BAR.draw_vertical(img, y_mid - BAR_HEIGHT, y_mid + BAR_HEIGHT)

    # TODO: gradient
    txt_l = centre_text(img, text, FONT_L, (*COLOR, 80))
    txt_s = centre_text(img, text, FONT_S, (*COLOR, 255))

    if isinstance(col, Gradient):
        fill = Image.new("RGBA", img.size)
        col.draw_horizontal(fill, x0=int(x_mid - w // 2), x1=int(x_mid + w // 2))
    else:
        fill = Image.new("RGBA", img.size, col)

    img = Image.composite(fill, img, txt_l)
    img = Image.composite(fill, img, txt_s)

    return img
