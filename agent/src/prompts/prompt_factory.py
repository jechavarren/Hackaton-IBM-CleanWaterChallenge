import os
import yaml
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate


prompts_dir = os.path.abspath(os.path.join(__file__, os.path.pardir))


class PromptFactory:

    @staticmethod
    def load(
        prompt_path: str,
    ) -> Dict:
        """
        TODO
        """

        with open(prompt_path, "r") as fin:
            prompt_data = yaml.load(fin.read(), Loader=yaml.FullLoader)

        prompt = prompt_data["PROMPT"]

        if isinstance(prompt, list):
            if all([isinstance(item, dict) for item in prompt]):
                prompt = [tuple(item.items())[0] for item in prompt]
                prompt = ChatPromptTemplate.from_messages(prompt)

        if isinstance(prompt, list):
            prompt = ChatPromptTemplate.from_template(prompt)

        prompt_data["PROMPT"] = prompt

        return prompt_data

    @classmethod
    def factory_method(
        cls,
        domain: str,
    ) -> Dict[str, str]:
        if domain not in os.listdir(prompts_dir):
            raise Exception(
                f"PromptFactory Error: domain {domain} not in the defined "
                f"domains: {os.listdir(prompts_dir)}"
            )

        prompts = {}
        for filename in os.listdir(os.path.join(prompts_dir, domain)):
            if filename.endswith(".yml"):
                prompts[filename.replace(".yml", "")] = cls.load(
                    os.path.join(
                        prompts_dir,
                        domain,
                        filename,
                    ),
                )
        return prompts
