FROM python:3.10

WORKDIR /pypost

COPY . /pypost

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

ENV NAME World

CMD ["python", "/app/main.py"]
