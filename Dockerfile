FROM python:3.12-slim AS assemble
COPY . /source
RUN python /source/prepare_repository.py /source /assembled

FROM python:3.12-slim
WORKDIR /app
COPY --from=assemble /assembled/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=assemble /assembled/ .
RUN python weights/download.py
ENV PYTHONUNBUFFERED=1 YUKSAVA_READ_ONLY_SETTINGS=1
EXPOSE 8765
CMD ["python", "scripts/serve.py"]
