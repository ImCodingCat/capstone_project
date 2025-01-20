FROM python:3.10-slim

WORKDIR /app

COPY requirements-inference.txt ./
COPY model ./model
COPY inference ./inference
COPY dataset/anime.csv ./dataset/anime.csv

RUN pip install --no-cache-dir -r requirements-inference.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "./inference/app.py", "--server.port=8501", "--server.address=0.0.0.0"]