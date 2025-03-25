FROM python:3.10.12

WORKDIR /front

RUN apt-get update && apt-get install
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ /front

CMD ["streamlit", "run", "app.py", "--server.port=8002", "--server.address=0.0.0.0", "--server.enableWebsocketCompression=false"]

