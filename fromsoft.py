from PIL import Image, ImageDraw, ImageFont
from gradient import Gradient

IMG_SIZE = (1920, 300)
COLOR = (255, 208, 66)
FONT_S = ImageFont.truetype("agmena.ttf", 96)
FONT_L = ImageFont.truetype("agmena.ttf", 104)

TRANSPARENT = (0, 0, 0, 0)
SHADOW_BAR = Gradient.from_hex('0000 000a 000a 000a 0000'.split())

GRADIENTS = {
    "gay":     Gradient.from_hex("f00 f80 fe0 0a0 26c a0a".split()),
    "trans":   Gradient.from_hex("7bf 7bf f9a f9a fff fff f9a f9a 7bf 7bf".split()),
    "bi":      Gradient.from_hex("f08 f08 a6a 80f 80f".split()),
    "lesbian": Gradient.from_hex("f20 f64 fa8 fff f8f f4c f08".split()),
    "nb":      Gradient.from_hex("ff2 fff 84d 333".split()),
    "pan":     Gradient.from_hex("f2c f2c ff2 ff2 2cf 2cf".split()),
    "men":     Gradient.from_hex("2a6 6ea 8fc fff 88f 44c 22a".split()),
}

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
    return cvs

def elden_ring(
    text: str,
    col_or_gradient: str | Gradient
) -> Image.Image:
    img = Image.new("RGBA", IMG_SIZE, TRANSPARENT)

    x_mid = img.width // 2
    y_mid = img.height // 2
    _, _, w, _ = ImageDraw.Draw(img).textbbox((0, 0), text, font=FONT_L)

    BAR_HEIGHT = 100
    SHADOW_BAR.draw_vertical(img, y_mid - BAR_HEIGHT, y_mid + BAR_HEIGHT)

    # TODO: gradient
    txt_l = centre_text(img, text, FONT_L, (*COLOR, 80))
    txt_s = centre_text(img, text, FONT_S, (*COLOR, 255))

    if isinstance(col_or_gradient, Gradient):
        fill = Image.new("RGBA", img.size)
        col_or_gradient.draw_horizontal(fill, x0=x_mid-w//2, x1=x_mid+w//2)
    else:
        fill = Image.new("RGBA", img.size, col_or_gradient)

    img = Image.composite(fill, img, txt_l)
    img = Image.composite(fill, img, txt_s)
    
    return img


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('text', nargs='*')
    parser.add_argument(
        '--color', default='#ffd042',
        help="A color, or one of: " + ", ".join(GRADIENTS.keys())
    )
    parser.add_argument(
        '--no-caps',
        action='store_false', dest='caps',
        help="Don't autocapitalise text.")

    args = parser.parse_args()
    text = ' '.join(args.text)
    if args.caps:
        text = text.upper()
    
    if args.color in GRADIENTS:
        args.color = GRADIENTS[args.color]

    img = elden_ring(text, args.color)
    img.save("output.png")
