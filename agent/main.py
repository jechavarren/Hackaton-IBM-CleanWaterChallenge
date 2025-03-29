import os
import logging
import uvicorn
from dotenv import load_dotenv

from src.api import api

logger = logging.getLogger(__name__)
logging.basicConfig(
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    datefmt="%d/%m/%Y %I.%M.%S %p",
)

load_dotenv()
logger.info(f"Environment variables: {os.environ}")


if __name__ == "__main__":
    uvicorn.run(
        "src.api:api",
        host="0.0.0.0",
        port=8000,
        root_path="",
        #workers=int(os.getenv("WORKERS", 1)),
        lifespan="on",
    )
