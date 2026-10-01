from argparse import ArgumentParser

from .fromsoft import GRADIENTS, fromsoft_image

parser = ArgumentParser()
parser.add_argument("text", nargs="*")
parser.add_argument(
    "--color",
    default="#ffd042",
    help="A color, or one of: " + ", ".join(GRADIENTS.keys()),
)
parser.add_argument(
    "--no-caps",
    action="store_false",
    dest="caps",
    help="Don't autocapitalise text.",
)


def main():
    args = parser.parse_args()
    text = " ".join(args.text)
    if args.caps:
        text = text.upper()

    if args.color in GRADIENTS:
        args.color = GRADIENTS[args.color]

    img = fromsoft_image(text, args.color)
    img.save("output.png")


if __name__ == "__main__":
    main()
