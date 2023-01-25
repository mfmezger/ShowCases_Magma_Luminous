FROM python:3.10

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/"
ENV PORT=8000

RUN apt install tesseract-ocr
RUN apt install libtesseract-dev

# Install Poetry
RUN curl -sSL https://install.python-poetry.org/ | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

# moving the complete app as well as the stored models into the docker workspace
COPY . /app

ENTRYPOINT ["streamlit", "run", "detection/hello.py", "--server.port=8001", "--server.address=0.0.0.0"]
