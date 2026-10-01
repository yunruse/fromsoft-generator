from posixpath import expanduser

from PIL import Image, ImageDraw, ImageFont
from ._gradient import Gradient

IMG_SIZE = (1920, 300)
COLOR = (255, 208, 66)

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


def _centre_text(
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


def fromsoft_banner(
    text: str, col: str | Gradient, font_path: str = "agmena.ttf"
) -> Image.Image:
    "Generate a wide text banner in the style of a FROMSOFT game."

    try:
        font_text = ImageFont.truetype(expanduser(font_path), 104)
        font_shadow = ImageFont.truetype(expanduser(font_path), 96)
    except OSError:
        raise FileNotFoundError(f"Could not find a font {font_path!r}") from None

    w, h = IMG_SIZE
    text_width = font_text.getbbox(text)[2]
    w = max(w, int(text_width) + 20)

    img = Image.new("RGBA", (w, h), TRANSPARENT)

    if isinstance(col, str) and " " in col:
        col = Gradient.from_hex(col.split())

    x_mid = img.width // 2
    y_mid = img.height // 2
    _, _, w, _ = ImageDraw.Draw(img).textbbox((0, 0), text, font=font_text)

    BAR_HEIGHT = 100
    SHADOW_BAR.draw_vertical(img, y_mid - BAR_HEIGHT, y_mid + BAR_HEIGHT)

    txt_l = _centre_text(img, text, font_text, (*COLOR, 80))
    txt_s = _centre_text(img, text, font_shadow, (*COLOR, 255))

    if isinstance(col, Gradient):
        fill = Image.new("RGBA", img.size)
        col.draw_horizontal(fill, x0=int(x_mid - w // 2), x1=int(x_mid + w // 2))
    else:
        fill = Image.new("RGBA", img.size, col)

    img = Image.composite(fill, img, txt_l)
    img = Image.composite(fill, img, txt_s)

    return img
