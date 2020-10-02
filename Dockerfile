FROM python


RUN pip install poetry 

COPY pyproject.toml poetry.lock ./
COPY src src
COPY entrypoint.sh .

RUN chmod +x ./entrypoint.sh
RUN poetry install

ENTRYPOINT ["./entrypoint.sh"]