import os
from dotenv import load_dotenv
import json
import logging
from langchain_community.utilities import SerpAPIWrapper


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

        load_dotenv()
        
        self.search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERPAPI_API_KEY"))
        
        from langchain_core.tools import Tool

        # Tool to pass to an agent
        self.google_tool = Tool(
            name="google-search",
            description="Search Google for recent results",
            func=self.search.run,
        )

        logging.info("Email discovery agent initialized")


    def invoke(
        self,
        municipality: str
    ) -> str:
        """
        Creates the message
        """
        search = SerpAPIWrapper()
        email = search.run(f"Cual es el email del ayuntamiento de {municipality}?")

        return email
    

## Test
pipeline = CreateMessagesPipeline()

print(pipeline.invoke("Lezo"))

