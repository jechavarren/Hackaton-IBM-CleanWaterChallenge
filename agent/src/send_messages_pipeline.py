import json
import logging
import pandas as pd
from typing import Literal, Optional
from langchain_core.output_parsers import JsonOutputParser

from .models import ModelFactory
from .prompts import PromptFactory


# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class SendMessagesPipeline:
    """
    Pipeline to make a review of water analysis results.
    """

    def __init__(self):
        
        model_gpt4 = ModelFactory.factory_method(
            temperature=0.0,
            model="gpt-4",
        )

        prompt = PromptFactory.factory_method(
            domain="describe_water_data",
        )[
            "describe_water_data"
        ]["PROMPT"]

        self.analysis_chain = prompt | model_gpt4
        
        logging.info("DescribeWaterGPT initialized successfully.")

    def get_water_data(sampling_point: str):

        data = pd.DataFrame() # Aquí hay que poner la etl para obtener los datos

        return data


    def invoke(
        self,
        sampling_point: str
    ) -> str:
        """
        Get the data and describe it
        """
        
        water_data = self.get_water_data(sampling_point)

        response = self.analysis_chain.invoke(
            {
                "water_data": water_data.to_json()
            }
        )

        return response
