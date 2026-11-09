from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory

import streamlit as st
from streamlit_extras.three_viewer import three_viewer

from hex_chess_board_generator.configuration import from_dict, load_config
from hex_chess_board_generator.generator import generate_hexagon

st.set_page_config(layout="wide")

conf = load_config(path=Path("src/configs/default.conf.yaml"))
conf_dict = asdict(conf)

st.header("Parametrizable hexagon generator")

config_col, preview_col = st.columns([0.3, 0.7])

with config_col:
    with st.container(border=True):
        conf_dict["hex_dims"]["r_mm"] = st.number_input(
            "hexgaon radius (mm)",
            value=conf.hex_dims.r_mm,
            help="base inner radius - half of the distances between two hexagon edges.",
            min_value=0.1,
        )
        conf_dict["hex_dims"]["height_mm"] = st.number_input(
            "hexagon height (mm)", value=conf.hex_dims.height_mm, min_value=0.1
        )
        conf_dict["mount_dims"]["length_mm"] = st.number_input(
            "mounting length (mm)",
            value=conf.mount_dims.length_mm,
            min_value=0.1,
            help="length of male mounting point, also width of smaller, trapezoid base.",
        )
        conf_dict["mount_dims"]["height_mm"] = st.slider(
            "mounting height (mm)",
            value=conf.mount_dims.height_mm,
            min_value=0.1,
            max_value=conf_dict["hex_dims"]["height_mm"],
            help="height of mounting male element. Should be lower than total height of hexagon.",
        )
        conf_dict["mount_dims"]["height_margin_mm"] = st.slider(
            "mounting height margin (mm)",
            value=conf.mount_dims.height_margin_mm,
            min_value=0.0,
            max_value=conf_dict["mount_dims"]["height_mm"],
            help="margin of the width - the amount of width cut off from male mouting point compared to female socket.",
        )
        conf_dict["mount_dims"]["width_margin_mm"] = st.slider(
            "mounting width margin (mm)",
            value=conf.mount_dims.width_margin_mm,
            min_value=0.0,
            max_value=conf_dict["mount_dims"]["length_mm"],
            help="margin of the width - the amount of width cut off from male mouting point compared to female socket",
        )

with preview_col:
    with TemporaryDirectory() as tmp_dir:
        model = generate_hexagon(from_dict(conf_dict))
        model_path = f"{tmp_dir}/hexagon.stl"
        model.save_as_stl(model_path)
        three_viewer(model_path, height=600, file_format=".stl")
        with open(model_path, "rb") as file:
            st.download_button(
                "download STL",
                file,
                type="primary",
                icon=":material/download:",
                mime="model/stl",
            )
