import os
import uuid
from typing import Dict




def dispatcher(
    sampling_point: str,
    metadata: Dict,
) -> Dict:
    
    pipeline = 1

    return pipeline.invoke(sampling_point)
