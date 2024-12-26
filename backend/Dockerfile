FROM python:3.9 AS builder

RUN python -m venv /venv;

WORKDIR /code

COPY ./requirements.txt  .

RUN /venv/bin/pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.9-slim

WORKDIR /code

COPY --from=builder /venv/ /venv/ 

ENV PATH=/venv/bin:$PATH

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]