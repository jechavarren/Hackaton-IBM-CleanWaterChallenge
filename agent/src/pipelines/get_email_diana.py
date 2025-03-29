import json
import logging
import pandas as pd
from typing import Literal, Optional
from langchain_core.output_parsers import JsonOutputParser

from src.models import ModelFactory
from src.prompts import PromptFactory


# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CreateMessagesPipeline:
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


    def invoke(
        self,
        water_info: str
    ) -> str:
        """
        Creates the message
        """

        response = self.analysis_chain.invoke(
            {
                "water_data": water_info
            }
        )

        return response
