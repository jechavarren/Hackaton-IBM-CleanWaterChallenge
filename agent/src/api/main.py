import os
import json
import logging
import pandas as pd
from typing import Dict
from fastapi import FastAPI
from openinference.semconv.trace import SpanAttributes
from openinference.semconv.trace import OpenInferenceSpanKindValues
from phoenix.trace import SpanEvaluations

from src import dispatcher
from .schemas import FeedbackRequest
from .schemas import InferenceRequest
from .schemas import InferenceResponse

if os.getenv("PHOENIX_URI"):
    from src import client
    from src import trace_api


logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %I.%M.%S %p",
)

api = FastAPI()


@api.get("/ping")
def ping():
    return 200


@api.post("/inference")
def inference(
    request: InferenceRequest,
) -> InferenceResponse:

    try:
        response = dispatcher(message = request.message,
                              metadata = request.metadata)


        logger.info(
            f"Message {request.message} "
            f"Medatadata {request.metadata} "
            f"Response: {response} ",
        )
        return InferenceResponse(**response)

    except Exception as error:

        logger.error(
            f"Error {error} in requests:"
            f"Message {request.message} "
            f"Medatadata {request.metadata} ",
        )

        return InferenceResponse(
            message="Lo siento, ha habido un error en el sistema",
            metadata={"error": str(error)},
        )


@api.post("/feedback")
def feedback(
    request: FeedbackRequest,
):

    try:
        tracer = trace_api.get_tracer(__name__)

        with tracer.start_as_current_span("UserFeedback") as span:
            span.set_attribute(SpanAttributes.INPUT_VALUE, request.question)
            span.set_attribute(SpanAttributes.OUTPUT_VALUE, request.answer)
            span_id = json.loads(span.to_json())["context"]["span_id"][2:]

        client.log_evaluations(
            SpanEvaluations(
                eval_name="feedback",
                dataframe=pd.DataFrame(
                    {
                        "context.span_id": [span_id],
                        "span_id": [span_id],
                        "score": [float(request.score)],
                        "label": ["ok" if request.score == 1 else "ko"],
                        "explanation": [request.valoration],
                    }
                ).set_index("context.span_id"),
            )
        )

        return 200

    except Exception as error:
        logger.error(
            f"error with score {request.score} and valoration {request.valoration} in message {request.question} {request.answer}: {error}"
        )

        return 500


@api.get("/metadata")
def metadata() -> list:
    return []


@api.get("/chains")
def chains() -> list:
    return []


@api.get("/examples")
def examples() -> list[tuple[InferenceRequest, InferenceResponse]]:
    return [
        (
            InferenceRequest(),
            InferenceResponse(),
        ),
    ]
