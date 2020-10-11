FROM python:3.8-slim
WORKDIR /Project/api
RUN pip install --upgrade pip
COPY requirements.txt /Project/api/requirements.txt
RUN pip install -r requirements.txt
COPY . /Project/api
CMD ["python3.8", "main.py"]