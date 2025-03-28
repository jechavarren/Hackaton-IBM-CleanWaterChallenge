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

class AnalyzeWaterDataPipeline:
    """
    Pipeline to analyze water data.
    """

    def __init__(self):

        self.constant = 'constant'

    def analyze_water_data(water_data: pd.DataFrame)

        analysis = {'alarm': True, 'element': 'Arsénico con una concentración de 100mg/l, superior al límite de 50mg/l'}

        return analysis
