import os

import phoenix
from opentelemetry import trace as trace_api
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from openinference.instrumentation.langchain import LangChainInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)

from .main import dispatcher


if os.getenv("PHOENIX_URI"):  # "http://phoenix:6006/v1/traces"

    client = phoenix.Client(
        endpoint=os.environ["PHOENIX_URI"].strip("/"),
    )

    span_exporter = OTLPSpanExporter(
        endpoint=os.environ["PHOENIX_URI"].strip("/") + "/v1/traces"
    )

    resource = Resource(attributes={})
    tracer_provider = trace_sdk.TracerProvider(resource=resource)
    span_processor = SimpleSpanProcessor(span_exporter=span_exporter)
    tracer_provider.add_span_processor(span_processor=span_processor)
    trace_api.set_tracer_provider(tracer_provider=tracer_provider)

    # Call the instrumentor to instrument OpenAI
    LangChainInstrumentor().instrument()
