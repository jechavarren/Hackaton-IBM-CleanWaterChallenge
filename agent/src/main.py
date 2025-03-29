import os
import uuid
from typing import Dict

from .pipelines.get_water_data_pipeline_paula import GetWaterDataPipeline
from .pipelines.analyze_water_data_pipeline_alberto import AnalyzeWaterDataPipeline
from .pipelines.create_messages_pipeline_alba import CreateMessagesPipeline
from .pipelines.send_email_alba import SendEmailPipeline


def dispatcher(
    sampling_point: str = "123",
    metadata: Dict = {"meta": "data"},
) -> Dict:
    
    data = "sample"
    analysis = AnalyzeWaterDataPipeline().sample_analyze_water_data()
    email_body = CreateMessagesPipeline().create_messages(total_water_data = analysis)
    result = SendEmailPipeline().send_email(body=email_body)

    return result