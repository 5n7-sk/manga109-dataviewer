import os.path
from enum import Enum
from typing import List, Tuple

import pandas as pd
import streamlit as st
import yaml
from PIL import Image, ImageDraw, ImageFont

from manga109 import Manga109
from manga109 import typing as T
from manga109.utils import get_all_titles

__version__ = "0.1.0"

with open("config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)


class Content(Enum):
    characters = "characters"
    pages = "pages"

    @classmethod
    def all(cls) -> Tuple[str]:
        return tuple(map(lambda c: c.value, cls))


class Annotation(Enum):
    body = "body"
    face = "face"
    frame = "frame"
    text = "text"

    @classmethod
    def all(cls) -> Tuple[str]:
        return tuple(map(lambda c: c.value, cls))


def draw_rectangle(
    img: Image.Image, x_min: int, y_min: int, x_max: int, y_max: int, annotation_type: str, text: str = ""
) -> Image.Image:
    color = {"body": "#258039", "face": "#e67e22", "frame": "#31a9b8", "text": "#cf3721"}[annotation_type]
    font = ImageFont.truetype(font=cfg["font_path"], size=30, encoding="utf-8")

    draw: ImageDraw.ImageDraw = ImageDraw.Draw(img)  # type: ignore
    draw.rectangle([x_min, y_min, x_max, y_max], outline=color, width=10)

    margin = 30
    text_y = max(0, y_min - margin)
    text_w, text_h = font.getsize(text)

    draw.rectangle((x_min, text_y, x_min + text_w, text_y + text_h), fill=color)
    draw.text((x_min, text_y), text, fill="white", font=font)

    return img


def main():
    st.title("Manga109 DataViewer")

    title: str = st.sidebar.selectbox("Title", get_all_titles(os.path.join(cfg["data_root"], "books.txt")))
    content: str = st.sidebar.selectbox("Content", Content.all(), index=0)

    st.markdown(f"## {title}")

    client = Manga109(cfg["data_root"], titles=[title])

    characters = client.books[0].characters
    characters_df = pd.DataFrame({"id": [c.id for c in characters], "name": [c.name for c in characters]})

    if content == Content.characters.value:
        st.table(characters_df)

    if content == Content.pages.value:
        show_table: bool = st.sidebar.checkbox("Show annotation table(s)")

        pages = client.books[0].pages
        num_pages = len(pages)

        index = st.sidebar.slider("Page index (1-index)", 1, num_pages, value=1)
        st.markdown(f"Page: {index}/{num_pages}")
        index -= 1  # convert to 0-index

        page = pages[index]

        annotation_types: List[str] = st.sidebar.multiselect("Annotation type(s)", (Annotation.all()))

        img = Image.open(client.books[0].pages[index].img_path)
        for annotation_type in annotation_types:
            annotations = None
            if annotation_type == Annotation.body.value:
                annotations = page.bodies
            elif annotation_type == Annotation.face.value:
                annotations = page.faces
            elif annotation_type == Annotation.frame.value:
                annotations = page.frames
            elif annotation_type == Annotation.text.value:
                annotations = page.texts

            annotations_df = pd.DataFrame(annotations)
            if show_table:
                if annotations is None:
                    st.markdown(f"No annotation for {annotation_type}")
                else:
                    st.table(annotations_df)

            if annotations is not None:
                for i, ann in enumerate(annotations):
                    text = ""

                    if isinstance(ann, (T.Body, T.Face)):
                        character = ann.character
                        text = f"{i:02d} {characters_df[characters_df['id'] == character]['name'].tolist()[0]}"

                    draw_rectangle(img, ann.xmin, ann.ymin, ann.xmax, ann.ymax, annotation_type, text)

        st.image(img, use_column_width=True)

    st.sidebar.markdown(
        f"<center>v{__version__} [<a href=https://github.com/skmatz/manga109-dataviewer>GitHub</a>]</center>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
