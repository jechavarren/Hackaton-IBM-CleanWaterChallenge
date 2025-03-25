import os
from langchain_openai import AzureChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel


class ModelFactory:
    env_vars = [
        "OPENAI_API_VERSION",
        "OPENAI_API_LLM_MODEL_35",
        "OPENAI_API_LLM_MODEL_4",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT",
    ]

    @classmethod
    def factory_method(
        cls,
        temperature: float,
        model="gpt-3.5",
        as_stream: bool = False,
        max_tokens=400,
    ) -> BaseChatModel:
        for var in cls.env_vars:
            if var not in os.environ.keys():
                print_vars = "\n".join(cls.env_vars)
                raise Exception(
                    f"""{__name__} Error: The environ variables are needed:
                    {print_vars}\n\nVariable `{var}` is missing."""
                )
        if model == "gpt-3.5":
            return AzureChatOpenAI(
                model="gpt-3.5",
                deployment_name=os.environ["OPENAI_API_LLM_MODEL_35"],
                openai_api_version=os.environ["OPENAI_API_VERSION"],
                temperature=temperature,
                streaming=as_stream,
                max_tokens=max_tokens,
            )
        elif model == "gpt-4":
            return AzureChatOpenAI(
                model="gpt-4",
                deployment_name=os.environ["OPENAI_API_LLM_MODEL_4"],
                openai_api_version=os.environ["OPENAI_API_VERSION"],
                temperature=temperature,
                streaming=as_stream,
                max_tokens=max_tokens,
            )
        elif model == "gpt-4o":
            return AzureChatOpenAI(
                model="gpt-4o",
                api_key=os.environ["AZURE_OPENAI_API_KEY"],
                azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
                deployment_name=os.environ["OPENAI_API_LLM_MODEL_4o"],
                api_version=os.environ["OPENAI_API_VERSION"],
                temperature=temperature,
                streaming=as_stream,
                max_tokens=max_tokens,
            )
        
        elif model == "gpt-4-classic":
            return AzureChatOpenAI(
                model="gpt-4",
                deployment_name=os.environ["OPENAI_API_LLM_MODEL_4_CLASSIC"],
                openai_api_version=os.environ["OPENAI_API_VERSION"],
                temperature=temperature,
                streaming=as_stream,
                max_tokens=max_tokens,
            )