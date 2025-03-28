import os
import logging
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM
from langchain.prompts import PromptTemplate

# from .models import ModelFactory
from .prompts import PromptFactory



# Configure logging
logging.basicConfig(
    # filename='app.log',
    filemode="a",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class CreateMessagesPipeline:
    """
    Pipeline to create body email based on water data.
    """

    # def __init__(self):
        
        # model_gpt4 = ModelFactory.factory_method(
        #     temperature=0.0,
        #     model="gpt-4",
        # )

        # prompt = PromptFactory.factory_method(
        #     domain="describe_water_data",
        # )[
        #     "describe_water_data"
        # ]["PROMPT"]

        # self.analysis_chain = prompt | model_gpt4
        
        # logging.info("DescribeWaterGPT initialized successfully.")


    def __init__(self):

        load_dotenv()
        self.watsonx_apikey = os.getenv('WATSONX_APIKEY')
        self.project_id = os.getenv('PROJECT_ID')
        self.url = os.getenv('URL')
        
        self.params_dic = {
            "decoding_method": "greedy",
            "min_new_tokens": 0,
            "max_new_tokens": 300,
            "repetition_penalty": 1,
            "stop_sequences": ["Vasco."]
        }
        
        self.llm = WatsonxLLM(
            model_id='ibm/granite-3-8b-instruct',            
            url=self.url,
            apikey=self.watsonx_apikey,
            project_id=self.project_id,
            params=self.params_dic
        )
        
       
        prompt_data = PromptFactory.factory_method(domain="generate_body_email")[
            "generate_body_email"
        ]
        self.prompt_template = prompt_data["PROMPT"]

        logging.info("CreateMessagesPipeline inicialized correctly.")

    def filter_water_data(self, total_water_data):
        water_data = {
            "city": total_water_data["city"],
            "water_tank_name": total_water_data["water_tank_name"],
            "component": [
                {
                    "name": c["name"],
                    "current_value": c["current_value"],
                    "lower_threshold": c["lower_threshold"],
                    "upper_threshold": c["upper_threshold"]
                }
                for c in total_water_data["component"]
                if c["component_alert"] == "KO"
            ]
        }
        return water_data
    
    def call_llm(self, water_data):

        llm_chain = self.prompt_template | self.llm
        output = llm_chain.invoke({"water_data": water_data})
        return output
    
    def create_messages(self, total_water_data):
        try:
            water_data = self.filter_water_data(total_water_data)
            body_email = self.call_llm(water_data)
            return body_email
        except Exception as e:
            logging.error(f"Error creating email: {str(e)}")
            return {"error": "Failed to create email"}
        




