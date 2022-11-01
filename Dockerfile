FROM python:3.10.8-slim
ENV MODULE_NAME="cocloud.src"
WORKDIR /app
COPY . .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
CMD python3 src/main.py