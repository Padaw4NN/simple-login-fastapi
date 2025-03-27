FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /app/

EXPOSE 8081

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081", "--reload" ]
