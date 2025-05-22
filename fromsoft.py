from PIL import Image, ImageDraw, ImageFont
from gradient import Gradient

IMG_SIZE = (1920, 300)
COLOR = (255, 208, 66)
FONT_S = ImageFont.truetype("agmena.ttf", 96)
FONT_L = ImageFont.truetype("agmena.ttf", 104)

TRANSPARENT = (0, 0, 0, 0)
SHADOW_BAR = Gradient([
    (0, (0, 0, 0, 0)),
    (0.25, (0, 0, 0, 170)),
    (0.75, (0, 0, 0, 170)),
    (1, (0, 0, 0, 0)),
])

def centre_text(
    img: Image.Image,
    text: str,
    font,
    color: str,
):
    cvs = Image.new("RGBA", img.size, TRANSPARENT)
    draw = ImageDraw.Draw(cvs)
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = int((cvs.width - w) * 0.5)
    y = int((cvs.height - h) * 0.485)
    draw.text((x, y), text, color, font=font)
    return Image.alpha_composite(img, cvs)

def elden_ring(text: str) -> Image.Image:
    img = Image.new("RGBA", IMG_SIZE, TRANSPARENT)

    y_mid = img.height // 2
    BAR_HEIGHT = 100
    SHADOW_BAR.draw_vertical(img, y_mid - BAR_HEIGHT, y_mid + BAR_HEIGHT)

    img = centre_text(img, text, FONT_L, (*COLOR, 80))
    img = centre_text(img, text, FONT_S, (*COLOR, 255))
    return img


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('text', nargs='*')

    args = parser.parse_args()
    text = ' '.join(args.text)

    img = elden_ring(text)
    img.save("output.png")
