FROM python:3.12-slim

WORKDIR /shop_api

COPY pyproject.toml poetry.lock /shop_api/
RUN python -m pip install --upgrade pip && pip install poetry && \
    poetry config virtualenvs.create false && poetry config installer.parallel false && \
    poetry install

COPY shop_api /shop_api/shop_api/

EXPOSE 80

CMD ["poetry", "run", "uvicorn", "shop_api.main:app", "--host", "0.0.0.0", "--port", "80"]