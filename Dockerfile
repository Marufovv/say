FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python weights/download.py
ENV PYTHONUNBUFFERED=1 YUKSAVA_READ_ONLY_SETTINGS=1
EXPOSE 8765
CMD ["python", "scripts/serve.py"]
