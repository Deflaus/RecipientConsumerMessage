FROM python:3.8-slim
WORKDIR /Project/worker
RUN pip install --upgrade pip
COPY requirements.txt /Project/worker/requirements.txt
RUN pip install -r requirements.txt
COPY . /Project/worker
CMD ["python3.8", "main.py"]