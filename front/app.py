import os
import logging
import json
from typing import Dict
from datetime import datetime
from pydantic import BaseModel
import asyncio



import requests
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from streamlit_feedback import streamlit_feedback

import uuid

logger = logging.getLogger(__name__)
logging.basicConfig(
    # filename=f"logs/{datetime.now()}.log",
    encoding="utf-8",
    level=logging.ERROR,
    format="%(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %I.%M.%S %p",
)


load_dotenv()
logger.info(f"Environment variables: {os.environ}")


def response_generator(
    body: Dict,
    api_endpoint: str,
):
    try:
        s = requests.Session()
        with s.post(
            api_endpoint,
            json=body,
            headers=None,
            stream=True,
        ) as response:
            logger.info(f"Agent service call: Success ")

            content = json.loads(response.content)

            return content

    except Exception as error:
        logger.error(f"Agent service call: Fail {error} {api_endpoint} {body}")



st.set_page_config(
    page_title="Analiza tu Agua",
    page_icon=":robot_face:",
    layout="centered",
    initial_sidebar_state="collapsed"
)

class StylesModel(BaseModel):
    background_image: str = "https://static.eldiario.es/clip/4fb1015f-1aa8-4d5e-ab69-93815f78c73b_16-9-discover-aspect-ratio_default_0.jpg"
    background_opacity: float = 0.9
    header_background_color: str = "rgba(0,0,0,0)"
    toolbar_right: str = "2rem"

# "https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoiaW5kcmFcL2FjY291bnRzXC82OVwvNDAwMDI4NVwvcHJvamVjdHNcLzJcL2Fzc2V0c1wvZWZcLzc4MzFcLzA4MTNlNmY3OTA1MGU1MzI0NThiMzQ0YjRjNzM5ZGMzLTE1ODUyMjAyNTIuanBnIn0:indra:E9WGy2gDmuJLvjl-bA2PsR2AmRrxemnmcSoPe0vbbsg?width=2400"

class TextStylesModel(BaseModel):
    h1_color: str = "#ffffff"
    h1_font_size: str = "50px"
    text_color: str = "#ffffff"
    text_font_size: str = "18px"
    button_background_color: str = "#1A3B47"
    button_text_color: str = "#ffffff"
    button_font_size: str = "18px"
    button_padding: str = "5px 10px"
    button_border_radius: str = "5px"


styles = StylesModel()
text_styles = TextStylesModel()

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("{styles.background_image}");
background-size: cover;
opacity: {styles.background_opacity};
}}
[data-testid="stHeader"]{{
background-color: {styles.header_background_color};
}}
[data-testid="stToolbar"]{{
right: {styles.toolbar_right};
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)
st.markdown(
    f"<h1 style='color: {text_styles.h1_color}; font-size: {text_styles.h1_font_size}; text-align: left;'>El Agua de tu zona</h1>",
    unsafe_allow_html=True)
for k in list(range(2)):
    st.write("")
st.markdown(f"""
    <div style='background-color: rgba(102, 102, 102, 0.5); padding: 20px; border-radius: 10px;'>
        <p style='color: {text_styles.text_color}; font-size: {text_styles.text_font_size};'>Agente construido con inteligencia artificial generativa, capaz de analizar la calidad del agua de un punto, utilizando datos abiertos. </p>
    </div>              
""", unsafe_allow_html=True)

st.write("")