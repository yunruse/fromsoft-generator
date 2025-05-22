from PIL import Image, ImageDraw

def lerp_tuple(a, b, t: float):
    return tuple(int(ai + (bi - ai) * t) for ai, bi in zip(a, b))

Color = tuple[int, int, int, int]
class Gradient(list[tuple[float, Color]]):
    def color_at(self, x: float):
        for i, (prop, _) in enumerate(self):
            if prop > x:
                break
        a, cola = self[i-1]
        b, colb = self[i]
        return lerp_tuple(cola, colb, (x-a)/(b-a))

    def draw_vertical(
        self,
        img: Image.Image,
        y0: int = 0,
        y1: int = None,
        x0: int = 0,
        x1: int = None,
    ):
        """Draw the gradient vertically from y0 to y1."""
        if y1 is None:
            y1 = img.height
        if x1 is None:
            x1 = img.width
        
        draw = ImageDraw.Draw(img)  
        for y in range(y0, y1+1):
            t = (y-y0) / (y1-y0)
            draw.line([(x0, y), (x1, y)], fill =self.color_at(t))
