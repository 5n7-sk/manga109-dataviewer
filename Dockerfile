FROM python:3.9

WORKDIR /app
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH /root/.local/bin:$PATH
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-ansi --no-dev --no-interaction

CMD ["make", "run", "port=8888"]
