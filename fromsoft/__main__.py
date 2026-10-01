from argparse import ArgumentParser

from .fromsoft import GRADIENTS, fromsoft_banner

parser = ArgumentParser()
parser.add_argument("text", nargs="*")
parser.add_argument(
    "--color",
    "-c",
    default="#ffd042",
    help="A color, or one of: " + ", ".join(GRADIENTS.keys()),
)
parser.add_argument(
    "--no-caps",
    action="store_false",
    dest="caps",
    help="Don't autocapitalise text.",
)
parser.add_argument(
    "--font",
    default="agmena.ttf",
    help="Path to the font to use.",
)
parser.add_argument(
    "--out",
    "-o",
    default="output.png",
    help="Path to the output file.",
)


def main():
    args = parser.parse_args()
    text = " ".join(args.text)
    if args.caps:
        text = text.upper()

    if args.color in GRADIENTS:
        args.color = GRADIENTS[args.color]

    img = fromsoft_banner(text, col=args.color, font_path=args.font)
    img.save(args.out)


if __name__ == "__main__":
    main()
