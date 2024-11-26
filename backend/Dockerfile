FROM python:3.8-slim

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

CMD ["uvicorn", "app:app", "--host", "0.0.0.0"]
