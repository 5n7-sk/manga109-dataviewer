import os.path
from typing import List

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import yaml
from PIL import Image

from manga109 import Manga109
from manga109 import typing as T
from manga109.utils import get_all_titles
from src import __version__
from src.drawer import Drawer
from src.eda import count_bodies, count_faces
from src.typing import Annotation, Content

with open("config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.SafeLoader)


def main():
    st.title("Manga109 DataViewer")

    title: str = st.sidebar.selectbox("Title", get_all_titles(os.path.join(cfg["data_root"], "books.txt")))
    content = Content.from_str((st.sidebar.selectbox("Content", Content.all(), index=0)))

    st.markdown(f"## {title}")

    client = Manga109(cfg["data_root"], titles=[title])

    characters = client.books[0].characters
    characters_df = pd.DataFrame({"id": [c.id for c in characters], "name": [c.name for c in characters]})

    if content == Content.characters:
        # count the number of appearances (bodies and faces)
        pages = client.books[0].pages
        bodies = count_bodies(pages)
        bodies_df = pd.DataFrame({"id": list(bodies.keys()), "num_bodies": list(bodies.values())})
        faces = count_faces(pages)
        faces_df = pd.DataFrame({"id": list(faces.keys()), "num_faces": list(faces.values())})

        characters_df = pd.merge(characters_df, pd.merge(bodies_df, faces_df, how="outer", on="id").fillna(0), on="id")
        st.table(characters_df)

        show_eda: bool = st.sidebar.checkbox("Show EDA", value=True)
        if show_eda:
            fig = go.Figure(  # type: ignore
                data=[
                    go.Bar(  # type: ignore
                        name="num_bodies",
                        x=characters_df["name"].values,
                        y=characters_df["num_bodies"].values,
                        marker_color=cfg["page"]["color"]["body"],
                    ),
                    go.Bar(  # type: ignore
                        name="num_faces",
                        x=characters_df["name"].values,
                        y=characters_df["num_faces"].values,
                        marker_color=cfg["page"]["color"]["face"],
                    ),
                ]
            )
            fig.update_layout(legend={"x": 0.0, "y": 1.0, "bgcolor": "rgba(255, 255, 255, 0)"})
            st.plotly_chart(fig)

    if content == Content.pages:
        show_table: bool = st.sidebar.checkbox("Show annotation table(s)")

        drawer = Drawer(cfg["font_path"])

        pages = client.books[0].pages
        num_pages = len(pages)

        index = st.sidebar.slider("Page index (1-index)", 1, num_pages, value=1)
        st.markdown(f"Page: {index}/{num_pages}")
        index -= 1  # convert to 0-index

        page = pages[index]

        annotations: List[Annotation] = [
            Annotation.from_str(v) for v in st.sidebar.multiselect("Annotation type(s)", (Annotation.all()))
        ]

        img = Image.open(client.books[0].pages[index].img_path)
        for annotation in annotations:
            anns = None
            if annotation == Annotation.body:
                anns = page.bodies
            elif annotation == Annotation.face:
                anns = page.faces
            elif annotation == Annotation.frame:
                anns = page.frames
            elif annotation == Annotation.text:
                anns = page.texts

            annotations_df = pd.DataFrame(anns)
            if show_table:
                if not annotations_df.empty:
                    st.markdown(f"<center>{annotation.value}</center>", unsafe_allow_html=True)

                    if annotation in (Annotation.body, Annotation.face):
                        annotations_df = pd.merge(
                            annotations_df,
                            characters_df,
                            how="left",
                            left_on="character",
                            right_on="id",
                            suffixes=("", "_"),  # type: ignore
                        ).drop("id_", axis=1)

                    st.table(annotations_df)

            if anns is not None:
                for i, ann in enumerate(anns):
                    text = f"{i:02d}"

                    if isinstance(ann, (T.Body, T.Face)):
                        character = ann.character
                        text += f" {characters_df[characters_df['id'] == character]['name'].tolist()[0]}"

                    drawer.draw(
                        img, ann.xmin, ann.ymin, ann.xmax, ann.ymax, cfg["page"]["color"][annotation.value], text
                    )

        st.image(img, use_column_width=True)

    st.sidebar.markdown(
        f"<center>v{__version__} [<a href=https://github.com/skmatz/manga109-dataviewer>GitHub</a>]</center>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
