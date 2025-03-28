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


# def response_generator(
#     body: Dict,
#     api_endpoint: str,
# ):
#     try:
#         s = requests.Session()
#         with s.post(
#             api_endpoint,
#             json=body,
#             headers=None,
#             stream=True,
#         ) as response:
#             logger.info(f"Agent service call: Success ")

#             content = json.loads(response.content)

#             return content

#     except Exception as error:
#         logger.error(f"Agent service call: Fail {error} {api_endpoint} {body}")



def trigger_full_process():
    try:
        funcion_main = "execute_pipeline"
        # Ajusta la URL según tu configuración de red/puerto
        response = requests.post(f'http://agent:8000/{funcion_main}')
        response_data = response.json()

        if 'error' in response_data['metadata']:
            error_message = response_data['metadata']['error']
            return f"Connection error: {error_message}"
        
        if response_data['status'] == 'OK':
            return "Process completed successfully!"
        else:
            return f"Error in the process: {response_data['message']}"
    except Exception as e:
        return "Conecction error: {e}"


st.set_page_config(
    page_title="Water Measurements Analysis",
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
    f"<h1 style='color: {text_styles.h1_color}; font-size: {text_styles.h1_font_size}; text-align: left;'>Anomaly Detection in Water Tank Sensor Data in the Basque Country</h1>",
    unsafe_allow_html=True)
for k in list(range(2)):
    st.write("")
st.markdown(f"""
    <div style='background-color: rgba(102, 102, 102, 0.5); padding: 20px; border-radius: 10px;'>
        <p style='color: {text_styles.text_color}; font-size: {text_styles.text_font_size};'>Agent built with generative Artificial Intelligence, able to analyse water measurements in a water tank, using data every 15 minutes. It is capable of detect anomalou measurements and send an email to the correspondent council.</p>
    </div>              
""", unsafe_allow_html=True)


if st.button(
    "Initialize the complete analysis", 
    key="trigger_process_btn",
    type="primary"
):
    
    result_message = trigger_full_process()
    st.markdown("""
        <style>
            .custom-text {
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                padding: 20px;
                border-radius: 10px;
                font-size: 22px;
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="custom-text">{result_message}</div>', unsafe_allow_html=True)


def test_backend_connection():
    try:
        # Usa la URL del contenedor de FastAPI
        backend_url = "http://agent:8000"  # 'agent' es el nombre del contenedor de FastAPI
        
        # Hacer una solicitud GET al endpoint de prueba
        response = requests.get(f'{backend_url}/test')
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data["status"] == "OK":
                return "Successful conection!"
            else:
                st.error(f"Error en la respuesta: {response_data.get('message', 'Sin mensaje')}")
        else:
            st.error(f"Error en la solicitud: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error de conexión: {e}")


# Prueba de conexion
if st.button("Probar conexión con FastAPI"):
    result_message = test_backend_connection()
    st.markdown("""
        <style>
            .custom-text {
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                padding: 20px;
                border-radius: 10px;
                font-size: 22px;
                text-align: center;
            }
        </style>
        """, unsafe_allow_html=True)
    st.markdown(f'<div class="custom-text">{result_message}</div>', unsafe_allow_html=True)