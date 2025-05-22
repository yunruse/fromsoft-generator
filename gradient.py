from PIL import Image, ImageDraw

def split(iterable, N):
    return (iterable[i:i+2] for i in range(0, len(iterable), N))

def from_hex(color: str):
    color = color.removeprefix('#')
    match len(color):
        case 3 | 4:
            return tuple(int(x, 16) * 17 for x in color)
        case 6 | 8:
            return tuple(int(x, 16) for x in split(color, 2))
    return NotImplemented

def lerp_tuple(a, b, t: float):
    return tuple(int(ai + (bi - ai) * t) for ai, bi in zip(a, b))

Color = tuple[int, int, int, int]
class Gradient(list[tuple[float, Color]]):

    @classmethod
    def from_hex(cls, cols: list[str]):
        N = len(cols)
        return cls([
            (i/(N-1), from_hex(c))
            for i, c in enumerate(cols)
        ])


    def color_at(self, x: float):
        for i, (prop, _) in enumerate(self):
            if prop > x:
                break
        a, cola = self[i-1]
        b, colb = self[i]
        return lerp_tuple(cola, colb, (x-a)/(b-a))

    def draw_vertical(
        self,
        img: Image.Image = None,
        y0: int = 0,
        y1: int = None,
        x0: int = 0,
        x1: int = None,
    ):
        """
        Draw the gradient vertically from y0 to y1.

        Modifies an image in place - unless no image is provided,
        in which case a new image is returned.
        """
        if img is None:
            img = Image.new("RGBA", (x1, y1))
        if y1 is None:
            y1 = img.height
        if x1 is None:
            x1 = img.width
        
        draw = ImageDraw.Draw(img)  
        for y in range(y0, y1+1):
            t = (y-y0) / (y1-y0)
            draw.line([(x0, y), (x1, y)], fill=self.color_at(t))
        return img

    def draw_horizontal(
        self,
        img: Image.Image = None,
        x0: int = 0,
        x1: int = None,
        y0: int = 0,
        y1: int = None,
    ):
        """
        Draw the gradient horizontally from x0 to x1.

        Modifies an image in place - unless no image is provided,
        in which case a new image is returned.
        """
        if img is None:
            img = Image.new("RGBA", (x1, y1))
        if x1 is None:
            x1 = img.width
        if y1 is None:
            y1 = img.height
        
        draw = ImageDraw.Draw(img)  
        for x in range(x0, x1+1):
            t = (x-x0) / (x1-x0)
            draw.line([(x, y0), (x, y1)], fill=self.color_at(t))
        return img
