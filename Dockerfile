FROM python:3.10.8-slim
ENV MODULE_NAME="cocloud.src"
WORKDIR /app
COPY ./pyproject.toml ./poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD python3 src/main.py