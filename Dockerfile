FROM python:3.6

COPY requirments.txt .
RUN pip install -r requirments.txt

COPY src /src
WORKDIR /src

CMD ["python3", "script.py"]

