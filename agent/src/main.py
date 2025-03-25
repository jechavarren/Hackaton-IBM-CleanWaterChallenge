import os
import uuid
from typing import Dict

from .describe_water_pipeline import DescribeWaterPipeline


def dispatcher(
    sampling_point: str,
    metadata: Dict,
) -> Dict:
    
    pipeline = DescribeWaterPipeline()    

    return pipeline.invoke(sampling_point)
