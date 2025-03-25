FROM python:3.10.12

WORKDIR /agent

RUN apt-get update && apt-get install
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install -r requirements.txt
COPY ./ /agent

CMD ["python", "main.py"]
