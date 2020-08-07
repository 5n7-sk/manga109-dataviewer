from PIL import Image, ImageDraw, ImageFont


class Drawer:
    def __init__(self, font_path, font_size: int = 30, rect_width: int = 10, text_margin: int = 30):
        self._font = ImageFont.truetype(font=font_path, size=font_size, encoding="utf-8")
        self._rect_width = rect_width
        self._text_margin = text_margin

    def draw(
        self, img: Image.Image, x_min: int, y_min: int, x_max: int, y_max: int, color: str, text: str = "",
    ):
        draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)  # type: ignore
        draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=self._rect_width)

        margin = self._text_margin
        text_y = max(0, y_min - margin)
        text_w, text_h = self._font.getsize(text)

        draw.rectangle((x_min, text_y, x_min + text_w, text_y + text_h), fill=color)
        draw.text((x_min, text_y), text, fill="white", font=self._font)
