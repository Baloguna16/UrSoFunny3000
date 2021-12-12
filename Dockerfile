FROM python:3.8.6

ADD src /src/
COPY run.py .
COPY requirements.txt .
RUN pip3 install -r requirements.txt

WORKDIR .
CMD ["python3", "run.py"]
