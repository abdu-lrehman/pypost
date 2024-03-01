FROM python:3.10

WORKDIR /pypost

COPY . /pypost

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app"]
