import json
import logging
import pandas as pd
from typing import Literal, Optional
from langchain_core.output_parsers import JsonOutputParser

from models import ModelFactory
from prompts import PromptFactory


# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class GetWaterDataPipeline:
    """
    Pipeline to get the water quelity data.
    """

    def __init__(self):

        self.constant='constant'

    def get_water_data(sampling_point: str):

        data = pd.DataFrame() # Aquí hay que poner la etl para obtener los datos

        return data
