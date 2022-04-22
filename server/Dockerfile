FROM python:3.10

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip uninstall bson
RUN pip uninstall pymongo
RUN pip install pymongo
RUN pip install -r requirements.txt

COPY . /code

CMD ["uvicorn", "app:app"]